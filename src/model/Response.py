"""
Author      :   Jackey Weng
Student ID  :   40130001
Description :   This file is the Response model that will be generated to send 
                information from the server to the client
"""

from enum import Enum
import json


class ResponseCode(Enum):
    SUCCESS_PUT_CHANGE = 0b000
    SUCCESS_GET = 0b001
    ERROR_FILE_NOT_FOUND = 0b010
    ERROR_UNKNOWN_REQUEST = 0b011
    UNSUCCESSFUL_CHANGE = 0B101
    SERVER_HELP = 0B110


class Response:
    # constructor
    def __init__(self, Response_code, Filename_length=None, Filename=None,
                 File_size=None, Help_length=None, Help_msg=None, Debug_mode=0):
        self.id = id
        self.Response_code = Response_code
        self.Filename_length = Filename_length
        self.Filename = Filename
        self.File_size = File_size
        self.Help_length = Help_length
        self.Help_msg = Help_msg
        self.Debug_mode = Debug_mode

    # return the response as an object
    @classmethod
    def deserialize(cls, put_string):
        # convert it to dictionary
        put_dict = json.loads(put_string)

        match put_dict['Res-code']:
            case ResponseCode.SUCCESS_PUT_CHANGE.value:
                # return the object by passing the keys as parameters
                return cls(put_dict['Res-code'])

            case ResponseCode.SUCCESS_GET.value:
                # return the object by passing the keys as parameters
                return cls(put_dict['Res-code'], Filename_length=put_dict['Filename Length'], Filename=put_dict['Filename'], File_size=put_dict['File Size'])

            case ResponseCode.ERROR_FILE_NOT_FOUND.value:
                # return the object by passing the keys as parameters
                return cls(put_dict['Res-code'])

            case ResponseCode.ERROR_UNKNOWN_REQUEST.value:
                # return the object by passing the keys as parameters
                return cls(put_dict['Res-code'])

            case ResponseCode.UNSUCCESSFUL_CHANGE.value:
                # return the object by passing the keys as parameters
                return cls(put_dict['Res-code'])

            case ResponseCode.SERVER_HELP.value:
                # return the object by passing the keys as parameters
                return cls(put_dict['Res-code'], Help_length=put_dict['Length'], Help_msg=put_dict['Help Data'], Debug_mode=put_dict['Debug Mode'])

    # return a workload representation
    def __repr__(self):
        sentence = None
        match self.Response_code:
            case ResponseCode.SUCCESS_PUT_CHANGE.value:
                sentence = f'---------Response Message---------\n'\
                    f"Res-code \t:{bin(self.Response_code)}\n" \
                    f"----------------------------------"

            case ResponseCode.SUCCESS_GET.value:
                sentence = f'---------Response Message---------\n'\
                    f"Res-code \t|{bin(self.Response_code)}\n"\
                    f"Filename Length |{self.Filename_length}\n"\
                    f"Filename \t|{self.Filename}\n"\
                    f"File Size \t|{self.File_size}\n" \
                    f"----------------------------------"

            case ResponseCode.ERROR_FILE_NOT_FOUND.value:
                sentence = f'---------Response Message---------\n'\
                    f"Res-code |{bin(self.Response_code)}\n" \
                    f"----------------------------------"

            case ResponseCode.ERROR_UNKNOWN_REQUEST.value:
                sentence = f'---------Response Message---------\n'\
                    f"Res-code |{bin(self.Response_code)}\n" \
                    f"----------------------------------"

            case ResponseCode.UNSUCCESSFUL_CHANGE.value:
                sentence = f'---------Response Message---------\n'\
                    f"Res-code |{bin(self.Response_code)}\n" \
                    f"----------------------------------"

            case ResponseCode.SERVER_HELP.value:
                sentence = f'---------Response Message---------\n'
                if self.Debug_mode == 1:
                    sentence += f'res-code|{bin(self.Response_code)} \n'
                    sentence += f'Length\t|{self.Help_length} \n'
                sentence += self.Help_msg
                sentence += f"\n----------------------------------"
        return sentence

    # return a dictionary format of the object
    def dictionary(self):
        Response = None
        match self.Response_code:
            case ResponseCode.SUCCESS_PUT_CHANGE.value:
                Response = {
                    "Res-code": self.Response_code
                }
            case ResponseCode.SUCCESS_GET.value:
                Response = {
                    "Res-code": self.Response_code,
                    "Filename Length": self.Filename_length,
                    "Filename": self.Filename,
                    "File Size": self.File_size
                }
            case ResponseCode.ERROR_FILE_NOT_FOUND.value:
                Response = {
                    "Res-code": self.Response_code
                }
            case ResponseCode.ERROR_UNKNOWN_REQUEST.value:
                Response = {
                    "Res-code": self.Response_code
                }
            case ResponseCode.UNSUCCESSFUL_CHANGE.value:
                Response = {
                    "Res-code": self.Response_code
                }
            case ResponseCode.SERVER_HELP.value:
                Response = {
                    "Res-code": self.Response_code,
                    "Length": self.Help_length,
                    "Help Data": self.Help_msg,
                    "Debug Mode": self.Debug_mode
                }
        return Response
