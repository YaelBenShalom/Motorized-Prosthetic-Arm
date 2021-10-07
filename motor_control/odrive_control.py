from __future__ import print_function

import argparse
import odrive
import time
import math

from odrive.utils import start_liveplotter
from odrive.enums import *

STRAIGHT_POSITION = 0.55

def liveplot(driver_name):
    start_liveplotter(lambda: [
        driver_name.axis0.encoder.pos_estimate,
        driver_name.axis0.encoder.vel_estimate,
        driver_name.axis0.motor.current_control.Iq_measured
    ])

def clear_errors(driver_name):
    if driver_name.axis0.error:
        print("axis 0", driver_name.axis0.error)
        driver_name.axis0.error = 0

    if driver_name.axis0.motor.error:
        print("motor 0", driver_name.axis0.motor.error)
        driver_name.axis0.motor.error = 0

    if driver_name.axis0.encoder.error:
        print("encoder 0", driver_name.axis0.encoder.error)
        driver_name.axis0.encoder.error = 0

def shut_down(driver_name):
    # Stopping the motor spin
    driver_name.axis0.controller.input_vel = 0

    # Moving to straight position
    driver_name.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    driver_name.axis0.controller.input_pos = STRAIGHT_POSITION
    print("Going back to home position")

def get_motor_state(driver_name):
    motor_pos =  driver_name.axis0.encoder.pos_estimate
    motor_vel =  driver_name.axis0.encoder.vel_estimate
    motor_current = driver_name.axis0.motor.current_control.Iq_setpoint

    return motor_pos, motor_vel, motor_current

def position_control(driver_name):
    driver_name.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL

    # A sine wave to test
    t0 = time.monotonic()
    while time.monotonic() - t0 < 10:
        try:
            pos = 4.0 * math.sin(2 * (time.monotonic() - t0))
            driver_name.axis0.controller.input_pos = pos
            clear_errors(driver_name)

            output_pos, output_vel, output_current = get_motor_state(driver_name)
            # print("Moving to {} [turn]".format(output_pos))
            # print("Moving at {} [turn/s]".format(output_vel))
            # print("Motor current is {} [A]".format(output_current))
            print("The position error is {} [turn]".format(pos - output_pos))
            time.sleep(0.01)

        except:
            print("Couldn't complete motion. shutting down")
            shut_down(driver_name)
            raise

def velocity_control(driver_name):
    driver_name.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

    # A sine wave to test
    t0 = time.monotonic()
    while time.monotonic() - t0 < 11:
        try:
            vel = 0.6 * math.sin(4 * (time.monotonic() - t0))
            driver_name.axis0.controller.input_vel = vel
            clear_errors(driver_name)

            output_pos, output_vel, output_current = get_motor_state(driver_name)
            # print("Moving to {} [turn]".format(output_pos))
            # print("Moving at {} [turn/s]".format(output_vel))
            # print("Motor current is {} [A]".format(output_current))
            print("The velocity error is {} [turn/s]".format(vel - output_vel))
            time.sleep(0.01)

        except:
            print("Couldn't complete motion. shutting down")
            shut_down(driver_name)
            raise

def current_control(driver_name):
    driver_name.axis0.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL

    elbow_torque = [2.37458493223537, 2.53541101912472, 2.71535162581618, 2.79712712480384, 2.89753012980830, 2.88033858629321, 2.68583182360936, 2.43815069603204, 2.24715930653493, 2.08851568149113, 1.79325891224888, 1.42505522402717, 0.991032435352766, 0.545332315715792, 0.173334316294113, -0.0921692020520510, -0.356910119386626, -0.556229603336114, -0.688975930569938, -0.828206038295802, -0.835397119784771, -0.781750442214531, -0.687441173315559, -0.708922081786844, -0.795921606658805, -1.07442897670189, -1.49510915981511, -2.20626982987132, -2.96034947568970, -3.48177435558243, -3.58499282214374, -3.28070835966980, -2.80585816932437, -2.25792935162583, -1.77749832239307, -1.41077217511196, -1.12867900018221, -1.08253711325750, -1.25301799295598, -1.54378903345873, -1.92268190898073, -2.24654769912022, -2.36051680528867, -2.34040995004839, -2.10944678691686, -1.70335464920963, -1.12477803821310, -0.445718968651639, 0.254523974009796, 0.961267715399454, 1.47241821070387, 1.92500823913052, 2.14231021889541, 2.30519479941741, 2.29716188141883, 2.18409345531697, 2.00170604267668, 1.83884777037637, 1.74221310907935, 1.69803553221544, 1.82354052958535, 1.99054295327268, 2.15441539257439, 2.23922652070092, 2.33824689986800, 2.37553314719150, 2.43116487623577, 2.38953401573107, 2.33674922594060, 2.27846321634097, 2.11467998491661, 1.96778270346646, 1.81103358913916, 1.65489437042977, 1.54398385163993, 1.42466459383764, 1.39739624590167, 1.27591036189222, 1.23288083556482, 1.15896138194169, 1.14700343457193, 1.06650843576467, 1.06896289926102, 0.991928912202756, 0.877665545486183, 0.731466811825421, 0.507826198895476, 0.318038281521116, 0.0586009643994303, -0.122291360236784, -0.376208386354174, -0.418376430243631, -0.456868413003972, -0.395493788206801, -0.167758652059083, 0.130279633982383, 0.474923218929945, 0.807988707282930, 1.19654113391877, 1.47088108570767, 1.76738430941024, 1.95090156999584, 2.06708005124034, 2.01997722774019, 1.87850256425890, 1.63997089338220, 1.43676090659792, 1.23166358260621, 0.997880582550426, 0.788092842472417, 0.750751163132323, 0.719070606455161, 0.867757137822967, 1.15213933452118, 1.55710229542858, 2.04099380103566, 2.55780302025742, 2.97842830918301, 3.45801182577891, 3.81154007574963, 4.23352299807736, 4.39243625332261, 4.33713481039933, 3.87117503894947, 3.06921548857122, 2.22500050219847, 1.35294394102616, 0.565172384847906, -0.121351529445584, -0.789952785910573, -1.22102419271835, -1.52754976465975, -1.55473933274663, -1.50787791122609, -1.43066664899792, -1.43284557668049, -1.42823113730022, -1.47994869915601, -1.43806859788781, -1.50380004881975, -1.58170300977571, -1.74449823202215, -1.87663224170525, -1.95577201306974, -2.04489394832649, -2.13199851516969, -2.18584733869068, -2.21623083854497, -2.14122994181443, -1.87838434777639, -1.52082392002619, -1.21558627875285, -1.04638268106299, -0.805146619215699, -0.524378388661950, -0.320144229369448, -0.171536077031253, -0.217033234070275, -0.383298551653490, -0.735231827070570, -1.11124975360824, -1.45717410052883, -1.78032361166821, -2.06924230002622, -2.03314953166972, -1.72614537543678, -1.05151819036077, -0.0938648337055176, 0.830491212979932, 1.47369440998143, 1.87993463942697, 1.97759185013814, 1.81934778705237, 1.56615298634576, 1.41128029754344, 1.30077120250425, 1.38855354655352, 1.65575864159937, 2.03327535909121, 2.26663431367170, 2.54453468620915, 2.89915978881068, 2.99733303239569, 3.01997135388723, 2.86900824539646, 2.56785106212009, 2.33372988266067, 2.11793561529295, 1.86172102022318, 1.76822203621511, 1.57920925326627, 1.40859057158386, 1.26375001379820, 1.00916740009926, 0.880746426486188, 0.747365006387870, 0.831536472501864, 0.991478048649568, 1.28084357761487, 1.58833318619039, 1.89654879152089, 2.08382393351076, 2.10281774041561, 1.84672327798251, 1.56540934055042, 1.23742042720609, 0.911243157239476, 0.700547879001012, 0.372967276884770, 0.127651417697091, -0.0522426994629726, -0.257707659607243, -0.432159061627324, -0.423478150559904, -0.183534023557145, 0.0865377731563774, 0.379246848531574, 0.600719087537192, 0.851169582296447, 1.11199071516310, 1.31722578323350, 1.54020577573228, 1.77046392385542, 2.07008036197878, 2.33294664450427, 2.43201884028784, 2.34066245863830, 2.04502274722664, 1.81985267544246, 1.52123724588481, 1.41326075003249, 1.32942863463229, 1.35641612299481, 1.52903843098497, 1.73473525350266, 2.04279550690847, 2.40246347412489, 2.69805244690665, 3.12380983974689, 3.34918642541620, 3.29464992574070, 2.84601844676672, 2.04520622956515, 0.973459770929467, -0.0495195638273093, -0.720330126681764, -1.19584690354048, -1.47997711180648, -1.63293124966863, -1.63105520578438, -1.56226062294776, -1.27127363889373, -0.982833394728821, -0.705666284870486, -0.508412003861125, -0.465961096036631, -0.405898065088628, -0.499110274425991, -0.542213594693419, -0.683942838312524, -0.680160442568611, -0.794836304251133, -0.963980664357190, -1.15588801614652, -1.34923300002753, -1.57523919179938, -1.67767344824183, -1.77913668729539, -1.81937384739947, -1.83669106379736, -1.72974115687304, -1.58134417009204, -1.28776935588232, -0.996226788385274, -0.706979011183793, -0.536052258747343, -0.441890221301216, -0.446544447959346, -0.625512344077446, -0.798348234277397, -1.03046380796191, -1.32037977332058, -1.51647651450990, -1.70430398839660, -1.74099368458762, -1.70907235002173, -1.48847526117933, -1.02810840154425, -0.492525300427788, 0.127266497210867, 0.641682189536678, 1.12511884462002, 1.48532854864884, 1.67553469038672, 1.69021575849138, 1.62122577093692, 1.67363325540104, 1.85430577061458, 2.04083159729013, 2.20773981614017, 2.35341961029397, 2.51289109493072, 2.60214642067591, 2.68335862862224, 2.63815337233702, 2.43132503597525, 2.12823739570138, 1.72986756285683, 1.51405728035090, 1.33022545766517, 1.24905037632719, 1.24010102230214, 1.16244566579778, 1.17844603645418, 1.12861331085284, 1.08235758875940, 1.09810515521836, 1.05596466796138, 1.10783744127622, 1.05668126634454, 1.06511528153338, 0.981017320701407, 0.977517659160762, 0.835705107367067, 0.742257180069464, 0.606215345589318, 0.561523880332962, 0.525091833656777, 0.459193376207291, 0.406157662137246, 0.240348476725220, 0.208071256211169, 0.142894981162377, 0.120291548347883, 0.0616870570492459, 0.192239265512194, 0.389429953333776, 0.641653425060474, 0.944597853652721, 1.29586962091933, 1.58302381801034, 1.80487399192662, 1.84601265552949, 1.80878964451341, 1.64493352245057, 1.45049618582695, 1.26566978943382, 1.11934362706156, 1.07082670269049, 1.11712108317344, 1.22705772723290, 1.51516292607050, 1.81778376597393, 2.22081903258372, 2.44010965116183, 2.68457179443071, 2.86499699562554, 3.17294239174878, 3.64642002273844, 4.16238928709426, 4.57659145972332, 4.76261017316802, 4.62772684793620, 4.24499829228963, 3.56279806467952, 2.64903634499104, 1.64642008007233, 0.743459622832136, -0.0862734426315485, -0.729885934360766, -1.32553211978379, -1.82975375514394, -2.26187294336344, -2.60521878353510, -2.69166558764497, -2.74585512735467, -2.58131491821398, -2.31546319218056, -2.07750294253581, -1.74080977796506, -1.50775999409640, -1.41094655782713, -1.47078094566135, -1.58214821307130, -1.70525004313246, -1.73463000463735, -1.75465769879555, -1.75076144279425, -1.81720052094792, -1.72793119906239, -1.57866438712533, -1.40824582078194, -1.22854998679261, -1.03995015643837, -0.700525014954498, -0.486612059389739, -0.315459723637888, -0.168169693708658, -0.0638339494714057, -0.0464419062922593, -0.0845930726697237, -0.433916136879505, -1.02393514279949, -1.69529587697098, -2.24187773474466, -2.53888368976720, -2.62626061103947, -2.38820483991652, -1.82531969503752, -1.11142149836049, -0.405735186932426]
    motor_kv = 115
    torque_const = 8.27 / motor_kv

    # A sine wave to test
    for torque in elbow_torque:
        try:
            driver_name.axis0.controller.input_torque = torque
            clear_errors(driver_name)

            output_pos, output_vel, output_current = get_motor_state(driver_name)
            # print("Moving to {} [turn]".format(output_pos))
            # print("Moving at {} [turn/s]".format(output_vel))
            print("Motor current is {} [A]".format(output_current))
            # print("The torque error is {} [N/m]".format(torque - output_current * torque_const))
            time.sleep(1/120)

        except:
            print("Couldn't complete motion. shutting down")
            shut_down(driver_name)
            raise


def main(args):
    # Find a connected ODrive
    print("Finding an ODrive...")
    odrv0 = odrive.find_any()

    if args["calibration"]:
        # Calibrate motor and wait for it to finish
        print("Starting calibration...")
        odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        while odrv0.axis0.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)

    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis0.controller.config.input_mode = INPUT_MODE_PASSTHROUGH

    # To read a value, simply read the property
    print("The boards main supply voltage is {}V".format(str(odrv0.vbus_voltage)))

    # Moving to straight position
    odrv0.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    odrv0.axis0.controller.input_pos = STRAIGHT_POSITION
    print("Initializing position")

    # Plotting position, velocity and current graph
    liveplot(odrv0)

    # position_control(odrv0)
    velocity_control(odrv0)
    # current_control(odrv0)

    print("Finished motion. shutting down")
    shut_down(odrv0)


if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--calibration", help="calibrate motor")
    args = vars(parser.parse_args())
    main(args)
