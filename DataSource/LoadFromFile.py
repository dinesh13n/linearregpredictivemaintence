
import os
from application_logging.AppLogging import AppLog
import pandas as pd
from Config_Files.Utility import GenericValidation


class ReadFileToDataFrame:

    def __init__(self, exeType='Training'):

        self.exeType = exeType

        self.applog = AppLog(self.exeType)
        self.log = self.applog.log("sLogger")

        self.GenValidation = GenericValidation(self.log)

    def ReadCSVData(self,DirName=None,FileName=None, Separator=','):

        try:
            Data = 'No Data'
            Status = 0
            if self.GenValidation.IsDirectoryAvailable(DirName) == 1:

                filepath = DirName + '\\'+ FileName
                self.log.info('File path to read file : {}'.format(filepath))

                if self.GenValidation.IsFileAvailable(filepath) == 1:

                    Data = pd.read_csv(filepath,sep=Separator)
                    Status = 1
        except Exception as e:
            self.log.critical("Exception occured, while reading the data from file : ".format(e))

        return Status, Data
