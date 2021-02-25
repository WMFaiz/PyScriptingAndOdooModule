import xmlrpc
import psycopg2
import pyodbc
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

    # MS SQL Server
    _server_MSSQLS = 'mobileappstest.eadeco.com.my,1433'
    _database_MSSQLS = 'ATTENDANCE'
    _username_MSSQLS = 'sa'
    _password_MSSQLS = 'bcs@1688'

    # # MS SQL Server
    # _server_MSSQLS = 'localhost,1433' 
    # _database_MSSQLS = 'SQLServer' 
    # _username_MSSQLS = 'sa' 
    # _password_MSSQLS = 'Admin123!@#' 

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


BNMSQLS = Bossnet_Attendance()
print(BNMSQLS.test())

# -----DB Info-------
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

# [('AEON AU2', 'AEON AMPANG UTARA 2'), ('AEON BANDAR DATO ONN JB', 'AEON BANDAR DATO ONN'), ('AEON BDR UTAMA', 'AEON BANDAR UTAMA'), ('AEON BIG AMPANG', 'AEON BIG AMPANG'), ('AEON BIG BATU PAHAT', 'AEON BIG BATU PAHAT'), ('AEON BIG FARLIM', 'AEON BIG FALIM IPOH'), ('AEON BIG JAYA ONE', 'AEON BIG JAYA ONE'), ('AEON BIG KEPONG', 'AEON BIG KEPONG'), ('AEON BIG KLANG', 'AEON BIG KLANG'), ('AEON BIG KLUANG', 'AEON BIG KLUANG'), ('AEON BIG KUANTAN', 'AEON BIG KUANTAN'), ('AEON BIG MID VALLEY', 'AEON BIG MID VALLEY'), ('AEON BIG PRAI', 'AEON BIG PENANG PRAI'), ('AEON BIG PUCHONG UTAMA', 'AEON BIG PUCHONG UTAMA'), ('AEON BIG PUTRA JAYA', 'AEON BIG PUTRAJAYA'), ('AEON BIG SHAH ALAM', 'AEON BIG SHAH ALAM'), ('AEON BIG SRI PETALIN', 'AEON BIG SRI PETALING'), ('AEON BIG SUBANG', 'AEON BIG SUBANG JAYA'), ('AEON BIG TUN HUSSEIN', 'AEON BIG T.HUSSEIN ONN'), ('AEON BIG W/MAJU', 'AEON BIG WANGSA MAJU'), ('AEON BUKIT INDAH', 'AEON BUKIT INDAH'), ('AEON BUKIT MERTAJAM', 'AEON BUKIT MERTAJAM'), ('AEON BUKIT TINGGI', 'AEON BUKIT TINGGI'), ('AEON CHERAS SELATAN', 'AEON CHERAS SELATAN'), ('AEON IOI PUCHONG', 'AEON IOI MALL PUCHONG'), ('AEON IPOH', 'AEON IPOH'), ('AEON KLANG', 'AEON BANDAR BARU KLANG'), ('AEON KLEBANG', 'AEON IPOH KLEBANG'), ('AEON KOTA BAHRU', 'AEON KOTA BHARU'), ('AEON KUCHING', 'AEON KUCHING'), ('AEON KULAI JAYA', 'AEON KULAI JAYA'), ('AEON MALACCA 2', 'AEON BANDARAYA MELAKA'), ('AEON MALURI', 'AEON TAMAN MALURI'), ('AEON MELAKA', 'AEON MELAKA'), ('AEON METRO PRIMA', 'AEON METRO PRIMA'), ('AEON MID VALLEY', 'AEON MID VALLEY'), ('AEON NILAI MALL', 'AEON NILAI MALL'), ('AEON PERMAS JAYA JB', 'AEON PERMAS JAYA'), ('AEON QUEENSBAY(PEN)', 'AEON QUEENSBAY'), ('AEON RAWANG', 'AEON RAWANG'), ('AEON SEREMBAN 2', 'AEON SEREMBAN 2'), ('AEON SHAH ALAM', 'AEON SHAH ALAM'), ('AEON SRI MANJUNG', 'AEON SRI MANJUNG'), ('AEON STATION 18', 'AEON IPOH STATION 18'), ('AEON SUNWAY PYRAMID', 'AEON BANDAR SUNWAY'), ('AEON TAIPING', 'AEON TAIPING'), ('AEON TAMAN EQUINE', 'AEON TAMAN EQUINE'), ('AEON TEBRAU CITY JB', 'AEON TEBRAU CITY'), ('AEON TMN UNIVERSITI', 'AEON TAMAN UNIVERSITI'), ('AEON WANGSA MAJU', 'AEON WANGSA MAJU'), ('BILLION BAHAU', 'BILLION BAHAU'), ('BILLION BANGI', 'BILLION B.B.BANGI'), ('BILLION KOTA BAHRU', 'BILLION KOTA BARU'), ('BILLION LANGKAWI', 'BILLION LANGKAWI'), ('BILLION PARIT BUNTAR', 'BILLION PARIT BUNTAR'), ('BILLION PORT DICKSON', 'BILLION PORT DICKSON'), ('BILLION SEBERANG JAY', 'BILLION SEBERANG JAYA'), ('BILLION SEGAMAT', 'BILLION SEGAMAT'), ('BILLION SEMENYIH', 'BILLION SEMENYIH'), ('BOULEVARD KUCHING', 'BOULEVARD KUCHING'), ('CT DEPTMTL STORES KK', 'CT DEPARTMENT STORE'), ('FARLEY BINTULU SWK', 'FARLEY BINTULU'), ('FARLEY SIBU', 'FARLEY SIBU'), ('GAMA PENANG', 'GAMA SUPERMARKET'), ('GIANT BANDAR KINRARA', 'GIANT BANDAR KINRARA'), ('GIANT BATU CAVES', 'GCH RETAIL BATU CAVES'), ('GIANT BAYAN BARU', 'GCH RETAIL BAYAN BARU'), ('GIANT HYPERMARKET SO', 'GCH RETAIL SOUTHERN CITY'), ('GIANT KELANA JAYA', 'GCH RETAIL KELANA JAYA (HYPER)'), ('GIANT KLANG', 'GCH RETAIL KLANG'), ('GIANT KOTA DAMANSARA', 'GCH RETAIL KOTA DAMANSARA'), ('GIANT KUANTAN', 'GCH RETAIL KUANTAN'), ('GIANT MESRAMALL KUAN', 'GIANT MESRAMALL KUANTAN'), ('GIANT PLENTONG', 'GCH RETAIL PLENTONG JB'), ('GIANT PUTRA HEIGHTS', 'GCH RETAIL PUTRA HEIGHTS'), ('GIANT SENAWANG', 'GCH RETAIL SENAWANG'), ('GIANT SETAPAK', 'GCH RETAIL SETAPAK'), ('GIANT SHAH ALAM STADIUM', 'GCH RETAIL SHAH ALAM STADIUM'), ('GIANT TAMPOI (JB)', 'GCH RETAIL TAMPOI'), ('GIANT TERENGGANU', 'GIANT TERENGGANU'), ('GIANT USJ', 'GCH RETAIL SUBANG JAYA'), ('HANIFFA KL', 'HANIFFA'), ('HOMEPRO IOI CITY MALL', 'HOMEPRO IOI MALL'), ('HOMEPRO JB', 'HOMEPRO JB'), ('HOMEPRO MELAKA', 'HOMEPRO MELAKA'), ('HOMEPRO PENANG', 'HOMEPRO PENANG'), ('HOMEPRO ST 18', 'HOMEPRO IPOH'), ('HOMEPRO SUMMIT USJ', 'HOMEPRO SUMMIT'), ('HOOGA GP', 'HOOGA GURNEY PLAZA'), ('HOOGA ONE UTAMA', 'HOOGA ONE UTAMA'), ('HOOGA SOUTHKEY', 'HOOGA SOUTHKEY'), ('HOOGA SUNWAY PYRAMID', 'HOOGA SUNWAY PYRAMID'), ('HOOGA THE STARLING', 'HOOGA THE STARLING'), ('LQ MID VALLEY', 'LIVING QUARTERS MID VALLEY'), ('LQ SURIA SABAH', 'LIVING QUARTERS SURIA KK'), ('MYDIN USJ', 'MYDIN SUBANG JAYA USJ'), ('NONE', 'NONE'), ('NSK SEREMBAN 2', 'NSK SEREMBAN 2'), ('PACIFIC BATU PAHAT', 'PACIFIC BATU PAHAT MALL'), ('PACIFIC HM ALOR SETA', 'PACIFIC AS MALL TANDOP'), ('PACIFIC HYPERMKT PRA', 'PACIFIC PRAI'), ('PACIFIC HYPERMRKT KTCC MALL', 'PACIFIC HYPERMRKT KUALA TERENGGANU'), ('PACIFIC KB', 'PACIFIC KOTA BAHRU'), ('PACIFIC KLUANG', 'PACIFIC KLUANG'), ('PACIFIC MENTAKAB', 'PACIFIC MENTAKAB STAR MALL'), ('PACIFIC STAR PARADE', 'PACIFIC STAR PARADE AS'), ('PARK. RIA SG PETANI', 'PARKSON SG PETANI'), ('PARKSON  1 BORNEO', 'PARKSON 1 BORNEO KK'), ('PARKSON 1ST AVENUE', 'PARKSON 1ST AVENUE PENANG'), ('PARKSON AKTIF OUG', 'PARKSON OUG'), ('PARKSON ALAMANDA', 'PARKSON ALAMANDA'), ('PARKSON AMAN CENTRAL', 'PARKSON AMAN CENTRAL'), ('PARKSON ANGSANA MALL', 'PARKSON ANGSANA MALL'), ('PARKSON BANDAR UTAMA', 'PARKSON U2'), ('PARKSON BATU PAHAT', 'PARKSON BATU PAHAT'), ('PARKSON DAMEN SUBANG', 'PARKSON DAMEN'), ('PARKSON EAST COAST M', 'PARKSON EAST COAST MALL'), ('PARKSON EVO MALL', 'PARKSON EVO MALL'), ('PARKSON FESTIVAL CIT', 'PARKSON FESTIVAL CITY MALL'), ('PARKSON GURNEY PLAZA', 'PARKSON GURNEY'), ('PARKSON HOLIDAY PLAZ', 'PARKSON HOLIDAY JAYA'), ('PARKSON IMAGO', 'PARKSON IMAGO KK'), ('PARKSON IOI CITY MALL', 'PARKSON IOI CITY MALL'), ('PARKSON IPOH', 'PARKSON IPOH'), ('PARKSON KAJANG', 'PARKSON KAJANG'), ('PARKSON KLANG', 'PARKSON KLANG'), ('PARKSON KLUANG', 'PARKSON KLUANG'), ('PARKSON KOTA BHARU', 'PARKSON KOTA BHARU'), ('PARKSON KUANTAN CITY MALL', 'PARKSON KUANTAN CITY MALL'), ('PARKSON LABUAN', 'PARKSON LABUAN'), ('PARKSON MAHKOTA PARA', 'PARKSON MELAKA'), ('PARKSON MERDEKA PLAZ', 'PARKSON MERDEKA PLAZA'), ('PARKSON MIRI', 'PARKSON MIRI'), ('PARKSON NU SENTRAL', 'PARKSON NU SENTRAL'), ('PARKSON PARADIGM MALL', 'PARKSON PARADIGM MALL'), ('PARKSON PAVILION', 'PARKSON PAVILION'), ('PARKSON RIA RAWANG', 'PARKSON RAWANG'), ('PARKSON RIA SIBU', 'PARKSON SIBU'), ('PARKSON SELAYANG', 'PARKSON SELAYANG'), ('PARKSON SEREMBAN PRI', 'PARKSON SEREMBAN PRIMA'), ('PARKSON SETIA CITY M', 'PARKSON SETIA CITY MALL'), ('PARKSON SUBANG', 'PARKSON SUBANG PARADE'), ('PARKSON SUNWAY', 'PARKSON SUNWAY PYRAMID'), ('PARKSON SUNWAY VELOCITY MALL', 'PARKSON SUNWAY VELOCITY'), ('PARKSON TERMINAL 1', 'PARKSON TERMINAL 1'), ('PARKSON THE SPRING', 'PARKSON THE SPRING'), ('PARKSON THE SPRING BINTULU', 'PARKSON THE SPRING BINTULU'), ('PARKSON VIVO CITY,KCH', 'PARKSON VIVA CITY KUCHING'), ('PARKWELL LIKAS', 'PARKWELL LIKAS'), ('PASARAYA TIMOR PASIR MAS', 'PASARAYA TIMOR PASIR MAS KUALA KRAI'), ('PREMEIR DEPT STORE SIBU', 'PREMIER DEPT STORE SARAWAK HOUSE'), ('PRK SUNWAY CARNIVAL', 'PARKSON SUNWAY CARNIVAL'), ('ROBINSON', 'ROBINSON&CO MID VALLEY'), ('ROBINSON AND CO FOUR SEASON', 'ROBINSON AND  CO FOUR SEASON'), ('SALES AND OPERATION', 'SALES & OPERATION'), ('SERVAY HYPER TAWAU', 'SERVAY HYPERMARKET TAWAU'), ('SERVAY HYPERMARKET S', 'SERVAY-SANDAKAN'), ('SERVAY HYPERMKT MIRI', 'SERVAY MIRI'), ('SERVAY INANAM', 'SERVAY INANAM'), ('SERVAY JAYA SUNGAI TAJONG', 'SERVAY JAYA SUPERMARKET  SDN BHD (SUNGAI TAJONG)'), ('SERVAY KENINGAU', 'SERVAY JAYA KENINGAU'), ('SERVAY LAHAD DATU', 'SERVAY LAHAD DATU'), ('SERVAY PENAMPANG', 'SERVAY PENAMPANG'), ('SERVAY PUTANTAN', 'SERVAY-PUTATAN'), ('SERVAY SUPER SANDAKAN 4MILE', 'SERVAY SANDAKAN 4 MILE'), ('SOGO I-CITY SHAH ALAM', 'SOGO I-CITY SHAH ALAM'), ('SOGO KL', 'SOGO KL'), ('SOGO SOUTHKEY JOHOR', 'SOGO SOUTHKEY JOHOR'), ('ST_OFFICE', 'ST_OFFICE'), ('ST_SAR', 'ST_SAR'), ('ST_SAS', 'ST_SAS'), ('SUNSHINE BERTAM', 'SUNSHINE BERTAM'), ('SUNSHINE FALIM', 'SUNSHINE FARLIM SHOP MALL'), ('SUNSHINE SQUARE', 'SUNSHINE SQUARE'), ('TEOH SOON HUAT/ LANG', 'TEOW SOON HUAT DUTY FREE'), ('TESCO AMPANG', 'TESCO AMPANG'), ('TESCO ARA DAMANSARA', 'TESCO ARA DAMANSARA'), ('TESCO BRD BKT PUCHONG', 'TESCO BRD BKT PUCHONG'), ('TESCO BUKIT BERUNTUNG', 'TESCO BUKIT BERUNTUNG'), ('TESCO BUKIT INDAH', 'TESCO BUKIT INDAH'), ('TESCO BUKIT MERTAJAM', 'TESCO BUKIT MERTAJAM'), ('TESCO EXTRA CHERAS', 'TESCO EXTRA CHERAS'), ('TESCO EXTRA IPOH', 'TESCO IPOH'), ('TESCO EXTRA PENANG', 'TESCO EXTRA PENANG'), ('TESCO EXTRA SELAYANG', 'TESCO EXTRA SELAYANG'), ('TESCO EXTRA SEREMBAN', 'TESCO EXTRA SEREMBAN 2'), ('TESCO IPOH', 'TESCO EXTRA IPOH'), ('TESCO JENJAROM', 'TESCO JENJAROM'), ('TESCO KAJANG', 'TESCO KAJANG'), ('TESCO KAMPAR', 'TESCO KAMPAR'), ('TESCO KEPONG', 'TESCO KEPONG'), ('TESCO KLANG', 'TESCO KLANG'), ('TESCO KOTA BAHRU', 'TESCO KOTA BHARU'), ('TESCO KUALA SELANGOR', 'TESCO KUALA SELANGOR'), ('TESCO KULAI JB', 'TESCO KULAI'), ('TESCO KULIM', 'TESCO KULIM'), ('TESCO MELAKA', 'TESCO MELAKA'), ('TESCO MELAKA CHENG', 'TESCO MELAKA CHENG'), ('TESCO MERGONG/ ALOR', 'TESCO MERGONG'), ('TESCO MUTIARA', 'TESCO MUTIARA'), ('TESCO MUTIARA RINI', 'TESCO MUTIARA RINI'), ('TESCO NILAI', 'TESCO PUTRA NILAI'), ('TESCO PENANG', 'TESCO PENANG'), ('TESCO PUCHONG', 'TESCO PUCHONG'), ('TESCO RAWANG', 'TESCO RAWANG'), ('TESCO SEBERANG JAYA', 'TESCO EXTRA SEBERANG JAYA'), ('TESCO SEMENYIH', 'TESCO SEMENYIH'), ('TESCO SEREMBAN JAYA', 'TESCO SEREMBAN JAYA'), ('TESCO SETIA ALAM', 'TESCO SETIA ALAM'), ('TESCO SETIAWAN', 'TESCO SITIAWAN'), ('TESCO SG PETANI', 'TESCO SUNGAI PETANI'), ('TESCO SG PETANI SELATAN', 'TESCO SG PETANI SELATAN'), ('TESCO SHAH ALAM', 'TESCO SHAH ALAM'), ('TESCO SRI ALAM', 'TESCO SERI ALAM'), ('TESCO STATION 18', 'TESCO IPOH SOUTH STATION 18'), ('TESCO TAIPING', 'TESCO TAIPING'), ('TESCO TANJUNG PINANG', 'TESCO TANJUNG PENANG'), ('THE STORE KAMUNTING', 'THE STORE TPG KAMUNTING'), ('THE STORE KUANTAN', 'THE STORE KUANTAN PARADE'), ('THE STORE MUAR(WETEX', 'THE STORE MUAR WETEX PARADE'), ('THE STORE SEREMBAN', 'THE STORE SEREMBAN JLN TM'), ('THE STORE TELUK INTA', 'THE STORE TELUK INTAN'), ('THE STORE TM TUN AMI', 'THE STORE JB TMN TUN AMINAH'), ('UCHI FESTIVAL CITY MALL', 'AKE UCHI FESTIVAL CITY'), ('UCHI PARADIGM MALL JB', 'AKE UCHI JB PARADIGM MALL'), ('UCHI SUNWAY VELOCITY MALL', 'AKE UCHI SUNWAY VELOCITY'), ('UCHI TEBRAU CITY JB', 'AKE UCHI AEON TEBRAU CITY')]

# -----Code Here-----
# print(BNMSQLS.test2())

# CA to BN
def CAtoBN():
    statement = BNMSQLS.MSSQLSCreateStatement('ATTENDANCE.dbo.bossnet_ca_bn_table', ['id','barcode','check_in', 'check_out','direction', 'remark'])
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
    statement = BNMSQLS.MSSQLSSelectStatement('ATTENDANCE.dbo.HR_Employee',['Barcode', 'Name','identification_no', 'location_code'])
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

# create_User_Employee()