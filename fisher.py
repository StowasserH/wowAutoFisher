#!/usr/bin/autokey
# -*- coding: utf-8 -*-
"""A small script that automates manual fishing in World of Warcraft.
   https://github.com/StowasserH/wowAutoFisher
"""

__author__ = "harald@stowasser.tv"
__copyright__ = "2023 Harald Stowasser"
__license__ = "MIT"
__maintainer__ = "Harald Stowasser"
__email__ = "harald@stowasser.tv"
__status__ = "Production"

import pyautogui
import time
from PIL import ImageGrab

# Position of the icon for fishing
b_fish = (1900, 345)

# Screen resolution
res_x = 1920
res_y = 1080

# Threshold splash
th_sp = 25
# rgb values for the swimmer
sw = (120, 100, 50)
# Threshold swimmer detection
th_sw = 4
# Verbose
v = 1
# use xte
xte = 1
# ___________________________________________________
#
# Area where the swimmer is searched
x_min = res_x // 4
x_max = res_x - res_x // 4
y_min = res_y // 6
y_max = res_y - res_y // 2 + 100

end_script = False


def xte(command: str) -> str:
    """
    Sends a xte commando from the system level.
    
    :param command: the commando
    :return:
    """
    # print(command)
    # A somewhat strange construct, but the system command requires this dummy.
    dummy_string: str = "" + system.exec_command("xte " + command + " && echo 'done'", True)
    return dummy_string


def interpolate_area(x: int, y: int, px: object) -> tuple:
    """
    Calculates the average values of a pixel area.

    :param x: x position of the area
    :param y: y position of the area
    :param px: The container for the pixel values
    :return: tuple of r g b vaues
    """
    n = r = g = b = 0
    for xx in range(x - 10, x + 10, 2):
        for yy in range(y - 10, y + 10, 2):
            n = n + 1
            rr, gg, bb = px[xx, yy]
            r = r + rr
            g = g + gg
            b = b + bb
    return r // n, g // n, b // n
    # rgb(111, 95, 68)


def find_float() -> object:
    """
    Look for the fishing float

    :return: None or a tuple of int [brightnes,x pos,y pos,r,g,b]
    """
    finds = []
    x, y = pyautogui.position()
    if v > 1:
        print("  find from " + str(x) + " " + str(y))
    px: None = ImageGrab.grab().load()
    # create an aray of posible positions
    for xx in range(x_min, x_max, 4):
        for yy in range(y_min, y_max, 4):
            if px[xx, yy][0] > sw[0] and px[xx, yy][1] > sw[1] and px[xx, yy][2] > sw[1]:
                r, g, b = interpolate_area(xx, yy, px)
                finds.append((r + g + b, xx, yy, r, g, b))
    # if too many positions are found, the image will be too bright and no good results can be expected
    if len(finds) > 40:
        if v > 0:
            print("  to much findings:" + str(len(finds)))
        return None
    # Sort the areas by brightness
    s_finds = sorted(finds, key=lambda x: x[0])
    found = False
    # position the mouse on the found position and check whether the float has become brighter.
    while s_finds:
        last = s_finds.pop()
        pyautogui.moveTo(last[1], last[2])
        time.sleep(0.1)
        px2 = ImageGrab.grab().load()
        r, g, b = interpolate_area(last[1], last[2], px2)
        if v > 1:
            print("  ." + str(last[1]) + " " + str(last[2]))
        if r > last[3] + th_sw and g > last[3] + th_sw and b > last[4] + th_sw:
            return last
    #time.sleep(0.1)
    return None


def wait_splash(last: tuple) -> bool:
    """
    Just wait until the splash lights up the area

    :param last: tuple of int [brightnes,x pos,y pos,r,g,b]
    :return:
    """
    if v > 0:
        print("found " + str(last))
    start_time = time.time()
    while time.time() - start_time < 12:
        px2 = ImageGrab.grab().load()
        r, g, b = interpolate_area(last[1], last[2], px2)
        if r > last[3] + th_sp and g > last[3] + th_sp and b > last[4] + th_sp:
            return True
        time.sleep(0.1)
    return False


def fish():
    """
    Click on the fishing icon
    """
    time.sleep(0.5)
    pyautogui.click(x=b_fish[0], y=b_fish[1], button='left')
    time.sleep(0.5)


def check_end():
    """Checks whether the script should end.
        If either store.GLOBALS["STOP"] or self.end_script is true, the script exits.
        This is very useful when testing a script, or when an error has crept in while it was running.
        You should definitely assign a hotkey to the "stop script" program for this.
    """
    if end_script or store.GLOBALS.get("STOP", False):
        # Reset the global variable, otherwise the next script will be aborted immediately.
        store.set_global_value("STOP", False)
        if v > 0:
            print("Stop is called... exiting")
        exit(1)
    else:
        return True


if v > 0:
    print(" search from " + str(x_min) + ":" + str(y_min) + " to " + str(x_max) + ":" + str(y_max))
# The main function for auto fishing.
while check_end():
    fish()
    time.sleep(0.5)
    find = find_float()
    if find:
        splash = wait_splash(find)
        if not splash:
            if v > 0:
                print("  no splash detected")
        else:
            time.sleep(0.2)
            if xte:
                xte("'mouseclick 3'")
            else:
                pyautogui.click(button='right')
            time.sleep(4)
