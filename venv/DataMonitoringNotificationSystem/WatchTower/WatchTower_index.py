


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

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, fields
from wtforms.validators import DataRequired, InputRequired
from modules import *
from  StateControl import *



#idea: consider adding sql snips in file to execute for validating system state
#idea: separate page for escalations, time between escalations and who for each level. basically the content of the config file.


app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'I%14&O0DgngP$?g'

# Flask-Bootstrap requires this line
Bootstrap(app)



# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class WatchTowerStatus(FlaskForm):
    CurrentStatusDate = fields.StringField('Datetime when warehouse health was last checked:', validators=[InputRequired()])
    CurrentErrorState = fields.StringField('Current Error State of datawarehouse:', validators=[InputRequired()])
    DefConStartTime = fields.StringField('Date and time of the last change to the Defcon level:', validators=[InputRequired()])
    CurrentDefConLevel = fields.StringField('Current DefCon status:', validators=[InputRequired()])
    MostRecentAcknowledgementDate = fields.StringField('Last time a warehouse malfunction was acknowledged:', validators=[InputRequired()])
    NextEscalationDateTime = fields.StringField('Next DefCon alert datetime:', validators=[InputRequired()])
    Ack_Alrt = fields.SubmitField('Acknowledge Alert')
    Config = fields.SubmitField('Watchtower Setup')


class WatchTowerConfig(FlaskForm):
    Server = fields.StringField('Server Monitored:', validators=[InputRequired()])
    Database = fields.StringField('Database Monitored:', validators=[InputRequired()])
    EscalationIntervalHrs = fields.FloatField('Hours between escalation:', validators=[InputRequired()])
    Defcon3Contact = fields.StringField('Defcon level 3 contact:', validators=[InputRequired()])
    Defcon2Contact = fields.StringField('Defcon level 2 contact:', validators=[InputRequired()])
    Defcon1Contact = fields.StringField('Defcon level 1 contact:', validators=[InputRequired()])
    WatchTowerHome = fields.SubmitField('WatchTower Home')
    SaveChanges = fields.SubmitField('SaveChanges')








# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    #--names = get_names(ACTORS)
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = WatchTowerStatus()

    #pull current state from AlertSTate YAML
    AlertState_dict = getCurrentAlertStateDict()
    Config_dict = getCurrentConfigAsDict()


    form.CurrentStatusDate.data = AlertState_dict['LastCheckedState']['CheckStateDateTime']
    form.CurrentErrorState.data = AlertState_dict['LastCheckedState']['LastRecordedErrorState']
    form.DefConStartTime.data = AlertState_dict['AlertState']['DefconStartTime']
    form.CurrentDefConLevel.data = AlertState_dict['AlertState']['DefconState']
    form.MostRecentAcknowledgementDate.data = AlertState_dict['LastCheckedState']['LastAcknowledgedDatetime']
    form.NextEscalationDateTime.data = getNextEscalationDateTime(AlertState_dict, Config_dict)



    if form.validate_on_submit():
        if form.Ack_Alrt.data:
            SetAcknowledgeAlert()
            form.CurrentStatusDate.data = AlertState_dict['LastCheckedState']['CheckStateDateTime']
            form.CurrentErrorState.data = AlertState_dict['LastCheckedState']['LastRecordedErrorState']
            form.DefConStartTime.data = AlertState_dict['AlertState']['DefconStartTime']
            form.CurrentDefConLevel.data = AlertState_dict['AlertState']['DefconState']
            form.MostRecentAcknowledgementDate.data = AlertState_dict['LastCheckedState']['LastAcknowledgedDatetime']
            form.NextEscalationDateTime.data = getNextEscalationDateTime(AlertState_dict, Config_dict)
        elif form.Config.data:
            return redirect(url_for('Configuration'))

    return render_template('index.html', form=form)


@app.route('/Configuration', methods=['GET', 'POST'])
def Configuration():
    form = WatchTowerConfig()

    # pull current configuration
    Config_dict = getCurrentConfigAsDict()

    form.Server.data = Config_dict['DBConnectionCredentials']['Server']
    form.Database.data = Config_dict['DBConnectionCredentials']['Database']

    if request.method == "GET":
        form.EscalationIntervalHrs.data = Config_dict['TimeBetweenEscalations']
        form.Defcon3Contact.data = Config_dict['EscalationPolicy']['Defcon3']['Contact']
        form.Defcon2Contact.data = Config_dict['EscalationPolicy']['Defcon2']['Contact']
        form.Defcon1Contact.data = Config_dict['EscalationPolicy']['Defcon1']['Contact']



    if form.validate_on_submit():
        if form.SaveChanges.data:
            Config_dict['TimeBetweenEscalations'] = form.EscalationIntervalHrs.data
            Config_dict['EscalationPolicy']['Defcon3']['Contact'] = form.Defcon3Contact.data
            Config_dict['EscalationPolicy']['Defcon2']['Contact'] = form.Defcon2Contact.data
            Config_dict['EscalationPolicy']['Defcon1']['Contact'] = form.Defcon1Contact.data

            print(Config_dict['TimeBetweenEscalations'])

            SetNewConfigData(Config_dict)
            render_template('Configuration.html', form=form)
        elif form.WatchTowerHome.data:
            return redirect('/')
    return render_template('Configuration.html', form=form)


#         name = form.name.data
#         if name.lower() in names:
#             # empty the form field
#             form.name.data = ""
#             id = get_id(ACTORS, name)
#             # redirect the browser to another route and template
#             return redirect( url_for('actor', id=id) )
#         else:
#             message = "That actor is not in our database."
#     return render_template('index.html', names=names, form=form, message=message)
#
# @app.route('/actor/<id>')
# def actor(id):
#     # run function to get actor data based on the id in the path
#     id, name, photo = get_actor(ACTORS, id)
#     if name == "Unknown":
#         # redirect the browser to the error template
#         return render_template('404.html'), 404
#     else:
#         # pass all the data for the selected actor to the template
#         return render_template('actor.html', id=id, name=name, photo=photo)
#
# # 2 routes to handle errors - they have templates too
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500


#keep this as is, run the server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)