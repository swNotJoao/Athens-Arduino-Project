from pynput import mouse
import pyautogui

# get the screen size to check for the right limit of the screen
print(f'screen size: {pyautogui.size()}')
LEFT_BORDER = 0 + 20
RIGHT_BORDER = pyautogui.size().width - 20


class ArmController:
    """
    This class is used to be able to control the arm of the car by using the horizontal movement of the mouse and
    the scroll wheel of the mouse and to toggle the laser on the car on or off by using the left mouse button.
    """
    # increments of the angles of the car
    ARM_ANGLE_INCREMENT = 1
    BASE_ANGLE_INCREMENT = 1.5
    MAX_ANGLE = 175
    MIN_ANGLE = 5

    def __init__(self):
        self.available_keys = ['base', 'arm', 'laser_on']
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_scroll=self.on_scroll,
            on_click=self.on_click)
        self.number_buffer_size = 2
        self.composite_buffer_size = 3
        self.number_buffer = []
        self.composite_buffer = []
        self.angle_states = {'base': 90, 'arm': 90, 'laser_on': False}

    def start_listening(self):
        """
        This method starts the ArmController object to listen to mouse changes.
        """
        self.mouse_listener.start()

    def get_states(self):
        return self.angle_states

    def on_move(self, x, y):
        """
        This method is called whenever the mouse is moved.
        If the mouse is moved horizontally the values self.angle_states['base'] will be changed accordingly.
        The number_buffer and composite_buffer are used to avoid jittery movement of the mouse.
        """
        self.number_buffer.append(x)
        if len(self.number_buffer) == self.number_buffer_size:
            average_of_numbers = sum(self.number_buffer) / self.number_buffer_size
            self.composite_buffer.append(average_of_numbers)
            self.number_buffer = []
            self.handle_added_composite()

    def handle_added_composite(self):
        if len(self.composite_buffer) < 3:  # composite_buffer is not full yet
            return
        c1, c2, c3 = self.composite_buffer
        if c1 >= RIGHT_BORDER and c2 >= RIGHT_BORDER and c3 >= RIGHT_BORDER:  # means the mouse moved right
            self.move_base_angle(False)
        elif c1 <= LEFT_BORDER and c2 <= RIGHT_BORDER and c3 <= LEFT_BORDER:  # means the mouse moved left
            self.move_base_angle(True)
        elif c1 <= c2 <= c3:  # means the mouse moved right
            self.move_base_angle(False)
        elif c1 >= c2 >= c3:  # means the mouse moved left
            self.move_base_angle(True)
        self.composite_buffer = []  # empty the composite_buffer

    def move_base_angle(self, needs_to_increment: bool):
        """
        This method changes the value of self.angle_states['base'] by + or -BASE_ANGLE_INCREMENT.
        """
        if needs_to_increment:
            new_angle = self.angle_states['base'] + ArmController.BASE_ANGLE_INCREMENT
            self.angle_states['base'] = new_angle if new_angle < ArmController.MAX_ANGLE else ArmController.MAX_ANGLE
        else:
            new_angle = self.angle_states['base'] - ArmController.BASE_ANGLE_INCREMENT
            self.angle_states['base'] = new_angle if new_angle > ArmController.MIN_ANGLE else ArmController.MIN_ANGLE

    def on_scroll(self, x, y, dx, dy):
        """
        This method is called whenever the scroll wheel on the mouse is used.
        The values self.angle_states['arm'] will be changed accordingly.
        """
        if dy < 0:  # means the mouse scrolled down
            self.move_arm_angle(False)
        else:
            self.move_arm_angle(True)

    def move_arm_angle(self, needs_to_increment: bool):
        """
        This method changes the value of self.angle_states['arm'] by + or -BASE_ANGLE_INCREMENT.
        """
        if needs_to_increment:
            new_angle = self.angle_states['arm'] + ArmController.ARM_ANGLE_INCREMENT
            self.angle_states['arm'] = new_angle if new_angle < ArmController.MAX_ANGLE else ArmController.MAX_ANGLE
        else:
            new_angle = self.angle_states['arm'] - ArmController.ARM_ANGLE_INCREMENT
            self.angle_states['arm'] = new_angle if new_angle > ArmController.MIN_ANGLE else ArmController.MIN_ANGLE

    def on_click(self, x, y, button, pressed):
        """
        This method is called whenever the left mouse button is clicked.
        The values self.angle_states['laser_on'] will be changed accordingly.
        """
        try:
            button_name = button.char
        except AttributeError:
            button_name = button.name
        if button_name == 'left' and pressed:
            self.angle_states['laser_on'] = not self.angle_states['laser_on']
