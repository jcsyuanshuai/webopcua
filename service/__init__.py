import json


class Res:
    code: int
    msg: str

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Ok(Res):
    code = 200
    msg = "success"

    def __init__(self, data=None):
        if data is not None:
            self.data = data
