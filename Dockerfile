#START OF SUMMIT_XL_SIM_DOCKERFILE
FROM osrf/ros:melodic-desktop-full
MAINTAINER Guillem Gari <ggari@robontik.es>

# Non Root user
ARG user_name=robot
ARG user_uid=1000
ARG user_home=/home/$user_name
ARG user_shell=/bin/bash
ARG ck_dir=$user_home/catkin_ws
ARG ck_src_dir=$ck_dir/src
ARG ros_brup_pkg=rostful_bringup

RUN useradd -m -d $user_home -s $user_shell -u $user_uid $user_name \
	&& echo "PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;33m\]\u\[\033[00m\]@\[\033[01;31m\]\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> ~/.bashrc

ENV DEBIAN_FRONTEND noninteractive

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F42ED6FBAB17C654

RUN apt-get update \
	&& apt-get install -q -y \
		wget \
		apt-utils \
		# dialog \
		sudo \
		python3-vcstool \
		git \
	&& apt-get clean -q -y \
	&& apt-get autoremove -q -y \
	&& rm -rf /var/lib/apt/lists/* \
	&& echo '%robot ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN apt-get update \
	&& apt upgrade -y \
	&& apt-get clean -q -y \
	&& apt-get autoremove -q -y \
	&& rm -rf /var/lib/apt/lists/*

COPY ros-requirements.txt /tmp

RUN apt-get update \
	&& apt-get install -q -y \
	--no-install-recommends \
		$(eval "echo $(cat /tmp/ros-requirements.txt | xargs)") \
	&& apt-get clean -q -y \
	&& apt-get autoremove -q -y \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm /tmp/ros-requirements.txt

USER $user_name

RUN mkdir -p $ck_src_dir
RUN true \
	&& echo "PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]@\[\033[01;31m\]\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> ~/.bashrc \
	&& echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc \
	&& echo "source $ck_dir/devel/setup.bash" >> ~/.bashrc

ARG gazebo_model_path=$user_home/.gazebo
ARG gazebo_models_url=https://github.com/osrf/gazebo_models.git
RUN true \
	&& mkdir -p $gazebo_model_path/models \
	&& chown -R $user_name: $gazebo_model_path \
	&& git clone --depth 1 $gazebo_models_url $gazebo_model_path/models \
	&& rm -rf $gazebo_model_path/models/.git \
	&& true

WORKDIR $ck_dir

COPY --chown=$user_name \
	summit_xl_gazebo \
	$ck_src_dir/summit_xl_gazebo

COPY --chown=$user_name \
	summit_xl_sim \
	$ck_src_dir/summit_xl_sim

COPY --chown=$user_name \
	summit_xl_sim_bringup \
	$ck_src_dir/summit_xl_sim_bringup

ARG repo_file=summit_xl_sim_devel_docker.repos

COPY --chown=$user_name \
	repos/$repo_file \
	/tmp/

ARG repo_file_list_to_use=/tmp/$repo_file
ARG fresh_download_of_git_repos=no

RUN true \
	&& vcs import --input $repo_file_list_to_use \
	&& rosdep update --include-eol-distros \
	&& echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections \
	&& sudo apt-get update \
	&& rosdep install --from-paths src --ignore-src -y \
	&& sudo apt-get clean -q -y \
	&& sudo apt-get autoremove -q -y \
	&& sudo rm -rf /var/lib/apt/lists/*

RUN true \
	&& . /opt/ros/melodic/setup.sh \
	&& export ROS_PARALLEL_JOBS=-j$(nproc --all) \
	&& catkin_make

ARG ign_version=4_4.0.0
ARG ign_cfg_url=https://raw.githubusercontent.com/ignitionrobotics/ign-fuel-tools/ignition-fuel-tools$ign_version/conf/config.yaml
ARG ign_cfg_dir=$user_home/.ignition/fuel
ARG ign_cfg_file=config.yaml
ARG ign_cfg_path=$ign_cfg_dir/$ign_cfg_file
RUN mkdir -p $ign_cfg_dir \
	&& wget $ign_cfg_url -O $ign_cfg_path

ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

ENV USE_GPU_FOR_SIMULATION true

ENV ROS_BU_PKG "summit_xl_sim_bringup"
ENV ROS_BU_LAUNCH "summit_xl_complete.launch"
ENV CATKIN_WS $ck_dir
ENV RBK_CATKIN_PATH $ck_dir

#END OF SUMMIT_XL_SIM DOCKERFILE

#Install RAFCON dependencies and nano
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
