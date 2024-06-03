
def execute(self, inputs, outputs, gvm):
    self.logger.debug("Reset mission related global variables")
    #gvm.set_variable("global_timeout", 1.0)
    gvm.set_variable("global_timeout", 4.0)
    if gvm.variable_exists("current_action_id"):
        gvm.delete_variable("current_action_id")
    if gvm.variable_exists("index_when_stopped"):
        gvm.delete_variable("index_when_stopped")
    if gvm.variable_exists("is_mission_finished"):
        gvm.delete_variable("is_mission_finished")
    if gvm.variable_exists("is_paused_reactively"):
        gvm.delete_variable("is_paused_reactively")
    if gvm.variable_exists("is_in_wifi_range"):
        gvm.delete_variable("is_in_wifi_range")
    if gvm.variable_exists("is_in_wifi_range_with_margin"):
        gvm.delete_variable("is_in_wifi_range_with_margin")
    if gvm.variable_exists("is_battery_remaining"):
        gvm.delete_variable("is_battery_remaining")
    if gvm.variable_exists("is_battery_remaining_with_margin"):
        gvm.delete_variable("is_battery_remaining_with_margin")
    if gvm.variable_exists("requested_state"):
        gvm.delete_variable("requested_state")
    if gvm.variable_exists("requested_state"):
        gvm.delete_variable("requested_state")
    if gvm.variable_exists("is_reactive_preemption_required"):
        gvm.delete_variable("is_reactive_preemption_required")
    if gvm.variable_exists("is_sync_waiting"):
        gvm.delete_variable("is_sync_waiting")
    if gvm.variable_exists("update_action_status_request_list"):
        gvm.delete_variable("update_action_status_request_list")
    return 0
