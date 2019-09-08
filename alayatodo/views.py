from flask import (
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    Response
)

from alayatodo import app, db
from .models import User, Todo


@app.route('/')
def home() -> Response:
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login() -> Response:
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post() -> Response:
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user'] = {
            'id': user.id,
            'username': user.username
        }
        session['logged_in'] = True
        return redirect('/todo')
    else:
        flash('Nice try buddy', 'danger')
        return redirect('/login')


@app.route('/logout')
def logout() -> Response:
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('See you space cowboy', 'success')
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id: str) -> Response:
    todo = db.session.query(Todo).filter_by(id=id).first()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos() -> Response:
    if not session.get('logged_in'):
        return redirect('/login')
    todos = Todo.query.all()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_post() -> Response:
    if not session.get('logged_in'):
        return redirect('/login')
    user_id = session['user']['id']
    description = request.form.get('description')
    if description:
        todo = Todo(user_id, description)
        db.session.add(todo)
        db.session.commit()
        flash('Time to hustle!', 'success')
    else:
        flash('Not exactly worthwhile to add nothing, is it?', 'warning')
    return redirect('/todo')


@app.route('/todo/complete/<id>', methods=['POST'])
def todo_toggle_completion(id: str) -> Response:
    todo = db.session.query(Todo).filter_by(id=id).first()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id: str):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    flash("Task #%s chucked into the void!" % id, 'success')
    return redirect('/todo')


@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id: str):
    todo = Todo.query.filter_by(id=id).first()
    return jsonify(todo.to_dict())
