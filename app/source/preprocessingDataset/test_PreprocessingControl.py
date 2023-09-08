import os
import pathlib
import unittest
from os.path import exists
import re

from app import app


class TestPreprocessingControl(unittest.TestCase):

    # Imposta l'ambiente per i test, copiando alcuni file di dati utilizzati nei test.
    def setUp(self):
      
        pathOrigin = pathlib.Path(__file__).parents[0] / "testingFiles"
        pathMock = pathlib.Path(__file__).parents[0]

        f = open((pathMock / "Data_testing.csv").__str__(), "a+")
        g = open((pathOrigin / "Data_testing.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        f = open((pathMock / "Data_training.csv").__str__(), "a+")
        g = open((pathOrigin / "Data_training.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        f = open((pathMock / "bupa.csv").__str__(), "a+")
        g = open((pathOrigin / "bupa.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        f = open((pathMock / "bupaToPredict.csv").__str__(), "a+")
        g = open((pathOrigin / "bupaToPredict.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        self.assertTrue(exists(pathMock / "Data_training.csv"))
        self.assertTrue(exists(pathMock / "Data_training.csv"))
        self.assertTrue(exists(pathMock / "bupa.csv"))
        self.assertTrue(exists(pathMock / "bupaToPredict.csv"))

    # Testa la funzionalità di controllo di preprocessing quando l'utente vuole eseguire la classificazione senza alcun preprocessing.
    # Verifica se esistono i due dataset da classificare.
    def test_PreprocessingControl_onlyQSVM(self):
        """
        Tests when the user wants to execute classification but no Preprocessing.
        Check if exists the two dataset to classify
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathToPredict = (
            pathlib.Path(__file__).parents[0]/ "testingFiles" / "bupaToPredict.csv"
        )

        userpathToPredict = None
        prototypeSelection = None
        featureExtraction = None
        featureSelection = None
        numRowsPS = 10
        numColsFE = 2
        numColsFS = None
        model = True

        response = tester.post(
            "/preprocessingControl",
            data=dict(
                userpath=userpath,
                userpathToPredict=userpathToPredict,
                prototypeSelection=prototypeSelection,
                featureExtraction=featureExtraction,
                featureSelection=featureSelection,
                numRawsPS=numRowsPS,
                numColsFE=numColsFE,
                numColsFS=numColsFS,
                model=model,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathMock = pathlib.Path(__file__).parents[0] / "testingFiles"
        self.assertTrue(exists(pathMock / "DataSetTrainPreprocessato.csv"))
        self.assertTrue(exists(pathMock / "DataSetTestPreprocessato.csv"))

# Testa la funzionalità di controllo di preprocessing quando l'utente vuole eseguire solo la selezione del prototipo sul dataset di addestramento.
# Verifica se esistono i due dataset da classificare e il dataset di addestramento ridotto.
    def test_PreprocessingControl_onlyPS(self):
        """
        Test when the user wants to execute only Prototype Selection on the training dataset.
        Check if exist the two dataset to classify and the reduced Train
        """
        tester = app.test_client(self)

        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = True
        featureExtraction = None
        featureSelection = None
        numRowsPS = 10
        numColsFE = 2
        numColsFS = None
        model = None

        response = tester.post(
            "/preprocessingControl",
            data=dict(
                userpath=userpath,
                userpathToPredict=userpathToPredict,
                prototypeSelection=prototypeSelection,
                featureExtraction=featureExtraction,
                featureSelection=featureSelection,
                numRawsPS=numRowsPS,
                numColsFE=numColsFE,
                numColsFS=numColsFS,
                model=model,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathMock = pathlib.Path(__file__).parents[0] / "testingFiles"
        self.assertTrue(exists(pathMock / "DataSetTrainPreprocessato.csv"))
        self.assertTrue(exists(pathMock / "DataSetTestPreprocessato.csv"))
        self.assertTrue(exists(pathMock / "reducedTrainingPS.csv"))

    # Testa la funzionalità di controllo di preprocessing quando l'utente vuole eseguire solo la prototype selection sul dataset di addestramento,
    # ma cerca di ridurre le righe con più righe rispetto al DataSet originale. Verifica che i due dataset non siano stati creati.
    def test_PreprocessingControl_failPS(self):
        """
        Test when the user wants to execute only Prototype Selection on the training dataset,
        but try to reduce the rows whit more rows then the original DataSet
        Check if the two dataset are not created
        """
        tester = app.test_client(self)

        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = True
        featureExtraction = None
        featureSelection = None
        numRowsPS = 0
        numColsFE = 2
        numColsFS = None
        model = None

        response = tester.post(
            "/preprocessingControl",
            data=dict(
                userpath=userpath,
                userpathToPredict=userpathToPredict,
                prototypeSelection=prototypeSelection,
                featureExtraction=featureExtraction,
                featureSelection=featureSelection,
                numRawsPS=numRowsPS,
                numColsFE=numColsFE,
                numColsFS=numColsFS,
                model=model,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 500)

        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"
        self.assertFalse(exists(pathData / "DataSetTrainPreprocessato.csv"))
        self.assertFalse(exists(pathData / "DataSetTestPreprocessato.csv"))
        self.assertFalse(exists(pathData / "reducedTrainingPS.csv"))

    # Testa la funzionalità di controllo di preprocessing quando l'utente vuole eseguire solo lla Feature Extraction
    # sui dataset di addestramento e test. Verifica se esistono i due dataset da classificare e i dataset di addestramento e test ridotti.
    def test_PreprocessingControl_onlyFE(self):
        """
        Test when the user wants to execute only Feature Extraction on the training and testing dataset.
        Check if exist the two dataset to classify and the reduced Train and Test
        """
        tester = app.test_client(self)

        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = None
        featureExtraction = True
        featureSelection = None
        numRowsPS = 10
        numColsFE = 2
        numColsFS = None
        model = None

        response = tester.post(
            "/preprocessingControl",
            data=dict(
                userpath=userpath,
                userpathToPredict=userpathToPredict,
                prototypeSelection=prototypeSelection,
                featureExtraction=featureExtraction,
                featureSelection=featureSelection,
                numRawsPS=numRowsPS,
                numColsFE=numColsFE,
                numColsFS=numColsFS,
                model=model,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"
        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"
        self.assertTrue(exists(pathData / "DataSetTrainPreprocessato.csv"))
        self.assertTrue(exists(pathData / "DataSetTestPreprocessato.csv"))
        self.assertTrue(exists(pathData / "Test_Feature_Extraction.csv"))
        self.assertTrue(exists(pathData / "Train_Feature_Extraction.csv"))

# Testa la funzionalità di controllo di preprocessing quando l'utente vuole eseguire solo l'estrazione delle caratteristiche
# sui dataset di addestramento e test, ma cerca di ridurre le colonne con più colonne rispetto al DataSet originale.
# Verifica che tutti i dataset non siano stati creati.
    def test_PreprocessingControl_failFE(self):
        """
        Test when the user wants to execute only Feature Extraction on the training and testing dataset,
        but try to reduce the columns whit more columns then the original DataSet
        Check if the two dataset are not created
        """
        tester = app.test_client(self)

        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = None
        featureExtraction = True
        featureSelection = None
        numRowsPS = 10
        numColsFE = 15
        numColsFS = None
        model = None

        response = tester.post(
            "/preprocessingControl",
            data=dict(
                userpath=userpath,
                userpathToPredict=userpathToPredict,
                prototypeSelection=prototypeSelection,
                featureExtraction=featureExtraction,
                featureSelection=featureSelection,
                numRawsPS=numRowsPS,
                numColsFE=numColsFE,
                numColsFS=numColsFS,
                model=model,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 500)

        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"
        self.assertFalse(exists(pathData / "DataSetTrainPreprocessato.csv"))
        self.assertFalse(exists(pathData / "DataSetTestPreprocessato.csv"))
        self.assertFalse(exists(pathData / "reducedTrainingPS.csv"))
        self.assertFalse(exists(pathData / "Test_Feature_Extraction.csv"))
        self.assertFalse(exists(pathData / "Train_Feature_Extraction.csv"))

# Testa la funzionalità di controllo di preprocessing quando l'utente vuole eseguire l'estrazione delle caratteristiche sui dataset di addestramento e test
# e la selezione del prototipo sul dataset di addestramento.
# Verifica se esistono i due dataset da classificare e i dataset di addestramento e test ridotti.

    def test_PreprocessingControl_FE_PS(self):
        """
        Test when the user wants to execute Feature Extraction on the training and testing dataset
        and Prototype Selection on the training dataset.
        Check if exist the two dataset to classify and the reduced Train and Test
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        print("\n\n\n\t########Userpath: " + str(userpath))
        userpathToPredict = None
        prototypeSelection = True
        featureExtraction = True
        featureSelection = None
        numRowsPS = 10
        numColsFE = 2
        numColsFS = None
        model = None

        response = tester.post(
            "/preprocessingControl",
            data=dict(
                userpath=userpath,
                userpathToPredict=userpathToPredict,
                prototypeSelection=prototypeSelection,
                featureExtraction=featureExtraction,
                featureSelection=featureSelection,
                numRawsPS=numRowsPS,
                numColsFE=numColsFE,
                numColsFS=numColsFS,
                model=model,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"
        self.assertTrue(exists(pathData / "DataSetTrainPreprocessato.csv"))
        self.assertTrue(exists(pathData / "DataSetTestPreprocessato.csv"))
        self.assertTrue(exists(pathData / "reducedTrainingPS.csv"))
        self.assertTrue(exists(pathData / "Test_Feature_Extraction.csv"))
        self.assertTrue(exists(pathData / "Train_Feature_Extraction.csv"))

    # Pulisce l'ambiente di test rimuovendo tutti i file creati.
    def tearDown(self):
        """
        Remove all the files created
        """
        pathData = pathlib.Path(__file__).parents[0] / "testingFiles"
        files_to_keep = ["bupa.csv", "bupaToPredict.csv", "Data_testing.csv", "Data_training.csv"]

        files = os.listdir(pathData)

        for file in files:
            if re.search("\.csv$", file):
                if file not in files_to_keep:
                    # cancellalo
                    os.remove(pathData / file)
                    print(f"File {file} eliminato.")