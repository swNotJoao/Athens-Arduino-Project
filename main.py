import serial
import serial.tools.list_ports
import time
import CarController
import ArmController


def print_ports():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print(f'{port}: {desc} [{hwid}]')


# this is to check which ports are available at the moment
print_ports()
arduino = serial.Serial(port='COM8', baudrate=115200, timeout=0.1)

SEND_RATE = 0.07  # the time in seconds between packets getting send

# set up the controllers
car_controller = CarController.CarController()
car_controller.start_listening()
arm_controller = ArmController.ArmController()
arm_controller.start_listening()


def get_all_states(car_controller: CarController.CarController, arm_controller: ArmController.ArmController) -> list[str]:
    """
    This method gets the states of the given controllers and puts them in a list of strings.
    """
    output = []
    car_controller_states = car_controller.get_states()
    arm_controller_states = arm_controller.get_states()
    for key in car_controller.available_keys:
        output.append(str(int(car_controller_states[key])))
    for key in arm_controller.available_keys:
        output.append(str(int(arm_controller_states[key])))
    return output


def encode_states(all_states: list[str]) -> bytes:
    """
    This method gets a list of strings and joins them separated by a ',' and converts this string to bytes.
    """
    return bytes(','.join(all_states), 'utf-8')


def write_to_arduino(data_to_send: bytes):
    """
    This method writes to the given data_to_send to the Arduino.
    The Arduino will normally send the received data back to check if the correct data has been received.
    """
    arduino.write(data_to_send)
    time.sleep(0.05)
    data_forward = str(arduino.readline()[:-2], 'utf-8')
    data_backward = str(arduino.readline()[:-2], 'utf-8')
    data_left = str(arduino.readline()[:-2], 'utf-8')
    data_right = str(arduino.readline()[:-2], 'utf-8')
    data_base = str(arduino.readline()[:-2], 'utf-8')
    data_arm = str(arduino.readline()[:-2], 'utf-8')
    data_laser = str(arduino.readline()[:-2], 'utf-8')
    print(f'Arduino data:\tforward: {data_forward}\tbackward: {data_backward}\tleft: {data_left}\tright: {data_right}\tbase: {data_base}\tarm: {data_arm}\tlaser: {data_laser}')


if __name__ == "__main__":
    while True:
        time.sleep(SEND_RATE)
        state_array = get_all_states(car_controller, arm_controller)
        encoded_states = encode_states(state_array)
        write_to_arduino(encoded_states)
