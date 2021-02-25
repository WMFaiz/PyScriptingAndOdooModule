import xmlrpc
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import sched, time
from datetime import datetime, date, timedelta
from threading import Timer
from xmlrpc import client as xmlrpclib
import urllib.request, urllib.parse, urllib.error

class Bossnet_Attendance:
    # Odoo Setup
    _url = "http://localhost:8069"
    _db = "odooDB"
    _username = "oa_faiz@exmple.com"
    _password_odoo = "admin"

    # PostgresSQL Setup
    _user = 'postgres'
    _password_postgres= 'admin'
    _host = '127.0.0.1'
    _database = 'bosnet'

    # Odoo Methods
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

    def createEmployee(self,uid,barcode):
        status = self._models().execute_kw(self._db, self._getLocalUID(), self._password_odoo, 'hr.employee', 'create', [{
            'name': uid,
            'barcode':barcode
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

    # PostgresSQL Setup
    def pgConnectionCheck(self):
        try:
            connection = psycopg2.connect(user=self._user, password=self._password_postgres, host=self._host, database=self._database)
            cursor = connection.cursor()
            print(connection.get_dsn_parameters(), "\n")
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            output = "You are connected to - ", record, "\n"
            return output
        except(Exception, psycopg2.Error) as error:
            output = "Error while connecting to PostgreSQL", error
            return output
        finally:
            if(connection):
                cursor.close()
                connection.close()
                output = "PostgreSQL connection is closed"
                return output

    def pgCreateStatement(self, table_name, columns):
        SQL_Statement = "INSERT INTO " + table_name + "("
        listDataLen = len(columns)
        assignValue = ''
        x = 0
        for data in columns:
            x += 1
            if(x < listDataLen):
                assignValue += '%s,'
                SQL_Statement += data + ', '
            elif(x >= listDataLen):
                assignValue += '%s'
                SQL_Statement += data +  ') VALUES (' + assignValue + ');'
        return SQL_Statement

    def pgSelectStatement(self, table_name, columns):
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

    def pgCursorCA_BN(self, statement, values):
        try:
            connection = psycopg2.connect(user=self._user, password=self._password_postgres, host=self._host, database=self._database)
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
            connection = psycopg2.connect(user=self._user, password=self._password_postgres, host=self._host, database=self._database)
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



BA = Bossnet_Attendance()
# statement = BA.pgCreateStatement('public.bossnet_ca_bn_table', ['id','barcode','check_in', 'check_out','direction', 'remark'])
print(BA._getCurrentDateOdoo())
# CA to BN
# statement = BA.pgCreateStatement('public.bossnet_ca_bn_table', ['id','barcode','check_in', 'check_out','direction', 'remark'])
# EmployeesID = BA.getEmployeesID()
# AttendancesID = BA.getAttendancesID()
# barcode = BA.getListEmployeesBarcode(EmployeesID)
# checkin = BA.getListAttendancesCheckIn(AttendancesID)
# checkout = BA.getListAttendancesCheckOut(AttendancesID)
# x = 0
# for employeeID in EmployeesID:
#     values = (employeeID, barcode[x], checkin[x], checkout[x], 'check out', 'this is remark')
#     status = BA.pgCursorCA_BN(statement, values)
#     print(status)
#     x += 1

# BN to CA
# statement = BA.pgSelectStatement('public.bossnet_bn_ca_table',['id','barcode','recorded_at','direction'])
# records = BA.pgCursorBN_CA(statement)
# for record in records:
#     pguid = record[0]
#     pgbarcode = record[1]
#     # pgdatetime = record[2] + timedelta(hours=8)
#     pgdatetime = record[2] + timedelta(hours=10)
#     pgdirection = record[3]
#     employeeBaseName = BA.getEmployee_baseName(pguid)
#     employeeBarcode = BA.getEmployeeBarcode(pguid)
#     if employeeBaseName != False and employeeBarcode == False:
#         EBNId = employeeBaseName[0]['id']
#         BA.modifyAttendance(EBNId, pgdatetime, pgdirection)
#     elif employeeBaseName == False and employeeBarcode != False:
#         empId = employeeBarcode[0]['id']
#         BA.modifyAttendance(empId, pgdatetime, pgdirection)
#     elif employeeBaseName == False and employeeBarcode == False:
#         empId = BA.createEmployee(pguid,pgbarcode)
#         BA.modifyAttendance(empId, pgdatetime, pgdirection)