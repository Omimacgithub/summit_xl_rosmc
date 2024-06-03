import rospy
from robot_simple_command_manager_msgs.msg import CommandString
def execute(self, inputs, outputs, gvm):
    try:
        pub = rospy.Publisher('/command_manager/command', CommandString, queue_size=10)
        rospy.init_node('robot', anonymous=True)
        msg = "GOTO " + inputs["x_pos"] + " " + inputs["y_pos"] + " " + str(0.0)
	    rospy.loginfo(msg)
        pub.publish(msg)
	    return "success"
    except rospy.ROSInterruptException:
		pass