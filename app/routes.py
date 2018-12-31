from app import app
from flask import render_template, session, redirect
from flask import request
from app.db import User, Session, News, Problem
from test_system.ts import test

db_session = Session()


@app.route('/')
def main_page():
    if 'is_logged' in session:
        pass
    else:
        session['is_logged'] = False
    news_tuple = db_session.query(News).all()
    return render_template('mainpage.html', session=session, news_tuple=news_tuple)


@app.route('/profile/<nickname>')
def profile_page(nickname):
    if 'admin' in session:
        if session['admin']:
            return redirect('/admin')
    return render_template('profile.html', session=session)


@app.route('/problem/<int:problem_id>', methods=['GET', 'POST'])
def problem_page(problem_id):
    problem = db_session.query(Problem).filter_by(id=problem_id).first()
    if request.method == 'POST':
        if 'problem_solution' in request.form:
            test(request.form['problem_solution'], 'a_plus_b', path='test_system')

    return render_template('problem.html', session=session, problem=problem)


@app.route('/sign-in-page', methods=['GET', 'POST'])
def sign_in_page():
    if request.method == 'POST':
        if request.form['nickname']:
            sign_in(request.form['nickname'], request.form['password'])
            if 'admin' not in session:
                return redirect('/sign-in-page')
            elif session['admin']:
                return redirect('/admin')
            else:
                return redirect('/profile/'+session['nickname'])
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
            add_user(False)
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
    problems_tuple = db_session.query(Problem).all()
    return render_template('problems.html', session=session, problems_tuple=problems_tuple)


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'GET' and (not('admin' in session) or not session['admin']):
        return redirect('/')
    elif request.method == 'POST':
            if 'nick' in request.form:
                add_user(True)
            elif 'new_label' in request.form:
                add_new()
            elif 'problem_name' in request.form:
                add_problem()
    return render_template('admin.html', session=session)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


def add_user(admin):
    session['password_match_error'] = False
    user = User(request.form['name'],
                request.form['second_name'],
                request.form['nick'],
                request.form['pass'],
                request.form['email'],
                admin
                )
    db_session.add(user)
    db_session.commit()


def add_new():
    new = News(request.form['new_label'],
               request.form['new_body']
               )
    db_session.add(new)
    db_session.commit()


def add_problem():
    problem = Problem(request.form['problem_name'],
                      request.form['problem_body'],
                      request.form['problem_solution'],
                      request.form['problem_in'],
                      request.form['problem_out'],
                      request.form['theme'],
                      request.form['complexity']
                      )
    print(problem)
    db_session.add(problem)
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
        print("\n\n\n admin --------> '%s'" % obj.admin)
