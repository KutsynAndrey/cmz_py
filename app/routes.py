from app import app
from flask import render_template, session, redirect
from flask import request
from app.db import User, Session


db_session = Session()


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
            sign_in(request.form['nickname'], request.form['password'])
            if session['admin']:
                return redirect('/admin')
            else:
                return redirect('/profile')
        if session['is_logged']:
            return redirect('/')
    return render_template('sign-in-page.html', session=session)


@app.route('/sign-up-page', methods=['GET', 'POST'])
def sign_up_page():
    if request.method == 'POST':
        if request.form['pass'] != request.form['checkpass']:
            session['password_match_error'] = True
            session['identiсal_nick_error'] = False
        elif check_identity():
            session['identiсal_nick_error'] = True
            session['password_match_error'] = False
        else:
            add_user()
            session['identiсal_nick_error'] = False
            session['password_match_error'] = False
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


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'GET' and (not('admin' in session) or session['admin'] == False):
        return redirect('/')

    return render_template('admin.html', session=session)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


def add_user():
    session['password_match_error'] = False
    user = User(request.form['name'],
                request.form['second_name'],
                request.form['nick'],
                request.form['pass'],
                request.form['email'],
                False
                )
    db_session.add(user)
    db_session.commit()


def check_identity():
    for person in db_session.query(User):
        if person.nickname == request.form['nick']:
            return True
    return False


def sign_in(nickname, password):
    obj = db_session.query(User).filter_by(nickname=nickname).first()
    if obj is None:
        session['Wrong_nickname'] = True
    elif obj.password != password:
        session['Wrong_password'] = True
        session['Wrong_nickname'] = False
    else:
        session['Wrong_nickname'] = False
        session['Wrong_password'] = False
        session['is_logged'] = True
        session['nickname'] = obj.nickname
        session['name'] = obj.name
        session['second_name'] = obj.second_name
        session['email'] = obj.email
        session['admin'] = obj.admin









