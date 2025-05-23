from secops.models.History.repository.ActionHistory import ActionHistory as Repository


class ActionHistory:
    def __init__(self, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(id)
        self.asset_id: int = 0
        self.action: str = ""
        self.response_status: str = ""
        self.username: str = ""



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def add(data: dict) -> None:
        try:
            Repository.add(data)
        except Exception as e:
            raise e
