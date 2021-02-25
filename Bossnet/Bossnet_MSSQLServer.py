import pyodbc
import xmlrpc
import sched, time
from datetime import datetime, date, timedelta
from threading import Timer
from xmlrpc import client as xmlrpclib
import urllib.request, urllib.parse, urllib.error

class Bossnet_MSSQLServer:
    # Odoo Setup
    _url = "http://localhost:8069"
    _db = "odooDB"
    _username = "oa_faiz@exmple.com"
    _password_odoo = "admin"

    # # MS SQL Server
    # _server_MSSQLS = 'localhost,1433' 
    # _database_MSSQLS = 'SQLServer' 
    # _username_MSSQLS = 'sa' 
    # _password_MSSQLS = 'Admin123!@#' 

    # # Odoo Setup
    # _url = "http://192.168.41.161:8069"
    # _db = "ed_testing"
    # _username = "api"
    # _password_odoo = "Ckhu9yDJd7fF5ZRK"

    # MS SQL Server
    _server_MSSQLS = 'mobileappstest.eadeco.com.my,1433'
    _database_MSSQLS = 'ATTENDANCE'
    _username_MSSQLS = 'sa'
    _password_MSSQLS = 'bcs@1688'

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

    def getAttendanceStatus(self, uid):
        status = self._models().execute_kw(self._db,self._getLocalUID(),self._password_odoo, 'hr.employee', 'search', [], {'fields': ['id','attendance_state']})
        for currStatus in status:
            if uid == int(currStatus['id']):
                return currStatus['attendance_state']

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
            'conapp_passwd': identification_id
            # 'notification_type': 'inbox',
            # 'odoobot_state': 'not_initialized',
            # 'email': barcode+'@example.com'
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

    def MSSQLSCreateStatement(self, table_name, columns):
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

    def MSSQLSSelectStatement(self, table_name, columns):
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
# BNMSQLS.MSSQLS_Connection_Checker()

# CA to BN
# statement = BNMSQLS.MSSQLSCreateStatement('SQLServer.dbo.bossnet_ca_bn_table', ['id','barcode','check_in', 'check_out','direction', 'remark'])
# EmployeesID = BNMSQLS.getEmployeesID()
# AttendancesID = BNMSQLS.getAttendancesID()
# barcode = BNMSQLS.getListEmployeesBarcode(EmployeesID)
# checkin = BNMSQLS.getListAttendancesCheckIn(AttendancesID)
# checkout = BNMSQLS.getListAttendancesCheckOut(AttendancesID)
# print(statement)
# x = 0
# for employeeID in EmployeesID:
#     values = (employeeID, barcode[x], checkin[x], checkout[x], 'check out', 'this is remark')
#     status = BNMSQLS.MSSQLSCursorCA_BN(statement, values)
#     print(status)
#     x += 1


# BN to CA
# statement = BNMSQLS.MSSQLSSelectStatement('SQLServer.dbo.bossnet_bn_ca_table',['id','barcode','recorded_at','direction'])
# records = BNMSQLS.MSSQLSCursorBN_CA(statement)
# for record in records:
#     MSQLSuid = record[0]
#     MSQLSbarcode = record[1]
#     # MSSQLSdatetime = record[2] + str(timedelta(hours=8))
#     MSSQLSdatetime = record[2] + str(timedelta(hours=10))
#     MSSQLSdirection = record[3]
#     employeeBaseName = BNMSQLS.getEmployee_baseName(MSQLSuid)
#     employeeBarcode = BNMSQLS.getEmployeeBarcode(MSQLSuid)
#     if employeeBaseName != False and employeeBarcode == False:
#         EBNId = employeeBaseName[0]['id']
#         BNMSQLS.modifyAttendance(EBNId, MSSQLSdatetime, MSSQLSdirection)
#     elif employeeBaseName == False and employeeBarcode != False:
#         empId = employeeBarcode[0]['id']
#         BNMSQLS.modifyAttendance(empId, MSSQLSdatetime, MSSQLSdirection)
#     elif employeeBaseName == False and employeeBarcode == False:
#         empId = BNMSQLS.createEmployee(MSQLSuid,MSQLSbarcode)
#         BNMSQLS.modifyAttendance(empId, MSSQLSdatetime, MSSQLSdirection)

def create_employee():
    statement = BNMSQLS.MSSQLSSelectStatement('ATTENDANCE.dbo.HR_Employee',['Barcode', 'Name','identification_no', 'location_code'])
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
            # empId = BNMSQLS.createEmployee(userId, MSQLSname, MSQLSbarcode, MSQLSidentification_no)
            # print(empId)

create_employee()
