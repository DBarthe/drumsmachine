from pynput import keyboard

from . import interface
from . import state

seq_keys = "azertyui"[0:int(state.cycle_size / 2)] + "qsdfghjk"[0:int(state.cycle_size / 2)]
selected_track_num = 0
selected_track = interface.list_tracks()[selected_track_num]


def display_track():
    track = interface.get_track(selected_track)
    track = "".join(["x" if note else "." for note in track])
    track = [track[x:x + int(state.cycle_size / 2)] for x in range(0, len(track), int(state.cycle_size / 2))]
    print("{}\n{}".format(selected_track, "\n".join(track)))


def select_track_up():
    global selected_track_num, selected_track
    selected_track_num += 1
    track_list = interface.list_tracks()
    selected_track_num %= len(track_list)
    selected_track = track_list[selected_track_num]


def select_track_down():
    global selected_track_num, selected_track
    selected_track_num -= 1
    track_list = interface.list_tracks()
    if selected_track_num < 0:
        selected_track_num += len(track_list)
    selected_track = track_list[selected_track_num]


last_flames_key = None


def on_press(key):
    try:
        key_str = key.char  # single-char keys
    except:
        key_str = key.name  # other keys

    if key == keyboard.Key.right:
        interface.increase_tempo(1)
    elif key == keyboard.Key.left:
        interface.increase_tempo(-1)

    if key == keyboard.Key.up:
        select_track_up()
    elif key == keyboard.Key.down:
        select_track_down()

    elif key_str is not None and len(key_str) == 1 and key_str in seq_keys:
        cursor = seq_keys.index(key_str)
        interface.toogle_note(selected_track, cursor)

    global last_flames_key
    if key == keyboard.Key.alt:
        state.tracks_params['/kick'][1] = 2
        state.tracks_params['/kick'][2] = (60 / state.tempo) / 8
        last_flames_key = key

    if key == keyboard.Key.shift:
        state.tracks_params['/kick'][1] = 3
        state.tracks_params['/kick'][2] = (60 / state.tempo) / 6
        last_flames_key = key

    if key == keyboard.Key.space:
        state.tracks_params['/kick'][1] = 3
        state.tracks_params['/kick'][2] = (60 / state.tempo) / 3
        last_flames_key = key

    display_track()


def on_release(key):
    global last_flames_key
    if key is last_flames_key:
        state.tracks_params['/kick'][1] = 1
        state.tracks_params['/kick'][2] = 0
        last_flames_key = None


def start():
    display_track()
    lis = keyboard.Listener(on_press=on_press, on_release=on_release)
    lis.start()
    #  lis.join()
