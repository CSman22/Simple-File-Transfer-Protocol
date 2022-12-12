"""
Author      :   Jackey Weng
Student ID  :   40130001
Description :   This file contains all the Request model that will be 
                generated to send information from the client to the server
"""
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
        return f'---------Request Message---------\n' \
            f'opcode \t\t|{bin(self.opcode)} \n'\
            f'filename_length\t|{self.filename_length} \n'\
            f'filename \t|{self.filename} \n'\
            f'file_size \t|{self.file_size}\n'\
            '---------------------------------'

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


class Get:
    # constructor
    def __init__(self, opcode, filename_length, filename):
        self.opcode = opcode
        self.filename_length = filename_length
        self.filename = filename

    # return a Get representation
    def __repr__(self):
        return f'---------Request Message---------\n' \
            f'opcode \t\t|{bin(self.opcode)} \n'\
            f'filename_length\t|{self.filename_length} \n'\
            f'filename \t|{self.filename}\n'\
            '---------------------------------'

    # return the Get as an object
    @classmethod
    def deserialize(cls, get_string):
        # convert it to dictionary
        get_dict = json.loads(get_string)
        # return the object by passing the keys as parameters
        return cls(**get_dict)

    # return a Get dictionary
    def dictionary(self):
        get = {
            "opcode": self.opcode,
            "filename_length": self.filename_length,
            "filename": self.filename,
        }
        return get


class Change:
    # constructor
    def __init__(self, opcode, old_filename_length, old_filename, new_filename_length, new_filename):
        self.opcode = opcode
        self.old_filename_length = old_filename_length
        self.old_filename = old_filename
        self.new_filename_length = new_filename_length
        self.new_filename = new_filename

    # return a Change representation
    def __repr__(self):
        return f'---------Request Message---------\n' \
            f'opcode     \t\t|{bin(self.opcode)} \n'\
            f'Old filename length\t|{self.old_filename_length} \n'\
            f'Old filename  \t\t|{self.old_filename} \n'\
            f'New filename length \t|{self.new_filename_length} \n'\
            f'New filename \t\t|{self.new_filename}\n'\
            '---------------------------------'

    # return the Change as an object
    @classmethod
    def deserialize(cls, change_string):
        # convert it to dictionary
        change_dict = json.loads(change_string)
        # return the object by passing the keys as parameters
        return cls(**change_dict)

    # return a Change dictionary
    def dictionary(self):
        change = {
            "opcode": self.opcode,
            "old_filename_length": self.old_filename_length,
            "old_filename": self.old_filename,
            "new_filename_length": self.new_filename_length,
            "new_filename": self.new_filename,
        }
        return change


class Help:
    # constructor
    def __init__(self, opcode):
        self.opcode = opcode

    # return a Help representation
    def __repr__(self):
        return f'---------Request Message---------\n' \
            f'opcode \t|{bin(self.opcode)}'

    # return the Help as an object
    @classmethod
    def deserialize(cls, help_string):
        # convert it to dictionary
        help_dict = json.loads(help_string)
        # return the object by passing the keys as parameters
        return cls(**help_dict)

    # return a Help dictionary
    def dictionary(self):
        help = {
            "opcode": self.opcode,
        }
        return help


class Bye:
    # constructor
    def __init__(self, opcode):
        self.opcode = opcode

    # return a Bye representation
    def __repr__(self):
        return f'---------Request Message---------\n' \
            f'opcode \t|{bin(self.opcode)}'

    # return the Bye as an object
    @classmethod
    def deserialize(cls, bye_string):
        # convert it to dictionary
        bye_dict = json.loads(bye_string)
        # return the object by passing the keys as parameters
        return cls(**bye_dict)

    # return a Put dictionary
    def dictionary(self):
        bye = {
            "opcode": self.opcode,
        }
        return bye


class Error:
    # constructor
    def __init__(self, opcode):
        self.opcode = opcode

    # return a Error representation
    def __repr__(self):
        return f'---------Request Message---------\n' \
            f'opcode |{bin(self.opcode)}\n'\
            '---------------------------------'

    # return the Error as an object
    @classmethod
    def deserialize(cls, error_string):
        # convert it to dictionary
        error_dict = json.loads(error_string)
        # return the object by passing the keys as parameters
        return cls(**error_dict)

    # return a Error dictionary
    def dictionary(self):
        Error = {
            "opcode": self.opcode,
        }
        return Error
