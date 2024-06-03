
def execute(self, inputs, outputs, gvm):
    index_when_stopped = gvm.get_variable("index_when_stopped", per_reference=False, default=None)
    if index_when_stopped is None or index_when_stopped == "None":
        outputs["old_index"] = None
        outputs["new_mission"] = True
    else:
        outputs["old_index"] = index_when_stopped - 1
        outputs["new_mission"] = False
        # Reset global variable "index_when_stopped"
        gvm.set_variable("index_when_stopped", None)
    return 0
