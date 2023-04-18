import yaml
from yaml.loader import SafeLoader
from pprint import pprint
import datetime



# CurrentTime = datetime.datetime.now()
# print(CurrentTime) #2023-03-21 20:53:09.828947


def DecrimentDefConState():

    # Open the file and load the file. use config file to get the specifics needed for connection and notification
    with open('Config.yaml') as ConfigFile:
        Config_Dict = yaml.load(ConfigFile, Loader=SafeLoader)
       #pprint(Config_Dict)
        # print()
        # print(Config_Dict["Email_AlertCredentials"]["Login"])
        #StateDict = (Config_Dict["AlertStateTemplate"])


    #open the Alertstate yaml file to get current state of things
    with open('AlertState.yaml') as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)

        if (AlertState_Dict['AlertState']['DefconState']>1):
            AlertState_Dict['AlertState']['DefconState'] = AlertState_Dict['AlertState']['DefconState']-1
            AlertState_Dict['AlertState']['DefconStartTime'] = datetime.datetime.now()
        AlertStateFile.close()

    #open the Alertstate yaml file to write new state of things
    with open('AlertState.yaml', 'w') as AlertStateFile:
        AlertStateFile.write(yaml.dump(AlertState_Dict, default_flow_style=False))
        AlertStateFile.close()

def IncrementDefConState():

    # Open the file and load the file. use config file to get the specifics needed for connection and notification
    with open('Config.yaml') as ConfigFile:
        Config_Dict = yaml.load(ConfigFile, Loader=SafeLoader)
       #pprint(Config_Dict)
        # print()
        # print(Config_Dict["Email_AlertCredentials"]["Login"])
        #StateDict = (Config_Dict["AlertStateTemplate"])


    #open the Alertstate yaml file to get current state of things
    with open('AlertState.yaml') as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)

        if (AlertState_Dict['AlertState']['DefconState']<3):
            AlertState_Dict['AlertState']['DefconState'] = AlertState_Dict['AlertState']['DefconState']+1
            AlertState_Dict['AlertState']['DefconStartTime'] = datetime.datetime.now()
        AlertStateFile.close()

    #open the Alertstate yaml file to write new state of things
    with open('AlertState.yaml', 'w') as AlertStateFile:
        AlertStateFile.write(yaml.dump(AlertState_Dict, default_flow_style=False))
        AlertStateFile.close()












