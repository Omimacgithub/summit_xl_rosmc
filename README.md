# summit_xl_rosmc

This repo contains a demo of the Robotnik Summit-XL working with a high-level mission designing and monitoring tool called rosmc.

![GIF](https://github.com/Omimacgithub/summit_xl_rosmc/assets/90336442/54ee2867-8713-49b1-b092-06775b29f3a1)

## Building the code

Add this repo to your catkin_ws.

~~~shell
git clone https://github.com/Omimacgithub/summit_xl_rosmc.git
catkin build rosmc
~~~

## Docker

~~~shell
docker compose up
~~~

## Using outdoors localization (only simulation):

You need to edit the file **summit_xl_complete.launch** as follows:
nano ~/catkin_ws/src/summit_xl_sim_bringup/launch/summit_xl_complete.launch

Copy ekf localization files:
~~~shell
cp ~/catkin_ws/src/summit_xl_rosmc/resources/gps_localization/navsat_transform_node.launch ~/catkin_ws/src/summit_xl_rosmc/resources/gps_localization/robot_localization_world.launch ~/catkin_ws/src/summit_xl_localization/launch/
~~~

Uncomment the blank_map line on launch:

Load any of the outdoor gazebo worlds:
~~~shell
cp ~/catkin_ws/src/summit_xl_rosmc/resources/gazebo_worlds/mission2.world ~/catkin_ws/src/summit_xl_gazebo/worlds/
nano ~/catkin_ws/src/summit_xl_sim_bringup/launch/summit_xl_complete.launch
~~~

Copy the blank map:
~~~shell
cp ~/catkin_ws/src/summit_xl_rosmc/resources/blank_map.pgm ~/catkin_ws/src/summit_xl_common/summit_xl_localization/maps/empty/map_empty.pgm
~~~

Comment the following line on **robot_localization_complete.launch**:
~~~shell
nano ~/catkin_ws/src/summit_xl_common/summit_xl_localization/launch/robot_localization_complete.launch
~~~

## Demos
- Simulations: [YT playlist](https://www.youtube.com/playlist?list=PLtkrT12EU5nWiCNHojNHtxvTQV09KULYj)
- Real: [YT playlist](https://www.youtube.com/playlist?list=PLtkrT12EU5nXhh0LXnHXoR5eReIP0TPGB)
