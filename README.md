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

To start rosmc on simulation:
~~~shell
chmod +x simlaunch.sh
./simlaunch.sh
~~~

To start rosmc on real Summit_XL:
~~~shell
chmod +x launch.sh
./launch.sh
~~~

## Docker
The root Dockerfile used is located [here](https://github.com/RobotnikAutomation/summit_xl_sim)

~~~shell
docker compose up
~~~

To stop the container
~~~shell
docker stop rosmc-base
~~~
To start the container
~~~shell
docker start rosmc-base
docker attach rosmc-base
~~~
To launch a new separated instance (note that if you close the terminal running the docker attach, all container instances would terminate)
~~~shell
docker exec -it rosmc-base bash
~~~

## Using outdoors localization (only simulation):

On **simlaunch.sh** file:
~~~shell
nano ~/catkin_ws/src/summit_xl_rosmc/simlaunch.sh
~~~

- Uncomment the blank_map line:

<img width="714" alt="imagen" src="https://github.com/Omimacgithub/summit_xl_rosmc/assets/90336442/663464ee-2e83-49d0-8ce9-d1016fa85f96">

- Comment the launch line for indoors
- Uncomment the launch line for outdoors

Comment the following line on **robot_localization_complete.launch**:
~~~shell
nano ~/catkin_ws/src/summit_xl_common/summit_xl_localization/launch/robot_localization_complete.launch
~~~
<img width="554" alt="imagen" src="https://github.com/Omimacgithub/summit_xl_rosmc/assets/90336442/3a639d80-1148-46a2-8f38-cefb8fbdaea1">
