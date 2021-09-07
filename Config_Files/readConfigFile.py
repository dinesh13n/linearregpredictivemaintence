import json
import os
from application_logging.AppLogging import AppLog

class Read_Config_File:
    """
                Class: Read_Config_File
                Description: Objective of this class to read the json file
                Input: file path including file name

                Written By: Dinesh Naik
                Version: 1.0
                Revisions: None

    """
    def __init__(self, log, filePath):
        self.filePath = filePath
        self.log = log
        self.log.debug("Initiate readConfiFile Object for {} config file".format(self.filePath))

    def readData(self):

        """
            Class: Read_Config_File
            Description: This method read the config file, where other process parameter defined for the process
            Input: file path including file name
            Output: status (Fail,Success), containt of the file, which is in json format
            On Failure: Raise FileNotFoundError,Exception

            Written By: Dinesh Naik
            Version: 1.0
            Revisions: None

        """

        try:
            status = 0
            self.log.debug("Initiate to read {} config file".format(self.filePath))

            if not os.path.isdir(os.path.dirname(self.filePath)):
                os.mkdir(os.path.dirname(self.filePath))

            if not os.path.isfile(self.filePath):
                with open(os.path.basename(self.filePath),'a+') as fp:
                    pass

            with open(self.filePath, 'r') as f:
                dic = json.load(f)
                status = 1
                self.log.debug("Read {} config file successfully and the data is : {}".format(self.filePath,dic))
                f.close()

        except FileNotFoundError:
            dic = "File {} not available".format(self.filePath)
            status = 0
            self.log.info("File {} not found ".format(self.filePath))

        except Exception as e:
            dic = "File {} read exception occured ".format(self.filePath)
            status = 0
            self.log.info("File {} read exception occured - {}".format(self.filePath, e))

        return status, dic
