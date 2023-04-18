

from pathlib import Path
import sys

#get the path of the 'DataMonitoringNotificationSystem' folder
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())



#add DMNS_Configurations to python project root path)
path_DMNS_Configurations = path+'\DMNS_Configurations'


#add Monitor directory to python project root path)
path_Monitor = path+'\Monitor'

#add Watchtower directory to python project root path)
path_WatchTower = path+'\WatchTower'

path_WatchTower = path+'\DMNS_Configurations'

#insert the paths to the folders in the project
sys.path.insert(0, path)
sys.path.insert(0, path_DMNS_Configurations)
sys.path.insert(0, path_Monitor)
sys.path.insert(0, path_WatchTower)
sys.path.insert(0, 'C:\PYthon\VirtualEnvironments\Watchtower-1\Lib\site-packages') ##needs to be made dynamic


import pyodbc as odbc
import datetime
from StateControl import *





def GetTelemetry_IsErrorState_Today():

    IsError = 1  #by default, we are in an "Error" state. .

    try:
        conn = odbc.connect('Driver={SQL Server};'
                        'Server=ProdWarehouse;'
                        'Database=SSISDB;'
                        'Trusted_Connection=yes;'
                        'autocommit=True;')


    except Exception as e:

        print("could not connect to database")
        IsError = 1 #if we cannot connect, then there is a server error that should be investigated.

    else:

        MyDict = getCurrentAlertStateAsDict()

        #obtain most recent acknowledge datetime
        AlertStateFile_IsAcknowledgedDateTime = MyDict['LastCheckedState']['LastAcknowledgedDatetime']

        AlertStateFile_IsAcknowledgedDateTime = AlertStateFile_IsAcknowledgedDateTime.strftime("%m/%d/%Y %H:%M")

        cursor = conn.cursor()

        #haxor solution to add the input parameter to the SQL scalar function
        SQLFunction = "select [etlcustom].[fnsWatchtowerMonitorCheck](\'" + AlertStateFile_IsAcknowledgedDateTime + "\')"


        cursor.execute(SQLFunction)
        IsError = cursor.fetchone()[0]

        cursor.close()
        conn.close()  # close connection


    return  IsError #-1:NoError   vs   1:Error


