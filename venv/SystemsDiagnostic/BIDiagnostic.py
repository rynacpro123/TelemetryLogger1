from TelemetryCheck import GetTelemetry_IsErrorState_Today
from StateControl import *
from AlertLog import *




#get today state of telemetry errors and update AlertState.Yaml with current state
if (GetTelemetry_IsErrorState_Today() == 1):   #    (1)"Error"  /  (-1)"NoError"
    #set state of yaml state file when there is an error
    #print("errorIdentified")
    SetControlState('Error')
else:
    # set state of yaml state file when there is no error
    #print("else")
    SetControlState('NoError')


#assess if defcon escalation needed and send alert as needed
if (CheckIfDefConEscalationNeeded() == 1):
    IncrementDecrimentDefConLevel(-1)
    SendAlertNotification()

#log current state of alertState file to DB log
LogCurrentStatusToDB()


print("BIDiagnostic execution complete")




