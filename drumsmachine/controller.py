import clockblocks
from pythonosc import udp_client, osc_bundle_builder, osc_message_builder

from . import state

client = udp_client.SimpleUDPClient("127.0.0.1", 57120)


def play_one(cursor):
    messages = []

    for (name, track) in state.tracks.items():
        if track[cursor]:

            mute = state.tracks_tmp_mute.get(name, 0)
            if mute > 0:
                state.tracks_tmp_mute[name] = mute - 1
                continue

            msg_builder = osc_message_builder.OscMessageBuilder(address=name)
            for value in state.tracks_params[name]:
                if callable(value):
                    value = value()
                msg_builder.add_arg(value, msg_builder.ARG_TYPE_FLOAT if type(value) == float else msg_builder.ARG_TYPE_INT)  # todo: improve this shit
            messages.append(msg_builder.build())

    if len(messages) > 0:
        bundle_builder = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
        for msg in messages:
            bundle_builder.add_content(msg)
        client.send(bundle_builder.build())


def wait_one(clock, cursor):
    actual_time = (clock.beats() * 4) % state.cycle_size
    if cursor % 2 == 0:
        next_time = cursor + state.shuffle / 50
    else:
        next_time = cursor + 1
    delay = (next_time - actual_time) / 4
    clock.wait(delay)


def start():
    clock = clockblocks.Clock(initial_tempo=state.tempo)
    cursor = -1
    while True:
        clock.tempo = state.tempo
        cursor = (cursor + 1) % state.cycle_size
        play_one(cursor)
        wait_one(clock, cursor)
