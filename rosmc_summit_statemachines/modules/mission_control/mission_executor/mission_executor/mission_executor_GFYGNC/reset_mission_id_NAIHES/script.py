
def execute(self, inputs, outputs, gvm):
    self.logger.debug("reset id of current action")
    gvm.set_variable("current_action_id", '', per_reference=True)
    return 0
