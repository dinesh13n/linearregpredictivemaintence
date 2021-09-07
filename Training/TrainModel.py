
from application_logging.AppLogging import AppLog
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from Config_Files.Utility import GenericValidation
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

import pickle

class TrainModel:

    def __init__(self, exeType='Training'):

        self.exeType = exeType

        self.applog = AppLog(self.exeType)
        self.log = self.applog.log("sLogger")

        self.GenValid = GenericValidation(self.log)

    def TrainTestSplit(self, DataToTrain='Example Data', TargetData='Example Data'):

        try:
            self.log.info("Train test split is in progress....")
            print("Train test split is in progress....")
            # Split the dataset into training and testing data, train/test sets with 80:20 ratio
            train_data, test_data, train_target, test_target = train_test_split(DataToTrain, TargetData, test_size=0.2)
            self.log.info("Train test split is completed....")

        except Exception as e:
            self.log.critical("Exception occured, while spliting the dataset into train and test dataset : {}".format(e))

        return train_data, test_data, train_target, test_target

    def ClassifierPipeline(self, classifier='NB', vect='count_vect'):

        try:
            text_clf = None
            print("{} Classifire Pipeline".format(classifier))
            self.log.info("Initiate classifire pipline for the {} classifire ..".format(classifier))

            if classifier == 'NB':
                text_clf = Pipeline([
                    ('vect', vect),
                    ('tfidf', TfidfTransformer()),
                    ('clf', MultinomialNB(fit_prior=True))
                ])
            elif classifier == 'SVM':
                # Training Support Vector Machines - SVM
                text_clf = Pipeline([(
                    'vect', vect),
                    ('tfidf', TfidfTransformer()),
                    ('clf', SGDClassifier()
                        #loss='hinge', penalty='l2', tol=1e-3, random_state=42
                    #)
                     )])
                #n_iter=5,

        except Exception as e:
            self.log.critical("Exception occured, while prepare Pipeline for {} classifier : {}".format(classifier,e))

        return text_clf

    def GridSearchParam(self, classifier='NB'):

        try:
            parameters = None
            self.log.info("Initiate Gridsearch param for the {} classifire ..".format(classifier))

            if classifier == 'NB':
                parameters = {
                    'vect__ngram_range': [(1, 1),(1, 2)],
                    'tfidf__use_idf': (True,False),
                    'clf__alpha': (1e-2,1e-3)
                }

            elif classifier == "SVM":
                # SVM parameters
                '''
                 parameters = {
                    'vect__max_df': (0.5, 0.75, 1.0),
                    'vect__max_features': (None, 5000, 10000, 50000),
                    'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
                    'tfidf__use_idf': (True, False),
                    'tfidf__norm': ('l1', 'l2'),
                    'clf__alpha': (0.00001, 0.000001),
                    'clf__penalty': ('l1','l2', 'elasticnet'),
                    'clf__n_iter_no_change': [45,50],
                 }
                '''
                parameters = {
                    'vect__max_df': [0.5],
                    'vect__max_features': [10000],
                    'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
                    'tfidf__use_idf': [False],
                    'tfidf__norm': ['l1'],
                    'clf__alpha': [1e-05],
                    'clf__penalty': ['l2'],
                    'clf__n_iter_no_change': [50],
                }

        except Exception as e:
            self.log.critical("Exception occured, while prepare Pipeline for {} classifier : {}".format(classifier,e))

        return parameters

    def DumpModel(self, model=None, dirpath="//Training//Model//", classifier='NB', hyperparameter=False, ver='1.0'):

        try:
            self.log.info("Initiate to dump the trained model")
            print("Initiate to dump the trained model")

            status = self.GenValid.MakeDir(dirpath=dirpath+classifier)

            if status == 1:
                hyper = "-without-hyper-"
                if hyperparameter:
                    hyper = "-with-hyper-"

                filename = classifier+hyper+"v-"+ver+".sav"
                self.log.info("save the model to the disc with filename - {}".format(filename))
                pickle.dump(model,open(dirpath+classifier+"//"+filename,'wb'))
                self.log.info("Training model - {} created successfully :".format(filename))
            else:
                self.log.info("Issue to create directory path - {} ".format(dirpath))

        except Exception as e:
            self.log.critical("Exception occured, while dumping the model : {}".format(e))

    def LoadModel(self,classifier='NB', dirpath="//Training//Model//", hyperparameter=False, ver='1.0'):

        try:
            dirpath = dirpath+"//"+classifier

            isDirAvailable = 0
            model = None
            isDirAvailable = self.GenValid.IsDirectoryAvailable(dirpath)

            if isDirAvailable == 1:
                hyper = "-without-hyper-"
                if hyperparameter:
                    hyper = "-with-hyper-"

                filename = classifier+hyper+"v-"+ver+".sav"
                isFileAvailable = self.GenValid.IsFileAvailable(dirpath+"//"+filename)

                if isFileAvailable == 1:
                    model = pickle.load(open(dirpath+"//"+filename,'rb'))

        except Exception as e:
            self.log.critical("Exception occured, while loading the model : ".format(e))

        return model

    def TrainSupervisedModel(self,classifier, IndLabel, TargetLabel):

        try:
            self.log.info("Initiate to train {} Model".format(classifier))
            TrainModel=None
            if classifier == 'LinearRegression':
                TrainModel = LinearRegression()
                TrainModel.fit(IndLabel, TargetLabel)
            elif classifier == 'Ridge':
                TrainModel = Ridge()
                TrainModel.fit(IndLabel, TargetLabel)
            elif classifier == 'Lasso':
                TrainModel = Lasso()
                TrainModel.fit(IndLabel, TargetLabel)
            elif classifier == 'ElasticNet':
                TrainModel = ElasticNet()
                TrainModel.fit(IndLabel, TargetLabel)

            self.log.info("{} model training completed successfully".format(classifier))

        except Exception as e:
            self.log.critical("Exception occured, while training {} model : ".format(e))

        return TrainModel