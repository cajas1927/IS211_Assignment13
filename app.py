from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Mockup user credentials (replace with a more secure authentication mechanism in production)
USERNAME = 'admin'
PASSWORD = 'password'

# Sample data for students and quizzes
STUDENTS = [
    {'id': 1, 'first_name': 'John', 'last_name': 'Smith'},
    {'id': 2, 'first_name': 'Jane', 'last_name': 'Doe'},
    {'id': 3, 'first_name': 'Bob', 'last_name': 'Johnson'},
    
]

QUIZZES = [
    {'id': 1, 'subject': 'Python Basics', 'num_questions': 5, 'quiz_date': '2015-02-05'},
    {'id': 2, 'subject': 'Web Development', 'num_questions': 10, 'quiz_date': '2015-02-10'},
    {'id': 3, 'subject': 'Database Management', 'num_questions': 8, 'quiz_date': '2015-02-15'},
   
]

# Initialize the session variable for login status
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 600  # 10 minutes
app.secret_key = 'your_secret_key'

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.username.data == USERNAME and form.password.data == PASSWORD:
            # Successful login
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Incorrect credentials
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in; if not, redirect to the login page
    # You can implement a more robust user authentication system in production
    # For simplicity, we'll use a session variable to track the login status
    if not session.get('logged_in'):
        flash('You need to login first.', 'warning')
        return redirect(url_for('login'))

    return render_template('dashboard.html', students=STUDENTS, quizzes=QUIZZES)


@app.route('/student/<int:student_id>')
def view_student_results(student_id):
    # Check if the user is logged in; if not, redirect to the login page
    if not session.get('logged_in'):
        flash('You need to login first.', 'warning')
        return redirect(url_for('login'))

    # Get the student from the list (replace with database query)
    student = next((s for s in STUDENTS if s['id'] == student_id), None)

    if student:
        # Get the quiz results for the student (replace with database query)
        student_results = [result for result in STUDENT_RESULTS if result['student_id'] == student_id]

        return render_template('view_student_results.html', student=student, results=student_results)
    else:
        return "Student not found."


@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    # Check if the user is logged in; if not, redirect to the login page
    if not session.get('logged_in'):
        flash('You need to login first.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get form data
        subject = request.form.get('subject')
        num_questions = request.form.get('num_questions')
        quiz_date = request.form.get('quiz_date')

        # Validate form data (add more validation as needed)
        if not subject or not num_questions or not quiz_date:
            flash('Please provide all quiz details.', 'danger')
        else:
            # Add quiz to the list (replace with database insertion)
            new_quiz = {'id': len(QUIZZES) + 1, 'subject': subject, 'num_questions': num_questions, 'quiz_date': quiz_date}
            QUIZZES.append(new_quiz)
            flash('Quiz added successfully!', 'success')
            return redirect(url_for('dashboard'))

    return render_template('add_quiz.html')


@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    # Check if the user is logged in; if not, redirect to the login page
    if not session.get('logged_in'):
        flash('You need to login first.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        # Validate form data (add more validation as needed)
        if not first_name or not last_name:
            flash('Please provide both first name and last name.', 'danger')
        else:
            # Add student to the list (replace with database insertion)
            new_student = {'id': len(STUDENTS) + 1, 'first_name': first_name, 'last_name': last_name}
            STUDENTS.append(new_student)
            flash('Student added successfully!', 'success')
            return redirect(url_for('dashboard'))

    return render_template('add_student.html')

if __name__ == '__main__':
    app.run(debug=True)
