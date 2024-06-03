import rafcon

def execute(self, inputs, outputs, gvm):
    execution_engine = rafcon.core.singleton.state_machine_execution_engine
    self.logger.debug("Pause RAFCON and wait for RUN button to be triggered in Mission Control GUI")
    execution_engine.pause()
    while True:
        if self.wait_for_unpause(gvm.get_variable("global_timeout")):
            if self.preempted:
                return -2
            elif self.started:
                return 0
