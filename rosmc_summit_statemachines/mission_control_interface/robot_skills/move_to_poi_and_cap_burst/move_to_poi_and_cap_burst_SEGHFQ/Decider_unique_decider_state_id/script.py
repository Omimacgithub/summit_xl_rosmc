
def execute(self, inputs, outputs, gvm):
    #The unique purpose is to wait all child states to execute.
    if (inputs["fault_1"] == 1) or (inputs["fault_2"] == 1):
        return "aborted"
    return "success"
