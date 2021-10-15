from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lide.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    work = db.Column(db.String(100), nullable=True)
    about = db.Column(db.TEXT, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Article %r>' % self.id




@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении бланка произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.name = request.form['name']
        article.work = request.form['work']
        article.about = request.form['about']
        try:
            db.session.commit()
            return redirect('/posts')
        except: return "При обновлении бланка произошла ошибка"
    else:
        return render_template("post_update.html", article=article)



@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        name = request.form['name']
        work = request.form['work']
        about = request.form['about']

        article = Article(name=name, work=work, about=about)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При заполнении бланка произошла ошибка"
    else:
        return render_template("create-article.html")



if __name__ == '__main__':
    app.run(debug=True)
