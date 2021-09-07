from application_logging.AppLogging import AppLog
import pandas as pd
from sklearn.preprocessing import StandardScaler

class datapreprocess:

    def __init__(self,exeType='Training'):
        self.exeType = exeType

        self.applog = AppLog(self.exeType)
        self.log = self.applog.log("sLogger")

    def dropcolumn(self, df, columnname):

        try:
            self.log.info("Initiate to drop {} column from the dataset".format(columnname))
            df.drop(columns=columnname,axis=0,inplace=True)
            self.log.info("Successfully drop the {} column from the dataset".format(columnname))
        except Exception as e:
            self.log.critical("Exception occoured, while droping the {} column from dataset : {}".format(columnname,e))
        return df


    def stdscalling(self,df):

        try:
            # define standard scaler
            scaler = StandardScaler()
            # transform data
            scaled = scaler.fit_transform(df)

        except Exception as e:
            self.log.critical("Exception occoured, while scalling the dataframe dataset : {}".format(e))

        return scaled