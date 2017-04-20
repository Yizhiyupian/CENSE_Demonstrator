#from World.world import World
from RTDE_Interface import RTDE_Controller_CENSE as rtde
from Drahterfassung_OpenCV import Main_Vision as vision
import math

World = None


class RealWorld(World):
    pi = math.pi
    scaling_constant = 1
    turn_constant = 45

    def move_right(self):
        current_pos = rtde.current_position()
        current_pos[0] -= 1*RealWorld.scaling_constant
        pass

    def move_left(self):
        current_pos = rtde.current_position()
        current_pos[0] += 1*RealWorld.scaling_constant
        pass

    def move_up(self):
        current_pos = rtde.current_position()
        current_pos[1] -= 1*RealWorld.scaling_constant
        pass

    def turn_clockwise(self):
        current_pos = rtde.current_position()
        current_pos[5] += RealWorld.pi*RealWorld.turn_constant/180
        pass

    def move_down(self):
        current_pos = rtde.current_position()
        current_pos[1] += 1*RealWorld.scaling_constant
        pass

    def turn_counter_clockwise(self):
        current_pos = rtde.current_position()
        current_pos[5] -= RealWorld.pi*RealWorld.turn_constant/180
        pass

    def get_state(self, coordinates):
        # Ich weiss nicht was ich hier machen soll oder welche koordinaten sind in coordinates gespeichert.
        pass

    def go_to_coordinates(self, coordinates):
        # Ich weiss nicht was ich hier machen soll oder welche koordinaten sind in coordinates gespeichert.
        pass

    def reset(self):
        rtde.go_start_via_path()
        pass

    def take_picture(self):
        vision.take_picture()
        pass
