import time
import ast
import yaml

import rafcon
import rospy
from rosmc_interface_msgs.srv import Mission, MissionRequest, MissionResponse
from rafcon.utils import log
logger = log.get_logger("mission_service_advertiser")


class MissionService:

    def __init__(self, agent_name, process_name, gvm):
        self.agent_name = agent_name
        self.process_name = process_name
        self.gvm = gvm
        self.is_initial_mission = False
        self.is_new_mission = False
        self.actions_dict = dict()

        service = rospy.Service('send_mission', Mission, self.handle_mission_update_request)
        logger.debug("Ready to get mission executor requests.")

        service_list = gvm.get_variable("service_list", per_reference=True, default=[])
        service_list.append(service)
        gvm.set_variable("service_list", service_list, per_reference=True)

    def handle_mission_update_request(self, req):
        logger.debug("Called handle_mission_request")

        # --- simulator specific process from here
        if not self.gvm.get_variable("is_in_wifi_range", per_reference=False, default=True):
            return None  # Do not return MissionResponse() to raise error
        # --- simulator specific process until here

        self.actions_dict = dict()
        agents_actions = req.agents_actions
        action_index = 0
        for agent_actions in agents_actions:
            if agent_actions.agent_name == self.agent_name:
                for action in agent_actions.actions:
                    action_dict = dict()
                    action_dict["name"] = action.action_content.action_name
                    flag_dict = dict()
                    flag_dict["battery_flag"] = action.action_content.battery_flag
                    flag_dict["wlan_flag"] = action.action_content.wlan_flag
                    flag_dict["manual_flag"] = action.action_content.manual_flag
                    action_dict["flags"] = flag_dict
                    # action_dict["parameters"] = ast.literal_eval(action.action_content.parameters_yaml)
                    parameters = yaml.safe_load(action.action_content.parameters_yaml)
                    
                    # --- simulator specific process from here
                    # Remove the parameter turtle_name because it should not be assigned externally.
                    # NOTE: This is the case only for turtle_sim.
                    if "turtle_name" in parameters:
                        del parameters["turtle_name"]
                    # --- simulator specific process until here
                    
                    action_dict["parameters"] = parameters
                    action_dict["id"] = action.action_id
                    # self.actions_dict[action.action_id] = action_dict
                    self.actions_dict[action_index] = action_dict
                    action_index += 1

        # Check if the mission is received for the first time
        is_initial_mission = not self.gvm.variable_exist("current_mission")

        # Check if the updated mission is new mission or just modification
        is_new_mission = self.check_is_new_mission(self.gvm.get_variable("current_mission", default={}), self.actions_dict)

        # Set global variables
        self.gvm.set_variable("current_mission", self.actions_dict)
        self.gvm.set_variable("sync_ids_list", req.sync_ids_list)
        
        # this, eventually, will trigger this state to finish execution
        self.is_initial_mission = is_initial_mission
        self.is_new_mission = is_new_mission

        logger.info("is initial mission: {}".format(str(self.is_initial_mission)))
        logger.info("is new mission: {}".format(str(self.is_new_mission)))
        
        return MissionResponse()

    def check_is_new_mission(self, previous_mission, requested_mission):
        """
        Check if requested_mission is modification from previous_mission or totally new mission.
        The following actions are considered to be modification, not new mission:
            - add action
            - delete action
            - reorder action
        Check if ids are found or not
        :param previous_mission:
        :param requested_mission:
        :return: bool
        """
        logger.info(str(previous_mission))
        logger.info(str(requested_mission))
        is_new = False
        if len(previous_mission) >= len(requested_mission):
            id_list = [action["id"] for key, action in previous_mission.iteritems()]
            for key, action in requested_mission.iteritems():
                is_new = is_new or not action["id"] in id_list
        else:
            id_list = [action["id"] for key, action in requested_mission.iteritems()]
            for key, action in previous_mission.iteritems():
                is_new = is_new or not action["id"] in id_list
        return is_new


def execute(self, inputs, outputs, gvm):
    self.logger.debug("advertise mission service ...")
    m = MissionService(inputs["agent_name"], inputs["process_name"], gvm)

    """
    global is_new_mission
    while not is_new_mission:
        # use preemptive wait instead of sleep; otherwise the state does it not responsive to the execution engine
        if self.preemptive_wait(0.1):
            return -2
    
    return 0
    """

    # case 1: mission update
    # - update the mission in the gvm
    # - we stay inside this state

    # case 2: new mission
    # - update the mission in the gvm
    # - leave this state, thus preempt the mission executor

    # case 3: pause + resume
    # - wait for the signal that execution resumes (wait_for_unpause(), if self.paused())
    # - we stay inside this state

    # case 4: pause + mission update(s) + resume
    # - on mission update: we update the mission in gvm
    # - wait for the signal that execution resumes (wait_for_unpause(), if self.paused())
    # - we stay inside this state

    # case 5: pause + new mission(s) + resume
    # - during pause: we stay inside the state
    # - on mission update: we update the mission in gvm
    # - after resume: we leave the state

    while not (m.is_new_mission or m.is_initial_mission):
        # logger.info("cp0")  # for debugging only
        if self.wait_for_interruption(gvm.get_variable("global_timeout")):
            if self.preempted:
                return -2
            if self.paused:
                # logger.info("cp1")  # for debugging only
                self.wait_for_unpause(gvm.get_variable("global_timeout"))
    if m.is_new_mission:
        rafcon.core.singleton.state_machine_execution_engine.start()
        return "new_mission"
    elif m.is_initial_mission:
        return "initial_mission"
    else:
        self.logger.error("Unexpected sequence")
        return -1

