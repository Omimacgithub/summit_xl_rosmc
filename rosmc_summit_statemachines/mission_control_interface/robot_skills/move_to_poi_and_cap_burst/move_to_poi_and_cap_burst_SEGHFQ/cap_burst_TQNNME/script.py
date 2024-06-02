from __future__ import print_function
#This SM was made listening to Yakuza 8 soundtrack
import rospy
import subprocess
import std_srvs.srv
    
def execute(self, inputs, outputs, gvm):
    front = "front" #if inputs["frontcam_filename"] == "" else inputs["frontcam_filename"]
    left = "left" #if inputs["leftcam_filename"] == "" else inputs["leftcam_filename"]
    right = "right" #if inputs["rightcam_filename"] == "" else inputs["rightcam_filename"]
    #front camera
    front = ["rosservice", "call", "/front_saver/start"]
    subprocess.call(front)
    '''
    left = ["rosservice", "call", "/left_saver/start"]
    subprocess.call(left)
    right = ["rosservice", "call", "/right_saver/start"]
    subprocess.call(right)
    #gvm.set_variable('start', True)
    try:
	    #startf = rospy.ServiceProxy('/image_front/start', std_srvs.srv.Empty)
	    #startf()	    
	    
	    startl = rospy.ServiceProxy('/left_saver/start', std_srvs.srv.Empty)
	    startl()
	    startr = rospy.ServiceProxy('/right_saver/start', std_srvs.srv.Empty)
	    startr()
	    
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
    '''
    return "success"