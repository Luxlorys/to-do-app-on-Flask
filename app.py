from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# home page
@app.route('/')
def index():
    tasks = Task.query.order_by(Task.date.desc()).all()
    return render_template('index.html', tasks=tasks)


# details 
@app.route('/detail/<int:id>')
def task_detail(id):
    task = Task.query.get(id)
    return render_template('detail.html', task=task)


# create new task
@app.route('/create', methods=['POST', 'GET'])
def create_new_task():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        task = Task(title=title, text=text)

        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'При добавлении задачи произошла ошибка'
    else:
        return render_template('create.html')


# delete task
@app.route('/detail/<int:id>/del')
def delete_task(id):
    task = Task.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except Exception:
        return 'При удаление задачи произошла ошибка'


# update task
@app.route('/detail/<int:id>/update', methods=['POST', 'GET'])
def update_task(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.title = request.form['title']
        task.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'При редактировании статьи произошла ошибка'
    else:
        return render_template('update_task.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)