import yaml
from yaml.loader import SafeLoader
from datetime import *
import smtplib
from email.message import EmailMessage
import pyodbc as odbc
from StateControl import *




def SendAlertNotification():

    SMTPLoginAcct = "ryanc@spie.org"
    SMTPLoginPwd = "Rh44umba!"
    sender = "ryanc@spie.org"
    #receiver = "3607399044@msg.fi.google.com" # ryan
    #receiver = "2534323244@tmomail.net"  # Linden
    receiver = "ETLGroup@spie.org"  # BI team
    #receiver = "ryanc@spie.org"


    #set email message contents
    msg = EmailMessage()
    msg['Subject'] = 'PRODUCTION DW ETL ERROR ALERT!!!!!'
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content("""The Production Warehouse ETL load has thrown an error. \n\nEscalation policy: <Disabled> \n\nDefcon3 notification: <Null> """)

    try:
        smtpObj = smtplib.SMTP("automail.spie.org", 587)
        smtpObj.starttls()
        smtpObj.login(SMTPLoginAcct, SMTPLoginPwd)
        smtpObj.send_message(msg)
        smtpObj.quit()
        print ("Successfully sent notification")

    except Exception as e:
        print ("Error: unable to send email")


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




        cursor = conn.cursor()

        #LogEvent
        #Prepare stored procedure exeuction script and parameters
        storedProc = "exec [etlcustom].[UpdateDiagnosticLog] @AlertStateFile_DefconStartTime = ?, @AlertStateFile_DefconState = ?,@AlertStateFile_CheckStateDateTime = ?,@AlertStateFile_LastRecordedErrorState = ?"
        params = (AlertStateFile_DefconStartTime, AlertStateFile_DefconState, AlertStateFile_CheckStateDateTime, AlertStateFile_LastRecordedErrorState)

        #Execute Stored Procedure with Parameters
        cursor.execute(storedProc, params)

        #Call commit() method to save changes to db
        conn.commit()
        conn.close()




