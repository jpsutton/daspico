# USB HID Keyboard Controller

This project turns your DasKeyboard Model S Professional into a fully functional USB HID keyboard using CircuitPython.

## Hardware Requirements

- **Microcontroller**: Raspberry Pi Pico or compatible CircuitPython board with USB HID support
- **DasKeyboard Model S Professional**: Connected according to the GPIO mapping in the code
- **USB connection**: To the host computer

## Software Requirements

- **CircuitPython**: Version 8.0+ recommended
- **adafruit_hid library**: For USB HID functionality

## Setup Instructions

### 1. Install CircuitPython

1. Download the latest CircuitPython UF2 file for your board from [circuitpython.org](https://circuitpython.org/downloads)
2. Put your board into bootloader mode (hold BOOTSEL while plugging in USB for Pico)
3. Copy the UF2 file to the RPI-RP2 drive that appears
4. The board will reboot and appear as CIRCUITPY drive

### 2. Install Required Libraries

1. Download the CircuitPython Library Bundle from [circuitpython.org/libraries](https://circuitpython.org/libraries)
2. Extract the bundle and copy these folders to `CIRCUITPY/lib/`:
   ```
   lib/
   └── adafruit_hid/
       ├── __init__.py
       ├── keyboard.py
       ├── keycode.py
       ├── mouse.py
       └── consumer_control.py
   ```

### 3. Deploy the Code

1. Copy `kb_ctrl_test.py` to the CIRCUITPY drive
2. Rename it to `code.py` (or `main.py`)
3. The keyboard will start automatically when the board boots

## Features

### ✅ **Full USB HID Functionality**
- All standard keyboard keys supported
- Proper modifier key handling (Shift, Ctrl, Alt, GUI/Windows key)
- Multiple simultaneous key presses (N-key rollover within hardware limits)
- Function key combinations (Fn+key)

### ✅ **Advanced Matrix Scanning**
- Debounced scanning for reliable key detection
- Ghosting detection and warnings
- Optimized timing for responsive input

### ✅ **Smart Key Processing**
- Automatic key press/release tracking
- Modifier key categorization
- Readable console output for debugging

### ✅ **Error Handling**
- Graceful fallback if USB HID fails
- Debug mode for troubleshooting
- Proper cleanup on exit

## Key Mapping

The keyboard supports a full 104-key layout including:

- **Function keys**: F1-F12, ESC
- **Number row**: 1-9, 0, `, -, =, Backspace
- **QWERTY layout**: Full alphabet with brackets, backslash
- **Modifiers**: Left/Right Shift, Ctrl, Alt, GUI/Meta
- **Navigation**: Arrow keys, Home, End, Page Up/Down, Insert, Delete
- **Numpad**: Full numeric keypad with operators
- **Special keys**: Tab, Caps Lock, Enter, Space, Print Screen, etc.

## Fn Key Combinations

The Fn key enables secondary functions:

- **Fn + F1-F12**: Extended function keys (F13-F24)
- **Fn + Arrow Keys**: 
  - Fn + Up → Page Up
  - Fn + Down → Page Down  
  - Fn + Left → Home
  - Fn + Right → End

## Usage

### Normal Operation
1. Connect the keyboard to your computer via USB
2. The keyboard will be recognized as a standard USB HID device
3. Start typing! All keys and combinations work as expected

### Debug Mode
- Connect to the serial console to see key press information
- Useful for troubleshooting matrix connections
- Shows modifier combinations and Fn key states

### Example Console Output
```
🎹 Pressed keys (2):
  🔧 Modifiers: Lctrl
  ⌨️  Keys: c
  🔗 Combination: Lctrl+c

🎹 Pressed keys (3):
  🔧 Modifiers: Lshift, Lctrl
  ⌨️  Keys: a
  🔗 Combination: Lshift+Lctrl+a
```

## Troubleshooting

### USB HID Not Working
- Ensure CircuitPython version supports USB HID
- Check that `adafruit_hid` library is properly installed
- Try a different USB cable/port
- Restart the board

### Keys Not Detected
- Check GPIO connections in the code
- Verify DasKeyboard Model S Professional matrix wiring matches `KEY_MAPPING_GPIO`
- Look for ghosting warnings in console output
- Test individual keys in debug mode

### Multiple Key Issues
- This is normal for matrices without diodes
- The ghosting detection will warn about problematic combinations
- Consider adding diodes to your matrix for true N-key rollover

### Modifier Keys Not Working
- Check that modifier keys are mapped correctly in `MODIFIER_KEYS`
- Ensure proper key categorization in `categorize_keys()`
- Verify timing isn't too fast for reliable detection

## Customization

### Adding New Keys
1. Add the key to `KEY_MAPPING_GPIO` with proper GPIO coordinates
2. Add the key name to `KEY_TO_KEYCODE` with the appropriate `Keycode`
3. If it's a modifier, add it to `MODIFIER_KEYS`

### Changing Fn Combinations
Modify the `_get_fn_combination()` method in the `HIDKeyboard` class:

```python
fn_mappings = {
    "F1": Keycode.F13,           # Your custom mapping
    "Up": Keycode.PAGE_UP,       # Custom arrow behavior
    # Add more combinations...
}
```

### Adjusting Scan Timing
- Modify `time.sleep_ms(20)` in main loop for different responsiveness
- Adjust `time.sleep_us()` values in `scan_matrix()` for different settling times
- Change `num_scans=3` in `scan_matrix_debounced()` for more/less debouncing

## Circuit Notes

This code assumes:
- **Active-low matrix**: Columns driven low, rows pulled high (DasKeyboard Model S Professional configuration)
- **Standard matrix layout**: Without individual key diodes (as used in DasKeyboard Model S Professional)
- **GPIO mapping**: Matches the DasKeyboard Model S Professional ribbon cable connections

For different hardware configurations, modify:
- `COLUMN_GPIOS` and `ROW_GPIOS` arrays
- `KEY_MAPPING_GPIO` dictionary  
- Pin setup in `setup_pins()`

## License

Open source - modify and distribute as needed for your custom keyboard projects!