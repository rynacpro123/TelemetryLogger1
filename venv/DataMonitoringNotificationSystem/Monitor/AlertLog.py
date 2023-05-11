import yaml
from yaml.loader import SafeLoader
from datetime import *
import smtplib
from email.message import EmailMessage
import pyodbc as odbc
from StateControl import *




def SendAlertNotification(MessageType='GeneralError'):

    #SMTPLoginAcct = "ryanc@spie.org"
    #SMTPLoginPwd = "ddd!"
    #sender = "ryanc@spie.org"
    sender = "Watchtower-EDWAlert@spie.org"
    #receiver = "3607399044@msg.fi.google.com" # ryan
    #receiver = "2534323244@tmomail.net"  # Linden
    #receiver = "ETLGroup@spie.org"  # BI team
    receiver = "ryanc@spie.org"

    AlertStatus_Dict = getCurrentAlertStateAsDict()
    Config_Dict = getCurrentConfigAsDict()

    DefconLevel = AlertStatus_Dict['AlertState']['DefconState']
    NextEscalationTime =  AlertStatus_Dict['AlertState']['DefconStartTime'] + timedelta(hours=Config_Dict['TimeBetweenEscalations'])
    AlertStateFile_LastRecordedErrorState = AlertStatus_Dict['LastCheckedState']['LastRecordedErrorState']
    NextEscalationTime_friendlyName = NextEscalationTime.strftime("%m/%d/%Y %H:%M")
    DefConLevel1 = Config_Dict['EscalationPolicy']['Defcon1']['Contact']
    DefConLevel2 = Config_Dict['EscalationPolicy']['Defcon2']['Contact']
    DefConLevel3 = Config_Dict['EscalationPolicy']['Defcon3']['Contact']


    match MessageType:
        case 'GeneralError':
            Message = "The Warehouse ETL load has thrown an error.\n\nCurrent DefCon Level is: "+ str(DefconLevel) + "\n\nNext escalation will be sent at: " + NextEscalationTime_friendlyName + "\n"
            Message = Message + "-----------------------------------------------------------------------"
            Message = Message + "\n     DefConlevel3 Escalation contact: " + DefConLevel3
            Message = Message + "\n     DefConlevel2 Escalation contact: " + DefConLevel2
            Message = Message + "\n     DefConlevel1 Escalation contact: " + DefConLevel1
            Message = Message + "\n---------------------------------------------------------------------"

            # set email message contents
            msg = EmailMessage()
            msg['Subject'] = 'General DW ETL Error Alert'
            msg['From'] = sender
            msg['To'] = receiver
            msg.set_content(Message)


        case 'AutoAcknowledge':
            Message = "Watchtower Auto acknowledement complete. Defcon and Error level reset to default values. \n\nCurrent DefCon Level is: " + str(DefconLevel) + "\n\nCurrent ErrorState: " + str(AlertStateFile_LastRecordedErrorState) +"\n\n"
            Message = Message + "-----------------------------------------------------------------------"
            Message = Message + "\n     DefConlevel3 Escalation contact: " + DefConLevel3
            Message = Message + "\n     DefConlevel2 Escalation contact: " + DefConLevel2
            Message = Message + "\n     DefConlevel1 Escalation contact: " + DefConLevel1
            Message = Message + "\n---------------------------------------------------------------------"

            Message = Message + "\n\n\n\n *NOTE* This notification is to let you know that the Watchtower system has automatically acknowledged any unacknowledged alerts. This resetting will ensure that the system is ready to detect any new errors that may occur during the next day. \n\nWatchtower alert status page: http://devapp23:5000/"

            # set email message contents
            msg = EmailMessage()
            msg['Subject'] = 'AutoAcknowledge - DW ETL Error Alert'
            msg['From'] = sender
            msg['To'] = receiver
            msg.set_content(Message)


        case 'Reporing service Offline':
            Message = "The production reporting service is not responding. Potentially offline. \n\nCurrent DefCon Level is: " + str(DefconLevel) + "\n\nCurrent ErrorState: " + str(AlertStateFile_LastRecordedErrorState) +"\n\n"
            Message = Message + "-----------------------------------------------------------------------"
            Message = Message + "\n     DefConlevel3 Escalation contact: " + DefConLevel3
            Message = Message + "\n     DefConlevel2 Escalation contact: " + DefConLevel2
            Message = Message + "\n     DefConlevel1 Escalation contact: " + DefConLevel1
            Message = Message + "\n---------------------------------------------------------------------"



            # set email message contents
            msg = EmailMessage()
            msg['Subject'] = 'Reporting service unavailable'
            msg['From'] = sender
            msg['To'] = receiver
            msg.set_content(Message)

        case _:
            Message = "Default Nofitication - Watchtower Processing Error\n\n"

            # set email message contents
            msg = EmailMessage()
            msg['Subject'] = 'Default Nofitication - Watchtower Processing Error -- unhandled alert'
            msg['From'] = sender
            msg['To'] = receiver
            msg.set_content(Message)




    try:
        smtpObj = smtplib.SMTP("automail.spie.org")
        smtpObj.send_message(msg)
        smtpObj.quit()
        print ("Successfully sent notification")



    except Exception as e:
        print ("Error: unable to send email")
        print(repr(e))


def LogCurrentStatusToDB():
    try:
        conn = odbc.connect('Driver={SQL Server};'
                        'Server=PRODAPP23\PRODREPORT;'
                        'Database=SSISDB;'
                        'Trusted_Connection=yes;'
                        'autocommit=True;')


    except Exception as e:

        print("could not connect to database")

    else:

        MyDict = getCurrentAlertStateAsDict()

        AlertStateFile_DefconStartTime = MyDict['AlertState']['DefconStartTime']
        AlertStateFile_DefconState = MyDict['AlertState']['DefconState']
        AlertStateFile_CheckStateDateTime = MyDict['LastCheckedState']['CheckStateDateTime']
        AlertStateFile_LastRecordedErrorState = MyDict['LastCheckedState']['LastRecordedErrorState']
        AlertStateFile_IsAcknowledgedDateTime = MyDict['LastCheckedState']['LastAcknowledgedDatetime']




        cursor = conn.cursor()

        #LogEvent
        #Prepare stored procedure exeuction script and parameters
        storedProc = "exec [etlcustom].[UpdateDiagnosticLog] @AlertStateFile_DefconStartTime = ?, @AlertStateFile_DefconState = ?,@AlertStateFile_CheckStateDateTime = ?,@AlertStateFile_LastRecordedErrorState = ?, @AlertStateFile_IsAcknowledgedDateTime = ?"
        params = (AlertStateFile_DefconStartTime, AlertStateFile_DefconState, AlertStateFile_CheckStateDateTime, AlertStateFile_LastRecordedErrorState, AlertStateFile_IsAcknowledgedDateTime)

        #@AlertStateFile_IsAcknowledgedDateTime
        #Execute Stored Procedure with Parameters
        cursor.execute(storedProc, params)

        #Call commit() method to save changes to db
        conn.commit()
        conn.close()




