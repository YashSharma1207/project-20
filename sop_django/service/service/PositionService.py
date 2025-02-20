from ..models import Position
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class PositionService(BaseService):

    def search(self,params):
        pageNo = (params["pageNo"] - 1) * self.pageSize
        sql = "select * from sos_position where 1=1"
        val = params.get("identifier", None)
        if DataValidator.isNotNull(val):
            sql += " and identifier like '" + val + "%%'"
        sql += " limit %s, %s"
        cursor = connection.cursor()
        print("--------", sql, pageNo, self.pageSize)
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'identifier', 'designation', 'openingDate', 'requiredExperience', 'condition')
        res = {
            "data": [],
        }
        res["index"] = ((params['pageNo'] - 1) * self.pageSize) + 1
        for x in result:
            print({columnName[i]: x[i] for i, _ in enumerate(x)})
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Position
