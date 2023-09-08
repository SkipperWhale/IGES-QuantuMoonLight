import datetime
from datetime import datetime
from unittest import TestCase

from sqlalchemy_utils import database_exists, create_database

from app import app, db
from app.source.model.models import User, Article

#Classe di test per Utente
class TestUser(TestCase):

    #Setup
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
            user = User(
                email="mariorossi12@gmail.com",
                password="prosopagnosia",
                username="Antonio de Curtis ",
                token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccZZ",
                name="Antonio",
                surname="De Curtis",
                isAdmin=False,
                newsletter=False,
                isResearcher=False
            )
            db.session.add(user)
            db.session.commit()

    # Testa la funzionalità di rimozione dell'utente, verificando prima che l'account esista,
    # quindi lo elimina e verifica che sia stato rimosso correttamente.
    def test_removeUser(self):
        """
        test the removeUser functionality, checking first that the account exists,
        then delete it and verify that it was deleted correctly
        """
        tester = app.test_client(self)
        with app.app_context():
            db.create_all()
            self.assertTrue(
                User.query.filter_by(email="mariorossi12@gmail.com").first()
            )
            response = tester.post(
                "/removeUser/",
                data=dict(email="mariorossi12@gmail.com"),
            )
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertFalse(
                User.query.filter_by(email="mariorossi12@gmail.com").first()
            )
            db.session.commit()

    # Testa la funzionalità di modifica dell'utente, verificando prima che l'account esista,
    # quindi lo modifica e verifica che sia stato modificato correttamente.
    def test_modifyUser(self):
        """
        test the modifyUser functionality, checking first that the account exists,
        then modify it and verify that it has been modified correctly
        """
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        self.assertTrue(
            User.query.filter_by(email="mariorossi12@gmail.com").first()
        )
        response = tester.post(
            "/ModifyUserByAdmin/",
            data=dict(
                email="mariorossi12@gmail.com",
                token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccZZ"
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            User.query.filter_by(
                email="mariorossi12@gmail.com",
                token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccZZ"
            ).first()
        )
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

#Classe di test per il BLOG
class TestList(TestCase):
    #SetUp
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
                username="Antonio de Curtis ",
                token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccZZ",
                name="Antonio",
                surname="De Curtis",
                isAdmin=False,
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
                title="BuonNatale",
                body="primobody",
                author="giuVerdiProXX",
                category="primaCat",
                data=datetime(2021, 12, 25),
                authorized=True
            )
            art2 = Article(
                email_user="mariorossi12@gmail.com",
                title="BuonCapodanno",
                body="secondoBody",
                author="giuVerdiProXX",
                category="secondaCat",
                data=datetime(2022, 1, 1),
                authorized=True
            )
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
            db.session.add(art1)
            db.session.add(art2)
            db.session.commit()

    # Testa la funzionalità di ottenere tutti gli utenti registrati sul sito.
    def test_listUser(self):
        """
        test the functionality of getting all registered users to the site
        """
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        response = tester.post(
            "/gestione/",
            data=dict(scelta="listUser"),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(User.query.filter_by(email="mariorossi12@gmail.com").first())
        self.assertTrue(User.query.filter_by(email="giuseppeverdi@gmail.com").first())
        db.session.commit()

    # Testa la funzionalità di ottenere gli articoli scritti da un utente.
    def test_listArticlesUser(self):
        """
        test the functionality of getting articles written by a user
        """
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        response = tester.post(
            "/gestione/",
            data=dict(
                scelta="listArticlesUser",
                email="mariorossi12@gmail.com",
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            Article.query.filter_by(
                email_user="mariorossi12@gmail.com"
            ).limit(2)
        )
        db.session.commit()

    # Testa la funzionalità di ottenere gli articoli scritti tra due date.
    def test_listArticlesData(self):
        """
        tests the functionality of getting articles written between two dates
        """
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        response = tester.post(
            "/gestione/",
            data=dict(
                scelta="listArticlesData",
                firstData="2021-12-20",
                secondData="2021-12-30",
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            Article.query.filter(
                Article.data.between("2021-12-20", "2021-12-30")
            ).first()
        )
        db.session.commit()

    #TearDown
    def tearDown(self):
        with app.app_context():
            db.drop_all()
