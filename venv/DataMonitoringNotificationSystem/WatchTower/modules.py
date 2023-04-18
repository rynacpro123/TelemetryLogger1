import yaml
from yaml.loader import SafeLoader




def getCurrentAlertStateDict():
    with open('Configurations/AlertState.yaml') as AlertStateFile:
        AlertState_Dict = yaml.load(AlertStateFile, Loader=SafeLoader)
    return AlertState_Dict

