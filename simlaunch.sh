export ROS_MASTER_URI=http://localhost:11311
#Rosmc mission server
ROSMC_SUMMIT_STATEMACHINES=$HOME/catkin_ws/src/summit_xl_rosmc/rosmc_summit_statemachines roslaunch rosmc_mission_server summit_mission_server.launch &
sleep 2
#Task marker servers
roslaunch rosmc_task_marker_server all_task_marker_server.launch &
sleep 1
#Launch summit_xl_sim
roslaunch summit_xl_sim_bringup summit_xl_complete.launch launch_rviz:=false & #gazebo_gui:=false &
#Frontend tools
#rosmc mission commander
ROS_NAMESPACE=mission_control rosrun rosmc_command_gui rosmc_command_gui register_to_mission_server:=/mission_control/register_to_mission_server &
#rviz
roslaunch rosmc_3d_gui 3d_gui.launch &
#EXPORT ~/.local/bin to $PATH (for RAFCON)
export PATH="$HOME/.local/bin:$PATH"
#RAFCON statemachine (inside GUI, launch with play button)
sleep 2
SM_DIR=$HOME/catkin_ws/src/summit_xl_rosmc/rosmc_summit_statemachines; ROS_NAMESPACE=summit_xl rafcon -c $SM_DIR/config.yaml -o $SM_DIR/modules/mission_control/mission_executor/mission_executor &
#Load empty map (if you are using amcl, comment this line)
#ROS_NAMESPACE=robot roslaunch summit_xl_localization map_server.launch prefix:=robot_ map_file:=empty/map_empty.yaml &
#Image view node (front camera)
#Wait for cams
sleep 5
rosrun image_view image_saver image:=/robot/front_rgbd_camera/rgb/image_raw _image_transport:=compressed _request_start_end:=true  _filename_format:=$HOME/shots/front$(date +%F-%R)/%04d.%s __name:=front_saver &
#Single shot
rosrun image_view image_saver image:=/robot/front_rgbd_camera/rgb/image_raw _image_transport:=compressed _save_all_image:=false  _filename_format:=$HOME/shots/frontsingleshots$(date +%F-%R)/%04d.%s __name:=front_save &
