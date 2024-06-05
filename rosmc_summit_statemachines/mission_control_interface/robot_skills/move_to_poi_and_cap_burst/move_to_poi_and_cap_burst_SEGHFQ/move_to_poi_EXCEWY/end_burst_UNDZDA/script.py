import rospy
import std_srvs.srv
import subprocess

def execute(self, inputs, outputs, gvm):
    '''
    front = ["rosservice", "call", "/front_saver/end"]
    subprocess.call(front)
    left = ["rosservice", "call", "/left_saver/end"]
    subprocess.call(left)
    right = ["rosservice", "call", "/right_saver/end"]
    subprocess.call(right)
    rospy.wait_for_service('/left_saver/end')
    rospy.wait_for_service('/right_saver/end')
    '''
    try:
        #endf = rospy.ServiceProxy('/front_saver/end', std_srvs.srv.Empty)
        #endf()
        endl = rospy.ServiceProxy('/left_saver/end', std_srvs.srv.Trigger)
        endl()
        endr = rospy.ServiceProxy('/right_saver/end', std_srvs.srv.Trigger)
        endr()
	    
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
        return "aborted" 
    return "success"
