import time
import rospy
import std_msgs.msg
from rosmc_interface_msgs.msg import ActionStatus
from rosmc_interface_msgs.srv import UpdateActionStatus, UpdateActionStatusRequest
from rosmc_interface_msgs.mission_utils import append_update_action_status_request


# function to check if id is included in sync_ids_list
def get_sync_ids(action_id, sync_ids_list):
    for sync_ids in sync_ids_list:
        if action_id in sync_ids.sync_ids:
            sync_ids_ = sync_ids.sync_ids
            sync_ids_.remove(action_id)
            return sync_ids_
    return None


def map_parameters(parameter_dict, outputs, logger):
    i = 0
    for k, v in sorted(parameter_dict.items()):
        # i is an index starting at 0, k is the key, v is the value
        # the key is not of interest here, the mapping is assumed to be alphabetically
        # outputs["param" + str(i)] = v
        outputs["param" + str(i)] = v["value"]
        logger.debug("param" + str(i) + ": " + str(v))
        i += 1


# this is only for debugging purposes
def generate_default_action_dict():
    action_dict = dict()
    action_dict["name"] = "test_name"
    flag_dict = dict()
    flag_dict["battery_flag"] = True
    flag_dict["wlan_flag"] = False
    flag_dict["manual_flag"] = True
    action_dict["flags"] = flag_dict
    action_dict["parameters"] = {"param-one": 1, "param-two": True}
    #self.actions_dict[action.action_id] = action_dict
    actions_dict = dict()
    actions_dict[0] = action_dict
    return actions_dict


class ActionSynchronizer(object):

    def __init__(self, action_id, gvm):
        self.action_id = action_id

        # publisher tell current action is ready to start
        self.pub = rospy.Publisher('is_ready_for_sync', std_msgs.msg.String, queue_size=10)

        # subscribers to know other actions are ready to start
        self.sub_list = []
        self.ready_ids = [self.action_id]
        agent_library_dict = rospy.get_param('{}agent_library_dict'.format(gvm.get_variable("mission_server_namespace", per_reference=False, default="/mission_control/")))
        for agent_name in agent_library_dict:
            if agent_name == rospy.get_namespace():
                continue
            sub = rospy.Subscriber('/{}/is_ready_for_sync'.format(agent_name), std_msgs.msg.String, self.sync_id_callback)
            self.sub_list.append(sub)

    def sync_id_callback(self, msg):
        # update self.ready_ids
        if msg.data not in self.ready_ids:
            self.ready_ids.append(msg.data)


def execute(self, inputs, outputs, gvm):
    self.logger.debug("Executing decider state")
    default_action_dict = {}
    actions = gvm.get_variable("current_mission", default=generate_default_action_dict())
    if len(actions) == 0:
        self.logger.warn("no action in current_mission")
        return "no_action_in_mission"
    for action_index, action in actions.iteritems():
        self.logger.debug("action_index: " + str(action_index))
        self.logger.debug("action: " + str(action))
    current_action = actions[inputs["current_index"]]
    map_parameters(current_action["parameters"], outputs, self.logger)

    # store current action id as global variable
    current_action_id = current_action["id"]
    gvm.set_variable("current_action_id", current_action_id, per_reference=True)
    # update the state of action from idle to running
    req = UpdateActionStatusRequest()
    req.action_id = current_action_id

    # If current_action_id is included in sync_ids_list, wait for other agents to finish actions
    sync_ids_list = gvm.get_variable("sync_ids_list", list())
    sync_ids = get_sync_ids(current_action_id, sync_ids_list)
    if sync_ids is not None:
        # update the state of action from idle to sync_waiting
        req.updated_status.value = ActionStatus.SYNCWAITING
        append_update_action_status_request(self, gvm, req)
        # instantiate a class to publish/subscribe msg to wait for all actions to be ready to start
        action_synchronizer = ActionSynchronizer(current_action_id, gvm)
        gvm.set_variable("is_sync_waiting", True)  # set global variable to change behavior of buttons of MCG
        while not set(sync_ids).issubset(set(action_synchronizer.ready_ids)):
            action_synchronizer.pub.publish(current_action_id)
            self.logger.debug('ready_ids: {}'.format(action_synchronizer.ready_ids))
            self.logger.debug('sync_ids: {}'.format(sync_ids))
            if self.wait_for_interruption(gvm.get_variable("global_timeout")):
                if self.preempted:
                    return -2
                if self.paused:
                    self.wait_for_unpause()
        action_synchronizer.pub.publish(current_action_id)
        gvm.set_variable("is_sync_waiting", False)  # set global variable to change behavior of buttons of MCG

    # update the state of action from idle to running
    req.updated_status.value = ActionStatus.RUNNING
    # Append request to global variable
    append_update_action_status_request(self, gvm, req)

    # TODO: reactive battery recharge should be implemented here?

    # comment out for debug purposes
    outputs["outcome_name"] = current_action["name"]
    return "success"
    #time.sleep(1.0)
    #return "test_loop"


