import logging
from logging import config
import os

class AppLog:
    """
        Class: AppLog
        Description: Objective of this class is to create db connection, table creation
        Input: file path including file name

        Written By: Dinesh Naik
        Version: 1.0
        Revisions: None

    """

    def __init__(self,execType='Training',logfile="AppLog.log"):
        self.logfile = logfile
        self.execType = execType

        self.dirpath = self.execType+'_Logs'
        if not os.path.isdir(self.dirpath):
            os.mkdir(self.dirpath)
        self.filepath = self.dirpath +'//'+self.logfile

        ''' Initiate the logging objects for the class'''
        # Log file path
        #self.logpath = self.execType+'_Logs//DataBaseConnection.log'
        #print(self.filepath)
        # refrence logging configuration files
        config.fileConfig("application_logging//Logging_Config.conf",defaults={"logfilename":self.filepath})
        #log = logging.getLogger("sLogger")

    def log(self,logger="root"):
        return logging.getLogger(logger)



