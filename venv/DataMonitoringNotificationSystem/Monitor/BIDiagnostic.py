

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

#insert the paths to the folders in the project
sys.path.insert(0, path)
sys.path.insert(0, path_DMNS_Configurations)
sys.path.insert(0, path_Monitor)
sys.path.insert(0, path_WatchTower)


from TelemetryCheck import GetTelemetry_IsErrorState_Today
#from StateControl import *
from AlertLog import *


#
# SetCheckStateDateTime()
#
#
# #get today state of telemetry errors and update AlertState.Yaml with current state
# if (GetTelemetry_IsErrorState_Today() == 1):   #    (1)"Error"  /  (-1)"NoError"
#     #set state of yaml state file when there is an error
#     SetControlState('Error')
#
#
#
# #assess if defcon escalation needed and send alert as needed
# if (CheckIfDefConEscalationNeeded() == 1):
#     IncrementDecrimentDefConLevel(-1)
#     SetNextEscalationDateTime()
#     SendAlertNotification()
#

#assess if we need to auto acknowledge an alert
if (CheckIfAutoAcknowledmentNeeded() == 1):
    SendAlertNotification()
    print("NeedToacknowledge2")

# #log current state of alertState file to DB log
# LogCurrentStatusToDB()


print("BIDiagnostic execution complete")




