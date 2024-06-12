from __future__ import print_function
#This SM was made listening to Yakuza 8 soundtrack
import rospy
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Header

def pose(inputs):
    p = Pose()
    p.position.x = inputs["x_pos"]
    p.position.y = inputs["y_pos"] 
    p.position.z = inputs["z_pos"]
    p.orientation.x = inputs["x_ori"]
    p.orientation.y = inputs["y_ori"]
    p.orientation.z = inputs["z_ori"]
    p.orientation.w = inputs["w_ori"]

    return p

def execute(self, inputs, outputs, gvm):
    try:
        client = actionlib.SimpleActionClient('/robot/move_base', MoveBaseAction)
        client.wait_for_server()
        header = Header()
        header.frame_id = "robot_map"
        header.stamp = rospy.Time.now()
        goal = MoveBaseGoal()
        goal.target_pose.header = header
        goal.target_pose.pose = pose(inputs)
	#Sending goal
        client.send_goal(goal)
        gvm.set_variable("clase", client, per_reference=True)
        client.wait_for_result()
        state = client.get_state()
        
        if state == GoalStatus.SUCCEEDED:
            return "success"
        elif (state == GoalStatus.ABORTED or state == GoalStatus.REJECTED):
            return "aborted"
    except rospy.ROSInterruptException:
        return "aborted"
    finally:
        gvm.delete_variable("clase")