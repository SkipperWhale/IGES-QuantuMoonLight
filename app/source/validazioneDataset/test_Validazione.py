import os
import pathlib
import unittest
from os.path import exists
import re

from app import app
from app.source.utils import utils
from app.source.validazioneDataset import kFoldValidation
from app.source.validazioneDataset import train_testSplit


class TestValidazioneControl(unittest.TestCase):
    def setUp(self):
        # path del dataset a disposizione del testing
        pathOrigin = pathlib.Path(__file__).parents[0] / "testingFiles"
        # path della cartella dove scrivere i files che verranno letti dai test
        pathMock = pathlib.Path(__file__).parents[0]

        f = open((pathMock / "bupa.csv").__str__(), "a+")
        g = open((pathOrigin / "bupa.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        self.assertTrue(exists(pathMock / "bupa.csv"))

    def test_ValidazioneControl_SimpleSplit(self):
        """
        Tests when the user wants to validate a dataset with SimpleSplit and checks if the new datasets exist
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathTest = None
        validation = "Simple Split"
        k = 10
        dataPath = pathlib.Path(__file__).parents[0] / "testingFiles"

        response = tester.post(
            "/validazioneControl",
            data=dict(
                userpath=userpath,
                userpathTest=userpathTest,
                validation=validation,
                k=k,
                dataPath=dataPath
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"
        self.assertTrue(exists(pathData / "Data_training.csv"))
        self.assertTrue(exists(pathData / "Data_testing.csv"))
        self.assertTrue(exists(pathData / "featureDataset.csv"))

    def test_ValidazioneControl_KFold(self):
        """
        Tests when the user wants to validate a dataset with kFold and checks if the new datasets exist
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathTest = None
        validation = "K Fold"
        k = 10
        dataPath = pathlib.Path(__file__).parents[0] / "testingFiles"

        response = tester.post(
            "/validazioneControl",
            data=dict(
                userpath=userpath,
                userpathTest=userpathTest,
                validation=validation,
                k=k,
                dataPath=dataPath
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"

        for x in range(k):
            StringaTrain = "training_fold_{}.csv".format(x + 1)
            print("\n\nString: " + StringaTrain)
            StringaTest = "testing_fold_{}.csv".format(x + 1)
            self.assertTrue(exists(pathData / StringaTrain))
            self.assertTrue(exists(pathData / StringaTest))

    def test_ValidazioneControl_kFold_Fail(self):
        """
        Tests when the user wants to validate a dataset with kFold and the "k" value is not correct
        and checks if no new datasets exist
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathTest = None
        validation = "K Fold"
        k = 1
        dataPath = pathlib.Path(__file__).parents[0] / "testingFiles"

        response = tester.post(
            "/validazioneControl",
            data=dict(
                userpath=userpath,
                userpathTest=userpathTest,
                validation=validation,
                k=k,
                dataPath=dataPath
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"
        StringaTrain = "training_fold_1.csv"
        StringaTest = "testing_fold_1.csv"
        self.assertFalse(exists(pathData / StringaTrain))
        self.assertFalse(exists(pathData / StringaTest))

    def test_ValidazioneControl_NoSplit(self):
        """
        Tests when the user wants not to validate the dataset and has to upload both training and testing
        dataset and checks if the new name of the loaded datasets are Data_training.csv and Data_testing.csv
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathTest = pathlib.Path(__file__).parents[0] / "bupa.csv"
        validation = None
        k = 10
        dataPath = pathlib.Path(__file__).parents[0] / "testingFiles"

        response = tester.post(
            "/validazioneControl",
            data=dict(
                userpath=userpath,
                userpathTest=userpathTest,
                validation=validation,
                k=k,
                dataPath=dataPath
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"
        self.assertTrue(exists(pathData / "Data_training.csv"))
        self.assertTrue(exists(pathData / "Data_testing.csv"))

    def test_ValidazioneControl_NoSplit_Fail(self):
        """
        Tests when the user doesn't want to validate the dataset and has not uploaded the test Set
         and checks if no new datasets exist
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathTest = None
        validation = None
        k = 10
        dataPath = pathlib.Path(__file__).parents[0] / "testingFiles"

        response = tester.post(
            "/validazioneControl",
            data=dict(
                userpath=userpath,
                userpathTest=userpathTest,
                validation=validation,
                k=k,
                dataPath=dataPath
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"

        self.assertFalse(exists(pathData / "Data_training.csv"))
        self.assertFalse(exists(pathData / "Data_testing.csv"))

    def tearDown(self):
        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"
        files_to_keep = ["bupa.csv"]

        files = os.listdir(pathData)

        for file in files:
            if re.search("\.csv$", file):
                if file not in files_to_keep:
                    # cancellalo
                    os.remove(pathData / file)
                    print(f"File {file} eliminato.")


class TestKFold(unittest.TestCase):
    def setUp(self):
        # path del dataset a disposizione del testing
        pathOrigin = pathlib.Path(__file__).parents[0] / "testingFiles"
        # path della cartella dove scrivere i files che verranno letti dai test
        pathMock = pathlib.Path(__file__).parents[0]

        f = open((pathMock / "bupa.csv").__str__(), "a+")
        g = open((pathOrigin / "bupa.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        self.assertTrue(exists(pathMock / "bupa.csv"))

    def test_KFold(self):
        """
        Tests when the user wants to validate a dataset with kFold and checks if the new datasets exist
        """
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        k = 10

        kFoldValidation.cross_fold_validation(userpath, k)
        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"

        for x in range(k):
            StringaTrain = "training_fold_{}.csv".format(x + 1)
            StringaTest = "testing_fold_{}.csv".format(x + 1)
            print(StringaTrain)
            self.assertTrue(exists(pathData / StringaTrain))
            self.assertTrue(exists(pathData / StringaTest))

    def tearDown(self):
        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"
        files_to_keep = ["bupa.csv"]

        files = os.listdir(pathData)

        for file in files:
            if re.search("\.csv$", file):
                if file not in files_to_keep:
                    # cancellalo
                    os.remove(pathData / file)
                    print(f"File {file} eliminato.")

class TestSimpleSplit(unittest.TestCase):
    def setUp(self):
        # path del dataset a disposizione del testing
        pathOrigin = pathlib.Path(__file__).parents[0] / "testingFiles"
        # path della cartella dove scrivere i files che verranno letti dai test
        pathMock = pathlib.Path(__file__).parents[0]

        f = open((pathMock / "bupa.csv").__str__(), "a+")
        g = open((pathOrigin / "bupa.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        self.assertTrue(exists(pathMock / "bupa.csv"))

    def test_simpleSplit(self):
        """
        Tests when the user wants to validate a dataset with SimpleSplit.
        Checks if the new datasets exist and the new datasets have the correct number of rows
        """
        path = pathlib.Path(__file__).parents[0] / "testingFiles"
        filename = path / "bupa.csv"
        numRaws = utils.numberOfRows(filename.__str__())

        train_testSplit.splitDataset(filename.__str__())
        self.assertEqual(69, utils.numberOfRows(pathlib.Path(__file__).parents[0] / "testingFiles" / "Data_testing.csv"))
        self.assertEqual(
            numRaws - 69, utils.numberOfRows(pathlib.Path(__file__).parents[0] / "testingFiles" / "Data_training.csv")
        )
        self.assertTrue(
            exists(pathlib.Path(__file__).parents[0] / "testingFiles" / "Data_testing.csv")
        )
        self.assertTrue(
            exists(pathlib.Path(__file__).parents[0] / "testingFiles" / "Data_training.csv")
        )

    def tearDown(self):
        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"
        files_to_keep = ["bupa.csv"]

        files = os.listdir(pathData)

        for file in files:
            if re.search("\.csv$", file):
                if file not in files_to_keep:
                    # cancellalo
                    os.remove(pathData / file)
                    print(f"File {file} eliminato.")