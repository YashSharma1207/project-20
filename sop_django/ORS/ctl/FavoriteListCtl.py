from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import  FavoriteList
from service.service.FavoriteListService import FavoriteListService
from ..utility.HTMLUtility import HTMLUtility


class FavoriteListCtl(BaseCtl):
    def preload(self, request, params):

        self.form["product"] = request.POST.get('product', '')

        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.form["product"] = obj.product

        self.static_preload = {"Keybord": "Keybord", "Mouse": "Mouse", "Moniter": "Moniter", "CPU": "CPU"}

        self.form["preload"]["product"] = HTMLUtility.get_list_from_dict(
            'product',
            self.form["product"],
            self.static_preload
        )

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['product'] = requestForm['product']
        self.form['addedDate'] = requestForm['addedDate']

    def model_to_form(self, obj):
        if (obj==None):
            return
        self.form['id'] = obj.id
        self.form['product'] = obj.product
        self.form['addedDate'] = obj.addedDate

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.product = self.form['product']
        obj.addedDate = self.form['addedDate']
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['product'])):
            inputError['product'] = "Product can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['addedDate'])):
            inputError['addedDate'] = "Date can not be null"
            self.form['error'] = True
        else:
            if(DataValidator.isDate(self.form['addedDate'])):
                inputError['addedDate']="enter correct date"
                self.form['error']=True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(FavoriteList())
        self.get_service().save(r)
        self.form['messege'] = "Data Saved successfully"
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_service(self):
        return FavoriteListService()

    def get_template(self):
        return "FavoriteList.html"
