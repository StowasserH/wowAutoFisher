import pyautogui
import sys
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
sw = (111, 95, 48)
# Threshold swimmer detection
th_sw = 4
# Verbose
v = 1
# use xte
xte = 1
# ___________________________________________________
#
# Area where the swimmer is searched
xmin = res_x // 4
xmax = res_x - res_x // 4
ymin = res_y // 6
ymax = res_y - res_y // 2 + 100

end_script = False


def xte(command):
    # print(command)
    dummy_string = "" + system.exec_command("xte " + command + " && echo 'done'", True)
    return dummy_string


if v > 0:
    print(" search from " + str(xmin) + ":" + str(ymin) + " to " + str(xmax) + ":" + str(ymax))


def checkhook(x, y, px):
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


def findhook():
    import pyautogui
    finds = []
    x, y = pyautogui.position()
    if v > 1:
        print("  find from " + str(x) + " " + str(y))
    px = ImageGrab.grab().load()
    for xx in range(xmin, xmax, 4):
        for yy in range(ymin, ymax, 4):
            if px[xx, yy][0] > sw[0] and px[xx, yy][1] > sw[1] and px[xx, yy][2] > sw[1]:
                r, g, b = checkhook(xx, yy, px)
                finds.append((r + g + b, xx, yy, r, g, b))
    if len(finds) > 40:
        if v > 0:
            print("  to much findings:" + str(len(finds)))
        return None
    s_finds = sorted(finds, key=lambda x: x[0])
    found = False
    while s_finds:
        last = s_finds.pop()
        pyautogui.moveTo(last[1], last[2])
        time.sleep(0.1)
        px2 = ImageGrab.grab().load()
        r, g, b = checkhook(last[1], last[2], px2)
        if v > 1:
            print("  ." + str(last[1]) + " " + str(last[2]))
        if r > last[3] + th_sw and g > last[3] + th_sw and b > last[4] + th_sw:
            return last
    time.sleep(1)
    return None


def wait_spash(last):
    if v > 0:
        print("found " + str(last))
    starttime = time.time()
    while time.time() - starttime < 12:
        px2 = ImageGrab.grab().load()
        r, g, b = checkhook(last[1], last[2], px2)
        if r > last[3] + th_sp and g > last[3] + th_sp and b > last[4] + th_sp:
            return True
        time.sleep(0.1)
    return False


def fish():
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


while check_end():
    fish()
    time.sleep(0.5)
    find = findhook()
    if find:
        splash = wait_spash(find)
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


