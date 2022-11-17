class Request:
    # constructor
    def __init__(self, opcode, filename_length, filename, file_size):
        self.opcode = opcode
        self.filename_length = filename_length
        self.filename = filename
        self.file_size = file_size

    # return a request representation
    def __repr__(self):
        return f'Opcode \t\t|{self.opcode} \n'\
            f'filename_length\t|{self.filename_length} \n'\
            f'filename \t|{self.filename} \n'\
            f'file_size \t|{self.file_size} \n'\
