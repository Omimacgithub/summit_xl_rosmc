import rospy
from rosmc_interface_msgs.msg import ActionStatus
from rosmc_interface_msgs.srv import UpdateActionStatus, UpdateActionStatusRequest


def execute(self, inputs, outputs, gvm):
    update_action_status_service_proxy = rospy.ServiceProxy(
        '{}update_action_status'.format(gvm.get_variable("mission_server_namespace", per_reference=False, default="mission_control")),
        UpdateActionStatus)
    actions = gvm.get_variable("current_mission", default={})
    for key in reversed(actions.keys()):
        action = actions[key]
        action_id = action["id"]
        req = UpdateActionStatusRequest()
        req.action_id = action_id
        req.updated_status.value = ActionStatus.IDLE
        update_action_status_service_proxy(req)
    return 0