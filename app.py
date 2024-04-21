from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


@app.route('/')
def main():
    db = sqlite3.connect('notes.db')
    c = db.cursor()
    c.execute('SELECT id,title,content FROM listnotes')
    notes = c.fetchall()
    db.close()
    return render_template('index.html', notes=notes)


@app.route('/note/<int:id>')
def articles(id):
    db = sqlite3.connect('notes.db')
    c = db.cursor()
    c.execute("SELECT * FROM listnotes WHERE id = ?", (id,))
    note = c.fetchone()
    db.close()
    return render_template('note.html', note = note)


@app.route('/add-note', methods =['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add-note.html')
    else:
        title_n = request.form['title']
        content_n = request.form['content']
        db = sqlite3.connect('notes.db')
        c = db.cursor()
        c.execute("INSERT INTO listnotes(title, content)  VALUES (?,?)",(title_n, content_n))
        db.commit()
        db.close()
        return redirect(url_for('main'))


@app.route('/edit/<int:id>', methods =['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        db = sqlite3.connect('notes.db')
        c = db.cursor()
        c.execute('SELECT * FROM listnotes WHERE id=?', (id,))
        note = c.fetchone()
        return render_template('edit-note.html',note = note)
    else:
        new_title = request.form['new_title']
        new_content = request.form['new_content']
        db = sqlite3.connect('notes.db')
        c = db.cursor()
        c.execute('UPDATE listnotes SET title = ?, content = ? WHERE id = ?', (new_title, new_content, id))
        db.commit()
        db.close()
        return redirect(url_for('main'))


@app.route('/delete/<int:id>')
def delete(id):
    db = sqlite3.connect('notes.db')
    c = db.cursor()
    c.execute('DELETE FROM listnotes WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True)