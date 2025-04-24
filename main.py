import sqlalchemy
from flask import Flask, render_template, redirect, request, abort, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from data.users import User
from forms.user import RegisterForm_user, LoginForm_user
from werkzeug.utils import secure_filename
import random
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['IMAGE'] = 'static\image_person'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.globals.update(BOTID='7543421341')
app.jinja_env.globals.update(BOTNAME='@hehe_rus_bot')
app.jinja_env.globals.update(
    BOTDOMAIN='http://127.0.0.1:5000')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def make_session_permanent():
    session.permanent = True


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm_user()
    avatar_file = None
    if form.avatar.data:
        avatar = form.avatar.data
        filename = secure_filename(avatar.filename)
        avatar_file = f'{random.randint(0, 99999999)}_{filename}'
        avatar.save(os.path.join(app.config['IMAGE'], avatar_file))

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form)

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация', form=form)

        user = User(
            nikname=form.nikname.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            avatar=avatar_file,
        )
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()

    if form.errors:
        app.logger.debug(f"Ошибки формы регистрации: {form.errors}")

    return render_template('register.html',
                           title='Регистрация',
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.args.get('username'):
        user_id = request.args.get("id")
        first_name = request.args.get("first_name")
        photo_url = request.args.get("photo_url")

        session['user_id'] = user_id
        session['name'] = first_name
        session['photo'] = photo_url

        return render_template('profile.html',
                               name=session['name'])
    form = LoginForm_user()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)

    return render_template('login.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()


def main():
    db_session.global_init('db/users.db')
    app.run()


if __name__ == '__main__':
    main()
