import pyodbc
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import xmlrpc
import sched, time
from datetime import datetime, date, timedelta
from threading import Timer
from xmlrpc import client as xmlrpclib
import urllib.request, urllib.parse, urllib.error

class Bossnet_MSSQLServer:
    # Odoo Setup
    _url = "http://192.168.41.161:8069"
    _db = "ed_testing"
    _username = "api"
    _password_odoo = "Ckhu9yDJd7fF5ZRK"

    # MS SQL Server
    _server_MSSQLS = 'mobileappstest.eadeco.com.my,1433' 
    _database_MSSQLS = 'ATTENDANCE' 
    _username_MSSQLS = 'sa' 
    _password_MSSQLS = 'bcs@1688' 

    # Postgres
    _server_Postgres = '192.168.41.163'
    _port_Postgres = '5432'
    _database_Postgres = 'ed_testing'
    _username_Postgres = 'admin'
    _password_Postgres = 'ZY8jZ3AK'

    #Odoo
    def _common(self):
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self._url))
        return common

    def _models(self):
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self._url))
        return models

    def _getLocalUID(self):
        uid = self._common().authenticate(self._db,self._username, self._password_odoo, {})
        return uid

    def _getOnlineUID(self):
        info = xmlrpc.client.ServerProxy(self._url).start()
        self._url, self._db, self._username, self._password_odoo = \
            info['host'], info['database'], info['user'], info['password']
        return info

    def _getCurrentDatePython(self):
        now = datetime.now()
        curDate = now.strftime("%Y/%m/%d %H:%M:%S")
        return curDate

    def _getCurrentDateOdoo(self):
        DateTime = self._models().execute_kw(self._db, self._getLocalUID(),self._password_odoo, 'hr.attendance', 'search_read', [], {'fields': ['create_date'], 'limit':1})
        getDate = DateTime[0]['create_date']
        return getDate

    def getEmployeeAttendanceUID(self, uid):
        status = self._models().execute_kw(self._db,self._getLocalUID(),self._password_odoo, 'hr.attendance', 'search_read', [], {'fields': ['employee_id','check_out', 'check_in', 'id']})
        for currStatus in status:
            if uid == int(currStatus['employee_id'][0]):
                return currStatus['id']
        return 0

    def getModuleStatus(self):
        status = self._models().execute_kw(self._db,self._getLocalUID(),self._password_odoo, 'res.users', 'search_read', [], {'fields': ['id','name']})
        return status

    def getEmployeesID(self):
        listAttendance = []
        attendances = self._models().execute_kw(self._db,self._getLocalUID(),self._password_odoo, 'hr.attendance', 'search_read', [], {'fields': ['id','employee_id']})
        for attendance in attendances:
            uid = attendance['employee_id'][0]
            listAttendance.append(uid)
        return listAttendance

    def getAttendancesID(self):
        listEmployeeID = []
        attendances = self._models().execute_kw(self._db,self._getLocalUID(),self._password_odoo, 'hr.attendance', 'search_read', [], {'fields': ['id','employee_id']})
        for attendance in attendances:
            uid = attendance['id']
            listEmployeeID.append(uid)
        return listEmployeeID

    def getListEmployeesBarcode(self, listEmployeesID):
        listBarcode = []
        for attendanceID in listEmployeesID:
            employees = self._models().execute_kw(self._db,self._getLocalUID(),self._password_odoo, 'hr.employee', 'search_read', [[['id','=',attendanceID]]], {'fields': ['barcode']})
            barcode = employees[0]['barcode']
            listBarcode.append(barcode)
        return listBarcode
            
    def getListAttendancesCheckIn(self, listAttendancesID):
        listCheckIn = []
        for attendanceID in listAttendancesID:
            checkIns = self._models().execute_kw(self._db,self._getLocalUID(),self._password_odoo, 'hr.attendance', 'search_read', [[['id','=',attendanceID]]], {'fields': ['check_in']})
            checInStatus = checkIns[0]['check_in']
            if checInStatus == False:
                listCheckIn.append('False')
            elif checInStatus != False:
                listCheckIn.append(checkIns[0]['check_in'])
        return listCheckIn

    def getListAttendancesCheckOut(self, listAttendancesID):
        listCheckOut = []
        for attendanceID in listAttendancesID:
            checkOuts = self._models().execute_kw(self._db,self._getLocalUID(),self._password_odoo, 'hr.attendance', 'search_read', [[['id','=',attendanceID]]], {'fields': ['check_out']})
            checOutStatus = checkOuts[0]['check_out']
            if checOutStatus == False:
                listCheckOut.append('False')
            elif checOutStatus != False:
                listCheckOut.append(checkOuts[0]['check_out'])
        return listCheckOut

    def getEmployeeBarcode(self, uid):
        employees = self._models().execute_kw(self._db,self._getLocalUID(),self._password_odoo, 'hr.employee', 'search_read', [[['id','=',uid]]], {'fields':['name','barcode']})
        if not employees:
            return False
        else:
            return employees

    def getAttendance_baseId(self,uid):
        attendances = self._models().execute_kw(self._db,self._getLocalUID(),self._password_odoo, 'hr.attendance', 'search_read', [[['id','=',self.getEmployeeAttendanceUID(uid)]]], {'fields':['id','employee_id','check_in','check_out']})
        if not attendances:
            return False
        else:
            return attendances

    def getEmployee_baseName(self,name):
        employee = self._models().execute_kw(self._db,self._getLocalUID(),self._password_odoo, 'hr.employee', 'search_read', [[['name','=',name]]], {'fields':['id']})
        if not employee:
            return False
        else:
            return employee

    def createEmployee(self, user_id, name, barcode):
        status = self._models().execute_kw(self._db, self._getLocalUID(), self._password_odoo, 'hr.employee', 'create', [{
            'user_id': user_id,
            'name': name,
            # 'work_email': barcode+'@gmail.com'
        }])
        return status

    def createUsers(self, name, barcode, identification_id):
        status = self._models().execute_kw(self._db, self._getLocalUID(), self._password_odoo, 'res.users', 'create', [{
            'name': name,
            'login': barcode,
            'password': identification_id,
            'conapp_passwd': identification_id,
            'notification_type': 'inbox',
            'odoobot_state': 'not_initialized',
            'email': barcode+'@example.com'
        }])
        return status

    def modifyAttendance(self,uid,datetime,direction):
        try:
            if direction.lower() == 'check in':
                status = self._models().execute_kw(self._db, self._getLocalUID(), self._password_odoo, 'hr.attendance', 'create', [{
                    'employee_id': uid, 
                    'check_in': datetime
                }])
                return status
            elif direction.lower() == 'check out':
                status = self._models().execute_kw(self._db, self._getLocalUID(), self._password_odoo, 'hr.attendance', 'write', [self.getEmployeeAttendanceUID(uid), {
                    'check_out': datetime
                }])
                return status
        except:
            return "Data already exist"

    # MS SQL Server
    # cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server_MSSQLS+';DATABASE='+_database_MSSQLS+';UID='+_username_MSSQLS+';PWD='+ _password_MSSQLS+';')
    # cursor = cnxn.cursor()

    # cursor.execute("SELECT @@version;") 
    # row = cursor.fetchone() 
    # while row: 
    #     print(row[0])
    #     row = cursor.fetchone()

    # Postgres
    def pgConnectionCheck(self):
        try:
            connection = psycopg2.connect(user=self._username_Postgres, password=self._password_Postgres, host=self._server_Postgres, database=self._database_Postgres)
            cursor = connection.cursor()
            print(connection.get_dsn_parameters(), "\n")
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            output = "You are connected to - ", record, "\n"
            if(connection):
                cursor.close()
                connection.close()
                output = "PostgreSQL connection is closed"
                return output
            return output
        except(Exception, psycopg2.Error) as error:
            output = "Error while connecting to PostgreSQL", error
            return output

    def pgCursorCA_BN(self, statement, values):
        try:
            connection = psycopg2.connect(user=self._username_Postgres, password=self._password_Postgres, host=self._server_Postgres, database=self._database_Postgres)
            cursor = connection.cursor()
            cursor.execute(statement, values)
            connection.commit()
            count = cursor.rowcount
            print(str(count) + " Record inserted successfully into table")
        except(Exception, psycopg2.Error) as error:
            output = "Cursor error:", str(error)
            print(output)
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print('Connection close')

    def pgCursorBN_CA(self,statement):
        try:
            connection = psycopg2.connect(user=self._username_Postgres, password=self._password_Postgres, host=self._server_Postgres, database=self._database_Postgres)
            cursor = connection.cursor()
            cursor.execute(statement)
            record = cursor.fetchall()
            return record
        except(Exception, psycopg2.Error) as error:
            output = "Cursor error:", str(error)
            return output
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print('Connection close')

    # MS SQL Server
    def MSSQLS_Connection_Checker(self):
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self._server_MSSQLS+';DATABASE='+self._database_MSSQLS+';UID='+self._username_MSSQLS+';PWD='+self._password_MSSQLS+';')
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT @@version;") 
            row = cursor.fetchone() 
            while row: 
                print(row[0])
                row = cursor.fetchone()
            return "Connected"
        except(Exception, pyodbc.Error) as error:
            output = "Error while connecting to MS SQL Server", error
            return output
        finally:
            if(connection):
                cursor.close()
                connection.close()
                output = "MS SQL Server connection is closed"
                return output

    def MSQLS_Cursor(self, statement, values):
        try:
            connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self._server_MSSQLS+';DATABASE='+self._database_MSSQLS+';UID='+self._username_MSSQLS+';PWD='+self._password_MSSQLS+';')
            cursor = connection.cursor()
            cursor.execute(statement, values)
            connection.commit()
            count = cursor.rowcount
            print(str(count) + " Record inserted successfully into table")
        except(Exception, pyodbc.Error) as error:
            output = "Cursor error:", str(error)
            print(output)
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print('Connection close')

    def SQLCreateStatement(self, table_name, columns):
        SQL_Statement = "INSERT INTO " + table_name + "("
        listDataLen = len(columns)
        assignValue = ''
        x = 0
        for data in columns:
            x += 1
            if(x < listDataLen):
                assignValue += '?,'
                SQL_Statement += data + ', '
            elif(x >= listDataLen):
                assignValue += '?'
                SQL_Statement += data +  ') VALUES (' + assignValue + ');'
        return SQL_Statement

    def SQLSelectStatement(self, table_name, columns):
        SQL_Statement = "SELECT "
        listDataLen = len(columns)
        x = 0
        for data in columns:
            x += 1
            if(x < listDataLen):
                SQL_Statement += data + ', '
            elif(x >= listDataLen):
                SQL_Statement += data +  ' FROM ' + table_name + ';'
        return SQL_Statement


    def MSSQLSCursorCA_BN(self, statement, values):
        try:
            connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self._server_MSSQLS+';DATABASE='+self._database_MSSQLS+';UID='+self._username_MSSQLS+';PWD='+self._password_MSSQLS+';')
            cursor = connection.cursor()
            cursor.execute(statement, values)
            connection.commit()
            count = cursor.rowcount
            print(str(count) + " Record inserted successfully into table")
        except(Exception, pyodbc.Error) as error:
            output = "Cursor error:", str(error)
            print(output)
        finally:
            if(connection):
                cursor.close()
                connection.close();
                print('Connection close')

    def MSSQLSCursorBN_CA(self,statement):
        try:
            connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self._server_MSSQLS+';DATABASE='+self._database_MSSQLS+';UID='+self._username_MSSQLS+';PWD='+self._password_MSSQLS+';')
            cursor = connection.cursor()
            cursor.execute(statement)
            record = cursor.fetchall()
            return record
        except(Exception, pyodbc.Error) as error:
            output = "Cursor error:", str(error)
            return output
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print('Connetion close')

    def test(self):
        SQL_Statement = "SELECT * FROM ATTENDANCE.dbo.HR_Employee;"
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self._server_MSSQLS+';DATABASE='+self._database_MSSQLS+';UID='+self._username_MSSQLS+';PWD='+self._password_MSSQLS+';')
        cursor = connection.cursor()
        cursor.execute(SQL_Statement)
        myresult = cursor.fetchall()
        if(connection):
            cursor.close()
            connection.close()
            print('Connetion close')
        return myresult

    def test2(self):
        SQL_Statement = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'HR_Employee'"
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self._server_MSSQLS+';DATABASE='+self._database_MSSQLS+';UID='+self._username_MSSQLS+';PWD='+self._password_MSSQLS+';')
        cursor = connection.cursor()
        cursor.execute(SQL_Statement)
        myresult = cursor.fetchall()
        if(connection):
            cursor.close()
            connection.close()
            print('Connetion close')
        return myresult

    def test3(self):
        SQL_Statement = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'res_company'"
        connection = psycopg2.connect(user=self._username_Postgres, password=self._password_Postgres, host=self._server_Postgres, database=self._database_Postgres)
        cursor = connection.cursor()
        cursor.execute(SQL_Statement)
        record = cursor.fetchall()
        if(connection):
            cursor.close()
            connection.close()
            print('Connetion close')
        return record

    def test4(self):
        SQL_Statement = "SELECT DISTINCT location_code, location_name FROM ATTENDANCE.dbo.HR_Employee;"
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self._server_MSSQLS+';DATABASE='+self._database_MSSQLS+';UID='+self._username_MSSQLS+';PWD='+self._password_MSSQLS+';')
        cursor = connection.cursor()
        cursor.execute(SQL_Statement)
        myresult = cursor.fetchall()
        if(connection):
            cursor.close()
            connection.close()
            print('Connetion close')
        return myresult


BNMSQLS = Bossnet_MSSQLServer()
print(BNMSQLS.getModuleStatus())

# -----DB Info hr_employee Postgres------
# ('ed_testing', 'public', 'hr_employee', 'id', 1, "nextval('hr_employee_id_seq'::regclass)", 'NO', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '1', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'),
# ('ed_testing', 'public', 'hr_employee', 'message_main_attachment_id', 2, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '2', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'resource_id', 3, None, 'NO', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '3', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'name', 4, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '4', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'user_id', 5, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '5', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'),
# ('ed_testing', 'public', 'hr_employee', 'active', 6, None, 'YES', 'boolean', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bool', None, None, None, None, '6', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'address_home_id', 7, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '7', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'country_id', 8, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '8', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'gender', 9, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '9', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'marital', 10, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '10', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'spouse_complete_name', 11, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '11', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'spouse_birthdate', 12, None, 'YES', 'date', None, None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'date', None, None, None, None, '12', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'children', 13, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '13', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'place_of_birth', 14, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '14', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'),
# ('ed_testing', 'public', 'hr_employee', 'country_of_birth', 15, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '15', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'birthday', 16, None, 'YES', 'date', None, None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'date', None, None, None, None, '16', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'ssnid', 17, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '17', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'sinid', 18, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '18', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'identification_id', 19, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '19', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'passport_id', 20, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '20', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'bank_account_id', 21, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '21', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'permit_no', 22, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '22', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'visa_no', 23, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '23', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'visa_expire', 24, None, 'YES', 'date', None, None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'date', None, None, None, None, '24', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'additional_note', 25, None, 'YES', 'text', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'text', None, None, None, None, '25', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'certificate', 26, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '26', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'study_field', 27, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '27', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'study_school', 28, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '28', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'emergency_contact', 29, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '29', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'emergency_phone', 30, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '30', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'km_home_work', 31, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '31', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'google_drive_link', 32, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '32', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'job_title', 33, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '33', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'),
# ('ed_testing', 'public', 'hr_employee', 'address_id', 34, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '34', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'work_phone', 35, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '35', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'mobile_phone', 36, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '36', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'work_email', 37, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '37', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'work_location', 38, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '38', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'job_id', 39, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '39', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'department_id', 40, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '40', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'parent_id', 41, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '41', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'coach_id', 42, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '42', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'notes', 43, None, 'YES', 'text', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'text', None, None, None, None, '43', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'color', 44, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '44', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'company_id', 45, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '45', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'resource_calendar_id', 46, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '46', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'create_uid', 47, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '47', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'create_date', 48, None, 'YES', 'timestamp without time zone', None, None, None, None, None, 6, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'timestamp', None, None, None, None, '48', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'write_uid', 49, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '49', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'write_date', 50, None, 'YES', 'timestamp without time zone', None, None, None, None, None, 6, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'timestamp', None, None, None, None, '50', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'barcode', 51, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '51', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'pin', 52, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '52', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'last_attendance_id', 53, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '53', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'rfid_card_code', 54, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '54', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'hr_employee', 'no_autoclose', 55, None, 'YES', 'boolean', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bool', None, None, None, None, '55', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES')]

# -----DB Info res_company Postgres------
# ('ed_testing', 'public', 'res_company', 'id', 1, "nextval('res_company_id_seq'::regclass)", 'NO', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '1', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'name', 2, None, 'NO', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '2', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'partner_id', 3, None, 'NO', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '3', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'currency_id', 4, None, 'NO', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '4', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'sequence', 5, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '5', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'create_date', 6, None, 'YES', 'timestamp without time zone', None, None, None, None, None, 6, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'timestamp', None, None, None, None, '6', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'parent_id', 7, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '7', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'report_header', 8, None, 'YES', 'text', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'text', None, None, None, None, '8', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'report_footer', 9, None, 'YES', 'text', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'text', None, None, None, None, '9', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'logo_web', 10, None, 'YES', 'bytea', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bytea', None, None, None, None, '10', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'account_no', 11, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '11', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'email', 12, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '12', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'phone', 13, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '13', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'company_registry', 14, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '14', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'paperformat_id', 15, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '15', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'external_report_layout_id', 16, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '16', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'base_onboarding_company_state', 17, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '17', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'),
# ('ed_testing', 'public', 'res_company', 'create_uid', 18, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '18', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'write_uid', 19, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '19', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'write_date', 20, None, 'YES', 'timestamp without time zone', None, None, None, None, None, 6, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'timestamp', None, None, None, None, '20', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'nomenclature_id', 21, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '21', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'partner_gid', 22, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '22', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'snailmail_color', 23, None, 'YES', 'boolean', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bool', None, None, None, None, '23', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'snailmail_duplex', 24, None, 'YES', 'boolean', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bool', None, None, None, None, '24', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'propagation_minimum_delta', 25, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '25', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'internal_transit_location_id', 26, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '26', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'fiscalyear_last_day', 27, None, 'NO', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '27', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'fiscalyear_last_month', 28, None, 'NO', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '28', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'period_lock_date', 29, None, 'YES', 'date', None, None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'date', None, None, None, None, '29', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'fiscalyear_lock_date', 30, None, 'YES', 'date', None, None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'date', None, None, None, None, '30', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'transfer_account_id', 31, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '31', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'expects_chart_of_accounts', 32, None, 'YES', 'boolean', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bool', None, None, None, None, '32', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'chart_template_id', 33, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '33', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'bank_account_code_prefix', 34, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '34', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'cash_account_code_prefix', 35, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '35', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'transfer_account_code_prefix', 36, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '36', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'account_sale_tax_id', 37, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '37', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'account_purchase_tax_id', 38, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '38', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'tax_cash_basis_journal_id', 39, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '39', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'tax_calculation_rounding_method', 40, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '40', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'currency_exchange_journal_id', 41, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '41', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'anglo_saxon_accounting', 42, None, 'YES', 'boolean', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bool', None, None, None, None, '42', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'property_stock_account_input_categ_id', 43, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '43', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'property_stock_account_output_categ_id', 44, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '44', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'property_stock_valuation_account_id', 45, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '45', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'overdue_msg', 46, None, 'YES', 'text', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'text', None, None, None, None, '46', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'tax_exigibility', 47, None, 'YES', 'boolean', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bool', None, None, None, None, '47', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'account_bank_reconciliation_start', 48, None, 'YES', 'date', None, None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'date', None, None, None, None, '48', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'incoterm_id', 49, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '49', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'invoice_reference_type', 50, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '50', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'qr_code', 51, None, 'YES', 'boolean', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bool', None, None, None, None, '51', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'invoice_is_email', 52, None, 'YES', 'boolean', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bool', None, None, None, None, '52', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'invoice_is_print', 53, None, 'YES', 'boolean', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bool', None, None, None, None, '53', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'account_opening_move_id', 54, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '54', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'account_setup_bank_data_state', 55, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '55', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'account_setup_fy_data_state', 56, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '56', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'account_setup_coa_state', 57, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '57', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'account_onboarding_invoice_layout_state', 58, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '58', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'account_onboarding_sample_invoice_state', 59, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '59', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'account_onboarding_sale_tax_state', 60, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '60', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'account_invoice_onboarding_state', 61, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '61', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'account_dashboard_onboarding_state', 62, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '62', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'payment_acquirer_onboarding_state', 63, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '63', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'payment_onboarding_payment_method', 64, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '64', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'invoice_is_snailmail', 65, None, 'YES', 'boolean', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bool', None, None, None, None, '65', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'sale_note', 66, None, 'YES', 'text', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'text', None, None, None, None, '66', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'portal_confirmation_sign', 67, None, 'YES', 'boolean', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bool', None, None, None, None, '67', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'portal_confirmation_pay', 68, None, 'YES', 'boolean', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'bool', None, None, None, None, '68', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'quotation_validity_days', 69, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '69', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'sale_quotation_onboarding_state', 70, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '70', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'sale_onboarding_order_confirmation_state', 71, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '71', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'sale_onboarding_sample_quotation_state', 72, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '72', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'sale_onboarding_payment_method', 73, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '73', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'security_lead', 74, None, 'NO', 'double precision', None, None, 53, 2, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'float8', None, None, None, None, '74', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'resource_calendar_id', 75, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '75', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'so_double_validation', 76, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '76', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'so_double_validation_limit', 77, None, 'YES', 'double precision', None, None, 53, 2, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'float8', None, None, None, None, '77', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'category_id', 78, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '78', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'code', 79, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '79', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'rfid', 80, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '80', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'employee_id_gen_method', 81, None, 'YES', 'character varying', None, 1073741824, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'varchar', None, None, None, None, '81', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'employee_id_random_digits', 82, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '82', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'employee_id_sequence', 83, None, 'YES', 'integer', None, None, 32, 2, 0, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'int4', None, None, None, None, '83', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES'), 
# ('ed_testing', 'public', 'res_company', 'attendance_maximum_hours_per_day', 84, None, 'YES', 'numeric', None, None, None, 10, None, None, None, None, None, None, None, None, None, None, None, None, None, 'ed_testing', 'pg_catalog', 'numeric', None, None, None, None, '84', 'NO', 'NO', None, None, None, None, None, 'NO', 'NEVER', None, 'YES')

# -----DB Info MS SQL Server-------
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'Barcode', 1, none, 'NO', 'varchar', 50, 50, none, none, none, none, none, none, 'iso_1', none, none, 'Latin1_General_CI_AI', none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'Name', 2, none, 'YES', 'varchar', 100, 100, none, none, none, none, none, none, 'iso_1', none, none, 'Latin1_General_CI_AI', none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'identification_no', 3, none, 'YES', 'varchar', 30, 30, none, none, none, none, none, none, 'iso_1', none, none, 'Latin1_General_CI_AI', none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'joined_at', 4, none, 'YES', 'datetime', none, none, none, none, none, 3, none, none, none, none, none, none, none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'resigned_at', 5, none, 'YES', 'datetime', none, none, none, none, none, 3, none, none, none, none, none, none, none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'location_code', 6, none, 'YES', 'varchar', 30, 30, none, none, none, none, none, none, 'iso_1', none, none, 'Latin1_General_CI_AI', none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'location_name', 7, none, 'YES', 'varchar', 500, 500, none, none, none, none, none, none, 'iso_1', none, none, 'Latin1_General_CI_AI', none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'workgroup_code', 8, none, 'YES', 'varchar', 30, 30, none, none, none, none, none, none, 'iso_1', none, none, 'Latin1_General_CI_AI', none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'workgroup_name', 9, none, 'YES', 'varchar', 500, 500, none, none, none, none, none, none, 'iso_1', none, none, 'Latin1_General_CI_AI', none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'company_code', 10, none, 'YES', 'varchar', 10, 10, none, none, none, none, none, none, 'iso_1', none, none, 'Latin1_General_CI_AI', none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'company_name', 11, none, 'YES', 'varchar', 100, 100, none, none, none, none, none, none, 'iso_1', none, none, 'Latin1_General_CI_AI', none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'job_code', 12, none, 'YES', 'varchar', 50, 50, none, none, none, none, none, none, 'iso_1', none, none, 'Latin1_General_CI_AI', none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'job_name', 13, none, 'YES', 'varchar', 500, 500, none, none, none, none, none, none, 'iso_1', none, none, 'Latin1_General_CI_AI', none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'mobile_phone', 14, none, 'YES', 'varchar', 20, 20, none, none, none, none, none, none, 'iso_1', none, none, 'Latin1_General_CI_AI', none, none, none), 
#  ('ATTENDANCE', 'dbo', 'HR_Employee', 'Created_Date', 15, none, 'YES', 'datetime', none, none, none, none, none, 3, none, none, none, none, none, none, none, none, none) 

# [('AREA SALES ASSISTANT MANAGER I', 'AREA SALES ASSISTANT MANAGER I'), 
# ('AREA SALES ASSISTANT MANAGER II', 'AREA SALES ASSISTANT MANAGER II'), 
# ('AREA SALES MANAGER I', 'AREA SALES MANAGER I'), 
# ('AREA SALES MANAGER II', 'AREA SALES MANAGER II'), 
# ('COORDINATOR II', 'COORDINATOR II'), 
# ('DIR', 'DIRECTORS'), 
# ('DIVISION SALES MANAGER II', 'DIVISION SALES MANAGER II'), 
# ('DIVISION SALES SENIOR MANAGER II', 'DIVISION SALES SENIOR MANAGER II'), 
# ('EVT_TL', 'EVENT TEAM LEADER'), 
# ('FITTER_SPVR', 'FITTER SUPERVISOR'), 
# ('GEN_WKR', 'GENERAL WORKER'), 
# ('MERCHANDISING_EXE_II', 'MERCHANDISING EXECUTIVE II'), 
# ('MKT_EXE', 'MARKETING EXECUTIVE'), 
# ('RET_ASST_MGR', 'RETAIL ASSISTANT MANAGER II'), 
# ('RETAIL_JNR_EXE_II', 'RETAIL_JNR_EXE_II'), 
# ('S&O_ASST_MGR_II', 'SALES & OPERATION ASSISTANT MANAGER II'), 
# ('S&O_MGR', 'SALES & OPERATION MANAGER'), 
# ('S&O_MGR II', 'SALES & OPERATION MANAGER II'), 
# ('SA', 'SALES ASSOCIATE'), 
# ('SA_SNR', 'SALES SENIOR ASSOCIATE'), 
# ('SAL_ASST', 'SALES ASSISTANT'), 
# ('SAL_SNR_SPVR', 'SALES SENIOR SUPERVISOR'), 
# ('SAL_SPVR', 'SALES SUPERVISOR'), 
# ('SALES MANAGER I', 'SALES MANAGER I'), 
# ('SALES_ASST_SPVSR', 'SALES ASSISTANT SUPERVISOR'), 
# ('SALES_TRAINEE_ASSOC', 'TRAINEE SALES ASSOCIATES'), 
# ('SAR', 'SALES ASSOCIATE ROTATE'), 
# ('SAS', 'SALES ASSOCIATE SUPERVISOR'), 
# ('SE II', 'SALES EXECUTIVE II'), 
# ('SE_I', 'SALES EXECUTIVE I'), 
# ('SENIOR FITTER', 'SENIOR FITTER'), 
# ('SEWER', 'SEWER'), 
# ('SNR_CASHIER', 'SENIOR CASHIER'), 
# ('SPVR', 'SUPERVISOR'), 
# ('STL', 'SALES TEAM LEADER'), 
# ('STORE_BOY', 'STORE BOY'), 
# ('STORE_MGR', 'STORE MANAGER'), 
# ('STORE_SPVR', 'STORE SUPERVISOR')]

# [('AKE', 'AKEMI'), 
# ('AT_IN', 'AT&IN'), 
# ('FAV', 'FAVORITA'), 
# ('HOOGA', 'HOOGA'), 
# ('NICE', 'NICE'), 
# ('NONE', 'NONE'), 
# ('PREM', 'PREMIUM BRAND'), 
# ('ST1', 'STUDIO 1'), 
# ('UCHI', 'AKEMIUCHI'), 
# ('WINNY', 'WINNY')]

# -----Code Here-----

# CA to BN
def CAtoBN():
    statement = BNMSQLS.SQLCreateStatement('ATTENDANCE.dbo.bossnet_ca_bn_table', ['id','barcode','check_in', 'check_out','direction', 'remark'])
    EmployeesID = BNMSQLS.getEmployeesID()
    AttendancesID = BNMSQLS.getAttendancesID()
    barcode = BNMSQLS.getListEmployeesBarcode(EmployeesID)
    checkin = BNMSQLS.getListAttendancesCheckIn(AttendancesID)
    checkout = BNMSQLS.getListAttendancesCheckOut(AttendancesID)
    print(statement)
    x = 0
    for employeeID in EmployeesID:
        values = (employeeID, barcode[x], checkin[x], checkout[x], 'check out', 'this is remark')
        status = BNMSQLS.MSSQLSCursorCA_BN(statement, values)
        print(status)
        x += 1


# BN to CA
def BNtoCA():
    statement = BNMSQLS.SQLSelectStatement('ATTENDANCE.dbo.HR_Employee',['Barcode', 'Name','identification_no', 'location_code'])
    records = BNMSQLS.MSSQLSCursorBN_CA(statement)
    for record in records:
        MSQLSname = record[0]
        MSQLSbarcode = record[1]
        MSQLSidentification_no = record[2]
        MSQLSlocation_code = record[3]
        MSSQLSdatetime = record[2] + timedelta(hours=8)
        
        MSSQLSdatetime = record[2] + str(timedelta(hours=10))
        MSSQLSdirection = record[3]
        employeeBaseName = BNMSQLS.getEmployee_baseName(MSQLSname)
        employeeBarcode = BNMSQLS.getEmployeeBarcode(MSQLSname)
        
        if employeeBaseName != False and employeeBarcode == False:
            EBNId = employeeBaseName[0]['id']
            BNMSQLS.modifyAttendance(EBNId, MSSQLSdatetime, MSSQLSdirection)
        elif employeeBaseName == False and employeeBarcode != False:
            empId = employeeBarcode[0]['id']
            BNMSQLS.modifyAttendance(empId, MSSQLSdatetime, MSSQLSdirection)
        elif employeeBaseName == False and employeeBarcode == False:
            empId = BNMSQLS.createEmployee(MSQLSname,MSQLSbarcode)
            BNMSQLS.modifyAttendance(empId, MSSQLSdatetime, MSSQLSdirection)


def create_User_Employee():
    statement = BNMSQLS.SQLSelectStatement('ATTENDANCE.dbo.HR_Employee',['Barcode', 'Name','identification_no', 'location_code'])
    records = BNMSQLS.MSSQLSCursorBN_CA(statement)
    for record in records:
        MSQLSname = record[0]
        MSQLSbarcode = record[1]
        MSQLSidentification_no = record[2]
        MSQLSlocation_code = record[3]
        # print(MSQLSname, MSQLSbarcode, MSQLSidentification_no, MSQLSlocation_code)
        employeeBaseName = BNMSQLS.getEmployee_baseName(MSQLSname)
        # employeeBarcode = BNMSQLS.getEmployeeBarcode(MSQLSname)
        if employeeBaseName == False:
            userId = BNMSQLS.createUsers(MSQLSname, MSQLSbarcode, MSQLSidentification_no)
            print(userId)
create_User_Employee()

def import_data_SQLS_PS():
    statement = BA.pgCreateStatement('public.bossnet_ca_bn_table', ['id','barcode','check_in', 'check_out','direction', 'remark'])
    EmployeesID = BA.getEmployeesID()
    AttendancesID = BA.getAttendancesID()
    barcode = BA.getListEmployeesBarcode(EmployeesID)
    checkin = BA.getListAttendancesCheckIn(AttendancesID)
    checkout = BA.getListAttendancesCheckOut(AttendancesID)
    x = 0
    for employeeID in EmployeesID:
        values = (employeeID, barcode[x], checkin[x], checkout[x], 'check out', 'this is remark')
        status = BA.pgCursorCA_BN(statement, values)
        print(status)
        x += 1

def MSQLStoPostgres():
    statement = BNMSQLS.SQLSelectStatement('ATTENDANCE.dbo.HR_Employee',['Barcode', 'Name', 'identification_no', 'mobile_phone'])
    records = BNMSQLS.pgCursorBN_CA(statement)
    for record in records:
        print(record)

# ed_testing.public.hr_employee
# MSQLStoPostgres()


