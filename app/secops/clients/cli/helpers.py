import json
import logging
import functools


########################################################################################################################
# errorHandler
########################################################################################################################

def errorHandler(method):
    @functools.wraps(method)
    def w(*methodArgs, **methodKwargs):
        response = method(*methodArgs, **methodKwargs) # run the wrapped method.

        if response.status_code in (200, 201, 202, 204, 206):
            try:
                responsePayload = response.json()
            except Exception:
                responsePayload = {}

            return responsePayload.get("data", None)
        else:
            raise CustomException(
                status=response.status_code,
                payload={"error": response.json().get("error", "unknown")}
            )

    return w



########################################################################################################################
# Util
########################################################################################################################

class Util:
    @staticmethod
    def baseLog(o: any, title: str = "") -> None:
        log = logging.getLogger("django")
        if title:
            if title == "_":
                for j in range(120):
                    title = title + "_"

        if title:
            log.debug(title)

        log.debug(o)



    @staticmethod
    def log(data: object, msg: str = "") -> None:
        try:
            if data:
                Util.baseLog(data, msg)
                print(msg, str(json.dumps(data, indent=4)))
        except Exception:
            print(msg, str(data))



    @staticmethod
    def out(msg: str) -> None:
        try:
            Util.baseLog(msg)
            print(msg)
        except Exception:
            pass



########################################################################################################################
# CustomException
########################################################################################################################

class CustomException(Exception):
    def __init__(self, status: int, payload: dict = None):
        payload = payload or {}

        self.status = int(status)
        self.payload = payload

    def status(self):
        return self.status

    def __str__(self):
        if self.payload:
            o = str(self.status) + ", " + str(self.payload)
        else:
            o = str(self.status)

        return o
