from service.models import Staff
from service.service.StaffService import StaffService
from .BaseCtl import BaseCtl
from django.shortcuts import render

from ..utility.DataValidator import DataValidator


class StaffCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['fullName'] = requestForm['fullName']
        self.form['joiningDate'] = requestForm['joiningDate']
        self.form['division'] = requestForm['division']
        self.form['previousEmployer'] = requestForm['previousEmployer']

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['fullName'] = obj.fullName
        self.form['joiningDate'] = obj.joiningDate
        self.form['division'] = obj.division
        self.form['previousEmployer'] = obj.previousEmployer

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.fullName = self.form['fullName']
        obj.joiningDate = self.form['joiningDate']
        obj.division = self.form['division']
        obj.previousEmployer = self.form['previousEmployer']
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['fullName'])):
            inputError['fullName'] = "full Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['fullName'])):
                inputError['fullName'] = "full contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['joiningDate'])):
            inputError['joiningDate'] = "Date can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['joiningDate'])):
                inputError['joiningDate'] = "enter correct date"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['division'])):
            inputError['division'] = "division can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['division'])):
                inputError['division'] = "division contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['previousEmployer'])):
            inputError['previousEmployer'] = "previousEmployer can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['previousEmployer'])):
                inputError['previousEmployer'] = "previousEmployer contains only letters"
                self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(Staff())
        self.get_service().save(r)
        self.form['messege'] = "Data Saved successfully"
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_service(self):
        return StaffService()

    def get_template(self):
        return "Staff.html"
