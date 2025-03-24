from django.shortcuts import render, redirect

from ORS.ctl.BaseCtl import BaseCtl
from service.models import Staff
from service.service.EmployeeService import EmployeeService
from service.service.StaffService import StaffService


class EmployeeListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form["fullName"] = requestForm.get("fullName", None)
        self.form["userName"] = requestForm.get("userName", None)
        self.form["password"] = requestForm.get("password", None)
        self.form["gender"] = requestForm.get("gender", None)
        self.form["birthDate"] = requestForm.get("birthDate", None)
        self.form["contactNumber"] = requestForm.get("contactNumber", None)
        self.form["ids"] = requestForm.getlist("ids", None)

    def display(self, request, params={}):
        EmployeeListCtl.count = self.form['pageNo']
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        EmployeeListCtl.count += 1
        self.form['pageNo'] = EmployeeListCtl.count
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['LastId'] = Staff.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def previous(self, request, params={}):
        EmployeeListCtl.count -= 1
        self.form['pageNo']=EmployeeListCtl.count
        records=self.get_service().search(self.form)
        self.page_list=records['data']
        res=render(request,self.get_template(),{'pageList':self.page_list,'form':self.form})
        return res

    def new(self, request, params={}):
        res=redirect("/Employee/")
        return res

    def submit(self,request,params={}):
        EmployeeListCtl.count=1
        records=self.get_service().search(self.form)
        self.page_list=records['data']
        if self.page_list==[]:
            self.form['mesg']="No record found"
        res=render(request,self.get_template(),{'pageList':self.page_list,'form':self.form})
        return res

    def deleteRecord(self,request,params={}):
        if not self.form['ids']:
            self.form['error']=True
            self.form['mesg']="Please select at least one checkbox"
        else:
            for id in self.form['ids']:
                id = int(id)
                record = self.get_service().get(id)
                if record:
                    self.get_service().delete(id)
                    self.form['mesg'] = "Data has been deleted successfully"
                else:
                    self.form['error'] = True
                    self.form['mesg'] = "Data is not deleted"
            self.form['pageNo'] = 1
            records = self.get_service().search(self.form)
            self.page_list = records['data']
            # self.form['lastId'] = Attribute.objects.last().id
            return render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})

    def get_service(self):
        return EmployeeService()

    def get_template(self):
        return "EmployeeList.html"
