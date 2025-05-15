from secops.models.Asset.repository.Asset import Asset as Repository

from secops.helpers.Exception import CustomException
from secops.helpers.Misc import Misc


class Asset:
    def __init__(self, assetId: int, showPassword: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = int(assetId)
        self.technology: str = ""
        self.fqdn: str = ""
        self.protocol: str = "https"
        self.port: int = 443
        self.path: str = "/"
        self.tlsverify: bool = True
        self.baseurl: str = ""
        self.account: str = ""
        self.datacenter: str = ""
        self.environment: str = ""
        self.position: str = ""
        self.appid: str = ""
        self.username: str = ""
        self.password: str = ""
        self.repokey: str = ""
        self.userkey: str = ""
        self.certificate_authority_data: str = ""
        self.client_certificate_data: str = ""
        self.client_key_data: str = ""

        self.__load(showPassword=showPassword)



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        return vars(self)



    def modify(self, data: dict) -> None:
        try:
            Repository.modify(self.id, data)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Repository.delete(self.id)
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def rawDataList(showPassword: bool = True) -> list:
        try:
            return Repository.list(showPassword=showPassword)
        except Exception as e:
            raise e



    @staticmethod
    def add(data: dict) -> None:
        try:
            Repository.add(data)
        except Exception as e:
            raise e



    @staticmethod
    def getAssetIdOfTechnology(technology: str) -> dict:
        try:
            return list(
                filter(lambda a: a.get("technology", "") == technology, Asset.rawDataList())
            )[0]
        except IndexError:
            raise CustomException(status=400)
        except KeyError:
            raise CustomException(status=400)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self, showPassword: bool = True) -> None:
        try:
            data = Repository.get(self.id, showPassword=showPassword)
            for k, v in data.items():
                setattr(self, k, v)

            if not showPassword:
                del self.username
                del self.password
                del self.client_certificate_data
                del self.client_key_data
        except Exception as e:
            raise e
