import sqlite3

# Create or open the SQLite database
conn = sqlite3.connect('feedback.db')
cursor = conn.cursor()

# Create the feedback table
cursor.execute('''
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully!")






from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # You can use a more secure key for production

# Dummy admin credentials (for simplicity)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

# Route for feedback form submission
@app.route('/', methods=['GET', 'POST'])
def feedback_form():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        
        # Insert feedback into database
        with sqlite3.connect("feedback.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO feedback (name, message) VALUES (?, ?)", (name, message))
            conn.commit()
        return redirect(url_for('feedback_form'))
    return render_template('feedback_form.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if credentials are correct
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True  # Create a session for the logged-in admin
            return redirect(url_for('admin_view'))
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")
    
    return render_template('login.html')

# Route for admin view to display all feedback (accessible only when logged in)
@app.route('/admin')
def admin_view():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    with sqlite3.connect("feedback.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, message, timestamp FROM feedback ORDER BY timestamp DESC")
        feedbacks = cursor.fetchall()
    return render_template('admin_view.html', feedbacks=feedbacks)

# Route for logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Remove the session to log out
    return redirect(url_for('login'))  # Redirect to login page after logout

if __name__ == '__main__':
    app.run(debug=True)
