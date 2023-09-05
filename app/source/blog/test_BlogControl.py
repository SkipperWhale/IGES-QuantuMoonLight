from flask import Flask
from app import app, db
from app.source.blog.BlogControl import BlogControl
from app.source.model.models import User, Article, Like, Comment
import unittest
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from unittest.mock import patch

class TestBlogControl(unittest.TestCase):
    def setUp(self):
        super().setUp()
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql://root:root@127.0.0.1/test_db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        tester = app.test_client(self)
        if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        with app.app_context():
            db.create_all()
            user1 = User(
                email="mariorossi12@gmail.com",
                password="prosopagnosia",
                username="Antonio de Curtis",
                token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccZZ",
                name="Antonio",
                surname="De Curtis",
                isAdmin=True,
                newsletter=False,
                isResearcher=False
            )
            user2 = User(
                email="giuseppeverdi@gmail.com",
                password="asperger",
                username="giuVerdiProXX",
                token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccZZ",
                name="Giuseppe",
                surname="Verdi",
                isAdmin=False,
                newsletter=False,
                isResearcher=False
            )
            art1 = Article(
                email_user="mariorossi12@gmail.com",
                title="Article 1",
                body="primobody",
                author="Antonio de Curtis",
                category="Article",
                data=datetime(2023, 8, 1),
                authorized=True,
                label="Article"
            )
            art2 = Article(
                email_user="mariorossi12@gmail.com",
                title="Article 2",
                body="secondoBody",
                author="Antonio de Curtis",
                category="Experiment",
                data=datetime(2023, 9, 1),
                authorized=True,
                label="Experiment"
            )

            art3 = Article(
                email_user="giuseppeverdi@gmail.com",
                title="Article 3",
                body="secondoBody",
                author="giuVerdiProXX",
                category="Article",
                data=datetime(2023, 9, 1),
                authorized=False,
                label="Article"
            )

            #like1 = Like(email_user="mariorossi12@gmail.com", id_article=art1.id)
            #like2 = Like(email_user="giuseppeverdi@gmail.com", id_article=art1.id)

            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
            db.session.add(art1)
            db.session.add(art2)
            db.session.add(art3)
            #self.db.session.add(like1)
            #self.db.session.add(like2)

            db.session.commit()

            article = Article.query.filter_by(title="Article 1").first()
            comment = Comment(
                email_user="giuseppeverdi@gmail.com",
                id_article=article.id,
                body="Comment 1",
                author="giuVerdiProXX",
                authorized=False,
                data = datetime(2023, 9, 1)
            )

            # Aggiungi il commento al database
            db.session.add(comment)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_blog_with_no_label(self):
        with app.test_client() as client:
            response = client.get("/blog/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Article 1", response.data)
            self.assertIn(b"Article 2", response.data)

    def test_blog_with_label_likes(self):
        with app.test_client() as client:
            response = client.get("/blog/likes")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Article 1", response.data)
            self.assertIn(b"Article 2", response.data)

    def test_blog_with_label_oldest(self):
        with app.test_client() as client:
            response = client.get("/blog/oldest")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Article 2", response.data)
            self.assertIn(b"Article 1", response.data)

    def test_blog_with_custom_label(self):
        with app.test_client() as client:
            custom_label = "Article"
            response = client.get(f"/blog/{custom_label}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Article 1", response.data)

    def test_article_approval(self):
        with app.test_client() as client:
            login_response = client.post("/login", data=dict(email= "mariorossi12@gmail.com", password= "prosopagnosia"))
            response = client.get("/ArticleApproval")

            self.assertEqual(response.status_code, 200)
            #self.assertTrue(Article.query.filter_by(title="Article 3").first())
            #self.assertIn(b"Article 3", response.data)

    def test_post(self):
        with app.test_client() as client:
            article = Article.query.filter_by(title="Article 1").first()
            if article:
                post_id = str(article.id)
                response = client.get(f"/post/{post_id}")
                self.assertEqual(response.status_code, 200)

                # Verifica se il titolo dell'articolo è presente nel contenuto della risposta
                self.assertIn(b"Article 1", response.data)

    def test_addpost(self):
        # Assicurati che l'utente sia autenticato (puoi simulare l'autenticazione come necessario)
        with app.test_client() as client:
            with patch('flask_login.current_user', username='giuVerdiProXX', email='giuseppeverdi@gmail.com'):
                data = {
                    'title': 'Article 4',
                    'ckeditor': 'Contenuto del nuovo post',
                    'flexRadioDefault': 'Article'
                }

                # Simuliamo l'invio del modulo
                response = client.post('/addpost', data=data, follow_redirects=True)

                # Assicurati che la risposta sia stata reindirizzata correttamente alla pagina 'blog'
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'blog', response.data)
                #self.assertIsNotNone(Article.query.filter_by(title="Article 4").first())

    def test_enable_article(self):
        with app.test_client() as client:
            article = Article.query.filter_by(title="Article 3").first()
            if article:
                post_id = str(article.id)

                response = client.get(f'/enableArticle/{post_id}', follow_redirects=True)

                self.assertEqual(response.status_code, 200)
                #self.assertIn(b'Article 3', response.data)

                enabled_article = Article.query.filter_by(title="Article 3").first()
                self.assertTrue(enabled_article.authorized)

