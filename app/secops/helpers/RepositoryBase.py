from typing import List

from django.db import connection
from django.db import transaction
from django.utils.html import strip_tags

from secops.helpers.Exception import CustomException
from secops.helpers.Database import Database as DBHelper


class RepositoryBase:

    ####################################################################################################################
    # SINGLE TABLE. Public static methods
    ####################################################################################################################

    @staticmethod
    def get(table: str, select: str, where: List[tuple]) -> dict:
        idk = ["", "1"]
        idv = [0, 1]

        for i in range(0, 1):
            idk[i] = where[i][0]
            if where[i][2] == "string":
                idv[i] = where[i][1]
            else:
                idv[i] = int(where[i][1])

        if table and select:
            c = connection.cursor()

            try:
                c.execute(f"SELECT {select} FROM {table} WHERE {idk[0]} = %s AND {idk[1]} = %s", [ # simple qry for max 2 WHEREs.
                    idv[0], idv[1]
                ])

                o = DBHelper.asDict(c)[0]
            except IndexError:
                raise CustomException(status=404, payload=None)
            except Exception as e:
                raise CustomException(status=400, payload={"Backend": e.__str__()})
            finally:
                c.close()
        else:
            raise CustomException(status=404)

        return o



    @staticmethod
    def list(table: str, select: str, where: tuple = None, filter: tuple = None, limit: int = 0, orderBy: str = "id ASC") -> list:
        where = where or () # example: ("username", username, "string")
        filter = filter or ()

        if table and select:
            c = connection.cursor()

            try:
                if where and filter:
                    idk = where[0]
                    if where[2] == "string":
                        idv = where[1]
                    else:
                        idv = int(where[1])

                    if idk and idv:
                        if limit:
                            c.execute(f"SELECT {select} FROM {table} WHERE {idk} = %s AND {filter[0]} LIKE %s ORDER BY {orderBy} LIMIT %s", [
                                idv,
                                "%" + filter[1] + "%",
                                int(limit)
                            ])
                        else:
                            c.execute(f"SELECT {select} FROM {table} WHERE {idk} = %s AND {filter[0]} LIKE %s ORDER BY {orderBy}", [
                                idv,
                                "%" + filter[1] + "%",
                            ])
                    else:
                        raise CustomException(status=404)

                elif where:
                    idk = where[0]
                    if where[2] == "string":
                        idv = where[1]
                    else:
                        idv = int(where[1])

                    if idk and idv:
                        c.execute(f"SELECT {select} FROM {table} WHERE {idk} = %s", [
                            idv
                        ])
                    else:
                        raise CustomException(status=404)

                elif filter:
                    if limit:
                        c.execute(f"SELECT {select} FROM {table} WHERE {filter[0]} LIKE %s ORDER BY {orderBy} LIMIT %s", [
                            "%" + filter[1] + "%",
                            int(limit)
                        ])
                    else:
                        c.execute(f"SELECT {select} FROM {table} WHERE {filter[0]} LIKE %s ORDER BY {orderBy}", [
                            "%" + filter[1] + "%"
                        ])

                else:
                    c.execute(f"SELECT {select} FROM {table}")

                o = DBHelper.asDict(c)
            except Exception as e:
                raise CustomException(status=400, payload={"Backend": e.__str__()})
            finally:
                c.close()
        else:
            raise CustomException(status=404)

        return o



    @staticmethod
    def add(table: str, data: dict, allowHtmlFields: list = None, rejectFields: list = None) -> dict:
        allowHtmlFields = allowHtmlFields or []
        rejectFields = rejectFields or []

        s = ""
        keys = "("
        values = []

        if table and data:
            for f in rejectFields:
                if f in data:
                    del data[f]

            c = connection.cursor()

            # Build SQL query according to dict fields (only whitelisted fields pass).
            for k, v in data.items():
                s += "%s,"
                keys += k + ","

                if k not in allowHtmlFields:
                    if v is not None:
                        v = strip_tags(v) # no HTML allowed.

                values.append(v)

            keys = keys[:-1] + ")"

            try:
                with transaction.atomic():
                    c.execute(f"INSERT INTO {table} {keys} VALUES ({s[:-1]})", values) # user data are filtered by the serializer.
                    id = c.lastrowid

                    return {
                        "id": id
                    }
            except Exception as e:
                if e.__class__.__name__ == "IntegrityError" and e.args and e.args[0] and e.args[0] == 1062:
                    raise CustomException(status=409, payload={"Backend": f"Duplicated {table} or missing value"})
                elif e.__class__.__name__ == "IntegrityError" and e.args and e.args[0] and e.args[0] == 1364:
                    raise CustomException(status=409, payload={"Backend": f"Missing required value"})
                else:
                    raise CustomException(status=400, payload={"Backend": e.__str__()})
            finally:
                c.close()
        else:
            raise CustomException(status=400)



    @staticmethod
    def modify(table: str, id: int, data: dict, allowHtmlFields: list = None, rejectFields: list = None) -> None:
        allowHtmlFields = allowHtmlFields or []
        rejectFields = rejectFields or []

        sql = ""
        values = []

        id = int(id)
        if table and id and data:
            for f in rejectFields:
                if f in data:
                    del data[f]

            c = connection.cursor()

            # %s placeholders and values for SET.
            for k, v in data.items():
                sql += k + "=%s,"
                if k not in allowHtmlFields:
                    if v is not None:
                        v = strip_tags(v)
                values.append(v)

            values.append(id)

            try:
                c.execute(f"UPDATE {table} SET {sql[:-1]} WHERE id = %s", values) # user data are filtered by the serializer.
            except Exception as e:
                if e.__class__.__name__ == "IntegrityError" and e.args and e.args[0] and e.args[0] == 1062:
                    raise CustomException(status=400, payload={"Backend": f"Duplicated {table}"})
                elif e.__class__.__name__ == "IntegrityError" and e.args and e.args[0] and e.args[0] == 1452:
                    raise CustomException(status=400, payload={"Backend": "Incorrect values"})
                else:
                    raise CustomException(status=400, payload={"Backend": e.__str__()})
            finally:
                c.close()
        else:
            raise CustomException(status=400)



    @staticmethod
    def delete(table: str, id: int) -> None:
        id = int(id)
        if id:
            c = connection.cursor()

            try:
                c.execute(f"DELETE FROM {table} WHERE id = %s", [id])
            except Exception as e:
                raise CustomException(status=400, payload={"Backend": e.__str__()})
            finally:
                c.close()
        else:
            raise CustomException(status=404)
