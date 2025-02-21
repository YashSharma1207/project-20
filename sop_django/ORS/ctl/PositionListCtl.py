from .BaseCtl import BaseCtl
from django.shortcuts import render
from service.models import Position
from service.service.PositionService import PositionService


class PositionListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['designation'] = requestForm.get('designation', None)
        self.form['openingDate'] = requestForm.get('openingDate', None)
        self.form['requiredExperience'] = requestForm.get('requiredExperience', None)
        self.form['condition'] = requestForm.get('condition', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        PositionListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        # self.form['LastId'] = Position.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        PositionListCtl.count += 1
        self.form['pageNo'] = PositionListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Position.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def previous(self, request, params={}):
        PositionListCtl.count -= 1
        self.form['pageNo'] = PositionListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def submit(self, request, params={}):
        PositionListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['mesg'] = "No record found"
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = PositionListCtl.count
        if (bool(self.form['ids']) == False):
            self.form['error'] = True
            self.form['messege'] = "Please Select at least one Checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        else:
            for ids in self.form['ids']:
                record = self.get_service().search(self.form)
                self.page_list = record['data']

                id = int(ids)
                if (id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form['pageNo'] = 1
                        record = self.get_service().search(self.form)
                        self.page_list = record['data']
                        self.form['LastId'] = Position.objects.last().id
                        PositionListCtl.count = 1

                        self.form['error'] = False
                        self.form['messege'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
                    else:
                        self.form['error'] = True
                        self.form['messege'] = "DATA WAS NOT DELETED"
                        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    # Template html of CourseList page
    def get_template(self):
        return "PositionList.html"

    def get_service(self):
        return PositionService()
