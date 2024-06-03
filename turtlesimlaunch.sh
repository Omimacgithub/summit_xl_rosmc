roscore &
sleep 2
#ROSMC servers
ROSMC_TURTLESIM_STATEMACHINES=$HOME/rosmc_turtlesim_statemachines roslaunch rosmc_mission_server turtlesim_mission_server.launch &
sleep 2
roslaunch rosmc_task_marker_server all_task_marker_server.launch &
sleep 2
ROS_NAMESPACE=mission_control rosrun rosmc_agents turtles_int_marker_publisher.py &
sleep 2
#Launch turtlesim
rosrun turtlesim turtlesim_node &
sleep 2
#Add 2º turtle
rosservice call /spawn 2.0 6.0 3.14 'turtle2' &
#Turtle position topic publisher
roslaunch rosmc_agents turtle1_tf_broadcaster.launch &
roslaunch rosmc_agents turtle2_tf_broadcaster.launch &
rosrun rosmc_agents turtles_status_publisher.py &
#Frontend tools
#rosmc mission commander
ROS_NAMESPACE=mission_control rosrun rosmc_command_gui rosmc_command_gui register_to_mission_server:=/mission_control/register_to_mission_server &
#rviz
roslaunch rosmc_3d_gui 3d_gui.launch &
#Status icons
ROS_NAMESPACE=mission_control rosrun rosmc_status_monitor status_icons_publisher.py _frame_id_suffix:="" &
#EXPORT ~/.local/bin to $PATH (for RAFCON)
export PATH="$HOME/.local/bin:$PATH"
#RAFCON statemachines (inside GUI, launch both turtles with play button)
#SM_DIR=~/rosmc_turtlesim_statemachines; ROS_NAMESPACE=turtle1 rafcon -c $SM_DIR/config.yaml -o $SM_DIR/modules/mission_control/mission_executor/mission_executor &
#SM_DIR=~/rosmc_turtlesim_statemachines; ROS_NAMESPACE=turtle2 rafcon -c $SM_DIR/config.yaml -o $SM_DIR/modules/mission_control/mission_executor/mission_executor &
