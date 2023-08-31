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

