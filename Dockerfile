#docker run --name prueba3 --rm -ti -v /tmp/.X11-unix:/tmp/.X11-unix fail bash
#TODO: Meter la imagen en un docker-compose
#TODO: rviz_satellite
#X display: https://gursimarsm.medium.com/run-gui-applications-in-a-docker-container-ca625bad4638
FROM robotnik/summit-xl-sim:melodic-devel
USER 0
RUN apt-get update \
	&& apt-get install -y python-pip glade python-gi-cairo libgirepository1.0-dev python-tk gir1.2-gtksource-3.0
USER robot
ENV CK_DIR /home/robot/catkin_ws
WORKDIR $CK_DIR 
SHELL ["/bin/bash", "-c"]
#Make PATH ENV persistent
RUN echo "export PATH="$HOME/.local/bin:$PATH"" >> ~/.profile \
	&& source ~/.profile
#TODO: fichero /home/robot/.local/lib/python2.7/site-packages/yaml_configuration/config.py
COPY requirements.txt $CK_DIR 
RUN pip install --upgrade pip setuptools \
	&& pip install -r requirements.txt --user 
WORKDIR $CK_DIR/src
RUN git clone https://github.com/DLR-RM/rosmc_interface_msgs.git \
	&& git clone https://github.com/Omimacgithub/summit_xl_rosmc.git
WORKDIR $CK_DIR
RUN source devel/setup.bash \
	&& catkin_make summit_xl_rosmc/rosmc \
	&& catkin_make install \
	&& source devel/setup.bash
