import os
import pathlib
import unittest
from os.path import exists
from unittest.mock import patch
from app.source.model.models import User
import flask
import re

from app import app
from app.source.classificazioneDataset.ClassifyControl import ClassificazioneControl
from app.source.utils import utils



class TestClassifyControl(unittest.TestCase):

    def test_classify_control(self):
        """
        Test the input coming from the form and the status code returned, and check if the classification result
        file is created
        """
        path_train = (
            pathlib.Path(__file__).resolve().parent
            / "testingFiles"
            / "DataSetTrainPreprocessato.csv"
        )
        path_test = (
            pathlib.Path(__file__).resolve().parent
            / "testingFiles"
            / "DataSetTestPreprocessato.csv"
        )
        path_prediction = (
            pathlib.Path(__file__).resolve().parent / "testingFiles" / "doPrediction.csv"
        )
        features = utils.createFeatureList(2)
        token = "43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe5196" \
                "91a7ad17643eecbe13d1c8c4adccd2"
        backend = "aer_simulator"
        email = "quantumoonlight@gmail.com"

        response = app.test_client(self).post(
            "/classify_control",
            data=dict(
                pathTrain=path_train,
                pathTest=path_test,
                email=email,
                userpathToPredict=path_prediction,
                features=features,
                token=token,
                backend=backend,
            ),
        )
        thread = flask.g
        thread.join()
        statuscode = response.status_code
        self.assertEqual(200, statuscode)

    @patch('app.source.model.models.User.query')
    def test_classification_thread(self, mock_query):
        """
        Test if thread that calls the classify and QSVM works properly
        """
        path_train = (
                pathlib.Path(__file__).resolve().parent
                / "testingFiles"
                / "DataSetTrainPreprocessato.csv"
        )
        path_test = (
                pathlib.Path(__file__).resolve().parent
                / "testingFiles"
                / "DataSetTestPreprocessato.csv"
        )
        path_prediction = (
                pathlib.Path(__file__).resolve().parent / "testingFiles" / "doPrediction.csv"
        )
        features = utils.createFeatureList(2)
        token = "43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe5196" \
                "91a7ad17643eecbe13d1c8c4adccd2"
        backend_selected = "aer_simulator"
        email = "quantumoonlight@gmail.com"
        model = "QSVC"
        C = 1000
        tau = 100
        optimizer = "SLSQP"
        loss = "squared_error"
        max_iter = 100
        kernelSVR = "rbf"
        kernelSVC = "rbf"
        C_SVC = 1
        C_SVR = 1
        id_dataset = 1
        user_id = email

        user = User(email='quantumoonlight@gmail.com', password='quercia', isResearcher=False)
        mock_query.filter_by.return_value.first.return_value = user

        result = ClassificazioneControl().classification_thread(path_train,
                                                                path_test,
                                                                path_prediction,
                                                                features,
                                                                token,
                                                                backend_selected,
                                                                email,
                                                                model,
                                                                C,
                                                                tau,
                                                                optimizer,
                                                                loss,
                                                                max_iter,
                                                                kernelSVR,
                                                                kernelSVC,
                                                                C_SVC,
                                                                C_SVR,
                                                                id_dataset,
                                                                user_id)
        self.assertNotEqual(result, 1)
        self.assertTrue(
            exists(
                pathlib.Path(__file__).resolve().parent
                / "testingFiles"
                / "classifiedFile.csv"
            )
        )

    @patch('app.source.model.models.User.query')
    def test_classify(self, mock_query):
        """
        Test the classify function with correct parameters and input files, and check if the classification result
        file is created
        """
        path_train = (
            pathlib.Path(__file__).resolve().parent
            / "testingFiles"
            / "DataSetTrainPreprocessato.csv"
        )
        path_test = (
            pathlib.Path(__file__).resolve().parent
            / "testingFiles"
            / "DataSetTestPreprocessato.csv"
        )
        path_prediction = (
            pathlib.Path(__file__).resolve().parent / "testingFiles" / "doPrediction.csv"
        )
        features = utils.createFeatureList(2)
        token = "43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519" \
                "691a7ad17643eecbe13d1c8c4adccd2"
        backend_selected = "aer_simulator"

        model = "QSVC"
        C = 1000
        tau = 100
        optimizer = "SLSQP"
        loss = "squared_error"
        max_iter = 100
        kernelSVR = "rbf"
        kernelSVC = "rbf"
        C_SVC = 1
        C_SVR = 1
        id_dataset = 1
        user_id = "quantumoonlight@gmail.com"

        user = User(email='quantumoonlight@gmail.com', password='quercia', isResearcher=False)
        mock_query.filter_by.return_value.first.return_value = user

        result = ClassificazioneControl().classify(
            path_train,
            path_test,
            path_prediction,
            features,
            token,
            backend_selected,
            model,
            C,
            tau,
            optimizer,
            loss,
            max_iter,
            kernelSVR,
            kernelSVC,
            C_SVC,
            C_SVR,
            id_dataset,
            user_id
        )

        self.assertNotEqual(result, 1)
        self.assertTrue(
            exists(
                pathlib.Path(__file__).resolve().parent
                / "testingFiles"
                / "classifiedFile.csv"
            )
        )

class TestIbmFail(unittest.TestCase):

    def setUp(self):
        if os.path.exists(
            pathlib.Path(__file__).resolve().parent
            / "testingFiles"
            / "classifiedFile.csv"
        ):
            os.remove(
                pathlib.Path(__file__).resolve().parent
                / "testingFiles"
                / "classifiedFile.csv"
            )
        open(
            pathlib.Path(__file__).resolve().parent
            / "testingFiles"
            / "emptyFile.csv",
            "w",
        ).write("1234567890987654321")

    @patch('app.source.model.models.User.query')
    def test_classify_ibmFail(self, mock_query):
        """
        Test the classify function with not valid train and test datasets, to make the IBM backend fail on purpose
        """
        path_train = (
            pathlib.Path(__file__).resolve().parent
            / "testingFiles"
            / "DataSetTrainPreprocessato.csv"
        )
        path_test = (
            pathlib.Path(__file__).resolve().parent
            / "testingFiles"
            / "DataSetTestPreprocessato.csv"
        )
        path_prediction = (
            pathlib.Path(__file__).resolve().parent / "testingFiles" / "emptyFile.csv"
        )
        features = utils.createFeatureList(2)
        token = "43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691" \
                "a7ad17643eecbe13d1c8c4adccd2"
        backend_selected = "aer_simulator"
        model = "QSVC"
        C = 1000
        tau = 100
        optimizer = "SLSQP"
        loss = "squared_error"
        max_iter = 100
        kernelSVR = "rbf"
        kernelSVC = "rbf"
        C_SVC = 1
        C_SVR = 1
        id_dataset = 1
        user_id = "quantumoonlight@gmail.com"

        user = User(email='quantumoonlight@gmail.com', password='quercia', isResearcher=False)
        mock_query.filter_by.return_value.first.return_value = user

        result = ClassificazioneControl().classify(
            path_train,
            path_test,
            path_prediction,
            features,
            token,
            backend_selected,
            model,
            C,
            tau,
            optimizer,
            loss,
            max_iter,
            kernelSVR,
            kernelSVC,
            C_SVC,
            C_SVR,
            id_dataset,
            user_id
        )

        self.assertEqual(result['error'], 1)
        self.assertFalse(
            exists(
                pathlib.Path(__file__).resolve().parent
                / "testingFiles"
                / "classifiedFile.csv"
            )
        )

    def tearDown(self) -> None:
        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"
        files_to_keep = ["bupa.csv", "DataSetTestPreprocessato.csv", "DataSetTrainPreprocessato.csv", "Data_training.csv", "doPrediction.csv"]

        files = os.listdir(pathData)

        for file in files:
            if re.search("\.csv$", file):
                if file not in files_to_keep:
                    # cancellalo
                    os.remove(pathData / file)
                    print(f"File {file} eliminato.")