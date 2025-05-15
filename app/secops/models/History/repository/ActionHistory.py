from secops.helpers.RepositoryBase import RepositoryBase


class ActionHistory:

    # Table: log_request

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def add(data: dict) -> None:
        try:
            RepositoryBase.add(table="log_request", data=data)
        except Exception as e:
            raise e
