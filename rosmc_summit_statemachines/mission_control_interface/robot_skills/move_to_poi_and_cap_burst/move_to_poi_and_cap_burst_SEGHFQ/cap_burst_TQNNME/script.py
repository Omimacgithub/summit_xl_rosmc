from __future__ import print_function
#This SM was made listening to Yakuza 8 soundtrack
import rospy
import subprocess
import std_srvs.srv
    
def execute(self, inputs, outputs, gvm):
    try:
	    if inputs["frontcam"] == 1:
	        startf = rospy.ServiceProxy('/front_saver/start', std_srvs.srv.Trigger)
	        startf()
	    #If you encounter an md5sum issue when calling the service, ensure the message type that service accepts is the same type you specifi
	    #You can check the message type of a service with: rosservice info <service> 	    
	    if inputs["leftcam"] == 1:
	        startl = rospy.ServiceProxy('/left_saver/start', std_srvs.srv.Trigger)
	        startl()
	    if inputs["rightcam"] == 1:
	        startr = rospy.ServiceProxy('/right_saver/start', std_srvs.srv.Trigger)
	        startr()
	    
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
        outputs["fault"] = 1
        return "success"
    return "success"