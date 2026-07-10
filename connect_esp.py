# serial connection to the ESP32-C6 controlling the spherical actuator joint
import serial
import time
from config import *


def connect_esp(port=SERIAL_PORT, baudrate=BAUD_RATE):
    esp = serial.Serial(port, baudrate, timeout=SERIAL_TIMEOUT)
    time.sleep(2)  # ESP32 resets when the serial port opens, give it time to boot
    esp.reset_input_buffer()
    return esp


def close_esp(esp):
    esp.close()


def read_response(esp, wait=0.2):
    time.sleep(wait)
    lines = []
    while esp.in_waiting:
        lines.append(esp.readline().decode(errors="ignore").strip())
    return lines


def _clamp_us(us):
    lo = max(SERVO_BASE_US - SERVO_DEFLECT_US, SERVO_ABS_MIN_US)
    hi = min(SERVO_BASE_US + SERVO_DEFLECT_US, SERVO_ABS_MAX_US)
    return int(max(lo, min(hi, us)))


def set_position(esp, us1, us2):
    us1, us2 = _clamp_us(us1), _clamp_us(us2)
    esp.write(f"S{us1},{us2}\n".encode())
    return read_response(esp)


def set_angle(esp, deg1, deg2):
    # deg1/deg2 are offsets from the joint's centered base position
    us1 = SERVO_BASE_US + deg1 * US_PER_DEGREE
    us2 = SERVO_BASE_US + deg2 * US_PER_DEGREE
    return set_position(esp, us1, us2)


def reset_to_base(esp):
    esp.write(b'b')
    return read_response(esp)


def toggle_mode(esp):
    esp.write(b'p')
    return read_response(esp)


# quick manual test: connect, sweep, print ESP responses

# if __name__ == "__main__":
#     esp = connect_esp()
#     print(read_response(esp))       # boot + ledcAttach messages
#     print(set_angle(esp, 30, -30))
#     time.sleep(1)
#     print(reset_to_base(esp))
#     close_esp(esp)
