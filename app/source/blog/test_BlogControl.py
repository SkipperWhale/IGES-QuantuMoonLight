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

    # Configurazione e inizializzazione dell'ambiente di test
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

            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
            db.session.add(art1)
            db.session.add(art2)
            db.session.add(art3)

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
            db.session.add(comment)
            db.session.commit()

    # Rimuove tutte le tabelle del database nell'ambiente di test         
    def tearDown(self):
        with app.app_context():
            db.drop_all()

    # Verifica che la pagina /blog/ restituisca uno stato HTTP 200 e contenga
    # i nomi degli articoli "Article 1" e "Article 2" nel corpo della risposta.
    def test_blog_with_no_label(self):
        with app.test_client() as client:
            response = client.get("/blog/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Article 1", response.data)
            self.assertIn(b"Article 2", response.data)

    # Verifica che la pagina /blog/likes restituisca uno stato HTTP 200 e contenga
    # i nomi degli articoli "Article 1" e "Article 2" nel corpo della risposta.
    def test_blog_with_label_likes(self):
        with app.test_client() as client:
            response = client.get("/blog/likes")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Article 1", response.data)
            self.assertIn(b"Article 2", response.data)

    # Verifica che la pagina /blog/oldest restituisca uno stato HTTP 200 e contenga
    # i nomi degli articoli "Article 2" e "Article 1" nel corpo della risposta.
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

    # Verifica che la pagina /blog/{custom_label} restituisca uno stato HTTP 200 e contenga
    # il nome dell'articolo "Article 1" nel corpo della risposta quando si utilizza
    # la label personalizzata "Article".
    def test_article_approval(self):
        with app.test_client() as client:
            login_response = client.post("/login", data=dict(email= "mariorossi12@gmail.com", password= "prosopagnosia"))
            response = client.get("/ArticleApproval")

            self.assertEqual(response.status_code, 200)
         
    # Verifica se la pagina /post/{post_id} restituisce uno stato HTTP 200 e
    # se il titolo dell'articolo "Article 1" è presente nel corpo della risposta.
    def test_post(self):
        with app.test_client() as client:
            article = Article.query.filter_by(title="Article 1").first()
            if article:
                post_id = str(article.id)
                response = client.get(f"/post/{post_id}")
                self.assertEqual(response.status_code, 200)

                
                self.assertIn(b"Article 1", response.data)

    # Verifica se l'aggiunta di un nuovo post tramite la pagina /addpost restituisce uno stato HTTP 200
    # e se la parola chiave 'blog' è presente nel corpo della risposta dopo l'invio del modulo.
    def test_addpost(self):
        
        with app.test_client() as client:
            with patch('flask_login.current_user', username='giuVerdiProXX', email='giuseppeverdi@gmail.com'):
                data = {
                    'title': 'Article 4',
                    'ckeditor': 'Contenuto del nuovo post',
                    'flexRadioDefault': 'Article'
                }

                # Simuliamo l'invio del modulo
                response = client.post('/addpost', data=data, follow_redirects=True)

                
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'blog', response.data)
               
    # Verifica se l'abilitazione di un articolo specifico tramite la pagina /enableArticle/{post_id}
    # restituisce uno stato HTTP 200 e se l'articolo specifico "Article 3" è abilitato nel database
    # dopo l'operazione.
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

    # Verifica se l'eliminazione di un articolo specifico tramite la pagina /deleteArticle/{post_id}
    # restituisce uno stato HTTP 200 e se l'articolo specifico "Article 3" non esiste più nel database
    # dopo l'operazione.
    def test_delete_article(self):
        with app.test_client() as client:
            article = Article.query.filter_by(title="Article 3").first()
            if article:
                post_id = str(article.id)

                response = client.get(f'/deleteArticle/{post_id}', follow_redirects=True)

                self.assertEqual(response.status_code, 200)

                deleted_article = Article.query.filter_by(title="Article 3").first()
                self.assertIsNone(deleted_article)

    # Verifica se l'abilitazione di un commento specifico tramite la pagina /enableComment/{comment_id}
    # restituisce un reindirizzamento (stato HTTP 302) e se il commento specifico è abilitato nel database
    # dopo l'operazione.
    def test_enable_comment(self):
        with app.test_client() as client:
            article = Article.query.filter_by(title="Article 1").first()
            comment = Comment.query.filter_by(id_article=article.id).first()
            if article and comment:
                comment_id = str(comment.id)

                response = client.get(f'/enableComment/{comment_id}', headers={'Referer': '/previous-page'})

                self.assertEqual(response.status_code, 302)
                enabled_comment = Comment.query.filter_by(id_article=article.id).first()
                self.assertTrue(enabled_comment.authorized)

    # Verifica se l'eliminazione di un commento specifico tramite la pagina /deleteComment/{comment_id}
    # restituisce un reindirizzamento (stato HTTP 302) e se il commento specifico non esiste più nel database
    # dopo l'operazione.
    def test_delete_comment(self):
        with app.test_client() as client:
            comment = Comment.query.first()
            if comment:
                comment_id = str(comment.id)

                response = client.get(f'/deleteComment/{comment_id}', headers={'Referer': '/previous-page'})

                self.assertEqual(response.status_code, 302)
                deleted_comment = Comment.query.filter_by(id=comment.id).first()
                self.assertIsNone(deleted_comment)

    # Verifica se l'aggiunta di un nuovo commento tramite la pagina /addcomment
    # restituisce uno stato HTTP 200 e se la parola chiave 'post' è presente nel corpo della risposta
    # dopo l'invio del modulo.
    def test_addComment(self):
        with app.test_client() as client:
            article = Article.query.filter_by(title="Article 2").first()
            if article:
                with patch('flask_login.current_user', username='giuVerdiProXX', email='giuseppeverdi@gmail.com'):
                    data = {
                        'content': 'Contenuto del nuovo commento',
                        'artId': str(article.id)
                    }

                    # Simuliamo l'invio del modulo
                    response = client.post('/addcomment', data=data, follow_redirects=True)

                    self.assertEqual(response.status_code, 200)
                    self.assertIn(b'post', response.data)

    # Verifica se l'operazione di "like" su un articolo tramite la pagina /like/{article_id}
    # restituisce un reindirizzamento (stato HTTP 302) e se il "like" non è presente nel database
    # dopo l'operazione.
    def test_like(self):
        with app.test_client() as client:
            article = Article.query.filter_by(title="Article 1").first()
            with patch('flask_login.current_user', username='giuVerdiProXX', email='giuseppeverdi@gmail.com'):
                response = client.get('/like/1')
                self.assertEqual(response.status_code, 302)
                my_like = Like.query.filter_by(id_article=article.id).first()
                self.assertIsNone(my_like)