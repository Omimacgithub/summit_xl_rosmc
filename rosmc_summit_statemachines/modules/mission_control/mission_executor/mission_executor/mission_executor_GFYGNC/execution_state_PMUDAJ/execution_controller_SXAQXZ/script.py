import time
import rafcon
import rospy
from rosmc_interface_msgs.msg import ActionStatus
from rosmc_interface_msgs.srv import TriggerMissionExecutor, TriggerMissionExecutorRequest, TriggerMissionExecutorResponse, UpdateActionStatus, UpdateActionStatusRequest
from rafcon.utils import log

from rosmc_interface_msgs.mission_utils import append_update_action_status_request

logger = log.get_logger("execution controller")


class ExecutionController:
    """
    Listens to global variables related to execution status via rospy.Timer
    (in order to update regardless of execution status of RAFCON SM).
    Depending on the status, control SM execution.
    """

    def __init__(self, executor, process_name, gvm):
        self.executor = executor
        self.process_name = process_name
        self.gvm = gvm

        # Initialize global variables
        self.is_in_wifi_range = None
        self.is_in_wifi_range_with_margin = None
        self.requested_state = None
        self.is_mission_finished = None
        self.current_mission = None
        self.current_action_id = None
        self.index_when_stopped = None
        self.is_sync_waiting = None
        self.listen_to_global_variables()

        # Execution engine to control execution status of rafcon
        self.execution_engine = rafcon.core.singleton.state_machine_execution_engine

        # Define status as follows
        # - running: status reached first when this sm is entered. Action is being executed in this status.
        # - idle: status reached after pressing "stop". Idle actions remain synchronized and ready to be started.
        # - paused: status reached by pressing pause button only when status is running
        # - reactive_paused: status reached if wifi flag is True and not self.is_in_wifi_range_with_margin
        # - reset: status reached by pressing reset button
        if self.gvm.get_variable("is_reactive_preemption_required", per_reference=False, default=False):
            logger.info("Pause and set self.status as reactive_paused!")
            self.execution_engine.pause()
            self.status = "reactive_paused"
        else:
            self.status = "running"

        # Mutex for self.update()
        self.update_mutex = False

        # Timer for updating members from global variables
        self.timer = rospy.Timer(rospy.Duration(gvm.get_variable("global_timeout")), self.timer_cb)

    def timer_cb(self, _event):
        """
        Listens to global variables related to execution status via rospy.Timer
        :param _event:
        :return:
        """
        logger.debug("ExecutionController.timer_cb is called")
        self.listen_to_global_variables()
        self.update()

    def listen_to_global_variables(self):
        logger.debug("ExecutionController.listen_to_global_variables is called")
        self.is_in_wifi_range = self.gvm.get_variable("is_in_wifi_range", per_reference=False, default=True)
        self.is_in_wifi_range_with_margin = self.gvm.get_variable("is_in_wifi_range_with_margin", per_reference=False,
                                                                  default=True)
        self.requested_state = self.gvm.get_variable("requested_state", per_reference=False, default=None)
        self.is_mission_finished = self.gvm.get_variable("is_mission_finished", per_reference=False, default=False)
        self.current_mission = self.gvm.get_variable("current_mission", per_reference=False, default=None)
        self.current_action_id = self.gvm.get_variable("current_action_id", per_reference=False, default=None)
        self.index_when_stopped = self.gvm.get_variable("index_when_stopped", per_reference=False, default=None)
        self.is_sync_waiting = self.gvm.get_variable("is_sync_waiting", per_reference=False, default=False)

    def get_current_action(self):
        if self.current_mission is None:
            return None
        for action_index in self.current_mission:
            action_dict = self.current_mission[action_index]
            if self.current_action_id is None:
                return None
            if action_dict["id"] != self.current_action_id:
                continue
            return action_dict
        return None

    def is_reactive_preemption_required(self):
        current_action = self.get_current_action()
        if current_action is None:
            return False
        else:
            return current_action["flags"]["wlan_flag"] and (not self.is_in_wifi_range_with_margin)

    def update(self):
        logger.debug("ExecutionController.update is called")
        logger.debug("ExecutionController.status is " + self.status)

        # Check mutex
        if self.update_mutex:
            return

        # Get mutex
        self.update_mutex = True

        def make_status_idle():
            # Update action status
            self.update_current_action_status(ActionStatus.IDLE_SYNCHRONISED)
            # set global variables
            for action_index in self.current_mission:
                action_dict = self.current_mission[action_index]
                if action_dict["id"] != self.current_action_id:
                    continue
                self.gvm.set_variable("index_when_stopped", action_index)
                break
            # self.gvm.set_variable("current_action_id", "")
            self.execution_engine.pause()
            self.status = "idle"
            return

        if self.status == "running":  # Case of status is "running"
            # NOTE: "running" status has following sub-statuses:
            # 1. self.is_mission_finished
            if self.is_mission_finished:
                if self.requested_state == "run":
                    if self.is_new_action_waiting():  # resume only if next action exists
                        self.execution_engine.start()
                elif self.requested_state == "reset":
                    self.execution_engine.start()
                    self.status = "reset"
            # 2. NOT self.is_mission_finished AND self.is_sync_waiting
            elif self.is_sync_waiting:
                if self.requested_state == "run":
                    pass
                elif self.requested_state == "pause":
                    self.update_current_action_status(ActionStatus.PAUSED)  # update action status
                    self.execution_engine.pause()  # pause execution
                    self.status = "paused"
                elif self.requested_state == "stop":
                    self.gvm.set_variable("is_sync_waiting", False)
                    make_status_idle()
                elif self.requested_state == "reset":
                    self.gvm.set_variable("is_sync_waiting", False)
                    self.execution_engine.start()
                    self.status = "reset"
            # 3. NOT self.is_mission_finished AND NOT self.is_sync_waiting
            else:
                if self.is_reactive_preemption_required():
                    self.execution_engine.pause()  # pause execution
                    self.status = "reactive_paused"
                elif self.requested_state == "run":
                    pass
                elif self.requested_state == "pause":
                    self.update_current_action_status(ActionStatus.PAUSED)  # update action status
                    self.execution_engine.pause()  # pause execution
                    self.status = "paused"
                elif self.requested_state == "stop":
                    make_status_idle()
                elif self.requested_state == "reset":
                    self.execution_engine.start()
                    self.status = "reset"

        elif self.status == "paused":  # Case of status is "paused"
            # NOTE: "running" status has following sub-statuses:
            # 1. self.is_sync_waiting
            if self.is_sync_waiting:
                if self.requested_state == "run":
                    self.update_current_action_status(ActionStatus.SYNCWAITING)  # update action status
                    self.execution_engine.pause()
                    self.status = "running"
                elif self.requested_state == "pause":
                    pass
                elif self.requested_state == "stop":
                    self.gvm.set_variable("is_sync_waiting", False)
                    make_status_idle()
                elif self.requested_state == "reset":
                    self.gvm.set_variable("is_sync_waiting", False)
                    self.execution_engine.start()
                    self.status = "reset"
            # 2. NOT self.is_sync_waiting
            else:
                if self.is_reactive_preemption_required():
                    pass
                elif self.requested_state == "run":
                    self.update_current_action_status(ActionStatus.RUNNING)  # update action status
                    self.execution_engine.start()  # start execution
                    self.status = "running"
                elif self.requested_state == "pause":
                    pass
                elif self.requested_state == "stop":
                    make_status_idle()
                elif self.requested_state == "reset":
                    self.execution_engine.start()
                    self.status = "reset"

        elif self.status == "idle":  # Case of status is "idle"
            # NOTE: This status must just execute the following command triggered by external signals
            #  - self.timer.shutdown()
            #  - self.execution_engine.start()
            # because this SM must be left with "stop" outcome

            # NOTE: "running" status has two sub-statuses:
            # 1. self.is_mission_finished
            if self.is_mission_finished:
                logger.error("This condition should not be met. Force reset.")
                self.status = "reset"
            # 2. NOT self.is_mission_finished
            else:
                if self.requested_state == "run":
                    self.timer.shutdown()
                    self.execution_engine.start()  # start execution
                    self.status = "running"
                elif self.requested_state == "pause":
                    pass
                elif self.requested_state == "stop":
                    pass
                elif self.requested_state == "reset":
                    self.timer.shutdown()
                    self.execution_engine.start()
                    self.status = "reset"

        elif self.status == "reactive_paused":  # Case of status is "reactive_paused"
            if not self.is_reactive_preemption_required():  # Different condition from other status. Check if can be resumed or not
                self.execution_engine.start()  # start execution
                self.status = "running"
            elif self.requested_state == "run":
                pass
            elif self.requested_state == "pause":
                pass
            elif self.requested_state == "stop":
                make_status_idle()
            elif self.requested_state == "reset":
                self.execution_engine.start()
                self.status = "reset"

        elif self.status == "reset":  # Case of status is "reset"
            if self.is_reactive_preemption_required():
                pass
            elif self.requested_state == "run":
                pass
            elif self.requested_state == "pause":
                pass
            elif self.requested_state == "stop":
                pass
            elif self.requested_state == "reset":
                pass

        # Set global variables
        self.gvm.set_variable("is_reactive_preemption_required", self.is_reactive_preemption_required())

        # Release mutex
        self.update_mutex = False

    def is_new_action_waiting(self):
        """
        Check if there is more than one action(s) after current_action_id
        :return:
        """
        flag = False
        for action_index in self.current_mission:
            action_dict = self.current_mission[action_index]
            if action_dict["id"] == self.current_action_id \
                and len(self.current_mission) > action_index + 1:
                flag = True
                break
        return flag

    def update_current_action_status(self, new_action_status):
        if self.current_action_id is not None \
                and self.current_action_id != "" \
                and self.current_action_id != "None":
            req = UpdateActionStatusRequest()
            req.action_id = self.current_action_id
            req.updated_status.value = new_action_status
            append_update_action_status_request(self.executor, self.gvm, req)

    def reset_requested_state(self):
        logger.debug("Reset global variable requested_state")
        if self.gvm.variable_exists("requested_state"):
            self.gvm.delete_variable("requested_state")

    def terminate(self):
        self.timer.shutdown()
        self.reset_requested_state()


def execute(self, inputs, outputs, gvm):
    self.logger.debug("Wait for new execution commands ...")
    execution_controller = ExecutionController(self, inputs["process_name"], gvm)

    while True:
        self.logger.debug("execution_controller status is {}".format(execution_controller.status))
        if execution_controller.status == "reset":
            execution_controller.terminate()
            execution_controller.execution_engine.start()
            return "reset"
        elif execution_controller.status == "idle":
            # NOTE: execution_controller.timer.shutdown() is called inside of execution_controller.timer_cb()
            return "stop"
        # use preemptive wait instead of sleep; otherwise the state does it not responsive to the execution engine
        if self.wait_for_interruption(gvm.get_variable("global_timeout")):
            if self.preempted:
                execution_controller.terminate()
                return -2
            if self.paused:
                self.wait_for_unpause(0.2)
                if self.preempted:
                    execution_controller.terminate()
                    return -2
