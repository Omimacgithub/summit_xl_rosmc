import rospy
from rosmc_interface_msgs.msg import ActionStatus
from rosmc_interface_msgs.srv import UpdateActionStatus, UpdateActionStatusRequest
from rosmc_interface_msgs.mission_utils import append_update_action_status_request


def execute(self, inputs, outputs, gvm):
    current_action_id = gvm.get_variable("current_action_id", per_reference=True, default='')
    req = UpdateActionStatusRequest()
    req.action_id = current_action_id
    req.updated_status.value = ActionStatus.FAILURE

    # Append request to global variable
    append_update_action_status_request(self, gvm, req)
    return 0
