
def execute(self, inputs, outputs, gvm):
    self.logger.debug("Reset current mission")
    if gvm.variable_exists("current_mission"):
        gvm.delete_variable("current_mission")
    if gvm.variable_exists("sync_ids_list"):
        gvm.delete_variable("sync_ids_list")
    return 0
