import yaml
from yaml.loader import SafeLoader
from pprint import pprint
from datetime import *
import sys
import os





Root_VirtualEnvPath = os.path.split(os.environ['VIRTUAL_ENV'])[0]
YAML_Files_Root = '\\venv\\DataMonitoringNotificationSystem\\DMNS_Configurations\\'
Dir_YAML_Files = Root_VirtualEnvPath + YAML_Files_Root


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""

    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end



def getCurrentConfigAsDict():
    with open(Dir_YAML_Files + "Config.yaml") as ConfigFile:
        ConfigFile_Dict = yaml.load(ConfigFile, Loader=SafeLoader)
    return ConfigFile_Dict


def getCurrentAlertStateAsDict():
    with open(Dir_YAML_Files + "AlertState.yaml") as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
    return AlertState_Dict



def SetControlState(ErrorStateValue):
    with open(Dir_YAML_Files + 'AlertState.yaml') as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)

    AlertState_Dict['LastCheckedState']['LastRecordedErrorState'] = ErrorStateValue
    AlertState_Dict['LastCheckedState']['CheckStateDateTime'] = datetime.now()
    AlertStateFile.close()


    #open the Alertstate yaml file to write new state of things
    with open(Dir_YAML_Files + 'AlertState.yaml', 'w') as AlertStateFile:
        AlertStateFile.write(yaml.dump(AlertState_Dict, default_flow_style=False))
        AlertStateFile.close()



def  GetDefConStateEscalation_DateTime():
    with open(Dir_YAML_Files + 'AlertState.yaml') as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
        AlertStateDateTime = AlertState_Dict['LastCheckedState']['CheckStateDateTime']
        AlertStateFile.close()
    return AlertStateDateTime



def  GetDefConConfig_TimeBetweenEscalations():
    with open(Dir_YAML_Files + 'Config.yaml') as ConfigFile:
        ConfigFile_Dict = yaml.load(ConfigFile, Loader=SafeLoader)
        ConfigFile_Escalation_TimeBetweenEscalations = ConfigFile_Dict['TimeBetweenEscalations']
        ConfigFile.close()
    return ConfigFile_Escalation_TimeBetweenEscalations



def IncrementDecrimentDefConLevel(val):

    with open(Dir_YAML_Files + 'AlertState.yaml') as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
        AlertStateFile.close()

    AlertState_Dict['AlertState']['DefconState'] = (AlertState_Dict['AlertState']['DefconState'])+val
    AlertState_Dict['AlertState']['DefconStartTime'] = datetime.now()

    with open(Dir_YAML_Files + 'AlertState.yaml', 'w') as AlertStateFile:
        AlertStateFile.write(yaml.dump(AlertState_Dict, default_flow_style=False))
        AlertStateFile.close()



def CheckIfAutoAcknowledmentNeeded():
    with open(Dir_YAML_Files + "Config.yaml") as ConfigFile:
        ConfigFile_Dict = yaml.load(ConfigFile, Loader=SafeLoader)

    # open the Alertstate yaml file to write new state of things
    with open(Dir_YAML_Files + 'AlertState.yaml') as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)

    CurrentTime = datetime.now().time()
    AutoAcknowledgeStartTime = time(1, 00, 0) #11:30pm
    AutoAcknowledgeEndTime = time(23, 00, 0) #11:55pm
    CurrentErrorState = AlertState_Dict['LastCheckedState']['LastRecordedErrorState']

    if ((CurrentErrorState == "Error") and time_in_range(AutoAcknowledgeStartTime, AutoAcknowledgeEndTime, CurrentTime)):
        return 1 #(TRUE) We need to acknowldedge a stale alert
    else:
        return -1 #(FALSE) No alerts need to be acknowledged

def CheckIfDefConEscalationNeeded():
    with open(Dir_YAML_Files + 'Config.yaml') as ConfigFile:
        ConfigFile_Dict = yaml.load(ConfigFile, Loader=SafeLoader)
        ConfigFile.close()
    with open(Dir_YAML_Files + 'AlertState.yaml') as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
        AlertStateFile.close()

    IsEscalationNeeded = -1 #default condition
    CurrentDateTime = datetime.now()
    LastTimeLogUpdated = AlertState_Dict['LastCheckedState']['CheckStateDateTime']
    CurrentDefConLevel = AlertState_Dict['AlertState']['DefconState']
    TimeBetweenEscalations = ConfigFile_Dict['TimeBetweenEscalations']
    LastDateDefconLevelChanged = AlertState_Dict['AlertState']['DefconStartTime']
    CurrentTimePlusEscalationInterval = datetime.now() + timedelta(hours=1)
    CurrentErrorState = AlertState_Dict['LastCheckedState']['LastRecordedErrorState']
    NextEscalationDateTime = timedelta(hours=TimeBetweenEscalations) + LastDateDefconLevelChanged


    if ((CurrentErrorState == "Error") and (CurrentDefConLevel in range(2,4))):
        if (CurrentDateTime > NextEscalationDateTime):
            IsEscalationNeeded = 1 #set escalation needed to true
    return IsEscalationNeeded

    # print (CurrentDateTime)
    # print (LastTimeLogUpdated)
    # print(CurrentDefConLevel)
    # print(TimeBetweenEscalations)
    # print(LastDateDefconLevelChanged)


    # print("current time is: " + str(CurrentDateTime))
    # print("current + TimeBetweenEscalations time is: " + str(CurrentDateTime + datetime.timedelta(hours=1))   )

    #
    #  if (CurrentErrorState == "Error")  and   ((CurrentDateTime>NextEscalationDateTime)  or (NextEscalationDateTime=="NULL"))
    #     print("hi")


# def CheckIfDefConEscalationNeeded():
#     with open('Config.yaml') as ConfigFile:
#         ConfigFile_Dict = yaml.load(ConfigFile, Loader=SafeLoader)
#         ConfigFile.close()
#     with open('AlertState.yaml') as AlertStateFile:
#         AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
#         AlertStateFile.close()
#
#     IsEscalationNeeded = -1 #default condition
#     CurrentDateTime = datetime.now()
#     LastTimeLogUpdated = AlertState_Dict['LastCheckedState']['CheckStateDateTime']
#     CurrentDefConLevel = AlertState_Dict['AlertState']['DefconState']
#     TimeBetweenEscalations = ConfigFile_Dict['TimeBetweenEscalations']
#     LastDateDefconLevelChanged = AlertState_Dict['AlertState']['DefconStartTime']
#     CurrentTimePlusEscalationInterval = datetime.now() + timedelta(hours=1)
#     CurrentErrorState = AlertState_Dict['LastCheckedState']['LastRecordedErrorState']
#     AlertStateFile_LastAcknowledgedDatetime = AlertState_Dict['LastCheckedState']['LastAcknowledgedDatetime']
#     NextEscalationDateTime = timedelta(hours=TimeBetweenEscalations) + LastDateDefconLevelChanged
#
#     # when in error state
#     if ((CurrentErrorState == "Error") and (CurrentDateTime):
#         if ((CurrentDateTime > NextEscalationDateTime) and (AlertStateFile_LastAcknowledgedDatetime < NextEscalationDateTime)):
#             IsEscalationNeeded = 1 #set escalation needed to true
#     return IsEscalationNeeded


