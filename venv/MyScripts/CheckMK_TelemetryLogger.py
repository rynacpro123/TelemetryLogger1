import pypyodbc as odbc
import datetime

try:
    conn = odbc.connect('Driver={SQL Server};'
                      'Server=ProdWarehouse;'
                      'Database=SSISDB;'
                      'Trusted_Connection=yes;'
                        'autocommit=True;')
except Exception as e:
    print(e)
    print('task is terminated')
    sys.exit()

else:
    cursor = conn.cursor()

    Qry = """select IIF(count(1) > 0, '2 TelemetryError - Datawarehouse ETL Telemetry Error', '0 TelemetryError - No Errors reported')
	from ETLCustom.ETLTelemetry t
		join
			(--identify most recent orchestration execution
			SELECT top 1 ExecutionInstanceGUID, MostRecentCreatedDateTime = MAX(CreatedOnDateTime)
			FROM ETLCustom.ETLTelemetry
			where TelemetryMessage = 'Orchestration Begin'
			GROUP BY ExecutionInstanceGUID
			order by  MAX(CreatedOnDateTime) desc
			) MostRecent
				on MostRecent.ExecutionInstanceGUID = t.ExecutionInstanceGUID
		where t.TelemetryMessage not like '%error%'"""
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


with open('c:/ProgramData/checkmk/agent/local/bilog/BITelemetryLog.log', 'w') as file:
#with open('C:/Users/ryanc/PycharmProjects/TelemetryLogger1/BITelemetryLog.log', 'w') as file:
    file.writelines("<<<local>>>\r\n")
    file.write(result_set + " " + str(datetime.datetime.now()))





