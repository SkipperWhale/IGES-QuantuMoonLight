import hashlib
import os
import pathlib
import unittest
from os.path import exists

from flask_login import current_user
from sqlalchemy import desc
from sqlalchemy_utils import create_database, database_exists

from unittest.mock import patch
from app import app, db
from app.source.model.models import User, Dataset
from datetime import datetime
import hashlib
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestRoutes(unittest.TestCase):
    def setUp(self):
        super().setUp()
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql://root:root@127.0.0.1/test_db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        with app.app_context():
            db.create_all()

    def test_routes(self):
        # Login User and test if that works
        tester = app.test_client()
        self.assertFalse(current_user)
        with tester:
            # Setup for login testing
            password = "quercia12345"
            password = hashlib.sha512(password.encode()).hexdigest()
            response = tester.post(
                "/signup",
                data=dict(
                    email="boscoverde27@gmail.com",
                    password=password,
                    confirmPassword=password,
                    username="Antonio",
                    isResearcher=False,
                    isAdmin=False,
                    newsletter=False,
                    nome="Antonio",
                    cognome="De Curtis",
                    token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2"),
            )
            print(current_user)
            assert isinstance(current_user, User)
            self.assertTrue(current_user.is_authenticated)

            simpleSplit = True
            prototypeSelection = True
            featureExtraction = True
            numRowsPS = 10
            numColsFE = 2
            doQSVM = True
            token = "43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2"
            backend = "ibmq_qasm_simulator"
            email = "quantumoonlight@gmail.com"

            path = pathlib.Path(__file__).parent
            pathpred = path / "testingFiles" / "bupaToPredict.csv"
            pathtrain = path / "testingFiles" / "bupa.csv"

            # Test smista with that the whole
            # validation/preprocessing/classification process
            response = tester.post(
                "/formcontrol",
                data=dict(
                    dataset_train=open(pathtrain.__str__(), "rb"),
                    dataset_test=open(pathpred.__str__(), "rb"),
                    dataset_prediction=open(pathpred.__str__(), "rb"),
                    splitDataset=True,
                    reducePS=prototypeSelection,
                    reduceFE=featureExtraction,
                    doQSVM=doQSVM,
                    simpleSplit=simpleSplit,
                    nrRows=numRowsPS,
                    nrColumns=numColsFE,
                    backend=backend,
                    token=token,
                    email=email,
                    Radio="simpleSplit"

                ),
            )

            statuscode = response.status_code
            print(statuscode)
            self.assertEqual(statuscode, 200)
            pathData = pathlib.Path(__file__).parents[3] / "upload_dataset" / current_user.email / str(
                Dataset.query.filter_by(
                    email_user=current_user.email).order_by(
                    desc(
                        Dataset.id)).first().id)  # Find a way to get the id
            self.assertTrue(exists(pathData / "Data_training.csv"))
            self.assertTrue(exists(pathData / "Data_testing.csv"))
            self.assertTrue(exists(pathData / "featureDataset.csv"))
            self.assertTrue(exists(pathData / "DataSetTrainPreprocessato.csv"))
            self.assertTrue(exists(pathData / "DataSetTestPreprocessato.csv"))
            self.assertTrue(exists(pathData / "reducedTrainingPS.csv"))
            self.assertTrue(exists(pathData / "yourPCA_Train.csv"))
            self.assertTrue(exists(pathData / "yourPCA_Test.csv"))

    def tearDown(self):
        with app.app_context():
            db.drop_all()

class TestCompareExpriment(unittest.TestCase):

    def setUp(self):
        super().setUp()
        with app.app_context():
            db.create_all()
            user = User(
                email="quantum@gmail.com",
                password=hashlib.sha512("prosopagnosia".encode()).hexdigest(),
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
            dataset1 = Dataset(
                email_user='quantum@gmail.com',
                name='test',
                path='',
                upload_date=datetime.now(),
                validation='Simple Split',
                ps=0,
                fe=0,
                fs=None,
                model='SVC',
                accuracy=71.0145,
                precision=71.2513,
                recall=71.0145,
                mse=-1,
                mae=-1,
                rmse=-1,
                r2=-1,
                f1=69.4392,
                training_time=0,
                total_time=0
            )
            dataset2 = Dataset(
                email_user='quantum@gmail.com',
                name='test',
                path='',
                upload_date=datetime.now(),
                validation='Simple Split',
                ps=0,
                fe=0,
                fs=None,
                model='SVC',
                accuracy=71.0145,
                precision=71.2513,
                recall=71.0145,
                mse=-1,
                mae=-1,
                rmse=-1,
                r2=-1,
                f1=69.4392,
                training_time=0,
                total_time=0
            )

            db.session.add(dataset1)
            db.session.add(dataset2)
            db.session.commit()

            self.driver = webdriver.Chrome()

    def tearDown(self):
        with app.app_context():
            self.driver.quit()
            user = User.query.get("quantum@gmail.com")
            datasets = Dataset.query.filter_by(email_user="quantum@gmail.com").all()
            for dataset in datasets:
                db.session.delete(dataset)
            db.session.delete(user)
            db.session.commit()
    @patch('app.source.model.models.Dataset.query')
    def test_compare_dataset(self, mock_query):
        with app.test_client() as client:
            with patch('flask_login.current_user', username='giuVerdiProXX', email='giuseppeverdi@gmail.com'):
                data = {
                    'selectedDataset': '[]'
                }
                datasets = [
                    Dataset(
                        id=1,
                        email_user='quantum@gmail.com',
                        name='test',
                        path='',
                        upload_date=datetime.now(),
                        validation='Simple Split',
                        ps=0,
                        fe=0,
                        fs=None,
                        model='SVC',
                        accuracy=71.0145,
                        precision=71.2513,
                        recall=71.0145,
                        mse=-1,
                        mae=-1,
                        rmse=-1,
                        r2=-1,
                        f1=69.4392,
                        training_time=0,
                        total_time=0
                    ),
                    Dataset(
                        id=2,
                        email_user='quantum@gmail.com',
                        name='test',
                        path='',
                        upload_date=datetime.now(),
                        validation='Simple Split',
                        ps=0,
                        fe=0,
                        fs=None,
                        model='SVC',
                        accuracy=71.0145,
                        precision=71.2513,
                        recall=71.0145,
                        mse=-1,
                        mae=-1,
                        rmse=-1,
                        r2=-1,
                        f1=69.4392,
                        training_time=0,
                        total_time=0
                    )
                ]

                mock_query.filter.return_value.all.return_value = datasets
                response = client.post('/compareExperiments', data=data, follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b"SVC", response.data)
    def test_compare_experiment_frontend(self):
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.set_window_size(1550, 830)
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".user").click()
        time.sleep(2)
        self.driver.find_element(By.ID, "login").click()
        self.driver.find_element(By.ID, "login").send_keys("quantum@gmail.com")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("prosopagnosia")
        self.driver.find_element(By.CSS_SELECTOR, ".fourth").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".user").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "form:nth-child(10) > button").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".collapsible").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".collapsible").click()
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".collapsible.active")))
        time.sleep(2)
        self.driver.find_element(By.ID, "selectedDataset").click()
        self.driver.find_element(By.CSS_SELECTOR, ".divTableBody:nth-child(3) #selectedDataset").click()
        self.driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(2)
        self.driver.find_element(By.ID, "compareButton").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".user").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "form:nth-child(11) > button").click()
        time.sleep(2)
        self.driver.close()