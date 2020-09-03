#!/usr/bin/env python3


"""
TODO
    - Have a more robust argument parser (i.e. accept only positive float value)
"""


"""
Requires the following command line utilities (in PATH):
    - xrandr
    - grep
    - awk
"""


# dependencies (modules)
import argparse
import sh
import sys


class Controller:

    def __init__(self, display=None):
        """
        `display` - name of the OLED panel
        """

        self.display = display

    def get_display_name(self):
        """
        Returns the name (str) of the primary display found via xrandr;
        if an error occurs, returns None
        """

        try:
            xrandr_output = sh.xrandr()
            line_with_display = sh.grep(xrandr_output, '-im', '1', 'primary')
            display = sh.awk(line_with_display, '{print $1}')
            return display.strip()
        except sh.CommandNotFound:
            print('[error] missing tool')
        except:
            print('[error] something went wrong')
        return None

    def get_current_brightness(self):
        """
        Returns the current brightness (float) set with xrandr;
        if an error occurs returns None
        """

        try:
            xrandr_output = sh.xrandr('--verbose')
            line_with_brightness = sh.grep(xrandr_output, '-im', '1', 'brightness')
            brightness = sh.awk(line_with_brightness, '{print $2}')
            return float(brightness)
        except sh.CommandNotFound:
            print('[error] missing tool')
        except:
            print('[error] something went wrong')
        return None

    def set_new_brightness(self, new_brightness: float):
        """
        Requirement: 0 < new_brightness <= 1
        Note that for OLED displays, 0 brightness is pitch black,
        so `new_brightness` must be greater than 0
        """

        if 0 < new_brightness <= 1:
            try:
                sh.xrandr('--output', self.display, '--brightness', new_brightness)
            except sh.CommandNotFound:
                print('[error] missing tool')
            except:
                print('[error] something went wrong')
        else:
            print('[error] invalid new brightness')

    def parse_arguments(self, argument: list):
        """
        Accepts `argument` (list) and returns a parsed namespace with
        `increase` and `decrease` (default=None, float if specified)

        Possible arguments/flags:
            -h, --help
            -i, --increase
            -d, --decrease
        """

        description = 'Brightness controller for OLED displays in Linux'
        metavar = 'STEP'

        parser = argparse.ArgumentParser(description=description)
        required_group = parser.add_argument_group(title='Requires one or the other')
        group = required_group.add_mutually_exclusive_group(required=True)
        group.add_argument('-i', '--increase', nargs=1, type=float,
                           help=f'Increase brightness by {metavar}', metavar=metavar)
        group.add_argument('-d', '--decrease', nargs=1, type=float,
                           help=f'Decrease brightness by {metavar}', metavar=metavar)

        return parser.parse_args(argument)


def set_display_name(controller: Controller, display: str):
    if not display:
        tmp_display = controller.get_display_name()
        if tmp_display is None:
            sys.exit(1)
        controller.display = tmp_display
    else:
        controller.display = display


def get_delta(controller: Controller) -> float:
    arguments = controller.parse_arguments(sys.argv[1:])
    if arguments.increase is not None:
        return float(arguments.increase[0])
    return float(arguments.decrease[0] * -1)


if __name__ == '__main__':

    # start user config

    display = ''

    # end user config

    instance = Controller()
    set_display_name(instance, display)
    current_brightness = instance.get_current_brightness()
    if current_brightness is not None:
        instance.set_new_brightness(current_brightness + get_delta(instance))
