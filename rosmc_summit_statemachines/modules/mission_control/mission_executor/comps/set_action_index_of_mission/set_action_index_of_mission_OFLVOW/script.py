import time

def execute(self, inputs, outputs, gvm):
    self.logger.debug("setting index ...")
    # slow down execution for debugging purposes
    # time.sleep(1.0)
    actions = gvm.get_variable("current_mission", default={})
    # comment out for debugging purposes
    if inputs["new_mission"]:
        outputs["new_index"] = 0
    else:
        new_index = inputs["old_index"] + 1
        if new_index > len(actions) - 1:
            # set new_index for the case where all mission success and want to append new action
            outputs["new_index"] = inputs["old_index"]
            return "all_actions_executed"
        # comment out for debugging purposes
        #if new_index > len(actions) - 1:
        #    return "all_actions_executed"
        outputs["new_index"] = inputs["old_index"] + 1
    return "next action"
