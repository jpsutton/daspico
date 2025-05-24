import board
import digitalio
import time
import sys
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

print("🎹 CircuitPython USB HID Keyboard Starting...")

# GPIO mapping - using CircuitPython board pins
# Column pins (outputs)
COLUMN_PINS = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, 
               board.GP6, board.GP7, board.GP8, board.GP9, board.GP11, board.GP12, 
               board.GP14, board.GP15, board.GP16, board.GP17, board.GP20, board.GP27]

# Row pins (inputs)  
ROW_PINS = [board.GP10, board.GP13, board.GP18, board.GP19, board.GP21, 
            board.GP22, board.GP26, board.GP28]

# Convert pin objects to GPIO numbers for mapping
COLUMN_GPIOS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 16, 17, 20, 27]
ROW_GPIOS = [10, 13, 18, 19, 21, 22, 26, 28]

# Single unified key mapping: GPIO pairs -> key info
# Format: (row_gpio, col_gpio): {"name": "display_name", "keycode": Keycode.ACTUAL_CODE}
KEY_MAPPING = {
    # Function row
    (28, 6): {"name": "ESC", "keycode": Keycode.ESCAPE},
    (13, 7): {"name": "F1", "keycode": Keycode.F1},
    (13, 4): {"name": "F2", "keycode": Keycode.F2},
    (18, 4): {"name": "F3", "keycode": Keycode.F3},
    (28, 4): {"name": "F4", "keycode": Keycode.F4},
    (10, 9): {"name": "F5", "keycode": Keycode.F5},
    (28, 1): {"name": "F6", "keycode": Keycode.F6},
    (18, 3): {"name": "F7", "keycode": Keycode.F7},
    (13, 3): {"name": "F8", "keycode": Keycode.F8},
    (13, 8): {"name": "F9", "keycode": Keycode.F9},
    (10, 8): {"name": "F10", "keycode": Keycode.F10},
    (28, 8): {"name": "F11", "keycode": Keycode.F11},
    (21, 8): {"name": "F12", "keycode": Keycode.F12},
    (10, 0): {"name": "PrtScr", "keycode": Keycode.PRINT_SCREEN},
    (19, 0): {"name": "ScrLck", "keycode": Keycode.SCROLL_LOCK},
    (19, 9): {"name": "Pause", "keycode": Keycode.PAUSE},
    
    # Number row
    (13, 6): {"name": "`", "keycode": Keycode.GRAVE_ACCENT},
    (10, 6): {"name": "1", "keycode": Keycode.ONE},
    (10, 7): {"name": "2", "keycode": Keycode.TWO},
    (10, 4): {"name": "3", "keycode": Keycode.THREE},
    (10, 5): {"name": "4", "keycode": Keycode.FOUR},
    (13, 5): {"name": "5", "keycode": Keycode.FIVE},
    (13, 2): {"name": "6", "keycode": Keycode.SIX},
    (10, 2): {"name": "7", "keycode": Keycode.SEVEN},
    (10, 1): {"name": "8", "keycode": Keycode.EIGHT},
    (10, 3): {"name": "9", "keycode": Keycode.NINE},
    (10, 11): {"name": "0", "keycode": Keycode.ZERO},
    (13, 11): {"name": "-", "keycode": Keycode.MINUS},
    (13, 1): {"name": "=", "keycode": Keycode.EQUALS},
    (18, 8): {"name": "BckSpc", "keycode": Keycode.BACKSPACE},
    
    # Number row navigation
    (13, 12): {"name": "Ins", "keycode": Keycode.INSERT},
    (13, 16): {"name": "Home", "keycode": Keycode.HOME},
    (13, 20): {"name": "PgUp", "keycode": Keycode.PAGE_UP},
    
    # Numpad top row
    (22, 27): {"name": "NmLck", "keycode": Keycode.KEYPAD_NUMLOCK},
    (22, 12): {"name": "N_/", "keycode": Keycode.KEYPAD_FORWARD_SLASH},
    (22, 20): {"name": "N_*", "keycode": Keycode.KEYPAD_ASTERISK},
    (21, 20): {"name": "N_-", "keycode": Keycode.KEYPAD_MINUS},
    
    # QWERTY row
    (18, 6): {"name": "Tab", "keycode": Keycode.TAB},
    (19, 6): {"name": "q", "keycode": Keycode.Q},
    (19, 7): {"name": "w", "keycode": Keycode.W},
    (19, 4): {"name": "e", "keycode": Keycode.E},
    (19, 5): {"name": "r", "keycode": Keycode.R},
    (18, 5): {"name": "t", "keycode": Keycode.T},
    (18, 2): {"name": "y", "keycode": Keycode.Y},
    (19, 2): {"name": "u", "keycode": Keycode.U},
    (19, 1): {"name": "i", "keycode": Keycode.I},
    (19, 3): {"name": "o", "keycode": Keycode.O},
    (19, 11): {"name": "p", "keycode": Keycode.P},
    (18, 11): {"name": "[", "keycode": Keycode.LEFT_BRACKET},
    (18, 1): {"name": "]", "keycode": Keycode.RIGHT_BRACKET},
    (26, 8): {"name": "\\", "keycode": Keycode.BACKSLASH},
    
    # QWERTY row navigation
    (13, 27): {"name": "Del", "keycode": Keycode.DELETE},
    (10, 16): {"name": "End", "keycode": Keycode.END},
    (10, 20): {"name": "PgDn", "keycode": Keycode.PAGE_DOWN},
    
    # Numpad second row
    (19, 27): {"name": "P_7", "keycode": Keycode.KEYPAD_SEVEN},
    (19, 12): {"name": "P_8", "keycode": Keycode.KEYPAD_EIGHT},
    (19, 20): {"name": "P_9", "keycode": Keycode.KEYPAD_NINE},
    (19, 16): {"name": "P_+", "keycode": Keycode.KEYPAD_PLUS},
    
    # ASDF row
    (18, 7): {"name": "CpsLck", "keycode": Keycode.CAPS_LOCK},
    (26, 6): {"name": "a", "keycode": Keycode.A},
    (26, 7): {"name": "s", "keycode": Keycode.S},
    (26, 4): {"name": "d", "keycode": Keycode.D},
    (26, 5): {"name": "f", "keycode": Keycode.F},
    (28, 5): {"name": "g", "keycode": Keycode.G},
    (28, 2): {"name": "h", "keycode": Keycode.H},
    (26, 2): {"name": "j", "keycode": Keycode.J},
    (26, 1): {"name": "k", "keycode": Keycode.K},
    (26, 3): {"name": "l", "keycode": Keycode.L},
    (26, 11): {"name": ";", "keycode": Keycode.SEMICOLON},
    (28, 11): {"name": "'", "keycode": Keycode.QUOTE},
    (22, 8): {"name": "Enter", "keycode": Keycode.ENTER},
    
    # Numpad third row
    (18, 27): {"name": "P_4", "keycode": Keycode.KEYPAD_FOUR},
    (18, 12): {"name": "P_5", "keycode": Keycode.KEYPAD_FIVE},
    (18, 20): {"name": "P_6", "keycode": Keycode.KEYPAD_SIX},
    
    # ZXCV row
    (18, 17): {"name": "Lshift", "keycode": Keycode.LEFT_SHIFT},
    (22, 6): {"name": "z", "keycode": Keycode.Z},
    (22, 7): {"name": "x", "keycode": Keycode.X},
    (22, 4): {"name": "c", "keycode": Keycode.C},
    (22, 5): {"name": "v", "keycode": Keycode.V},
    (21, 5): {"name": "b", "keycode": Keycode.B},
    (21, 2): {"name": "n", "keycode": Keycode.N},
    (22, 2): {"name": "m", "keycode": Keycode.M},
    (22, 1): {"name": ",", "keycode": Keycode.COMMA},
    (22, 3): {"name": ".", "keycode": Keycode.PERIOD},
    (21, 11): {"name": "/", "keycode": Keycode.FORWARD_SLASH},
    (26, 17): {"name": "Rshift", "keycode": Keycode.RIGHT_SHIFT},
    
    # Arrow keys
    (28, 16): {"name": "Up", "keycode": Keycode.UP_ARROW},
    
    # Numpad fourth row
    (26, 27): {"name": "P_1", "keycode": Keycode.KEYPAD_ONE},
    (26, 12): {"name": "P_2", "keycode": Keycode.KEYPAD_TWO},
    (26, 20): {"name": "P_3", "keycode": Keycode.KEYPAD_THREE},
    (26, 16): {"name": "P_Enter", "keycode": Keycode.KEYPAD_ENTER},
    
    # Bottom row
    (13, 9): {"name": "Lctrl", "keycode": Keycode.LEFT_CONTROL},
    (18, 15): {"name": "L_Meta", "keycode": Keycode.LEFT_GUI},
    (28, 0): {"name": "L_Alt", "keycode": Keycode.LEFT_ALT},
    (28, 27): {"name": "SpcBar", "keycode": Keycode.SPACEBAR},
    (21, 0): {"name": "R_Alt", "keycode": Keycode.RIGHT_ALT},
    (26, 14): {"name": "R_Meta", "keycode": Keycode.RIGHT_GUI},
    (21, 3): {"name": "Fn", "keycode": None},  # Function key - no HID keycode
    (22, 9): {"name": "R_Ctrl", "keycode": Keycode.RIGHT_CONTROL},
    (21, 16): {"name": "Left", "keycode": Keycode.LEFT_ARROW},
    (21, 27): {"name": "Dn", "keycode": Keycode.DOWN_ARROW},
    (21, 12): {"name": "Right", "keycode": Keycode.RIGHT_ARROW},
    
    # Numpad bottom
    (28, 12): {"name": "P_0", "keycode": Keycode.KEYPAD_ZERO},
    (28, 20): {"name": "P_.", "keycode": Keycode.KEYPAD_PERIOD}
}

def setup_pins():
    """Initialize GPIO pins using CircuitPython syntax"""
    print("🔧 Setting up pins with CircuitPython...")
    
    # Set up column pins as outputs
    col_pins = []
    for pin in COLUMN_PINS:
        try:
            gpio_pin = digitalio.DigitalInOut(pin)
            gpio_pin.direction = digitalio.Direction.OUTPUT
            gpio_pin.value = True  # Start high (inactive)
            col_pins.append(gpio_pin)
            print(f"  ✅ Column pin {pin} initialized")
        except Exception as e:
            print(f"  ❌ Failed to initialize column pin {pin}: {e}")
    
    # Set up row pins as inputs with pull-ups
    row_pins = []
    for pin in ROW_PINS:
        try:
            gpio_pin = digitalio.DigitalInOut(pin)
            gpio_pin.direction = digitalio.Direction.INPUT
            gpio_pin.pull = digitalio.Pull.UP
            row_pins.append(gpio_pin)
            print(f"  ✅ Row pin {pin} initialized")
        except Exception as e:
            print(f"  ❌ Failed to initialize row pin {pin}: {e}")
    
    print(f"📊 Initialized {len(col_pins)} columns, {len(row_pins)} rows")
    return col_pins, row_pins

def lookup_key(gpio_a, gpio_b):
    """Look up key info by trying both GPIO combinations"""
    # Try (a,b) first
    key_info = KEY_MAPPING.get((gpio_a, gpio_b))
    if key_info:
        return key_info['name']
    
    # Try (b,a) if first lookup failed
    key_info = KEY_MAPPING.get((gpio_b, gpio_a))
    if key_info:
        return key_info['name']
    
    # If neither worked, return unknown key name
    return f"Unknown(GP{gpio_a},GP{gpio_b})"

def scan_matrix(col_pins, row_pins):
    """Scan the keyboard matrix using CircuitPython"""
    pressed_keys = []
    
    # Ensure all columns are high (inactive)
    for col_pin in col_pins:
        col_pin.value = True
    time.sleep(0.001)  # 1ms settling time
    
    # Scan each column
    for col_idx, col_pin in enumerate(col_pins):
        # Drive this column low (active)
        col_pin.value = False
        time.sleep(0.001)  # 1ms settling time
        
        # Check all rows for this column
        for row_idx, row_pin in enumerate(row_pins):
            if not row_pin.value:  # Key press detected (pulled low)
                col_gpio = COLUMN_GPIOS[col_idx]
                row_gpio = ROW_GPIOS[row_idx]
                key_name = lookup_key(row_gpio, col_gpio)
                pressed_keys.append((key_name, row_gpio, col_gpio))
        
        # Return column to high (inactive)
        col_pin.value = True
    
    return pressed_keys

class HIDKeyboard:
    """USB HID keyboard using CircuitPython"""
    
    def __init__(self):
        try:
            self.keyboard = Keyboard(usb_hid.devices)
            self.pressed_keys = set()
            print("✅ USB HID Keyboard initialized")
        except Exception as e:
            print(f"❌ Failed to initialize HID: {e}")
            raise
    
    def process_key_changes(self, current_keys):
        """Process key press/release changes"""
        current_key_names = {key[0] for key in current_keys}
        
        newly_pressed = current_key_names - self.pressed_keys
        newly_released = self.pressed_keys - current_key_names
        
        # Handle releases first
        for key_name in newly_released:
            self._release_key(key_name)
        
        # Handle presses
        for key_name in newly_pressed:
            self._press_key(key_name)
        
        self.pressed_keys = current_key_names
    
    def _press_key(self, key_name):
        """Press a key"""
        # Find keycode from the mapping by searching for the key name
        keycode = None
        for key_combo, key_info in KEY_MAPPING.items():
            if key_info['name'] == key_name:
                keycode = key_info['keycode']
                break
        
        if keycode:
            try:
                self.keyboard.press(keycode)
                print(f"⬇️ Pressed: {key_name}")
            except Exception as e:
                print(f"❌ Error pressing {key_name}: {e}")
    
    def _release_key(self, key_name):
        """Release a key"""
        # Find keycode from the mapping by searching for the key name
        keycode = None
        for key_combo, key_info in KEY_MAPPING.items():
            if key_info['name'] == key_name:
                keycode = key_info['keycode']
                break
        
        if keycode:
            try:
                self.keyboard.release(keycode)
                print(f"⬆️ Released: {key_name}")
            except Exception as e:
                print(f"❌ Error releasing {key_name}: {e}")
    
    def release_all(self):
        """Release all keys"""
        self.keyboard.release_all()
        self.pressed_keys.clear()

def main():
    """Main function using CircuitPython syntax"""
    print("🚀 Starting CircuitPython USB HID Keyboard")
    print("=" * 50)
    
    try:
        # Initialize hardware
        col_pins, row_pins = setup_pins()
        
        # Initialize HID keyboard
        hid_keyboard = HIDKeyboard()
        
        print("\n🎹 Keyboard ready! Start typing...")
        print("🛑 Press Ctrl+C to stop")
        
        last_pressed = set()
        
        while True:
            pressed_keys = scan_matrix(col_pins, row_pins)
            current_pressed = {key for key in pressed_keys}
            
            if current_pressed != last_pressed:
                hid_keyboard.process_key_changes(pressed_keys)
                
                if pressed_keys:
                    key_names = [key[0] for key in pressed_keys]
                    print(f"🎹 Active: {', '.join(key_names)}")
                
                last_pressed = current_pressed
            
            time.sleep(0.01)  # 10ms scan rate
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
        if 'hid_keyboard' in locals():
            hid_keyboard.release_all()
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'hid_keyboard' in locals():
            hid_keyboard.release_all()

if __name__ == "__main__":
    main() 