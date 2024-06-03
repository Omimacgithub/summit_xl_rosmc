import os

def execute(self, inputs, outputs, gvm):
    
    import os
    outputs["agent_name"] = os.environ['ROS_NAMESPACE']
    
    return "success"
