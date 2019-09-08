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
        session['logged_in'] = True
        session['page'] = 1
        session['user'] = {
            'id': user.id,
            'username': user.username
        }
        return redirect('/todo/%s' % session['page'])
    else:
        flash('Nice try buddy', 'danger')
        return redirect('/login')


@app.route('/logout')
def logout() -> Response:
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('See you space cowboy', 'success')
    return redirect('/')


@app.route('/todo/task/<int:id>', methods=['GET'])
def todo(id: int) -> Response:
    todo = db.session.query(Todo).filter_by(id=id).first()
    return render_template('todo.html', todo=todo)


@app.route('/todo/<int:page>', methods=['GET'])
def todos(page: int = 1) -> Response:
    if not session.get('logged_in'):
        return redirect('/login')
    session['page'] = page
    todos = Todo.query.paginate(
        page=session['page'],
        per_page=5,
        error_out=False
    )
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
    return redirect('/todo/%s' % session['page'])


@app.route('/todo/complete/<int:id>', methods=['POST'])
def todo_toggle_completion(id: int) -> Response:
    todo = db.session.query(Todo).filter_by(id=id).first()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect('/todo/%s' % session['page'])


@app.route('/todo/<int:id>', methods=['POST'])
def todo_delete(id: int) -> Response:
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    flash("Task #%s chucked into the void!" % id, 'success')
    return redirect('/todo/%s' % session['page'])


@app.route('/todo/<int:id>/json', methods=['GET'])
def todo_json(id: int) -> str:
    todo = Todo.query.filter_by(id=id).first()
    return jsonify(todo.to_dict())


@app.route('/page/<int:page>', methods=['GET'])
def change_page(page: int) -> Response:
    session['page'] = page
    return redirect('/todo/%s' % session['page'])
