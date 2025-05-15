from secops.models.Conjur.backend.Apikey import Apikey as Backend


class Apikey:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def rotate(**kwargs) -> str:
        try:
            return Backend.rotate(**kwargs)
        except Exception as e:
            raise e
