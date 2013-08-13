import sqlite3
from py3web import route, run


@route('/')
def root():
    return '<h1>Welcome </h1>'

@route('/todo')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    return str(result)
##comment on deployment
DEVELOPMENT=True
run()