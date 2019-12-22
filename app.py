from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable= False)
    game = db.Column(db.String(200))

    def __repr__(self):
        return '<Todo %r>' % self.id



@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        playerName= request.json['name']
        playerGame= request.json['game']
        newPlayer = Todo(name=playerName,game=playerGame)
        try:
            db.session.add(newPlayer)
            db.session.commit()
            return redirect('/')
        except:
            return "problem with post"
    else: 
        players = Todo.query.order_by(Todo.name).all()
        return render_template('index.html', players = players)

@app.route('/delete/<int:id>')
def delete(id):
    playerToDelete = Todo.query.get_or_404(id)

    try:
        db.session.delete(playerToDelete)
        db.session.commit()
        return redirect('/')
    except:
        return "Problem with deleting"

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    player= Todo.query.get_or_404(id)

    if request.method== "POST":
        player.name= request.json['name']
        player.game= request.json['game']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Problem with update"
            
    else :
        return render_template("update.html",player=player)

if __name__ == "__main__" :
    app.run(debug=True)
