from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    Response
)

from alayatodo import app
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
    try:
        user = User.get(username)
        if user and user.verify(password):
            session['logged_in'] = True
            session['page'] = 1
            session['user'] = {
                'id': user.id,
                'username': user.username
            }
            return redirect('/todo/%s' % session['page'])
        else:
            flash('Nice try buddy', 'danger')
    except Exception as e:
        flash('Error getting user for %s: %s' % (username, e))
    return redirect('/login')


@app.route('/logout')
def logout() -> Response:
    session.pop('logged_in', None)
    session.pop('page', None)
    session.pop('user', None)
    flash('See you space cowboy', 'success')
    return redirect('/')


@app.route('/todo/task/<int:id>', methods=['GET'])
def todo(id: int) -> Response:
    if not session.get('logged_in'):
        return redirect('/login')
    try:
        todo = Todo.get(id)
        return render_template('todo.html', todo=todo)
    except Exception as e:
        flash('Error getting todo task #%s: %s' % (id, e))
        return redirect('/todos/%s' % session['page'])


@app.route('/todo/<int:page>', methods=['GET'])
def todos(page: int = None) -> Response:
    if not session.get('logged_in'):
        return redirect('/login')
    try:
        todos = Todo.paginate(session['user']['id'], session['page'])
        return render_template('todos.html', todos=todos)
    except Exception as e:
        flash('Error paginating todos: %e' % e)
        return redirect('/')


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_post() -> Response:
    if not session.get('logged_in'):
        return redirect('/login')
    user_id = session['user']['id']
    description = request.form.get('description')
    if description:
        try:
            Todo.add(user_id, description)
            flash('Time to hustle!', 'success')
        except Exception as e:
            flash('Error adding task: %e' % e)
    else:
        flash('Not exactly worthwhile to add nothing, is it?', 'warning')
    return redirect('/todo/%s' % session['page'])


@app.route('/todo/complete/<int:id>', methods=['POST'])
def todo_toggle_completion(id: int) -> Response:
    if not session.get('logged_in'):
        return redirect('/login')
    try:
        Todo.toggle_completion(id)
    except Exception as e:
        flash('Error toggling completion for task #%s: %s' % (id, e))
    return redirect('/todo/%s' % session['page'])


@app.route('/todo/<int:id>', methods=['POST'])
def todo_delete(id: int) -> Response:
    if not session.get('logged_in'):
        return redirect('/login')
    try:
        Todo.delete(id)
        flash("Task #%s chucked into the void!" % id, 'success')
    except Exception as e:
        flash('Error deleting task #%s: %s' % (id, e), 'danger')
    return redirect('/todo/%s' % session['page'])


@app.route('/todo/<int:id>/json', methods=['GET'])
def todo_json(id: int) -> str:
    if not session.get('logged_in'):
        return redirect('/login')
    try:
        return Todo.get(id).json()
    except Exception as e:
        flash('Error rendering json for task #%s: %s' % (id, e), 'danger')
        return redirect('/todo/%s' % session['page'])


@app.route('/page/<int:page>', methods=['GET'])
def change_page(page: int) -> Response:
    if not session.get('logged_in'):
        return redirect('/login')
    session['page'] = page
    return redirect('/todo/%s' % page)
