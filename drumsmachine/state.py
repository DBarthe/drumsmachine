tempo = 160
cycle_size = 16
shuffle = 50

# tracks = {
#     "/kick": [
#         True, False, False, False,
#         True, False, False, False,
#         True, False, False, False,
#         True, False, True, True,
#     ],
#     "/snare": [
#         False, False, False, False,
#         True, False, False, False,
#         False, False, False, False,
#         True, False, False, False,
#     ],
#     "/openhat": [
#         False, False, True, False,
#         False, False, True, False,
#         False, False, True, False,
#         False, False, True, False,
#     ],
#     "/closedhat": [
#         False, False, True, False,
#         False, False, True, False,
#         False, False, True, False,
#         False, False, True, False,
#     ],
#     "/clap": [
#         False, False, False, True,
#         True, False, False, False,
#         False, False, False, True,
#         True, False, False, False,
#     ]
# }

# tracks = {
#     "/kick": [
#         True, False, False, False,
#         True, False, False, False,
#         True, False, False, False,
#         True, False, False, False,
#     ],
#     "/snare": [
#         False, False, False, False,
#         False, False, False, False,
#         False, False, False, False,
#         False, False, False, False,
#     ],
#     "/openhat": [
#         False, False, False, False,
#         False, False, False, False,
#         False, False, False, False,
#         False, False, False, False,
#     ],
#     "/closedhat": [
#         False, False, False, False,
#         False, False, False, False,
#         False, False, False, False,
#         False, False, False, False,
#     ],
#     "/clap": [
#         False, False, False, False,
#         False, False, False, False,
#         False, False, False, False,
#         False, False, False, False,
#     ]
# }


tracks = {
    "/kick": [
        True, False, False, False,
        True, False, False, False,
        True, False, False, False,
        True, False, False, False,
    ],
    "/snare": [
        False, False, False, False,
        False, False, False, False,
        False, False, True, True,
        True, False, False, False,
    ],
    "/openhat": [
        False, False, False, False,
        True, False, False, False,
        False, False, False, False,
        True, True, False, False,
    ],
    "/closedhat": [
        True, False, True, False,
        True, False, True, False,
        True, False, True, False,
        True, False, True, False,
    ],
    "/clap": [
        True, False, False, True,
        False, False, True, False,
        False, False, False, False,
        False, False, True, False,
    ]
}


tracks_order = ["/kick", "/snare", "/closedhat", "/openhat", "/clap"]

tracks_params = {
    "/kick": [1, 1, 0, 0.2, 0.01, 261, 50],
    "/snare": [
    ],
    "/openhat": [
    ],
    "/closedhat": [
    ],
    "/clap": [
    ]
}

tracks_tmp_mute = {}
