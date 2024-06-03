import rospy
from rosmc_interface_msgs.msg import ActionStatus
from rosmc_interface_msgs.srv import UpdateActionStatus, UpdateActionStatusRequest
from rafcon.utils import log

gv_name = "update_action_status_request_list"
logger = log.get_logger("update_action_status_handler")


class UpdateActionStatusHandler:

    def __init__(self, process_name, gvm):
        self.process_name = process_name
        self.gvm = gvm
        self.gvm.set_variable(key=gv_name, value=[])

        self.update_action_status_service_proxy = rospy.ServiceProxy(
            '{}update_action_status'.format(self.gvm.get_variable("mission_server_namespace", per_reference=False, default="/mission_control/")),
            UpdateActionStatus)

        #self.timer = rospy.Timer(rospy.Duration(1 / 2.), self.timer_cb)
        self.timer = rospy.Timer(rospy.Duration(2.), self.timer_cb)

    def timer_cb(self, _event):
        if self.gvm.is_locked(gv_name):
            logger.warn("Global variable " + gv_name + " is locked. Wait for being unlocked...")
            return

        logger.debug("Acquired lock of " + gv_name)
        access_key = self.gvm.lock_variable(key=gv_name, block=True)
        update_action_status_request_list = self.gvm.get_locked_variable(gv_name, access_key)

        while update_action_status_request_list:
            req = update_action_status_request_list.pop(0)
            # Try to call UpdateActionStatus service
            try:
                # --- simulator specific process from here
                if not self.gvm.get_variable("is_in_wifi_range", per_reference=False, default=True):
                    # Do not call UpdateActionStatus service and raise error
                    raise rospy.ServiceException("Cannot call service due to network error.")
                # --- simulator specific process until here

                logger.info("Update status of action id: " + req.action_id)
                self.update_action_status_service_proxy(req)

            except rospy.ServiceException as exc:
                logger.warn("Unable to call UpdateActionStatus service: " + str(exc))
                # revert popping
                update_action_status_request_list.insert(0, req)
                break

        # reset global variable
        self.gvm.set_locked_variable(key=gv_name, access_key=access_key,
                                     value=update_action_status_request_list)
        # unlock
        self.gvm.unlock_variable(key=gv_name, access_key=access_key)
        logger.debug("Released lock of " + gv_name)


def execute(self, inputs, outputs, gvm):
    self.logger.debug("Handle update action status service calls")
    update_action_status_handler = UpdateActionStatusHandler(inputs["process_name"], gvm)

    try:
        while True:
            # use preemptive wait instead of sleep; otherwise the state does it not responsive to the execution engine
            #self.logger.debug("Debug A")
            if self.wait_for_interruption(gvm.get_variable("global_timeout")):
                #self.logger.debug("Debug B")
                if self.preempted:
                    #self.logger.debug("Debug C")
                    return -2
                if self.paused:
                    #self.logger.debug("Debug D")
                    #self.wait_for_unpause(0.2)
                    self.wait_for_unpause(2)
                    if self.preempted:
                        #self.logger.debug("Debug E")
                        return -2
    finally:
        update_action_status_handler.timer.shutdown()  # shutdown timer + callback
