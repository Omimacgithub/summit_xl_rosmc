import rospy
import std_srvs.srv
import subprocess

def execute(self, inputs, outputs, gvm):
    try:
        if inputs["frontcam"] == 1:
            endf = rospy.ServiceProxy('/front_saver/end', std_srvs.srv.Trigger)
            endf()
        if inputs["leftcam"] == 1:
            endl = rospy.ServiceProxy('/left_saver/end', std_srvs.srv.Trigger)
            endl()
        if inputs["rightcam"] == 1:
            endr = rospy.ServiceProxy('/right_saver/end', std_srvs.srv.Trigger)
            endr()
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
        return "aborted"
        
    #The unique purpose is to wait all child states to execute.
    if (inputs["fault_1"] == 1) or (inputs["fault_2"] == 1):
        return "aborted"
    return "success"
