from app import app
from flask import render_template, session, redirect
from flask import request
from app.db import User, Session, News, Problem
from app.db import Status
from test_system.ts import test
from datetime import datetime

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
            session['all_result'], err = test(request.form['problem_solution'], problem.problem_title)
            if err == "not found":
                t = time_now(str(datetime.now()))
                add_solution(problem_id,
                             session['all_result'][0],
                             session['all_result'][1],
                             t,
                             problem.problem_theme,
                             problem.problem_title,
                             session['all_result'][2],
                             request.form['problem_solution'],
                             err,
                             session['all_result'][3],
                             str(session['all_result'][4])
                             )

            else:
                t = time_now(str(datetime.now()))
                add_solution(problem_id,
                             session['all_result'][0],
                             session['all_result'][1],
                             t,
                             problem.problem_theme,
                             problem.problem_title,
                             session['all_result'][2],
                             request.form['problem_solution'],
                             err,
                             session['all_result'][3],
                             str(session['all_result'][4])
                             )
            return redirect('/result/' + str(problem_id) + '/' + t)

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


@app.route('/status', methods=['GET'])
def status_page():
    results = db_session.query(Status).order_by('time').all()
    results.reverse()
    return render_template('status.html', session=session, results=results)


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


@app.route('/result/<int:problem_id>/<add_data>', methods=['GET'])
def show_result(problem_id, add_data):
    result = db_session.query(Status).filter_by(problem_id=problem_id, user_id=session['user_id'], time=add_data).first()
    t = result.tests_result.split("\n")
    t2 = result.compilation_time.split("\n")
    code = result.solution.split("\n")
    error = result.error.split("\n")
    m = result.memory.split("\n")
    print(t)
    return render_template('result.html', session=session, tests=t, size=len(t), time=t2, err=error, code=code, ram=m)


@app.route('/sends', methods=['GET'])
def my_sends():
    my_result = db_session.query(Status).filter_by(user_id=session['user_id']).order_by("time").all()
    my_result.reverse()
    return render_template('my-sends.html', session=session, my_result=my_result)


def add_user(admin):
    session['password_match_error'] = False
    user = User(request.form['name'],
                request.form['second_name'],
                request.form['nick'],
                request.form['pass'],
                request.form['email'],
                admin,
                time_now(str(datetime.now()))
                )
    db_session.add(user)
    db_session.commit()


def add_new():
    new = News(request.form['new_label'],
               request.form['new_body'],
               time_now(str(datetime.now()))
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
        session['user_id'] = obj.id
        print("\n\n\n admin --------> '%s'" % obj.admin)


def time_now(time):
    twms = ''
    for i in time:
        if i == '.':
            break
        twms += i

    return twms


def add_solution(problem_id, result, verdict, t, theme, title, time_compilation, solution, error, ram, mct):
    send = Status(session['user_id'],
                  problem_id,
                  result,
                  verdict,
                  t,
                  theme,
                  title,
                  time_compilation,
                  ram,
                  session['nickname'],
                  solution,
                  error,
                  mct
                  )
    db_session.add(send)
    db_session.commit()



