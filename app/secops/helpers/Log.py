import json
import logging
import traceback


class Log:
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    @staticmethod
    def log(o: any, title: str = "", logLevel: int = DEBUG) -> None:
        # If a title is provided, print it.
        # If title is "_" print a line of 80 _ characters.
        if title:
            if "_" in title:
                for j in range(80):
                    title = title + "_"
            Log.__debug(title, logLevel)

        # If it's not a string, try to convert it to a string.
        try:
            if not isinstance(o, str):
                Log.__debug(json.dumps(o), logLevel)
            else:
                Log.__debug(o, logLevel)
        except Exception:
            Log.__debug(o, Log.ERROR)

        if title:
            title = ""
            for j in range(81):
                title = title + "_"
            Log.__debug(title, logLevel)



    @staticmethod
    def dump(o: any) -> None:
        import re

        oOut = dict()
        oVars = vars(o)
        oDir = dir(o)

        for i, v in enumerate(oDir):
            if v in oVars:
                oOut[v] = oVars[v]
            else:
                if not re.search("^__(.*)__$", str(v)):
                    oOut[v] = getattr(o, v)

        Log.__debug(oOut)



    @staticmethod
    def logException(e: Exception) -> None:
        # Logs the stack trace information and the raw output if any.
        Log.log(traceback.format_exc(), '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Exception !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', Log.ERROR)



    @staticmethod
    def actionLog(o: any, user: dict = None) -> None:
        user = user or {}

        try:
            if "username" in user:
                Log.__debug("[" + user['username'] + "] " + o)
            else:
                Log.__debug(o)
        except Exception:
            pass



    # Method for setting the log level
    @staticmethod
    def setLogLevel(level: str) -> None:
        log = logging.getLogger("django")
        log.setLevel(level)



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __debug(o: any, logLevel: int = DEBUG) -> None:
        log = logging.getLogger("django")

        try:
            if isinstance(o, str):
                # Truncate the message if it's too long (only for DEBUG level logs)
                if len(o.encode('utf-8')) >= 262144 and logLevel == Log.DEBUG: # 256k (bytes).
                    log.debug(logLevel, o[:20000] + " [...] [MESSAGE TRUNCATED]") # chars.
                else:
                    log.log(logLevel, o)
            else:
                log.log(logLevel, o)
        except Exception as e:
            raise e
