# summit_xl_rosmc

This repo contains a demo of the Robotnik Summit-XL working with a high-level mission designing and monitoring tool called rosmc.

![GIF](https://github.com/Omimacgithub/summit_xl_rosmc/assets/90336442/54ee2867-8713-49b1-b092-06775b29f3a1)

## Demos
- Simulations: [YT playlist](https://www.youtube.com/playlist?list=PLtkrT12EU5nWiCNHojNHtxvTQV09KULYj)
- Real: [YT playlist](https://www.youtube.com/playlist?list=PLtkrT12EU5nXhh0LXnHXoR5eReIP0TPGB)

## Building the code

Add this repo to your catkin_ws.

~~~shell
git clone https://github.com/Omimacgithub/summit_xl_rosmc.git
catkin build rosmc
~~~

## Docker
The root Dockerfile used is located [here](https://github.com/RobotnikAutomation/summit_xl_sim)

~~~shell
docker compose up
~~~

To stop the container
~~~shell
docker stop 2q-base-1
~~~
To start the container
~~~shell
docker start 2q-base-1
docker attach 2q-base-1
~~~
To launch a new separated instance (note that if you close the terminal running the docker attach, all container instances would terminate)
~~~shell
docker exec -it 2q-base-1 bash
~~~

## Using outdoors localization (only simulation):

Uncomment the blank_map line on launch:
~~~shell
nano ~/catkin_ws/src/summit_xl_rosmc/simlaunch.sh
~~~
<img width="714" alt="imagen" src="https://github.com/Omimacgithub/summit_xl_rosmc/assets/90336442/663464ee-2e83-49d0-8ce9-d1016fa85f96">

Also comment the launch line for indoors and uncomment the launch line for outdoors.

Comment the following line on **robot_localization_complete.launch**:
~~~shell
nano ~/catkin_ws/src/summit_xl_common/summit_xl_localization/launch/robot_localization_complete.launch
~~~
<img width="554" alt="imagen" src="https://github.com/Omimacgithub/summit_xl_rosmc/assets/90336442/3a639d80-1148-46a2-8f38-cefb8fbdaea1">
