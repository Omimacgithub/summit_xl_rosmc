import rospy
from rosmc_interface_msgs.srv import Mission, MissionRequest, MissionResponse
from rafcon.utils import log
logger = log.get_logger(__name__)


def handle_mission_request(req):
    logger.debug("Called handle_mission_request")
    #logger.debug("req: " + str(req))
    return MissionResponse()


def mission_executor(state, agent_name):
    # init_node is not required as the init_ros_node state creates a node already
    #rospy.init_node(agent_name)
    service = rospy.Service(agent_name + '/mission', Mission, handle_mission_request)
    state.logger.debug("Ready to get mission executor requests.")
    # spin is not necessary in rafcon! basically, it only prevents the calling thread from exiting
    #rospy.spin()
    return service

def execute(self, inputs, outputs, gvm):
    self.logger.debug("advertise mission service ...")
    service = mission_executor(self, "mission_advertiser1")
    service_list = gvm.get_variable("service_list", per_reference=True, default=[])
    service_list.append(service)
    gvm.set_variable("service_list", service_list, per_reference=True)
    return 0
