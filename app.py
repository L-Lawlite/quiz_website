from flask import Flask, flash, render_template, request, redirect, url_for, session, g
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'.encode('utf8')

DATABASE = 'quiz_master.db'

# Database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Initializing database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']  # admin or user

        db = get_db()
        if user_type == 'admin':
            admin = db.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password)).fetchone()
            if admin:
                session['admin_logged_in'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid admin credentials')
        else:
            user = db.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username, password)).fetchone()
            if user:
                session['user_logged_in'] = True
                session['user_id'] = user['id']
                return redirect(url_for('user_dashboard'))
            else:
                flash('Invalid user credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        qualification = request.form['qualification']
        dob = request.form['dob']

        db = get_db()
        # Check if username already exists
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        if user:
            flash('Username already exists. Please choose a different username.')
            return render_template('register.html')

        # Insert new user into the database
        db.execute('INSERT INTO user (username, password, full_name, qualification, dob) VALUES (?, ?, ?, ?, ?)', 
                   (username, password, full_name, qualification, dob))
        db.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

@app.route('/user')
def user_dashboard():
    # User dashboard logic here
    pass

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin/subjects')
def view_subjects():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    subjects = db.execute('SELECT * FROM subject').fetchall()
    return render_template('subjects.html', subjects=subjects)

@app.route('/admin/subjects/add', methods=['GET', 'POST'])
def add_subject():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db = get_db()
        db.execute('INSERT INTO subject (name, description) VALUES (?, ?)', (name, description))
        db.commit()
        return redirect(url_for('view_subjects'))
    return render_template('add_subject.html')

@app.route('/admin/subjects/edit/<int:subject_id>', methods=['GET', 'POST'])
def edit_subject(subject_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    subject = db.execute('SELECT * FROM subject WHERE id = ?', (subject_id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db.execute('UPDATE subject SET name = ?, description = ? WHERE id = ?', (name, description, subject_id))
        db.commit()
        return redirect(url_for('view_subjects'))
    return render_template('edit_subject.html', subject=subject)

@app.route('/admin/subjects/delete/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    db.execute('DELETE FROM subject WHERE id = ?', (subject_id,))
    db.commit()
    return redirect(url_for('view_subjects'))

@app.route('/admin/chapters')
def view_chapters():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    chapters = db.execute('SELECT * FROM chapter').fetchall()
    return render_template('chapters.html', chapters=chapters)

@app.route('/admin/chapters/add', methods=['GET', 'POST'])
def add_chapter():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        subject_id = request.form['subject_id']
        name = request.form['name']
        description = request.form['description']
        db = get_db()
        db.execute('INSERT INTO chapter (subject_id, name, description) VALUES (?, ?, ?)', (subject_id, name, description))
        db.commit()
        return redirect(url_for('view_chapters'))
    return render_template('add_chapter.html')

@app.route('/admin/chapters/edit/<int:chapter_id>', methods=['GET', 'POST'])
def edit_chapter(chapter_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    chapter = db.execute('SELECT * FROM chapter WHERE id = ?', (chapter_id,)).fetchone()
    if request.method == 'POST':
        subject_id = request.form['subject_id']
        name = request.form['name']
        description = request.form['description']
        db.execute('UPDATE chapter SET subject_id = ?, name = ?, description = ? WHERE id = ?', (subject_id, name, description, chapter_id))
        db.commit()
        return redirect(url_for('view_chapters'))
    return render_template('edit_chapter.html', chapter=chapter)

@app.route('/admin/chapters/delete/<int:chapter_id>', methods=['POST'])
def delete_chapter(chapter_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    db.execute('DELETE FROM chapter WHERE id = ?', (chapter_id,))
    db.commit()
    return redirect(url_for('view_chapters'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
