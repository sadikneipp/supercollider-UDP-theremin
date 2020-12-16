import math
from time import sleep
from multiprocessing import Process, Value

from receiver import create_socket, get_data
from sc_interface import connect, send_message

TONE_LB = 220
TONE_UB = 880

VOL_UB = 1
VOL_LB = 0
VOL_LOG_LB = 1e-3
VOL_LOG_UB = 1


PITCH_LB = -90
PITCH_UB = 90


def convert_scales(tx, lbx=PITCH_LB, ubx=PITCH_UB, lby=TONE_LB, uby=TONE_UB):  # x -> y
    ty = lby + (tx - lbx) * (uby - lby) / (ubx - lbx)
    return ty


def constrain(x, ub, lb):
    if x > ub:
        return ub
    if x < lb:
        return lb
    return x


def update_state(sock, raw_pitch, raw_roll):
    while True:
        raw_pitch.value = get_data(sock)["pitch"]
        raw_roll.value = get_data(sock)["roll"]

def dbify(vol_perc, log_lb=VOL_LOG_LB, log_ub=VOL_LOG_UB):
    vol_scaled = convert_scales(vol_perc, VOL_LB, VOL_UB, VOL_LOG_LB, VOL_LOG_UB)
    print(vol_scaled)
    return math.log(vol_scaled)

if __name__ == "__main__":
    sock = create_socket()
    client = connect()

    raw_pitch = Value("d", 0)
    raw_roll = Value("d", 0)
    p = Process(target=update_state, args=(sock, raw_pitch, raw_roll))
    p.start()

    while True:
        tone = convert_scales(raw_pitch.value)
        print(raw_roll.value)
        volume_perc = convert_scales(
            constrain(raw_roll.value, 90, -90), lby=VOL_LB, uby=VOL_UB
        )
        print(tone, volume_perc)
        send_message(tone, volume_perc, client)
        sleep(0.001)
