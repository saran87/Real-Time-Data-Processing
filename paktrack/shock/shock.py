
from paktrack.common.base_model import BaseModel

SHOCK_COLLECTION = "shock"


class Shock(BaseModel):

    def __init__(self, db_host, db_port, db, db_user="", db_pass=""):
        super(Shock, self).__init__(
            db_host, db_port, db, db_user, db_pass, SHOCK_COLLECTION)
