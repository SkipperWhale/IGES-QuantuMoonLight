from app import app, db
from flask_login import login_required
from app.source.model.models import Article
from flask import render_template, request

class BlogControl:
    @app.route("/blog/<string:label>")
    @app.route("/blog/")
    def blog(label=None):
        if label is None:
            posts = Article.query.order_by(Article.data.desc()).all()
        elif label == "likes":
            posts = db.session.query(Article, func.count(Like.email_user).label('total')).outerjoin(Like).group_by(
                Article).order_by(desc('total')).all()
            posts = [item[0] for item in posts]

        elif label == "oldest":
            posts = Article.query.order_by(Article.data.asc()).all()

        else:
            posts = Article.query.filter_by(label=label).order_by(Article.data.desc()).all()

        return render_template("blog.html", posts=posts)

    @app.route("/ArticleApproval")
    def ArticleApproval():
        posts = Article.query.filter_by(authorized=False).order_by(Article.data.desc()).all()

        return render_template("ArticleApproval.html", posts=posts)

    @app.route('/post/<int:post_id>')
    def post(post_id):
        post = Article.query.filter_by(id=post_id).one()
        comments = Comment.query.filter_by(id_article=post_id).all()
        return render_template('post.html', post=post, comments=comments)

    @app.route('/add')
    @login_required
    def add():
        return render_template('add.html')