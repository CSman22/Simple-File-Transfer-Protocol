import json


class Put:
    # constructor
    def __init__(self, opcode, filename_length, filename, file_size):
        self.opcode = opcode
        self.filename_length = filename_length
        self.filename = filename
        self.file_size = file_size

    # return a Put representation
    def __repr__(self):
        return f'opcode \t\t|{self.opcode} \n'\
            f'filename_length\t|{self.filename_length} \n'\
            f'filename \t|{self.filename} \n'\
            f'file_size \t|{self.file_size} \n'

    # return the PUT as an object
    @classmethod
    def deserialize(cls, put_string):
        # convert it to dictionary
        put_dict = json.loads(put_string)
        # return the object by passing the keys as parameters
        return cls(**put_dict)

    # return a Put dictionary
    def dictionary(self):
        put = {
            "opcode": self.opcode,
            "filename_length": self.filename_length,
            "filename": self.filename,
            "file_size": self.file_size,
        }
        return put
