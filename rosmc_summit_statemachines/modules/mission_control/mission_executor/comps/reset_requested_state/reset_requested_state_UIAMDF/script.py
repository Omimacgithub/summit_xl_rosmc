
def execute(self, inputs, outputs, gvm):
    self.logger.debug("Reset global variable requested_state")
    if gvm.variable_exists("requested_state"):
        gvm.delete_variable("requested_state")
    return 0
