import yaml
from yaml.loader import SafeLoader
from pprint import pprint
from datetime import *






def getCurrentConfigAsDict():
    with open('Config.yaml') as ConfigFile:
        ConfigFile_Dict = yaml.load(ConfigFile, Loader=SafeLoader)
    return ConfigFile_Dict


def getCurrentAlertStateAsDict():
    with open('AlertState.yaml') as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
    return AlertState_Dict



def SetControlState(ErrorStateValue):
    with open('AlertState.yaml') as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)

    AlertState_Dict['LastCheckedState']['LastRecordedErrorState'] = ErrorStateValue
    AlertState_Dict['LastCheckedState']['CheckStateDateTime'] = datetime.now()
    AlertStateFile.close()


    #open the Alertstate yaml file to write new state of things
    with open('AlertState.yaml', 'w') as AlertStateFile:
        AlertStateFile.write(yaml.dump(AlertState_Dict, default_flow_style=False))
        AlertStateFile.close()



def  GetDefConStateEscalation_DateTime():
    with open('AlertState.yaml') as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
        AlertStateDateTime = AlertState_Dict['LastCheckedState']['CheckStateDateTime']
        AlertStateFile.close()
    return AlertStateDateTime



def  GetDefConConfig_TimeBetweenEscalations():
    with open('Config.yaml') as ConfigFile:
        ConfigFile_Dict = yaml.load(ConfigFile, Loader=SafeLoader)
        ConfigFile_Escalation_TimeBetweenEscalations = ConfigFile_Dict['TimeBetweenEscalations']
        ConfigFile.close()
    return ConfigFile_Escalation_TimeBetweenEscalations



def IncrementDecrimentDefConLevel(val):

    with open('AlertState.yaml') as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
        AlertStateFile.close()

    AlertState_Dict['AlertState']['DefconState'] = (AlertState_Dict['AlertState']['DefconState'])+val
    AlertState_Dict['AlertState']['DefconStartTime'] = datetime.now()

    with open('AlertState.yaml', 'w') as AlertStateFile:
        AlertStateFile.write(yaml.dump(AlertState_Dict, default_flow_style=False))
        AlertStateFile.close()



def CheckIfDefConEscalationNeeded():
    with open('Config.yaml') as ConfigFile:
        ConfigFile_Dict = yaml.load(ConfigFile, Loader=SafeLoader)
        ConfigFile.close()
    with open('AlertState.yaml') as AlertStateFile:
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
    AlertStateFile_LastAcknowledgedDatetime = AlertState_Dict['LastCheckedState']['LastAcknowledgedDatetime']
    NextEscalationDateTime = timedelta(hours=TimeBetweenEscalations) + LastDateDefconLevelChanged

    # # when in nonError state and defcon 3... this is most of the time... get the ball rolling
    # if ((CurrentErrorState == "Error") and (CurrentDefConLevel == 3) and (AlertStateFile_LastAcknowledgedDatetime < NextEscalationDateTime)):
    #     IsEscalationNeeded = 1


    # when in error state
    if ((CurrentErrorState == "Error") and (CurrentDefConLevel in range(2,4))):
        if ((CurrentDateTime > NextEscalationDateTime) and (AlertStateFile_LastAcknowledgedDatetime < NextEscalationDateTime)):
            IsEscalationNeeded = 1 #set escalation needed to true
    return IsEscalationNeeded



