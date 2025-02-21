from django.shortcuts import render
from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.DataValidator import DataValidator
from service.models import Position
from service.service.PositionService import PositionService


class PositionCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['designation'] = requestForm['designation']
        self.form['openingDate'] = requestForm['openingDate']
        self.form['requiredExperience'] = requestForm['requiredExperience']
        self.form['condition'] = requestForm['condition']

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['designation'] = obj.designation
        self.form['openingDate'] = obj.openingDate
        self.form['requiredExperience'] = obj.requiredExperience
        self.form['condition'] = obj.condition

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.designation = self.form['designation']
        obj.openingDate = self.form['openingDate']
        obj.requiredExperience = self.form['requiredExperience']
        obj.condition = self.form['condition']
        return obj


    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['designation'])):
            inputError['designation'] = "Designation is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['designation'])):
                inputError['designation'] = 'Designation is Checked'
                self.form['error'] = True

        if (DataValidator.isNull(self.form['openingDate'])):
            inputError['openingDate'] = "openingDate is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['openingDate'])):
                inputError['openingDate'] = "openingDate is checked YYYY-MM-DD"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['requiredExperience'])):
            inputError['requiredExperience'] = "requiredExperience is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isNull(self.form['requiredExperience'])):
                inputError['requiredExperience'] = "requiredExperience is Check"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['condition'])):
            inputError['condition'] = "condition is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['condition'])):
                inputError['condition'] = "condition is Required"
                self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.model_to_form(obj)
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(Position())
        self.get_service().save(r)
        self.form['messege'] = "Data Successfully Saved"
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_service(self):
        return PositionService()

    def get_template(self):
        return "Position.html"
