# physical buttons for calibration and quitting, wired to the Pi's GPIO pins
from config import BUTTON_R_PIN, BUTTON_Q_PIN

# only reachable when wired to a Pi's GPIO pins -- fall back to "never pressed"
# so this still runs on a dev machine without the hardware attached
try:
    import board
    import digitalio

    def _make_button(pin_name):
        button = digitalio.DigitalInOut(getattr(board, pin_name))
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP
        return button

    _r_button = _make_button(BUTTON_R_PIN)
    _q_button = _make_button(BUTTON_Q_PIN)
except Exception:
    _r_button = None
    _q_button = None

def calibrate_pressed():
    # buttons are wired active-low: pulled up, grounded when pressed
    return _r_button is not None and not _r_button.value

def quit_pressed():
    return _q_button is not None and not _q_button.value
