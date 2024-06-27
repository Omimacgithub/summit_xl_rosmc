FROM robotnik/summit-xl-sim:melodic-devel
#Install RAFCON dependencies and nano
ARG user_name=robot
ARG user_home=/home/$user_name
ARG ck_dir=$user_home/catkin_ws
ARG ck_src_dir=$ck_dir/src
USER 0
RUN apt-get update \
	&& apt-get install -y python-pip glade python-gi-cairo libgirepository1.0-dev python-tk gir1.2-gtksource-3.0 nano
USER $user_name
WORKDIR $ck_dir
#Change to bash shell (for source commands to work)
SHELL ["/bin/bash", "-c"]
#Make PATH ENV persistent
RUN echo "export PATH="$HOME/.local/bin:$PATH"" >> ~/.profile \
	&& source ~/.profile
#Install requirements
COPY requirements.txt $ck_dir 
RUN pip install --upgrade pip setuptools \
	&& pip install -r requirements.txt --user 
WORKDIR $ck_src_dir
#Clone repos
RUN git clone https://github.com/DLR-RM/rosmc_interface_msgs.git \
	&& git clone https://github.com/Omimacgithub/summit_xl_rosmc.git \
	&& git clone --branch ros1 https://github.com/nobleo/rviz_satellite.git
WORKDIR $ck_dir
#Build repos
RUN source devel/setup.bash \
	&& catkin_make summit_xl_rosmc/rosmc rviz_satellite \
	&& catkin_make install \
	&& source devel/setup.bash
#RAFCON config file
COPY config.py $user_home/.local/lib/python2.7/site-packages/yaml_configuration/config.py
#Copy ekf localization files
COPY resources/gps_localization/* $ck_src_dir/summit_xl_common/summit_xl_localization/launch/
#Copy blank map
COPY resources/blank_map.pgm $ck_src_dir/summit_xl_common/summit_xl_localization/maps/empty/map_empty.pgm
#Copy gazebo worlds
COPY resources/gazebo_worlds/* $ck_src_dir/summit_xl_gazebo/worlds/
#Copy bringup config
COPY resources/summit_xl_complete.launch $ck_src_dir/summit_xl_sim_bringup/launch/summit_xl_complete.launch

CMD /bin/bash
