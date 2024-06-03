
def execute(self, inputs, outputs, gvm):
    self.logger.debug("shutdown all services")
    service_list = gvm.get_variable("service_list", per_reference=True, default=[])
    for service in service_list:
        self.logger.debug("shutdown service " + str(service))
        service.shutdown("cancel_from_rafcon")
    gvm.set_variable("service_list", [], per_reference=True)
    return 0
