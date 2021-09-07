# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, render_template, request, jsonify, flash, send_from_directory, current_app
from application_logging.AppLogging import AppLog
from DataSource.LoadFromFile import ReadFileToDataFrame
import pandas as pd
from Training.TrainModel import TrainModel
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
import numpy as np
from pandas_profiling import ProfileReport
from Config_Files.readConfigFile import Read_Config_File
from Training.preprocess import datapreprocess

app = Flask(__name__)

exeType = "Training"
applog = AppLog(exeType)
log = applog.log("sLogger")

objReadConfigFile = Read_Config_File(log,"Config_Files//Training_schema.json")
FileStatus, ConfigDict = objReadConfigFile.readData()

#exeType = ConfigDict.get("exeType")
classifier = ConfigDict["classifier"]
log.info("classifier : {}".format(classifier))

objTrainModel = TrainModel(exeType=exeType)

RawData = pd.DataFrame()
Status = 0

TrainModelPath = ConfigDict["TrainModelPath"] #"Training//Model//"
log.info("TrainModelPath : {}".format(TrainModelPath))

IndependentCol = ConfigDict["IndependentCol"] #'Summary'
log.info("IndependentCol : {}".format(IndependentCol))
TargetCol = ConfigDict["TargetCol"] #IndependentCol #'Owner_Group'
log.info("TargetCol : {}".format(TargetCol))

ModelVer = ConfigDict["ModelVer"] #"1.0"
log.info("ModelVer : {}".format(ModelVer))

DataDir = ConfigDict["DataDir"] #"DataSource//Data"
log.info("DataDir : {}".format(DataDir))
FileName = ConfigDict["ReadFileName"] #"ai4i2020.csv"
log.info("FileName : {}".format(FileName))

objPreProcData = datapreprocess(exeType)


if ConfigDict["hyperparam"] == "False":
    hyperparam = False
else:
    hyperparam = True #False
log.info("hyperparam : {}".format(hyperparam))

removecolumn = ConfigDict["removecolumn"] #
log.info("removecolumn : {}".format(removecolumn))

@app.route('/', methods=['GET','POST']) # To render Homepage
def home_page():
    return render_template('index.html')

def Load_Data(exeType='Training'):
    # Use a breakpoint in the code line below to debug your script.

    objReadCSVFile = ReadFileToDataFrame(exeType=exeType)
    log.info("Load the data from file - {} ".format(FileName))
    Status, RawData = objReadCSVFile.ReadCSVData(DirName=DataDir, FileName=FileName)
    columlst = [col for col in RawData.columns]
    print(columlst)
    print ("Shape of the data is : {}".format(RawData.shape))
    log.info("Shape of the data is : {}".format(RawData.shape))

    GeneratePrifileReport(exeType,Status,RawData)

    return RawData

def GeneratePrifileReport(exeType='Training',Status=0,RawData=None):

    if Status == 1:
        log.info("Initiate to generate the pandas profile report...")
        print("Initiate to generate the pandas profile report...")
        #profile = ProfileReport(RawData,title="AI4I 2020 Predictive Maintenance Dataset")
        #profile.to_file(output_file="DataSource//Reports//"+"AI4I_2020_Predictive-Maintenance-Dataset.html")
        log.info("Pandas profile AI4I_2020_Predictive-Maintenance-Dataset.html generated successfully : {}")
    else:
        log.critical("No data found from the file, please check the log file")

    PreprocessData(exeType,RawData)
    #if exeType == 'Training':
        #TrainingModel(exeType,RawData['ProcessedText'],RawData[TargetCol])

def PreprocessData(exeType=exeType,df=RawData):

    log.info("Initiate to preprocess the data :")
    print("Initiate to preprocess the data :")
    df_data = objPreProcData.dropcolumn(df,ConfigDict["removecolumn"])
    columlst = [col for col in df_data.columns]
    print(columlst)
    #TrainingModel(exeType=exeType,df=df_data)

    return df_data

def TrainingModel(exeType=exeType):

    try:
        df = Load_Data()
        df = PreprocessData(exeType=exeType,df=df)

        IndependentData = df[IndependentCol]
        TargetData = df[TargetCol]

        Train_Data, Test_Data, Train_Target, Test_Target = objTrainModel.TrainTestSplit(IndependentData,TargetData)

        Train_Data = objPreProcData.stdscalling(Train_Data)
        print(Train_Data)

        TrainModel = objTrainModel.TrainSupervisedModel(classifier=classifier,IndLabel=Train_Data,TargetLabel=Train_Target)

        print("Initiate to dump the Training model")
        log.info("Initiate to dump the Training {} model".format(classifier))
        objTrainModel.DumpModel(model=TrainModel, dirpath=TrainModelPath, classifier=classifier, ver=ModelVer)

        Test_Data = objPreProcData.stdscalling(Test_Data)
        score = TrainModel.score(Test_Data,Test_Target)
        print("Model score without hyperparameter tuning.. ",score)
        log.info("Model score without hyperparameter tuning for {} model.. : {}".format(classifier,score))

    except Exception as e:
        log.critical("Exceptin occured, while training the model : {}".format(e))

@app.route("/TestingModel", methods=['GET','POST'])
def TestingModel():

    try:
        classifier = request.form['classifier']
        print(classifier)
        param1 = request.form['Process_temperature'] +","+request.form['Rotational_speed']+","+request.form['Torque']+","+request.form['Tool_wear']
        param2 = request.form['Machine_failure'] +","+request.form['TWF']+","+request.form['HDF']+","+request.form['PWF']+","+request.form['OSF']+","+request.form['RNF']
        param = param1+","+param2
        param = np.array([float(itm) for itm in param.split(",")])
        print(param)
        model = objTrainModel.LoadModel(classifier=classifier,dirpath=TrainModelPath,hyperparameter=hyperparam,ver=ModelVer)
        print(model)
        scalled = objPreProcData.stdscalling(param.reshape(1,-1))
        print(scalled)
        coef = model.coef_
        print(coef)
        intercept = model.intercept_
        print(intercept)
        predict = model.predict(scalled)
        print(predict)
        #document.getElementById("mytext").value = "My value";

    
    except Exception as e:
        log.critical("Exception occured, while getting model result :{}".format(e))
    return render_template('results.html',rheader=classifier+' Model Prediction',coef=coef,intercept=intercept,predict=predict)
    #return render_template('../DataSource/Reports/AI4I_2020_Predictive-Maintenance-Dataset.html')

def DataCleansing(InpSent=None):

    try:
        '''
        CleanData = objRemovePunc.RemoveByStringPunct(InpSent)
        CleanData = objNLTKLemma.LemmatizeSentance(CleanData)
        CleanData = objNLTKToken.NLTKTextTokenizer(CleanData)
        '''
    except Exception as e:
        log.critical("Exception occured during the data preprocessing : {}".format(e))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)