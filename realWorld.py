#from World.world import World
from RTDE_Interface import RTDE_Controller_CENSE as rtde
import math
from multiprocessing import Process
import numpy as np


class RealWorld():
    pi = math.pi
    scaling_constant = .03
    turn_constant = 45

    def move_left(self):
        current_pos = rtde.current_position()
        current_pos[0] -= RealWorld.scaling_constant
        rtde.move_to_position(current_pos)
        pass

    def move_right(self):
        current_pos = rtde.current_position()
        current_pos[0] += RealWorld.scaling_constant
        rtde.move_to_position(current_pos)
        pass

    def move_up(self):
        current_pos = rtde.current_position()
        current_pos[2] -= RealWorld.scaling_constant
        rtde.move_to_position(current_pos)
        pass

    def move_down(self):
        current_pos = rtde.current_position()
        current_pos[2] += RealWorld.scaling_constant
        rtde.move_to_position(current_pos)
        pass

    def turn_counter_clockwise(self):
        current_pos = rtde.current_position()
        current_pos[4] += RealWorld.pi*RealWorld.turn_constant/180
        rtde.move_to_position(current_pos)
        pass

    def turn_clockwise(self):
        current_pos = rtde.current_position()
        current_pos[4] -= RealWorld.pi*RealWorld.turn_constant/180
        rtde.move_to_position(current_pos)
        pass

    def get_state(self):
        # Ich weiss nicht was ich hier machen soll oder welche koordinaten sind in coordinates gespeichert.
        pass

    def go_to_coordinates(self, coordinates):
        new_pos = rtde.current_position()
        new_pos[0] = coordinates[0]
        new_pos[2] = coordinates[1]
        rtde.move_to_position_no_append(new_pos)
        pass

    def reset(self):
        rtde.go_start_via_path()
        pass

    def take_picture(self):
        rtde.disengage()
        rtde.go_camera()
        rtde.take_picture()
        rtde.resume()
        rtde.go_start_disengaged()
        rtde.engage()
        pass

# def test():
#     print('CH1')
#     RealWorld.reset()
#
#     while True:
#         print('CH2')
#         RealWorld.move_up()
#         print('CH3')
#         RealWorld.move_down()
#         print('CH4')
#         RealWorld.move_left()
#         print('CH5')
#         RealWorld.move_right()
#         print('CH6')
#         RealWorld.turn_clockwise()
#         print('CH7')
#         RealWorld.turn_counter_clockwise()
#         print('CH8')
#         RealWorld.take_picture()


RealWorld = RealWorld()
print('CH1')
RealWorld.reset()

while True:
    print('CH2')
    RealWorld.move_up()
    print('CH3')
    RealWorld.move_down()
    print('CH4')
    RealWorld.move_left()
    print('CH5')
    RealWorld.move_right()
    print('CH6')
    RealWorld.turn_clockwise()
    print('CH7')
    RealWorld.turn_counter_clockwise()
    print('CH8')
    RealWorld.take_picture()
