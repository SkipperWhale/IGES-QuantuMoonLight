import unittest
from unittest.mock import patch, Mock
from flask import Flask
from app.source.blog.BlogControl import BlogControl
from app.source.model.models import User, Article, Like, Comment
from datetime import datetime
from app import app

class TestBlogControl(unittest.TestCase):

    
    def returnMockElements(self):
        elements = [Mock(
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
            ) ]
        return elements


    def setUp(self):
        self.app = app.test_client()
        self.blog_control = BlogControl()

    """
    Unit Test retrieving all articles
    """
    @patch('app.source.model.models.Article.query')
    def test_listLabelArticles(self, mock_query):
        element=self.returnMockElements()
      
        # Mock la query per Article.query
        mock_query.order_by.return_value.all.return_value = element

        response = self.app.get("/blog/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mock_query.order_by.return_value.all.call_args_list), 1)
        self.assertIn(b"Article 1", response.data)
        self.assertIn(b"Article 2", response.data)

    """
    Unit Test retrieving all articles without specific labels
    """
    @patch('app.source.model.models.Article.query')
    def test_ArticlesWithoutLabels(self, mock_query):

        element=self.returnMockElements()

        mock_query.filter_by.return_value.order_by.return_value.all.return_value = element
        
        response = self.app.get("/blog/Article")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mock_query.filter_by.return_value.order_by.return_value.all.return_value), 2)
        self.assertIn(b"Article 1", response.data)
        self.assertIn(b"Article 2", response.data)
