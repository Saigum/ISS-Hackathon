import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'contacts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ...

class Student(db.Model):
    roll_no = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.Integer)
    branch = db.Column(db.String(100), nullable=False)
    mob = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Student {self.firstname}>'


@app.route('/')
def index():
    students=Student.query.all()
    return render_template('index.html',students=students)

@app.route('/<int:student_roll_no>/')
def student(student_roll_no):
    student = Student.query.get_or_404(student_roll_no)
    return render_template('student.html', student=student)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        roll_no = int(request.form['roll_no'])
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        year = int(request.form['year'])
        branch = request.form['branch']
        mob= int(request.form['mob'])
        student = Student(roll_no=roll_no,
                          firstname=firstname,
                          lastname=lastname,
                          email=email,
                          year=year,
                          branch=branch,
                          mob=mob
        )
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html')