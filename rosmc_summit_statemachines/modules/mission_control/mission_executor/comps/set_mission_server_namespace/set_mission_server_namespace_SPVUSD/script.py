
def execute(self, inputs, outputs, gvm):
    if gvm.variable_exists("mission_server_namespace"):
        gvm.delete_variable("mission_server_namespace")
    gvm.set_variable("mission_server_namespace", inputs['mission_server_namespace'], per_reference=True)
    return "success"
