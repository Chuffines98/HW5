from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import os

dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')

#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://toor:Password1@localhost/myDb'
db = SQLAlchemy(app)

class GameDevForm(FlaskForm):
    game_name = StringField('Game Name:', validators=[DataRequired()])
    id = IntegerField('Id:', validators=[DataRequired()])
    dev_name = StringField('Developer Name:', validators=[DataRequired()])


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name =  db.Column(db.String(80))
    dev_name = db.Column(db.String(80))

    def __init__(self, game_name, dev_name):
        self.game_name = game_name
        self.dev_name = dev_name

    def __repr__(self):
        return '<Game %r>' % self.game_name

@app.route('/', methods=['GET'])
def index():
    pageTitle = 'Games of Cullen'
    games = Game.query.all() # retreive all data from db
    return render_template('index.html', title=pageTitle, games=games)

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    game = Game.query.get_or_404(id)
    try:
        db.session.delete(game)
        db.session.commit()
        games = Game.query.all() # retreive all data from db
        return render_template('index.html',games=games)
    except:
        return 'Could not Delete this Game'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == "POST":
        app.logger.info('You are posting and updating')
        gamename = request.form['game_name']
        app.logger.info(gamename)
        devname = request.form['dev_name']
        # print(devname, gamename)
        game = Game.query.get_or_404(id)
        game.dev_name = devname
        game.game_name = gamename
        db.session.commit()
        games = Game.query.all() # retreive all data from db
        return render_template('index.html',games=games)
    else:
        # using get and need to return the html page
        game = Game.query.get_or_404(id)
        form = GameDevForm()
        form.game_name.data = game.game_name
        form.id.data = game.id
        form.dev_name.data = game.dev_name
        return render_template('update.html', form=form, pageTitle='Updating A New Game')
    pageTitle = 'Updating Page'
    game = Game.query.get_or_404(id) # retreive all data from db
    return render_template('index.html', title=pageTitle, games=games)

@app.route('/add_game', methods=['GET', 'POST'])
def add_game():
    if request.method == "POST":
        form = GameDevForm()
        #if form.validate_on_submit():
        #gamename = form.game_name.data
        gamename = request.form['game_name']
        devname = request.form['dev_name']
        form.game_name.data = ''
        form.dev_name.data = ''
        game1 = Game(gamename, devname)
        db.session.add(game1)
        db.session.commit()
        games = Game.query.all() # retreive all data from db
        return render_template('index.html',games=games)
            #return '<h2> My game name is {0} and its dev is {1}'.format(form.game_name.data, form.dev_name.data)
        # return back to same page
    else:
        # using get and need to return the html page
        form = GameDevForm()
        return render_template('add_game.html', form=form, pageTitle='Add A New Game')




@app.route('/mike')
def mike():
    return render_template('mike.html', pageTitle='About Mike')

if __name__ == '__main__':
    app.run(debug=True)
