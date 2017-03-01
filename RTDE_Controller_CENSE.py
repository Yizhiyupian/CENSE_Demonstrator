import sys
import logging
import rtde_client.rtde.rtde as rtde
import rtde_client.rtde.rtde_config as rtde_config
from operator import sub,abs

# begin variable and object setup
ROBOT_HOST = '169.254.203.187'
ROBOT_PORT = 30004
config_filename = 'ur5_configuration_CENSE_test.xml'

START_POSITION = [-0.3391, 0.2359, 0.4865, -0.0030, -0.0938, 1.6205]

RTDE_PROTOCOL_VERSION = 1

keep_running = True

MAX_ERROR = 0.001

logging.getLogger().setLevel(logging.INFO)

conf = rtde_config.ConfigFile(config_filename)
state_names, state_types = conf.get_recipe('state')
setp_names, setp_types = conf.get_recipe('setp')
watchdog_names, watchdog_types = conf.get_recipe('watchdog')

con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
# end variable and object setup

# Initiate connection
con.connect()

# get_controller_version is used to know if minimum requirements are met
con.get_controller_version()

# Compares protocol version of the robot with that of the program. Mismatch leads to system exit
if not con.negotiate_protocol_version(RTDE_PROTOCOL_VERSION):
    sys.exit()

# Send configuration for output and input recipes
con.send_output_setup(state_names, state_types)
setp = con.send_input_setup(setp_names, setp_types)

# Send configuration for the watchdog timer (1 Hz) input recipe
watchdog = con.send_input_setup(watchdog_names, watchdog_types)

# Set input registers (double) to 0
setp.input_double_register_0 = 0
setp.input_double_register_1 = 0
setp.input_double_register_2 = 0
setp.input_double_register_3 = 0
setp.input_double_register_4 = 0
setp.input_double_register_5 = 0

# Set input register for watchdog timer to 0 so that it can be reset
watchdog.input_int_register_0 = 0


# Starts data sync
def start_sync():
    # start data exchange. If the exchange fails it returns 'Failed'
    if not con.send_start():
        return 'Failed'


# Pauses the data sync
def pause_sync():
    con.send_pause()


# Disconnects the RTDE
def disconnect_rtde():
    con.disconnect()


# current_position gives the current position of the TCP relative to the defined Cartesian plane in list format
def current_position():

    # Checks for the state of the connection
    state = con.receive()

    # If output config not initialized, RTDE synchronization is inactive, or RTDE is disconnected it returns 'Failed'
    if state is None:
        return 'Failed'

    # If successful RTDE sync is paused and it returns the list with the current position
    return state.actual_TCP_pose


# This class hold the list of all positions
class Positions:
    start_sync()
    all_positions = [START_POSITION]


# setp_to_list converts a serialized data object to a list
def setp_to_list(setp):
    list = []
    for i in range(0,6):
        list.append(setp.__dict__["input_double_register_%i" % i])
    return list


# list_to_setp converts a list int0 serialized data object
def list_to_setp(setp, list):
    for i in range (0,6):
        setp.__dict__["input_double_register_%i" % i] = list[i]
    return setp


# move_to_position changes the position and orientation of the TCP of the robot relative to the defined Cartesian plane
def move_to_position(new_pos):

    # Will try to move to position till current_position() is within a max error range from new_pos
    while max(map(abs, map(sub, current_position(), new_pos))) >= MAX_ERROR:
        # print (max(map(abs, map(sub, current_position(), new_pos))))

        # Checks for the state of the connection
        state = con.receive()

        # If output config not initialized, RTDE synchronization is inactive, or RTDE is disconnected it returns 'Failed'
        if state is None:
            return 'Failed'

        # The output_int_register_0 defines if the robot is in motion.
        if state.output_int_register_0 != 0:

            # Changes the value from setp to the new position
            list_to_setp(setp, new_pos)

            # Send new position
            con.send(setp)

        con.send(watchdog)

    # If successful the RTDE sync is paused, new position is added to all_positions, and it returns 'SUCCESS'
    Positions.all_positions.append(new_pos)
    return 'SUCCESS'


# move_to_position changes the position and orientation of the TCP of the robot relative to the defined Cartesian plane
def move_to_position_no_append(new_pos):

    # Will try to move to position till current_position() is within a max error range from new_pos
    while max(map(abs, map(sub, current_position(), new_pos))) >= MAX_ERROR:
        # print (max(map(abs, map(sub, current_position(), new_pos))))

        # Checks for the state of the connection
        state = con.receive()

        # If output config not initialized, RTDE synchronization is inactive, or RTDE is disconnected it returns 'Failed'
        if state is None:
            return 'Failed'

        # The output_int_register_0 defines if the robot is in motion.
        if state.output_int_register_0 != 0:

            # Changes the value from setp to the new position
            list_to_setp(setp, new_pos)

            # Send new position
            con.send(setp)

        con.send(watchdog)

    # If successful the RTDE sync is paused, new position is added to all_positions, and it returns 'SUCCESS'
    return 'SUCCESS'


# go_start_via_path moves the robot back to the defined starting position through all recorded positions
def go_start_via_path():

    # Makes a new list which is the reverses of all_positions to be able to go from end position to start position
    rev_all_positions = list(Positions.all_positions)
    rev_all_positions.reverse()
    move_to_position_no_append(rev_all_positions[0])

    # For all the positions in all_positions it implements the function move_to_position
    while len(rev_all_positions) != 1:
        move_response = 'Failed'

        # It will try the movement till 'SUCCESS' is returned
        while move_response == 'Failed':
            move_response = move_to_position_no_append(rev_all_positions[0])

        # It removes the position from all_positions
        rev_all_positions.remove(rev_all_positions[0])

    # Moves to start position
    move_to_position_no_append(rev_all_positions[0])

    # If successful all_positions will be cleared and redefined with initial position
    Positions.all_positions = list(rev_all_positions)
    return 'SUCCESS'
