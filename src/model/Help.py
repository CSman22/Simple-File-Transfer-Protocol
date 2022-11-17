import json


class Help:
    # constructor
    def __init__(self, opcode):
        self.opcode = opcode

    # return a Put representation
    def __repr__(self):
        return f'opcode \t\t|{self.opcode} \n'

    # return the PUT as an object
    @classmethod
    def deserialize(cls, put_string):
        # convert it to dictionary
        put_dict = json.loads(put_string)
        # return the object by passing the keys as parameters
        return cls(**put_dict)

    # return a Put dictionary
    def dictionary(self):
        help = {
            "opcode": self.opcode,
        }
        return help
