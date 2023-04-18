import pypyodbc as odbc
import datetime



def GetTelemetry_IsErrorState_Today():

    IsError = 1  #by default, we are in an "Error" state. .

    try:
        conn = odbc.connect('Driver={SQL Server};'
                        'Server=ProdWarehouse;'
                        'Database=SSISDB;'
                        'Trusted_Connection=yes;'
                        'autocommit=True;')


    except Exception as e:

        print("could not connect to database")
        IsError = 1 #if we cannot connect, then we have an error!

    else:
        cursor = conn.cursor()

        #check if the telemetry log contains an error from today. If so, then we can set state to NoError(IsError=-1)
        Qry = """select IIF(count(1) > 0, 1, -1)
        from ETLCustom.ETLTelemetry t
            join
                (--identify most recent orchestration error execution
            select top 1 ExecutionInstanceGUID, t.CreatedOnDateTime from ETLCustom.ETLTelemetry t
            where t.CreatedOnDateTime > CAST(GETDATE() AS DATE)
                and t.TelemetryMessage like '%error%'
                ) MostRecent
                    on MostRecent.ExecutionInstanceGUID = t.ExecutionInstanceGUID"""

        cursor.execute(Qry)
        IsError = cursor.fetchone()[0]

        cursor.close()


    if conn.connected == 1:
        conn.close() #close connection

    return  IsError


