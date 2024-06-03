import time
import rafcon
import rospy
from rosmc_interface_msgs.msg import ActionStatus
from rosmc_interface_msgs.srv import TriggerMissionExecutor, TriggerMissionExecutorRequest, TriggerMissionExecutorResponse, UpdateActionStatus, UpdateActionStatusRequest
from rafcon.utils import log

logger = log.get_logger("command_observer_advertiser")


class CommandObserver:

    def __init__(self, agent_name, process_name, gvm):
        self.agent_name = agent_name
        self.process_name = process_name
        self.gvm = gvm
        self.requested_state = None

        service = rospy.Service('trigger_mission_executor',
                                TriggerMissionExecutor, self.handle_trigger_mission_executor_request)
        logger.debug("Ready to get mission executor requests.")

        service_list = gvm.get_variable("service_list", per_reference=True, default=[])
        service_list.append(service)
        gvm.set_variable("service_list", service_list, per_reference=True)

    def handle_trigger_mission_executor_request(self, req):
        logger.debug("Called handle_trigger_mission_executor_request")
        res = TriggerMissionExecutorResponse()

        # Fails if agent is outside of wifi range
        if not self.gvm.get_variable("is_in_wifi_range", per_reference=False, default=True):
            res.msg = "Connection failed because the agent is outside of wifi range."
            res.success = False
            return res

        # Process only if the request is coming from the corresponding agent
        if req.agent_name == self.agent_name:
            if req.trigger == TriggerMissionExecutorRequest.RUN:
                self.requested_state = "run"
            elif req.trigger == TriggerMissionExecutorRequest.PAUSE:
                self.requested_state = "pause"
            elif req.trigger == TriggerMissionExecutorRequest.STOP:
                self.requested_state = "stop"
            elif req.trigger == TriggerMissionExecutorRequest.RESET:
                self.requested_state = "reset"
            else:
                logger.error("Unexpeced request")
            self.gvm.set_variable("requested_state", self.requested_state)
            res.success = True
            return res
        else:
            logger.error("No corresponding agent found: {}".format(req))
            res.msg = "No corresponding agent found."
            res.success = False
            return res


def execute(self, inputs, outputs, gvm):
    self.logger.debug("Wait for new execution commands ...")
    command_observer = CommandObserver(inputs["agent_name"], inputs["process_name"], gvm)

    while True:
        # use preemptive wait instead of sleep; otherwise the state does it not responsive to the execution engine
        if self.wait_for_interruption(gvm.get_variable("global_timeout")):
            if self.preempted:
                return -2
            if self.paused:
                self.wait_for_unpause(0.2)
                if self.preempted:
                    return -2
