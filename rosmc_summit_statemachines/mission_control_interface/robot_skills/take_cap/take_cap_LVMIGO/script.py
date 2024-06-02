from __future__ import print_function
#This SM was made listening to Yakuza 8 soundtrack
import rospy
import subprocess
import std_srvs.srv

def capture(topic, filename):
    cap = ["rosrun", "image_view", "image_saver", 
            "image:=" + topic, 
            "_save_all_image:=false", 
            "_image_transport:=compressed", 
            "_filename_format:=/home/robot/shots/" + filename + "%04d.%s", 
            "__name:=image_node"]
    process = subprocess.Popen(cap)
    #service = ["rosservice", "call", "/summit_xl/image_" + topic + "/save"]
    #subprocess.call(service)
    #Mejor forma:
    rospy.sleep(2)
    rospy.wait_for_service('/summit_xl/image_node/save')
    try:
	    calling = rospy.ServiceProxy('/summit_xl/image_node/save', std_srvs.srv.Empty)
	    calling()
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
    finally:
        kill = ["rosnode", "kill", "/summit_xl/image_node"]
        subprocess.call(kill)
        process.kill()
    
def execute(self, inputs, outputs, gvm):
    front = "front" if inputs["frontcam_filename"] == "" else inputs["frontcam_filename"]
    left = "left" if inputs["leftcam_filename"] == "" else inputs["leftcam_filename"]
    right = "right" if inputs["rightcam_filename"] == "" else inputs["rightcam_filename"]
    #front camera
    if inputs["frontcam"] == 1:
        capture("/robot/front_rgbd_camera/rgb/image_rect_color", front)
    #left camera
    if inputs["leftcam"] == 1:
        capture("/camera1/rgb/image_color", left)
    #right camera
    if inputs["rightcam"] == 1:
        capture("/camera2/rgb/image_color", right)
    return "success"