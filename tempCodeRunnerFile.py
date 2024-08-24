from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class ToDo(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    
    def __repr__(self) -> str:
        return f"{self.srno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        title = request.form.get('title')
        desc = request.form.get('desc')
        if title and desc:
            new_todo = ToDo(
                title=title,
                desc=desc
            )
            db.session.add(new_todo)
            db.session.commit()
        return redirect(url_for('index'))
    
    search_query = request.args.get('search', '')
    if search_query:
        allToDO = ToDo.query.filter(
            ToDo.title.contains(search_query) |
            ToDo.desc.contains(search_query)
        ).all()
    else:
        allToDO = ToDo.query.all()
    
    return render_template('index.html', allToDO=allToDO)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/update/<int:srno>', methods=['GET', 'POST'])
def update(srno):
    todo = ToDo.query.get_or_404(srno)
    
    if request.method == 'POST':
        todo.title = request.form.get('title')
        todo.desc = request.form.get('desc')
        todo.completed = 'completed' in request.form
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:srno>', methods=['POST'])
def delete(srno):
    todo = ToDo.query.get_or_404(srno)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:srno>', methods=['POST'])
def complete(srno):
    todo = ToDo.query.get_or_404(srno)
    todo.completed = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/undo/<int:srno>', methods=['POST'])
def undo(srno):
    todo = ToDo.query.get_or_404(srno)
    todo.completed = False
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
