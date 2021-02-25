import xmlrpc
from datetime import datetime, date
from xmlrpc import client as xmlrpclib
import urllib.request, urllib.parse, urllib.error

class OdooAttendanceXAPI:
    _url = "http://localhost:8069"
    _db = "odooDB"
    _username = "oa_faiz@exmple.com"
    _password = "admin"

    def _common(self):
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self._url))
        return common

    def _models(self):
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self._url))
        return models

    def _getLocalUID(self):
        uid = self._common().authenticate(self._db,self._username, self._password, {})
        return uid

    def _getOnlineUID(self):
        info = xmlrpc.client.ServerProxy(self._url).start()
        self._url, self._db, self._username, self._password = \
            info['host'], info['database'], info['user'], info['password']

    def _getCurrentDatePython(self):
        now = datetime.now()
        curDate = now.strftime("%Y/%m/%d %H:%M:%S")
        return curDate

    def _getCurrentDateOdoo(self):
        DateTime = self._models().execute_kw(self._db, self._getLocalUID(),self._password, 'hr.attendance', 'search_read', [], {'fields': ['create_date'], 'limit':1})
        getDate = DateTime[0]['create_date']
        return getDate

    def checkPrivilege(self, fields):
        privilege = self._models().execute_kw(self._db, self._getLocalUID(), self._password, fields, 'check_access_rights', ['read'], {'raise_exception': False})
        return privilege

    def getFirstEmployeeId(self):
        employees = self._models().execute_kw(self._db,self._getLocalUID(),self._password, 'hr.employee', 'search_read', [], {'fields': ['id'], 'limit': 1})
        empName = employees[0]['id']
        return empName

    def getEmployee_baseId(self,uid):
        employees = self._models().execute_kw(self._db,self._getLocalUID(),self._password, 'hr.employee', 'search_read', [])
        for employee in employees:
            if uid == int(employee['id']):
                return employee

    def getEmployee_baseName(self,name):
        employees = self._models().execute_kw(self._db,self._getLocalUID(),self._password, 'hr.employee', 'search_read', [])
        for employee in employees:
            if name in employee['display_name']:
                return employee

    def getEmployee_all(self):
        employees = self._models().execute_kw(self._db,self._getLocalUID(),self._password, 'hr.employee', 'search_read', [])
        return employees

    def getEmployeeCheckInStatus(self, uid):
        status = self._models().execute_kw(self._db,self._getLocalUID(),self._password, 'hr.attendance', 'search_read', [], {'fields': ['employee_id','check_out', 'check_in']})
        for currStatus in status:
            if uid == int(currStatus['employee_id'][0]):
                OdooCheckInDate = currStatus['check_in'].split()[0].split('-')
                currDate = self._getCurrentDateOdoo().split()[0].split('-')
                DateChecker = bool(OdooCheckInDate == currDate)
                if DateChecker == True:
                    if not currStatus['check_out']:
                        return True
                    else:
                        return False
        return None
    
    def getAttendanceStatus(self, uid):
        status = self._models().execute_kw(self._db,self._getLocalUID(),self._password, 'hr.employee', 'search', [], {'fields': ['id','attendance_state']})
        for currStatus in status:
            if uid == int(currStatus['id']):
                return currStatus['attendance_state']

    def getEmployeeAttendanceUID(self, uid):
        status = self._models().execute_kw(self._db,self._getLocalUID(),self._password, 'hr.attendance', 'search_read', [], {'fields': ['employee_id','check_out', 'check_in', 'id']})
        for currStatus in status:
            if uid == int(currStatus['employee_id'][0]):
                return currStatus['id']
        return 0

    def checkIn(self,uid):
        if self.getEmployeeCheckInStatus(uid) == False or self.getEmployeeCheckInStatus(uid) == None:
            self._models().execute_kw(self._db, self._getLocalUID(), self._password, 'hr.attendance', 'create', [{
                'employee_id': uid, 
                'check_in': self._getCurrentDateOdoo()
            }])
            return 'Successfully Check In'
        else:
            return 'Already Check In'

    def checkOut(self,uid):
        if self.getEmployeeCheckInStatus(uid) == True or self.getEmployeeCheckInStatus(uid) == None:
            self._models().execute_kw(self._db, self._getLocalUID(), self._password, 'hr.attendance', 'write', [self.getEmployeeAttendanceUID(uid),{
                'check_out': self._getCurrentDateOdoo()
            }])
            return 'Successfully Check Out'
        else:
            return 'Already Check Out'


# BA = OdooAttendanceXAPI()
# print(BA._getCurrentDateOdoo())