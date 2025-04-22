from data.users import User
from forms.user import RegisterForm_user, LoginForm_user
import sqlalchemy
from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from data.users import User
from forms.user import RegisterForm_user, LoginForm_user


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key-here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form)

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form)


        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
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
    form = LoginForm_user()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)


    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()


def main():
    db_session.global_init('db/users.db')
    app.run()


if __name__ == '__main__':
    main()
