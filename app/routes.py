from app import app
from flask import render_template, session, redirect
from flask import request
from app.db import User, Session


@app.route('/')
def main_page():
    if 'is_logged' in session:
        pass
    else:
        session['is_logged'] = False
    return render_template('mainpage.html', session=session)


@app.route('/profile')
def profile_page():
    return render_template('profile.html', session=session)


@app.route('/problem')
def problem_page():
    return render_template('problem.html', session=session)


@app.route('/sign-in-page', methods=['GET', 'POST'])
def sign_in_page():
    if request.method == 'POST':
        if request.form['nickname']:
            session['is_logged'] = True
            print(request.form['nickname'])
            print(request.form['password'])
            print(session['is_logged'])
            return redirect('/')
    return render_template('sign-in-page.html', session=session)


@app.route('/sign-up-page', methods=['GET', 'POST'])
def sign_up_page():
    if request.method == 'POST':
        if request.form['pass'] != request.form['checkpass']:
            session['password_match_error'] = True
        else:
            session['password_match_error'] = False
            db_session = Session()
            user = User(request.form['name'],
                        request.form['second_name'],
                        request.form['nick'],
                        request.form['pass'],
                        request.form['email']
                        )
            db_session.add(user)
            db_session.commit()

    return render_template('sign-up-page.html', session=session)

@app.route('/successfully-add')
def successfully_add():
    pass

@app.route('/status')
def status_page():
    return render_template('status.html', session=session)


@app.route('/problems')
def problems_page():
    return render_template('problems.html', session=session)

@app.route('/admin')
def admin_page():
    return render_template('admin/admin.html', session=session)

@app.route('/logout')
def logout():
    session['is_logged'] = False
    return redirect('/')


