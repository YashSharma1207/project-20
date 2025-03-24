from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import Employee
from service.service.EmployeeService import EmployeeService
from ..utility.HTMLUtility import HTMLUtility


class EmployeeCtl(BaseCtl):
    def preload(self, request, params):

        self.form["gender"] = request.POST.get('gender', '')
        self.static_preload = {"Male": "Male", "Female": "Female"}

        self.form["preload"]["gender"] = HTMLUtility.get_list_from_dict(
            'gender',
            self.form["gender"],
            self.static_preload
        )

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['fullName'] = requestForm['fullName']
        self.form['userName'] = requestForm['userName']
        self.form['password'] = requestForm['password']
        self.form['gender'] = requestForm['gender']
        self.form['birthDate'] = requestForm['birthDate']
        self.form['contactNumber'] = requestForm['contactNumber']

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['fullName'] = obj.fullName
        self.form['userName'] = obj.userName
        self.form['password'] = obj.password
        self.form['gender'] = obj.gender
        self.form['birthDate'] = obj.birthDate
        self.form['contactNumber'] = obj.contactNumber

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.fullName = self.form['fullName']
        obj.userName = self.form['userName']
        obj.password = self.form['password']
        obj.gender = self.form['gender']
        obj.birthDate = self.form['birthDate']
        obj.contactNumber = self.form['contactNumber']
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['fullName'])):
            inputError['fullName'] = "full Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['fullName'])):
                inputError['fullName'] = "Full Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['userName'])):
            inputError['userName'] = "User Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['userName'])):
                inputError['userName'] = "User Name Contains only letter"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['password'])):
            inputError['password'] = "Password can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['gender'])):
            inputError['gender'] = "Gender can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['birthDate'])):
            inputError['birthDate'] = "Birth Date can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['contactNumber'])):
            inputError['contactNumber'] = "Contact Number can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ismobilecheck(self.form['contactNumber'])):
                inputError['contactNumber'] = "Contact Number Contains only Number"
                self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(Employee())
        self.get_service().save(r)
        self.form['messege'] = "Data Saved successfully"
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_service(self):
        return EmployeeService()

    def get_template(self):
        return "Employee.html"
