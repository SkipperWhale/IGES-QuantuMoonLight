import unittest
from unittest.mock import patch, Mock
from flask import Flask
from app.source.blog.BlogControl import BlogControl
from app.source.model.models import User, Article, Like, Comment
from datetime import datetime
from app import app, db

class TestBlogControl(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_db.sqlite"
        db.create_all()
        self.app = app.test_client()
        self.blog_control = BlogControl()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('app.source.model.models.Article.query')
    def test_listAllArticles(self, mock_query):
        """
        Test retrieving all articles without a specific label.
        """
        # Mock la query per Article.query
        mock_query.order_by.return_value.all.return_value = [
            Mock(
                id=1,
                email_user="mariorossi12@gmail.com",
                title="Article 1",
                body="primobody",
                author="giuVerdiProXX",
                category="primaCat",
                data=datetime(2021, 12, 25),
                authorized=True,
                label="Article"
            ),
            Mock(
                id=2,
                email_user="mariorossi12@gmail.com",
                title="Article 2",
                body="secondoBody",
                author="giuVerdiProXX",
                category="secondaCat",
                data=datetime(2022, 1, 1),
                authorized=True,
                label="Article"
            )
        ]
        mock_article = Mock()
        mock_article.id = Mock(return_value=1)  # Imposta il mock di Article.id per restituire 1

        # Configura il mock di Article.query per restituire il mock di Article
        mock_query.filter_by.return_value.first.return_value = mock_article

        response = self.app.get("/blog/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mock_query.order_by.return_value.all.call_args_list), 1)
        self.assertIn(b"Article 1", response.data)
        self.assertIn(b"Article 2", response.data)
