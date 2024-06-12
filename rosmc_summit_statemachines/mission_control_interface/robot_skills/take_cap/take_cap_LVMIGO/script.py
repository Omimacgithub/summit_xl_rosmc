from __future__ import print_function
#This SM was made listening to Yakuza 8 soundtrack
import rospy
import std_srvs.srv

def capture(topic):
    try:
        #rospy.wait_for_service('/front_save/save')
        calling = rospy.ServiceProxy('/' + topic + '_save/save', std_srvs.srv.Empty)
        calling()
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
        return "aborted"
    
def execute(self, inputs, outputs, gvm):
    #front camera
    if inputs["frontcam"] == 1:
        #Real, for unsynchronize reason, the frontcam doesn't work
        capture("front")
    #left camera
    if inputs["leftcam"] == 1:
        capture("left")
    #right camera
    if inputs["rightcam"] == 1:
        capture("right")
    return "success"