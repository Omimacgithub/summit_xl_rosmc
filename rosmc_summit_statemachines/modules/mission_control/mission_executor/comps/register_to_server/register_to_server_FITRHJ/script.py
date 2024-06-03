import rospy
from rosmc_interface_msgs.srv import RegisterToServer, RegisterToServerRequest


def execute(self, inputs, outputs, gvm):
    self.logger.debug("Wait for MissionServer to be ready...")
    register_to_server_name = '{}register_to_mission_server'.format(gvm.get_variable("mission_server_namespace", per_reference=False, default="/mission_control/"))
    rospy.wait_for_service(register_to_server_name)
    mission_service_name = 'send_mission'
    rospy.wait_for_service(mission_service_name)
    self.logger.debug("MissionServer is ready.")
    register_to_server = rospy.ServiceProxy(register_to_server_name, RegisterToServer)
    try:
        req = RegisterToServerRequest()
        req.process_name = inputs["process_name"]
        req.namespace = rospy.get_namespace()
        req.mission_receive_mode = RegisterToServerRequest.SYNC
        resp = register_to_server(req)
        if resp.success:
            rospy.loginfo("Connection establishment succeed")
            self.logger.info("Connection establishment succeed")
            # NOTE: namespace of mission server is not dynamically configured by RegisterToServer.srv
            #       Instead, global variable mission_server_namespace is set in initializer of each robot
            # gvm.set_variable("mission_server_namespace", resp.mission_server_namespace, per_reference=True)
        else:
            rospy.logerr("Connection establishment failed")
            self.logger.error("Connection establishment failed")
    except rospy.ServiceException as exc:
        rospy.logerr("Service did not process request: " + str(exc))
        self.logger.error("Service did not process request: {}".format(str(exc)))
        rospy.logerr("Connection establishment failed")
    return 0
