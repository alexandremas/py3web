import sqlite3
from py3web import route, run, template

@route('/')
@route('/todo')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '0'")
    result = c.fetchall()
    c.close()
    output = template('make_table', rows=result)
    return output


run(development=True)