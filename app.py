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
        return f'<Student {self.roll_no}>'

class Teacher(db.Model):
    t_id = db.Column(db.Integer, primary_key=True)
    t_firstname = db.Column(db.String(100), nullable=False)
    t_lastname = db.Column(db.String(100), nullable=False)
    t_email = db.Column(db.String(80), unique=True, nullable=False)
    t_year = db.Column(db.Integer)
    t_lab = db.Column(db.String(100), nullable=False)
    t_mob = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<teacher {self.t_id}>'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/teacher/',methods=('GET', 'POST'))
def t_index():
    teachers=Teacher.query.all()
    return render_template('t_index.html',teachers=teachers)

@app.route('/teacher/<int:teacher_t_id>/')
def teacher(teacher_t_id):
    teacher = Teacher.query.get_or_404(teacher_t_id)
    return render_template('teacher.html', teacher=teacher)

@app.route('/teacher/create/', methods=('GET', 'POST'))
def create_t():
    if request.method == 'POST':
        t_id = int(request.form['t_id'])
        t_firstname = request.form['t_firstname']
        t_lastname = request.form['t_lastname']
        t_email = request.form['t_email']
        t_year = int(request.form['t_year'])
        t_lab = request.form['t_lab']
        t_mob= int(request.form['t_mob'])
        teacher = Teacher(t_id=t_id,
                          t_firstname=t_firstname,
                          t_lastname=t_lastname,
                          t_email=t_email,
                          t_year=t_year,
                          t_lab=t_lab,
                          t_mob=t_mob
        )
        db.session.add(teacher)
        db.session.commit()

        return redirect(url_for('t_index'))
    return render_template('t_create.html')

@app.route('/teacher/<int:teacher_t_id>/edit/', methods=('GET', 'POST'))
def edit_t(teacher_t_id):
    teacher = Teacher.query.get_or_404(teacher_t_id)

    if request.method == 'POST':
        t_id=int(request.form['t_id'])
        t_firstname = request.form['t_firstname']
        t_lastname = request.form['t_lastname']
        t_email = request.form['t_email']
        t_year=int(request.form['t_year'])
        t_lab = request.form['t_lab']
        t_mob = int(request.form['t_mob'])


        teacher.t_id=t_id
        teacher.t_firstname = t_firstname
        teacher.t_lastname = t_lastname
        teacher.t_email = t_email
        teacher.t_year = t_year
        teacher.t_lab=t_lab
        teacher.t_mob=t_mob

        db.session.add(teacher)
        db.session.commit()

        return redirect(url_for('t_index'))

    return render_template('t_edit.html', teacher=teacher)

@app.post('/teacher/<int:teacher_t_id>/delete/')
def delete_t(teacher_t_id):
    teacher = Teacher.query.get_or_404(teacher_t_id)
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for('t_index'))

@app.route('/teacher/search' ,methods=('GET','POST'))
def t_search():

    t_id = request.args.get('t_id')
    t_firstname = request.args.get('t_firstname')
    t_year = request.args.get('t_year')
    t_lab = request.args.get('t_lab')
    
    if  not t_id and not t_firstname and not t_year and not t_lab:
        return render_template('t_search.html')
    
    results = Teacher.query
    

    if t_id:
        results = results.filter_by(t_id = t_id)
    if t_firstname:
        results = results.filter_by(t_firstname = t_firstname)
    if t_year:
        results = results.filter_by(t_year=t_year)
    if t_lab:
        results=results.filter_by(t_lab=t_lab)
    
    results = results.all()
    
    return render_template('t_search.html', results=results)

@app.route('/student/',methods=('GET', 'POST'))
def index():
    students=Student.query.all()
    return render_template('index.html',students=students)

@app.route('/student/<int:student_roll_no>/')
def student(student_roll_no):
    student = Student.query.get_or_404(student_roll_no)
    return render_template('student.html', student=student)

@app.route('/student/create/', methods=('GET', 'POST'))
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

@app.route('/student/<int:student_roll_no>/edit/', methods=('GET', 'POST'))
def edit(student_roll_no):
    student = Student.query.get_or_404(student_roll_no)

    if request.method == 'POST':
        roll_no=int(request.form['roll_no'])
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        year=int(request.form['year'])
        branch = request.form['branch']
        mob = int(request.form['mob'])


        student.roll_no=roll_no
        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.year = year
        student.branch=branch
        student.mob=mob

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', student=student)

@app.post('/student/<int:student_roll_no>/delete/')
def delete(student_roll_no):
    student = Student.query.get_or_404(student_roll_no)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/student/search' ,methods=('GET','POST'))
def search():

    roll_no = request.args.get('roll_no')
    firstname = request.args.get('firstname')
    year = request.args.get('year')
    branch= request.args.get('branch')
    
    if  not roll_no and not firstname and not year and not branch:
        return render_template('search.html')
    
    results = Student.query
    

    if roll_no:
        results = results.filter_by(roll_no = roll_no)
    if firstname:
        results = results.filter_by(firstname = firstname)
    if year:
        results = results.filter_by(year=year)
    if branch:
        results=results.filter_by(branch=branch)
    
    results = results.all()
    
    return render_template('search.html', results=results)


