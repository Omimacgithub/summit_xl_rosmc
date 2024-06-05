
def execute(self, inputs, outputs, gvm):
    outputs["fault"] = 1
    return "success"