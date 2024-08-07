import rospy

def execute(self, inputs, outputs, gvm):
    #Claim class
    while not gvm.variable_exists("clase"):
        pass
    client = gvm.get_variable("clase", per_reference=True, default=None)
    status = gvm.get_variable("requested_state", default="run")
    while status != "stop": #) or (status != "reset"):
        if self.preempted:
            return "success"
        rospy.sleep(1)
        status = gvm.get_variable("requested_state", default="run")
    client.cancel_goal()
    return "aborted"
