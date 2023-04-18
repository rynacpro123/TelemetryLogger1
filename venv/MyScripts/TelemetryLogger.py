import pypyodbc as odbc
import datetime



try:
    conn = odbc.connect('Driver={SQL Server};'
                      'Server=ProdWarehouse;'
                      'Database=SSISDB;'
                      'Trusted_Connection=yes;'
                        'autocommit=True;')
except Exception as e:
    # print(e)
    # print('task is terminated')
    # sys.exit()

    with open('//prodin01/websites/ops.spie.org/ETLMonitor/GeneralETLTelemetryMonitor.html', 'w') as file:
        file.write("IsTelemetryErrorToday: True22  " + str(datetime.datetime.now()))
    sys.exit()

else:
    cursor = conn.cursor()

    Qry = """select IIF(count(1) > 0, 'IsTelemetryErrorToday: True', 'IsTelemetryErrorToday: False')
	from ETLCustom.ETLTelemetry t
		join
			(--identify most recent orchestration error execution
		select top 1 ExecutionInstanceGUID, t.CreatedOnDateTime from ETLCustom.ETLTelemetry t
		where t.CreatedOnDateTime > CAST(GETDATE() AS DATE)
			and t.TelemetryMessage like '%error%'
			) MostRecent
				on MostRecent.ExecutionInstanceGUID = t.ExecutionInstanceGUID"""
    #storedProc = "insert dbo.RyanTesting_Date(CurrentDate) values ('2023-01-11 20:36:16.987')"

    cursor.execute(Qry)

    result_set = cursor.fetchone()[0]
    #print(result_set)
   # conn.commit()


    cursor.close()

finally:
    if conn.connected  == 1:
        print('connection closed')
        conn.close()


with open('//prodin01/websites/ops.spie.org/ETLMonitor/GeneralETLTelemetryMonitor.html', 'w') as file:
    file.write(result_set + " " + str(datetime.datetime.now()))


#\\prodapiws01\websites\api\Site24x7_ETLMonitoring




