from django.shortcuts import render, redirect

from ORS.ctl.BaseCtl import BaseCtl
from service.models import FavoriteList
from service.service.FavoriteListService import FavoriteListService


class FavoriteListListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form["product"] = requestForm.get("product", None)
        self.form["addedDate"] = requestForm.get("addedDate", None)
        self.form["ids"] = requestForm.getlist("ids", None)

    def display(self, request, params={}):
        FavoriteListListCtl.count = self.form['pageNo']
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        FavoriteListListCtl.count += 1
        self.form['pageNo'] = FavoriteListListCtl.count
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['LastId'] = FavoriteList.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def previous(self, request, params={}):
        FavoriteListListCtl.count -= 1
        self.form['pageNo']=FavoriteListListCtl.count
        records=self.get_service().search(self.form)
        self.page_list=records['data']
        res=render(request,self.get_template(),{'pageList':self.page_list,'form':self.form})
        return res

    def new(self, request, params={}):
        res=redirect("/FavoriteList/")
        return res

    def submit(self,request,params={}):
        FavoriteListListCtl.count=1
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
        return FavoriteListService()

    def get_template(self):
        return "FavoriteListList.html"

