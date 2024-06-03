
def execute(self, inputs, outputs, gvm):
    list_pose = inputs["list_pose"]
    
    # assumes list_pose has 4 elements
    assert len(list_pose) == 4
    
    outputs["x_pos_1"] = list_pose[0]['x']
    outputs["y_pos_1"] = list_pose[0]['y']
    outputs["1"] = 1.0
    outputs["x_pos_2"] = list_pose[1]['x']
    outputs["y_pos_2"] = list_pose[1]['y']
    outputs["x_pos_3"] = list_pose[2]['x']
    outputs["y_pos_3"] = list_pose[2]['y']
    outputs["-1"] = -1.0
    outputs["x_pos_4"] = list_pose[3]['x']
    outputs["y_pos_4"] = list_pose[3]['y']
    return 0
