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
~~~shell
nano ~/catkin_ws/src/summit_xl_sim_bringup/launch/summit_xl_complete.launch
~~~
<img width="413" alt="imagen" src="https://github.com/Omimacgithub/summit_xl_rosmc/assets/90336442/30918c7d-be69-4fc9-9ec1-3a4f64316c70">
<img width="655" alt="imagen" src="https://github.com/Omimacgithub/summit_xl_rosmc/assets/90336442/39772168-44e3-455b-beaf-4bff29e752b3">


Copy ekf localization files:
~~~shell
cp ~/catkin_ws/src/summit_xl_rosmc/resources/gps_localization/navsat_transform_node.launch ~/catkin_ws/src/summit_xl_rosmc/resources/gps_localization/robot_localization_world.launch ~/catkin_ws/src/summit_xl_localization/launch/
~~~

Uncomment the blank_map line on launch:

TODO: CUANDO TENGA EL .LAUNCH

Load any of the outdoor gazebo worlds:
~~~shell
cp ~/catkin_ws/src/summit_xl_rosmc/resources/gazebo_worlds/mission2.world ~/catkin_ws/src/summit_xl_gazebo/worlds/
nano ~/catkin_ws/src/summit_xl_sim_bringup/launch/summit_xl_complete.launch
<img width="507" alt="imagen" src="https://github.com/Omimacgithub/summit_xl_rosmc/assets/90336442/0907ecde-d842-449d-86c3-7a438f4529a6">

~~~

Copy the blank map:
~~~shell
cp ~/catkin_ws/src/summit_xl_rosmc/resources/blank_map.pgm ~/catkin_ws/src/summit_xl_common/summit_xl_localization/maps/empty/map_empty.pgm
~~~

Comment the following line on **robot_localization_complete.launch**:
~~~shell
nano ~/catkin_ws/src/summit_xl_common/summit_xl_localization/launch/robot_localization_complete.launch
~~~
<img width="554" alt="imagen" src="https://github.com/Omimacgithub/summit_xl_rosmc/assets/90336442/3a639d80-1148-46a2-8f38-cefb8fbdaea1">


## Demos
- Simulations: [YT playlist](https://www.youtube.com/playlist?list=PLtkrT12EU5nWiCNHojNHtxvTQV09KULYj)
- Real: [YT playlist](https://www.youtube.com/playlist?list=PLtkrT12EU5nXhh0LXnHXoR5eReIP0TPGB)
