# mission_control_rafcon_statemachines
This repo contains all common rafcon statemachines which are used in context with mission control, namely interfacing with [ROSMC](https://github.com/DLR-RM/rosmc).

The structure of this repository is as follows:
* **mission_executor**: RACON statemachine which communicates with ROSMC
* **template**: example of robot-specific RAFCON statemachines used in 'mission_executor'

## How it works?
We use the same statemachine 'mission_executor' for every robot.
To achieve this, a RAFCON config file `config.yaml` needs to be prepared like the following example:
```yaml
LIBRARY_PATHS:
    VIRTUAL_LINK_TO_ACTIONS: /PATH/TO/THIS/REPO/template
    mission_control: /PATH/TO/THIS/REPO
    ...
    #(and other libraries necessary to compose high-level skills!)
    ...
```

**The library name 'VIRTUAL_LINK_TO_ACTIONS' is reserved and should not be changed.**
The 'mission_executor' inside the library 'mission_control' includes a robot-specific statemachines as a library named 'VIRTUAL_LINK_TO_ACTIONS'.

Therefore, 'mission_executor' can be instantiated for different robots by changing the reference of 'VIRTUAL_LINK_TO_ACTIONS' in your rafcon config file.


## Get started on your system
It is recommended to use Git submodule.
Suppose you implement your robot-specific statemachines in '/home/proj_statemachines'.
First, we clone this repo as a Git submodule;
* `cd /home/proj_statemachines`
* `git submodule init` (only once per local repository)
* `git submodule add https://github.com/DLR-RM/mission_control_rafcon_statemachines.git modules/mission_control`

This module also requires the ROS module;
* `git submodule add https://github.com/DLR-RM/RAFCON-ros-state-machines.git modules/ros`

Then, copy 'template' into '/home/proj_statemachines', adjust RAFCON config file, and start RAFCON;
* `cp -r /PATH/TO/THIS/REPO/template/* /home/proj_statemachines/mission_control_interface/`
* Adjust your RAFCON config file, e.g.
    ```yaml
    LIBRARY_PATHS:
        VIRTUAL_LINK_TO_ACTIONS: /home/proj_statemachines/mission_control_interface
        modules: /home/proj_statemachines/modules
        mission_control_interface: /home/proj_statemachines/mission_control_interface
        ...
        #(and other libraries necessary to compose high-level skills!)
        ...
    ```
* Start RAFCON with the config file
* Open the statemachine 'modules/mission_control/mission_executor/mission_executor'

Now your 'mission_executor' is configured with /home/proj_statemachines/mission_control_interface.
Therefore, the last step is to adjust/implement this interface RAFCON library.
Inside the copy of the template (here we named it as 'mission_control_interface') are organized as follows:
- **'initialize'**: custom initialization procedures
- **'custom\_observer'**: custom observer procedures
- **'custom\_mission\_preemption\_handler'**: custom mission preemption procedures
- **'decider'**: statemachine which parses mission data and triggers the next skill to execute
- **'robot_skills'**:
  - robot-specific high-level skills
  - these statemachines are used as a library in the 'decider'. Therefore, **if you add/delete/rename skills or change input parameters of them, you also need to adapt the 'decider' accordingly**.

## Examples of integration
For more concrete examples, please refer to
* [rosmc_turtlesim_statemachines](https://github.com/DLR-RM/rosmc_turtlesim_statemachines): integration with turtlesim
