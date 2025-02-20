from time import sleep

from service.models import Position
from service.service.PositionService import PositionService
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..utility.DataValidator import DataValidator


class PositionCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['identifier'] = requestForm['identifier']
        self.form['designation'] = requestForm['designation']
        self.form['openingDate'] = requestForm['openingDate']
        self.form['requiredExperience'] = requestForm['requiredExperience']
        self.form['condition'] = requestForm['condition']

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['identifier'] = obj.identifier
        self.form['designation'] = obj.designation
        self.form['openingDate'] = obj.openingDate
        self.form['requiredExperience'] = obj.requiredExperience
        self.form['condition'] = obj.condition

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.identifier = self.form['identifier']
        obj.designation = self.form['designation']
        obj.openingDate = self.form['openingDate']
        obj.requiredExperience = self.form['requiredExperience']
        obj.condition = self.form['condition']

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['identifier'])):
            inputError['identifier'] = "Identifier can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['identifier'])):
                inputError['identifier'] = "Identifier contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['designation'])):
            inputError['designation'] = "Designation can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['designation'])):
                inputError['designation'] = "Identifier contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['openingDate'])):
            inputError['openingDate'] = "Opening Date can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['openingDate'])):
                inputError['openingDate'] = "Enter correct date"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['requiredExperience'])):
            inputError['requiredExperience'] = "Required Experience can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isInt(self.form['requiredExperience'])):
                inputError['requiredExperience'] = "Required Experience contains only number"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['condition'])):
            inputError['condition'] = "Condition can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['condition'])):
                inputError['condition'] = "Condition contains only letters"
                self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(Position())
        self.get_service().save(r)
        self.form['messege'] = "Data Saved successfully"
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_service(self):
        return PositionService()

    def get_template(self):
        return "Position.html"
