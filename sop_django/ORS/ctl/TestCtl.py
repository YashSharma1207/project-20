from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import  Test
from service.service.TestService import TestService

class TestCtl(BaseCtl):


    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['firstName'] = requestForm['firstName']
        self.form['lastName'] = requestForm['lastName']
        self.form['userName'] = requestForm['userName']

    def model_to_form(self, obj):
        if (obj==None):
            return
        self.form['id'] = obj.id
        self.form['firstName'] = obj.firstName
        self.form['lastName'] = obj.lastName
        self.form['userName'] = obj.userName

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.firstName = self.form['firstName']
        obj.lastName = self.form['lastName']
        obj.userName = self.form['userName']
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['firstName'])):
            inputError['firstNamefirstName'] = "First Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['firstName'])):
                inputError['firstName'] = "First Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['lastName'])):
            inputError['lastName'] = "Last Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['lastName'])):
                inputError['lastName'] = "Last Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['userName'])):
            inputError['userName'] = "User Name can not be null"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(Test())
        self.get_service().save(r)
        self.form['messege'] = "Data Saved successfully"
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_service(self):
        return TestService()

    def get_template(self):
        return "Test.html"
