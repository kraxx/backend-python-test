from alayatodo import app
from flask import (
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session
    )

@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    description = request.form.get('description')
    if description:
        g.db.execute(
            "INSERT INTO todos (user_id, description) VALUES ('%s', '%s')"
            % (session['user']['id'], description)
        )
        g.db.commit()
        flash('Added new task!', 'success')
    else:
        flash('Please enter a description', 'warning')
    return redirect('/todo')


@app.route('/todo/complete/<id>', methods=['POST'])
def todo_complete(id):
    completed = True if request.args.get("completed") == "1" else False
    g.db.execute(
        "UPDATE todos SET completed='%s' WHERE id='%s'"
        % (0 if completed else 1, id)
    )
    g.db.commit()
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
    g.db.commit()
    flash("Deleted task #'%s'" % id, 'success')
    return redirect('/todo')


@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    row = g.db.execute(
        "SELECT * FROM todos WHERE id='%s'" % id,
    )
    return jsonify(row_to_dict(row))


def row_to_dict(row):
    ret = {}
    for r in row.fetchall():
        ret['id'] = r[0]
        ret['user_id'] = r[1]
        ret['description'] = r[2]
        ret['completed'] = r[3]
    return ret
