import uuid

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from secops.helpers.Exception import CustomException
from secops.helpers.Log import Log


class CustomControllerBase(APIView):
    if not settings.DISABLE_AUTHENTICATION:
        from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

        permission_classes = [IsAuthenticated]
        authentication_classes = [JWTTokenUserAuthentication]



    @staticmethod
    def loggedUser(request: Request) -> dict:
        if settings.DISABLE_AUTHENTICATION:
            user = {
                "authDisabled": True,
                "groups": []
            }
        else:
            # Retrieve user from the JWT token.
            import jwt

            authenticator = request.successful_authenticator
            user = jwt.decode(
                authenticator.get_raw_token(authenticator.get_header(request)),
                settings.SIMPLE_JWT['VERIFYING_KEY'],
                settings.SIMPLE_JWT['ALGORITHM'],
                do_time_check=True
            )
            user["authDisabled"] = False

        return user



    @staticmethod
    def validate(data, Serializer, validationType: str, partial: bool = False):
        cleanData = None
        mismatch = False

        try:
            if Serializer:
                if validationType == "value":
                    serializer = Serializer(data=data, partial=partial)
                    if serializer.is_valid():
                        cleanData = serializer.validated_data
                    else:
                        mismatch = True
                elif validationType == "list":
                    serializer = Serializer(data={"items": data}) # list serializer needs an "items" key.
                    if serializer.is_valid():
                        cleanData = serializer.validated_data["items"]
                    else:
                        mismatch = True
                else:
                    raise NotImplemented

                if mismatch:
                    Log.log("Upstream data incorrect: " + str(serializer.errors))
                    raise CustomException(
                        status=500,
                        payload={"Backend": "Upstream data mismatch"}
                    )
                else:
                    return cleanData
            else:
                return data
        except Exception as e:
            raise e



    @staticmethod
    def generateSessionUid() -> str:
        sUid = uuid.uuid4().hex
        Log.log("[SESSION] Session identifier: " + str(sUid))

        return sUid



    @staticmethod
    def exceptionHandler(e: Exception) -> tuple:
        Log.logException(e)

        data = dict()
        headers = { "Cache-Control": "no-cache" }

        if e.__class__.__name__ in ("ConnectionError", "Timeout", "ConnectTimeout", "TooManyRedirects", "SSLError", "HTTPError"):
            httpStatus = status.HTTP_503_SERVICE_UNAVAILABLE
            data["error"] = {
                "network": e.__str__()
            }
        elif e.__class__.__name__ == "CustomException":
            httpStatus = e.status
            if e.payload:
                data["error"] = e.payload
            else:
                data = None
        elif e.__class__.__name__ == "ParseError":
            data = None
            httpStatus = status.HTTP_400_BAD_REQUEST # json parse.
        else:
            data = None
            httpStatus = status.HTTP_500_INTERNAL_SERVER_ERROR # generic.

        return data, httpStatus, headers
