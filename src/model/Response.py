class Response:
    # constructor
    def __init__(self, id, workload):
        self.id = id
        self.workload = workload

    # return a workload representation
    def __repr__(self):
        return f'\n\tID: {self.id} \n'\
            f'\tWorkload: {self.workload} \n'

    # return a dictionary format of the object
    def dictionary(self):
        batch = {
            "batch id": self.id,
            "workload": self.workload
        }
        return batch
