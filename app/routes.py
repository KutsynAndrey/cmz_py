from app import app
from flask import render_template
from flask import request


@app.route('/')
def main_page():
    return render_template('mainpage.html')


@app.route('/profile')
def profile_page():
    return render_template('profile.html')


@app.route('/problem')
def problem_page():
    return render_template('problem.html')


@app.route('/sign-in-page', methods=['GET', 'POST'])
def sign_in_page():
    if request.method == 'POST':
        if request.form['nickname']:
            print(request.form['nickname'])
            print(request.form['password'])
    return render_template('sign-in-page.html')


@app.route('/sign-up-page', methods=['GET', 'POST'])
def sign_up_page():
    if request.method == 'POST':
        if request.form['nick']:
            print(request.form['nick'])
            print(request.form['pass'])
            print(request.form['school'])
            print(request.form['username'])
    return render_template('sign-up-page.html')


@app.route('/status')
def status_page():
    return render_template('status.html')


@app.route('/problems')
def problems_page():
    return render_template('problems.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')


def is_logged():
    pass

