export ROS_MASTER_URI=http://shl00-220622aa:11311
#Mission server
ROSMC_SUMMIT_STATEMACHINES=$HOME/catkin_ws/src/summit_xl_rosmc/rosmc_summit_statemachines roslaunch rosmc_mission_server summit_mission_server.launch &
sleep 2
#Task marker servers
roslaunch rosmc_task_marker_server all_task_marker_server.launch &
sleep 1
#Frontend tools
#rosmc mission commander
ROS_NAMESPACE=mission_control rosrun rosmc_command_gui rosmc_command_gui register_to_mission_server:=/mission_control/register_to_mission_server &
#rviz
roslaunch rosmc_3d_gui 3d_gui.launch &
#EXPORT ~/.local/bin to $PATH (for RAFCON)
export PATH="$HOME/.local/bin:$PATH"
#RAFCON statemachine (inside GUI, launch with play button)
SM_DIR=$HOME/catkin_ws/src/summit_xl_rosmc/rosmc_summit_statemachines; ROS_NAMESPACE=summit_xl rafcon -c $SM_DIR/config.yaml -o $SM_DIR/modules/mission_control/mission_executor/mission_executor &
#Image view node (front camera)
#rosrun image_view image_saver image:=/robot/front_rgbd_camera/rgb/image_raw _request_start_end:=true  _filename_format:=$HOME/shots/front$(date +%F-%R)/%04d.%s __name:=front_saver &
#Image view node (front camera for a single shot)
#rosrun image_view image_saver image:=/robot/front_rgbd_camera/rgb/image_raw _save_all_image:=false _image_transport:=compressed _filename_format:=$HOME/shots/front$(date +%F-%R)/%04d.%s __name:=image_node
#Image view node (left camera for a single shot)
#rosrun image_view image_saver image:=/camera1/rgb/image_color _save_all_image:=false _image_transport:=compressed _filename_format:=~/shots/left$(date +%F-%R)%04d.%s __name:=image_node
#rosrun --debug image_view image_saver image:=/robot/front_rgbd_camera/rgb/image_raw _request_start_end:=true  _filename_format:=$HOME/shots/front$(date +%F-%R)/%04d.%s __name:=left_saver
#Image view node (right camera)
#rosrun --debug image_view image_saver image:=/robot/front_rgbd_camera/rgb/image_raw _request_start_end:=true  _filename_format:=$HOME/shots/front$(date +%F-%R)/%04d.%s __name:=right_saver
