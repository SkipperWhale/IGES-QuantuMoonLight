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

    @app.route('/like/<int:action>', methods=['GET'])
    @app.route('/like/', methods=['GET'])
    @login_required
    def like(action=0):
        if action == 1:
            email_user = current_user.email
            data = request.args
            id_article = data['data']
            like = Like(email_user=email_user, id_article=id_article)

            db.session.add(like)
            db.session.commit()

        else:
            email_user = current_user.email
            data = request.args
            id_article = data['data']
            like = Like.query.filter_by(
                email_user=email_user,
                id_article=id_article).first()

            db.session.delete(like)
            db.session.commit()

        return render_template('add.html')
    @app.route('/addpost', methods=['POST'])
    @login_required
    def addpost():
        title = request.form['title']
        author = current_user.username
        email = current_user.email
        body = request.form.get('ckeditor')

        label = request.form['flexRadioDefault']

        post = Article(
            title=title,
            author=author,
            body=body,
            data=datetime.now(),
            email_user=email,
            label=label)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('blog'))
    @app.route('/enableArticle/<int:article_id>', methods=['POST', 'GET'])
    def enableArticle(article_id):
        article = Article.query.filter_by(id=article_id).one()
        article.authorized = True
        db.session.commit()

        return redirect(url_for('ArticleApproval'))



    @app.route('/deleteArticle/<int:article_id>', methods=['POST', 'GET'])
    def deleteArticle(article_id):
        article = Article.query.filter_by(id=article_id).one()
        db.session.delete(article)
        db.session.commit()
        return redirect(url_for('ArticleApproval'))



