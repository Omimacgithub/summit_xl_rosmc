
def execute(self, inputs, outputs, gvm):
    self.logger.debug("Reset global variable current_action_id")
    gvm.set_variable("current_action_id", '')
    return 0
