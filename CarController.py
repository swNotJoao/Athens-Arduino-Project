from pynput import keyboard
from pynput.keyboard import Key, KeyCode


class CarController:
    """
    This class is used to be able to control the car by using the arrow keys on the keyboard.
    """
    def __init__(self):
        self.available_keys = ['up', 'down', 'left', 'right']
        self.key_states = dict()
        for key in self.available_keys:  # initialize the values of the keys to False
            self.key_states[key] = False
        self.key_listener = keyboard.Listener(on_press=self.on_press,
                                              on_release=self.on_release)

    def start_listening(self):
        """
        This method starts the CarController object to listen to the arrow key inputs.
        """
        self.key_listener.start()

    def get_states(self):
        return self.key_states

    def on_press(self, key: Key | KeyCode):
        """
        This method is called whenever a key is pressed on the keyboard.
        If the key is an arrow key the corresponding value in the self.key_states will be changed to True.
        """
        try:
            key_name = key.char
        except AttributeError:
            key_name = key.name
        if key_name in self.available_keys:
            self.key_states[key_name] = True

    def on_release(self, key: Key | KeyCode):
        """
        This method is called whenever a key is pressed on the keyboard.
        If the key is an arrow key the corresponding value in the self.key_states will be changed to False.
        """
        try:
            key_name = key.char
        except AttributeError:
            key_name = key.name
        if key_name in self.available_keys:
            self.key_states[key_name] = False
