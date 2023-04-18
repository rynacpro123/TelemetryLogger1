import smtplib

SMTPLoginAcct = "ryanc@spie.org"
SMTPLoginPwd = "Rh44umba!"


sender = "ryanc@spie.org"
receiver = "3607399044@msg.fi.google.com"


message = """From: BI Alert System <ryanc@spie.org>
To: ryan <ryanc@spie.org>
Subject: Notification Test

This is a test e-mail message from Ryan!

"""


try:
    smtpObj = smtplib.SMTP("automail.spie.org", 587)
    smtpObj.starttls()
    smtpObj.login(SMTPLoginAcct, SMTPLoginPwd)
    smtpObj.sendmail(sender, receiver, message)
    smtpObj.quit()
    print ("Successfully sent email")

except Exception as e:
    print ("Error: unable to send email")