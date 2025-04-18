from data import db_session
from data.users import User
from forms.user import RegisterForm_user, LoginForm_user
import sqlalchemy
from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hihi_haha'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init('db/users.db')
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    info = db_sess.query(Job, User).join(User).all()
    return render_template('index.html', info=info)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm_user()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.speciality = form.speciality.data
        user.position = form.position.data
        user.address = form.address.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    else:
        print(form.errors)
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm_user()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/job', methods=['GET', 'POST'])
def add_job():
    form = RegisterForm_job()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Job).filter(Job.job == form.job.data).first():
            return render_template('reg_job.html', title='Регистрация',
                                   form=form,
                                   message="Такая работа уже есть")
        job = Job(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('reg_job.html', title='Регистрация работы', form=form)


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = RegisterForm_job()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Job).filter(Job.id == id
                                        ).first()
        if job:
            form.job.data = job.job
            form.is_finished.data = job.is_finished
            form.work_size.data = job.work_size
            form.team_leader.data = job.team_leader
            form.collaborators.data = job.collaborators
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Job).filter(Job.id == id,
                                        Job.user == current_user
                                        ).first()
        if job and (current_user.id == 1 or current_user.id == job.team_leader):
            job.job = form.job.data
            job.team_leader = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('reg_job.html',
                           title='Редактирование работы',
                           form=form)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).filter(Job.id == id,
                                     Job.user == current_user
                                     ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


if __name__ == '__main__':
    main()
