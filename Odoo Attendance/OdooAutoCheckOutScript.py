import xmlrpc
import sched, time
from datetime import datetime, date, timedelta
from threading import Timer
from xmlrpc import client as xmlrpclib
import urllib.request, urllib.parse, urllib.error

class OdooAutoCheckOutScript:
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
        return False

    def CheckEmployeeCheckInAndCheckOut(self):
        print("CheckEmployeeCheckInAndCheckOut run methods")
        status = self._models().execute_kw(self._db,self._getLocalUID(),self._password, 'hr.attendance', 'search_read', [], {'fields': ['employee_id','check_out', 'check_in']})
        for currStatus in status:
            if currStatus["check_in"] != False and currStatus["check_out"] == False:
                uid = int(currStatus['employee_id'][0])
                CurrentDateTime = str(self._getCurrentDateOdoo().split()[0]) + " 15:59:59"
                self._models().execute_kw(self._db, self._getLocalUID(), self._password, 'hr.attendance', 'write', [self.getEmployeeAttendanceUID(uid),{
                    'check_out': CurrentDateTime
                }])

def AutoCheckOut():
    print("AutoCheckOut run methods")
    OA = OdooAutoCheckOutScript()
    OA.CheckEmployeeCheckInAndCheckOut()


while True:
    DateTime = datetime.now()
    x = DateTime.replace(day=DateTime.day, hour=8, minute=0, second=0, microsecond=0)
    y = DateTime.replace(day=DateTime.day, hour=23, minute=59,second=59,microsecond=0)
    delta_t = y - x
    secs = delta_t.total_seconds()
    t = Timer(secs, AutoCheckOut)
    t.start()