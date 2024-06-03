
def execute(self, inputs, outputs, gvm):
    self.logger.debug("Set global variable is_mission_finished = False")
    gvm.set_variable("is_mission_finished", False)
    return "success"
