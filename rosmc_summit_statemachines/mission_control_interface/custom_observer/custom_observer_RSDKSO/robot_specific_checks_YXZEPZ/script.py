
def execute(self, inputs, outputs, gvm):
    self.logger.info("Executing robot specific checks ...")
    self.preemptive_wait(100)
    return "success"
