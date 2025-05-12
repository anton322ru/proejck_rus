import os
import random
from flask import Flask, render_template, redirect, request, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from data import db_session
from data.users import User, TelegramUser
from forms.user import RegisterForm_user, LoginForm_user
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/image_person'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB

# Инициализация расширений
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)

# Telegram конфигурация
app.jinja_env.globals.update(
    BOTID='7543421341',  # Замените на реальный ID бота
    BOTNAME='@hehe_rus_bot',  # Юзернейм должен начинаться с @
    BOTDOMAIN='http://127.0.0.1:5000'  # Для продакшена используйте HTTPS
)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm_user()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.nickname == form.nickname.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('profile'))

        flash('Неверный логин или пароль', 'error')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm_user()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash('Пароли не совпадают', 'error')
            return render_template('register.html', form=form)

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            flash('Пользователь с такой почтой уже существует', 'error')
            return render_template('register.html', form=form)

        avatar_filename = None
        if form.avatar.data:
            file = form.avatar.data
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config[
                'ALLOWED_EXTENSIONS']:
                filename = secure_filename(
                    f"{form.nickname.data}_{random.randint(1000, 9999)}.{file.filename.rsplit('.', 1)[1].lower()}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                avatar_filename = filename

        user = User(
            nickname=form.nickname.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            avatar=avatar_filename,
            global_mistakes=""
        )

        try:
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            db_sess.rollback()
            flash('Ошибка при регистрации', 'error')

    return render_template('register.html', form=form)


@app.route('/register_telegram', methods=['POST'])
def register_telegram():
    auth_data = request.get_json()
    print("Received Telegram auth data:", auth_data)  # Для отладки

    if not auth_data:
        return jsonify({'status': 'error', 'message': 'No data received'}), 400

    required_fields = ['id', 'first_name']
    for field in required_fields:
        if field not in auth_data:
            return jsonify({'status': 'error', 'message': f'Missing {field}'}), 400

    telegram_id = auth_data['id']
    first_name = auth_data['first_name']
    username = auth_data.get('username', f"user_{telegram_id}")

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.telegram_id == telegram_id).first()

    if not user:
        user = User(
            nickname=f"tg_{username}",
            telegram_id=telegram_id,
            global_mistakes=""
        )
        db_sess.add(user)
        db_sess.commit()

    login_user(user)
    return jsonify({
        'status': 'success',
        'redirect': url_for('profile')
    })


@app.route('/profile')
@login_required
def profile():
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    return render_template('profile.html', user=user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def main():
    db_session.global_init('db/users.db')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()