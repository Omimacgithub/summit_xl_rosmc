
def execute(self, inputs, outputs, gvm):
    self.logger.debug("All actions currently synchronised to agent are finished")
    self.logger.debug("Set global variable is_mission_finished = True")
    gvm.set_variable("is_mission_finished", True)
    return "success"
