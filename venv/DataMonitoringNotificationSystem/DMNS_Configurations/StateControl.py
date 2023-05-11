
import os
import yaml
from yaml.loader import SafeLoader
from pprint import pprint
from datetime import *
import requests

#capture relative location of AlertState.yaml file
AlertStateFile_relativeLocation = os.path.dirname(__file__) + "\\AlertState.yaml"


#capture relative location of Config.yaml file
ConfigFile_relativeLocation = os.path.dirname(__file__) + "\\Config.yaml"



def SetNewConfigData(Config_dict):
    with open(ConfigFile_relativeLocation, 'w') as ConfigFile:
        ConfigFile.write(yaml.dump(Config_dict))
        ConfigFile.close()

def getNextEscalationDateTime(AlertState_dict, Config_dict):
    CurrentErrorState = AlertState_dict['LastCheckedState']['LastRecordedErrorState']
    MostRecentEscalationDatetime = AlertState_dict['AlertState']['DefconStartTime']
    EscalationInterval = Config_dict['TimeBetweenEscalations']

    if (CurrentErrorState=='Error'):
        NextEscalationDateTime = MostRecentEscalationDatetime+timedelta(hours=EscalationInterval)
    else: NextEscalationDateTime='NA'

    return NextEscalationDateTime


def getCurrentConfigAsDict():
    with open(ConfigFile_relativeLocation) as ConfigFile:
        ConfigFile_Dict = yaml.load(ConfigFile, Loader=SafeLoader)
    return ConfigFile_Dict


def getCurrentAlertStateAsDict():
    with open(AlertStateFile_relativeLocation) as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
    return AlertState_Dict

def SetAcknowledgeAlert():
    #get current dictionary from alertstate.yaml file
    with open(AlertStateFile_relativeLocation) as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
        AlertState_Dict['LastCheckedState']['LastAcknowledgedDatetime'] = datetime.now()
        AlertState_Dict['AlertState']['DefconState'] = 4
        AlertState_Dict['LastCheckedState']['LastRecordedErrorState'] = "NoError"
        AlertStateFile.close()


    #write the new dictionary settings
    with open(AlertStateFile_relativeLocation, 'w') as AlertStateFile2:
        AlertStateFile2.write(yaml.dump(AlertState_Dict, default_flow_style=False))
        AlertStateFile2.close()




def SetCheckStateDateTime():
    with open(AlertStateFile_relativeLocation) as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
    AlertState_Dict['LastCheckedState']['CheckStateDateTime'] = datetime.now()
    AlertStateFile.close()


    #open the Alertstate yaml file to write new state of things
    with open(AlertStateFile_relativeLocation, 'w') as AlertStateFile:
        AlertStateFile.write(yaml.dump(AlertState_Dict, default_flow_style=False))
        AlertStateFile.close()


def SetControlState(ErrorStateValue):
    with open(AlertStateFile_relativeLocation) as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)

    AlertState_Dict['LastCheckedState']['LastRecordedErrorState'] = ErrorStateValue
    AlertState_Dict['LastCheckedState']['CheckStateDateTime'] = datetime.now()
    AlertStateFile.close()


    #open the Alertstate yaml file to write new state of things
    with open(AlertStateFile_relativeLocation, 'w') as AlertStateFile:
        AlertStateFile.write(yaml.dump(AlertState_Dict, default_flow_style=False))
        AlertStateFile.close()



def  GetDefConStateEscalation_DateTime():
    with open(AlertStateFile_relativeLocation) as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
        AlertStateDateTime = AlertState_Dict['LastCheckedState']['CheckStateDateTime']
        AlertStateFile.close()
    return AlertStateDateTime



def  GetDefConConfig_TimeBetweenEscalations():
    with open(ConfigFile_relativeLocation) as ConfigFile:
        ConfigFile_Dict = yaml.load(ConfigFile, Loader=SafeLoader)
        ConfigFile_Escalation_TimeBetweenEscalations = ConfigFile_Dict['TimeBetweenEscalations']
        ConfigFile.close()
    return ConfigFile_Escalation_TimeBetweenEscalations



def IncrementDecrimentDefConLevel(val):

    with open(AlertStateFile_relativeLocation) as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
        AlertStateFile.close()

    AlertState_Dict['AlertState']['DefconState'] = (AlertState_Dict['AlertState']['DefconState'])+val
    AlertState_Dict['AlertState']['DefconStartTime'] = datetime.now()

    with open(AlertStateFile_relativeLocation, 'w') as AlertStateFile:
        AlertStateFile.write(yaml.dump(AlertState_Dict, default_flow_style=False))
        AlertStateFile.close()

def SetNextEscalationDateTime():
    with open(AlertStateFile_relativeLocation) as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
        AlertStateFile.close()

        EscalationIncrementHours = GetDefConConfig_TimeBetweenEscalations()
        MostRecentDefConStartDateTime = AlertState_Dict['AlertState']['DefconStartTime']


    AlertState_Dict['NextEscalationDateTime'] = AlertState_Dict['AlertState']['DefconStartTime'] + timedelta(hours=EscalationIncrementHours)


    with open(AlertStateFile_relativeLocation, 'w') as AlertStateFile:
        AlertStateFile.write(yaml.dump(AlertState_Dict, default_flow_style=False))
        AlertStateFile.close()

def getCurrentAlertStateDict():
    with open(AlertStateFile_relativeLocation) as AlertStateFile:

        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)


    return AlertState_Dict

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""

    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def CheckIfAutoAcknowledmentNeeded():
    with open(ConfigFile_relativeLocation) as ConfigFile:
        ConfigFile_Dict = yaml.load(ConfigFile, Loader=SafeLoader)

    # open the Alertstate yaml file to write new state of things
    with open(AlertStateFile_relativeLocation) as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)

    CurrentTime = datetime.now().time()
    AutoAcknowledgeStartTime = time(23, 00, 0) #11:00pm
    AutoAcknowledgeEndTime = time(23, 55, 0) #11:55pm
    CurrentErrorState = AlertState_Dict['LastCheckedState']['LastRecordedErrorState']

    if ((CurrentErrorState == "Error") and time_in_range(AutoAcknowledgeStartTime, AutoAcknowledgeEndTime, CurrentTime)):
        return 1 #(TRUE) We need to acknowldedge a stale alert
    else:
        return -1 #(FALSE) No alerts need to be acknowledged


def CheckIfDefConEscalationNeeded():
    with open(ConfigFile_relativeLocation) as ConfigFile:
        ConfigFile_Dict = yaml.load(ConfigFile, Loader=SafeLoader)
        ConfigFile.close()
    with open(AlertStateFile_relativeLocation) as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
        AlertStateFile.close()

    IsEscalationNeeded = -1 #default condition of NO escalation needed
    CurrentDateTime = datetime.now()
    LastTimeLogUpdated = AlertState_Dict['LastCheckedState']['CheckStateDateTime']
    CurrentDefConLevel = AlertState_Dict['AlertState']['DefconState']
    TimeBetweenEscalations = ConfigFile_Dict['TimeBetweenEscalations']
    LastDateDefconLevelChanged = AlertState_Dict['AlertState']['DefconStartTime']
    CurrentTimePlusEscalationInterval = datetime.now() + timedelta(hours=1)
    CurrentErrorState = AlertState_Dict['LastCheckedState']['LastRecordedErrorState']
    AlertStateFile_LastAcknowledgedDatetime = AlertState_Dict['LastCheckedState']['LastAcknowledgedDatetime']
    NextEscalationDateTime = AlertState_Dict['NextEscalationDateTime']


    # when in error state
    if ((CurrentErrorState == "Error") and (CurrentDefConLevel in range(2,5))):
        if ((CurrentDateTime > NextEscalationDateTime)): # and (AlertStateFile_LastAcknowledgedDatetime < NextEscalationDateTime)):
            IsEscalationNeeded = 1 #set escalation needed to true
    return IsEscalationNeeded



def IS_URLAvailable(URL):

    try:
        response = requests.get(URL)
    except:
        return False
    return True




