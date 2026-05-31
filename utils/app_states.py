from enum import IntFlag


class AppStates(IntFlag):
    """
    TODO: Add summary.
    """
    starting = 1
    ready = 2
    running = 3
    handeling_exception = 4
    crashed = 5
    set_to_exit = 6
    exiting = 7
    exited = 8
