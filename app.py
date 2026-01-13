from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Подключение к PostgreSQL через DATABASE_URL из Render
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql+psycopg://flask_and_postgresql_user:"
    "qRCj6o4c9aIfNWQ6IgteN1IYDT7wRjFw@"
    "dpg-d5iu7e14tr6s73dvta30-a:5432/"
    "flask_and_postgresql"
)

db = SQLAlchemy(app)

# Модель статьи
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Article id={self.id!r}>'

# Создание таблиц при запуске
with app.app_context():
    db.create_all()

# Главная
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

# О проекте
@app.route('/about')
def about():
    return render_template('about.html')

# Список постов
@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)

# Детальный просмотр поста
@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get_or_404(id)
    return render_template('post_detail.html', article=article)

# Удаление поста
@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'При удалении статьи произошла ошибка'


# Редактирование поста
@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get_or_404(id)

    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При редактировании статьи произошла ошибка'
    else:
        return render_template('post_update.html', article=article)


# Создание нового поста
@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create-article.html')


if __name__ == '__main__':
    app.run(debug=True)