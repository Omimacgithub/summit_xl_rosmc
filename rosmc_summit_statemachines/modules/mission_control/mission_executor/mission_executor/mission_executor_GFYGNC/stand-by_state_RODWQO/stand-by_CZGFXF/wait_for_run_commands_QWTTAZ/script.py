import time
import rafcon
import rospy
from rosmc_interface_msgs.srv import TriggerMissionExecutor, TriggerMissionExecutorRequest, TriggerMissionExecutorResponse
# import arches_high_level_status.msg
from rafcon.utils import log

logger = log.get_logger("wait_for_run_commands")


class CommandObserver:

    def __init__(self, gvm):
        self.gvm = gvm
        
        # Initialization of global variables
        self.requested_state = None
        self.is_in_wifi_range = None

        self.is_started = False
        self.timer = rospy.Timer(rospy.Duration(1 / 10.), self.timer_cb)

    def timer_cb(self, _event):
        self.listen_to_global_variables()
        if self.is_in_wifi_range and self.requested_state == "run":
            self.is_started = True
    
    def listen_to_global_variables(self):
        self.is_in_wifi_range = self.gvm.get_variable("is_in_wifi_range", per_reference=False, default=True)
        self.requested_state = self.gvm.get_variable("requested_state", per_reference=False, default=None)


def execute(self, inputs, outputs, gvm):
    self.logger.debug("Wait for new execution commands ...")
    command_observer = CommandObserver(gvm)

    while True:
        if command_observer.is_started:
            return 0
        if self.wait_for_interruption(0.1):
            if self.preempted:
                return -2
            if self.paused:
                self.wait_for_unpause()
                if self.preempted:
                    return -2
