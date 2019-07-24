import math
from pythonosc import dispatcher
from pythonosc import osc_server
import threading

from . import state


def linlin(a, b, s):
    (a1, a2), (b1, b2) = a, b
    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


def update_kick_dist(address, *args):
    dist = linlin((0, 1023), (0, 20), args[0])
    state.tracks_params["/kick"][0] = dist


def update_kick_decay(address, *args):
    dist = linlin((0, 1023), (0.01, 0.5), args[0])
    state.tracks_params["/kick"][3] = dist


def update_kick_release(address, *args):
    dist = linlin((0, 1023), (0.001, 0.5), args[0])
    state.tracks_params["/kick"][4] = dist


def update_kick_pitch_high(address, *args):
    dist = math.exp(linlin((0, 1023), (4.6, 7.6), args[0]))
    state.tracks_params["/kick"][5] = dist


def update_kick_pitch_low(address, *args):
    dist = math.exp(linlin((0, 1023), (3, 5.2), args[0]))
    state.tracks_params["/kick"][6] = dist


def update_kick_roll(address, *args):
    num_rolls = int(linlin((0, 1023), (1, 2), args[0]))
    if num_rolls == 1:
        roll_delay = 0
    else:
        roll_delay = (60 / state.tempo) / (4 * num_rolls)
    state.tracks_params["/kick"][1] = num_rolls
    state.tracks_params["/kick"][2] = roll_delay


def update_shuffle(address, *args):
    shuffle = linlin((0, 1023), (50, 70), args[0])
    state.shuffle = shuffle


def start_background():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--ip",
    #   default="127.0.0.1", help="The ip to listen on")
    # parser.add_argument("--port",
    #   type=int, default=9999, help="The port to listen on")
    # args = parser.parse_args()
    ip = '10.0.0.2'
    port = 9999

    a_dispatcher = dispatcher.Dispatcher()
    a_dispatcher.map("/pot/0", update_kick_dist)
    a_dispatcher.map("/pot/1", update_kick_decay)
    a_dispatcher.map("/pot/2", update_kick_release)
    a_dispatcher.map("/pot/4", update_kick_pitch_high)
    a_dispatcher.map("/pot/3", update_kick_pitch_low)
    a_dispatcher.map("/pot/5", update_shuffle)

    # a_dispatcher.map("/pot/0", update_kick_roll)
    #  a_dispatcher.map("/*", print)


    server = osc_server.BlockingOSCUDPServer(
        (ip, port), a_dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()


def start():
    t = threading.Thread(target=start_background)
    t.start()
