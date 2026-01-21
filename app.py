import mysql.connector
from flask import Flask, render_template, g, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
import functools
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def get_db_connection():
    """Establishes and returns a database connection.
    Stores connection in Flask's global `g` object for the request duration.
    """
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=app.config['DB_HOST'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD'],
                database=app.config['DB_NAME']
            )
        except mysql.connector.Error as err:
            # In a real app, log this error
            print(f"Error connecting to database: {err}")
            return None
    return g.db

@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- Auth Decorator ---
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('admin_id') is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

# --- Public Routes ---

@app.route('/')
def home():
    """Public Home Route - Lists all published shayari."""
    conn = get_db_connection()
    shayari_list = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM shayari WHERE is_published = 1 ORDER BY created_at DESC")
        shayari_list = cursor.fetchall()
        cursor.close()
    return render_template('public/index.html', shayari_list=shayari_list)

@app.route('/shayari/<int:id>')
def shayari_detail(id):
    """Detail Route - Shows a single shayari."""
    conn = get_db_connection()
    shayari = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM shayari WHERE id = %s AND is_published = 1", (id,))
        shayari = cursor.fetchone()
        cursor.close()
    
    if shayari is None:
        return render_template('public/base.html', content="<h2 class='text-center text-red-500'>Shayari not found.</h2>"), 404 # Fallback
        
    return render_template('public/shayari_detail.html', shayari=shayari)

# --- Admin Routes ---

@app.route('/admin/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        error = None
        user = None
        
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password.'
            
        if error is None:
            session.clear()
            session['admin_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('admin_dashboard'))
            
        flash(error, 'error')
        
    return render_template('admin/login.html')

@app.route('/admin/logout')
def logout():
    session.clear()
    flash('By Allah, you have logged out safely.', 'success')
    return redirect(url_for('login'))

@app.route('/admin')
def admin_redirect():
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    conn = get_db_connection()
    shayari_list = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM shayari ORDER BY created_at DESC")
        shayari_list = cursor.fetchall()
        cursor.close()
    return render_template('admin/dashboard.html', shayari_list=shayari_list)

@app.route('/admin/shayari/add', methods=('GET', 'POST'))
@login_required
def add_shayari():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        mood = request.form['mood']
        is_published = 1 if request.form.get('is_published') else 0
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO shayari (title, content, category, mood, is_published) VALUES (%s, %s, %s, %s, %s)",
                (title, content, category, mood, is_published)
            )
            conn.commit()
            cursor.close()
            flash('Shayari added successfully.', 'success')
            return redirect(url_for('admin_dashboard'))
            
    return render_template('admin/add_shayari.html')

@app.route('/admin/shayari/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit_shayari(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            category = request.form['category']
            mood = request.form['mood']
            is_published = 1 if request.form.get('is_published') else 0
            
            cursor.execute(
                "UPDATE shayari SET title = %s, content = %s, category = %s, mood = %s, is_published = %s WHERE id = %s",
                (title, content, category, mood, is_published, id)
            )
            conn.commit()
            cursor.close()
            flash('Shayari updated successfully.', 'success')
            return redirect(url_for('admin_dashboard'))
        
        # GET request
        cursor.execute("SELECT * FROM shayari WHERE id = %s", (id,))
        shayari = cursor.fetchone()
        cursor.close()
        
        if shayari is None:
            flash('Shayari not found.', 'error')
            return redirect(url_for('admin_dashboard'))
            
        return render_template('admin/edit_shayari.html', shayari=shayari)
    return redirect(url_for('admin_dashboard')) # Fallback if DB fails

@app.route('/admin/shayari/delete/<int:id>', methods=('POST',))
@login_required
def delete_shayari(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM shayari WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        flash('Shayari deleted.', 'success')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
