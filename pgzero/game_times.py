import pygame
import datetime


def get_game_time_secs():
    """
    Total runtime of the game
    :return: time elapsed in seconds
    """
    return pygame.time.get_ticks() / 1000.0


def convert_secs_to_time_format(time_secs):
    """
    It converts a time in seconds to a readable format
    :param time_secs:
    :return: string
    """
    return str(datetime.timedelta(seconds=time_secs))


def get_game_timer():
    """
    It converts the Total Game Time from seconds to a readable format
    hh:mm:s:ms
    :return: string
    """
    return convert_secs_to_time_format(get_game_time_secs())



