# irwjplugin v0.0.3 by Ryan Otis

import gremlin
import threading
import time
from gremlin.user_plugin import *

mode = ModeVariable("Mode", "Mode in which to use these settings")

output = VirtualInputVariable(
    "Select vJoy device (MUST have at least 41 buttons)",
    "vJoy device to use as the output, must have at least 41 buttons",
    [gremlin.common.InputType.JoystickButton]
)

minWJbutton = PhysicalInputVariable(
    "Min WJ Button",
    "Button to set the weight jacker to the minimum value (default is -20)",
    [gremlin.common.InputType.JoystickButton]
)

midWJbutton = PhysicalInputVariable(
    "Mid WJ Button",
    "Button to set the weight jacker to the middle value (default is 0)",
    [gremlin.common.InputType.JoystickButton]
)

maxWJbutton = PhysicalInputVariable(
    "Max WJ Button",
    "Button to set the weight jacker to the maximum value (default is +20)",
    [gremlin.common.InputType.JoystickButton]
)

incWJbutton = PhysicalInputVariable(
    "Increment WJ Button",
    "Button that increments the current WJ setting",
    [gremlin.common.InputType.JoystickButton]
)

decWJbutton = PhysicalInputVariable(
    "Decrement WJ Button",
    "Button that decrements the current WJ setting",
    [gremlin.common.InputType.JoystickButton]
)

adjustmentSize = IntegerVariable(
    "WJ Increment size",
    "Number of steps taken with each increment or decrement",
    1,
    1,
    10
)

# I originally made this configurable, but it's really unnecessary and just caused confusion
#
# minDefault = IntegerVariable("Default min WJ", "Default value for minimum WJ", -20, -20, 0)
# midDefault = IntegerVariable("Default mid WJ", "Default value for middle WJ", 0, -19, 19)
# maxDefault = IntegerVariable("Default max WJ", "Default value for maximum WJ", 20, 0, 20 )
#
# g_wjValues = [ minDefault.value, midDefault.value, maxDefault.value ]

g_wjValues = [ -20, 0, 20 ]
g_wjCurrent = 1 # 0 = min, 1 = mid, 2 = max
g_state = [ 0, 0 ]
g_cal_t = None

g_btnMin = 1 # First button on device
g_btnMax = 41 # Last button on device
g_wjOffset = g_btnMin + 20 # Offset between absolute WJ value and button ID

decorator_min = minWJbutton.create_decorator(mode.value)
decorator_mid = midWJbutton.create_decorator(mode.value)
decorator_max = maxWJbutton.create_decorator(mode.value)
decorator_inc = incWJbutton.create_decorator(mode.value)
decorator_dec = decWJbutton.create_decorator(mode.value)

@decorator_min.button(minWJbutton.input_id)
def minWJbtn(event, vjoy):
    global g_wjCurrent, g_state
    g_wjCurrent = 0
    buttonId = gremlin.util.clamp((g_wjValues[g_wjCurrent]+g_wjOffset),g_btnMin,g_btnMax)
    vjoy[output.vjoy_id].button(buttonId).is_pressed = event.is_pressed

    g_state[0] = 1 if event.is_pressed else 0
    check_calibration(event.is_pressed, vjoy)

@decorator_mid.button(midWJbutton.input_id)
def midWJbtn(event, vjoy):
    global g_wjCurrent
    g_wjCurrent = 1
    buttonId = gremlin.util.clamp((g_wjValues[g_wjCurrent]+g_wjOffset),g_btnMin,g_btnMax)
    vjoy[output.vjoy_id].button(buttonId).is_pressed = event.is_pressed

@decorator_max.button(maxWJbutton.input_id)
def maxWJbtn(event, vjoy):
    global g_wjCurrent, g_state
    g_wjCurrent = 2
    buttonId = gremlin.util.clamp((g_wjValues[g_wjCurrent]+g_wjOffset),g_btnMin,g_btnMax)
    vjoy[output.vjoy_id].button(buttonId).is_pressed = event.is_pressed

    g_state[1] = 1 if event.is_pressed else 0
    check_calibration(event.is_pressed, vjoy)

@decorator_inc.button(incWJbutton.input_id)
def incWJbtn(event, vjoy):
    global g_wjValues
    if event.is_pressed and g_wjValues[g_wjCurrent] < 20:
        g_wjValues[g_wjCurrent] += adjustmentSize.value
    buttonId = gremlin.util.clamp((g_wjValues[g_wjCurrent]+g_wjOffset),g_btnMin,g_btnMax)
    vjoy[output.vjoy_id].button(buttonId).is_pressed = event.is_pressed

@decorator_dec.button(decWJbutton.input_id)
def decWJbtn(event, vjoy):
    global g_wjValues
    if event.is_pressed and g_wjValues[g_wjCurrent] > -20:
        g_wjValues[g_wjCurrent] -= adjustmentSize.value
    buttonId = gremlin.util.clamp((g_wjValues[g_wjCurrent]+g_wjOffset),g_btnMin,g_btnMax)
    vjoy[output.vjoy_id].button(buttonId).is_pressed = event.is_pressed

def check_calibration(is_pressed, vjoy):
    global g_cal_t

    # Check for calibration routine if min/max are both pressed
    if g_state[0] == 1 and g_state[1] == 1:
        if is_pressed:
            if g_cal_t is not None: g_cal_t.cancel()
            g_cal_t = threading.Timer(2.0, run_calibration, [vjoy])
            g_cal_t.start()
        else:
            if g_cal_t is not None: g_cal_t.cancel()
            g_cal_t = None
    else:
        if g_cal_t is not None:
            g_cal_t.cancel()
            g_cal_t = None

def run_calibration(vjoy):
    tts = gremlin.tts.TextToSpeech()
    tts.speak("Starting calibration routine, please release buttons.")

    gremlin.util.log("Starting calibration routine, please release buttons.")

    vjoy[output.vjoy_id].button(g_wjValues[0]+g_wjOffset).is_pressed = False
    vjoy[output.vjoy_id].button(g_wjValues[2]+g_wjOffset).is_pressed = False
    time.sleep(3.0)

    for n in range(5):
       vjoy[output.vjoy_id].button(g_btnMin).is_pressed = True 
       time.sleep(0.1)
       vjoy[output.vjoy_id].button(g_btnMin).is_pressed = False 
       time.sleep(0.4)
       vjoy[output.vjoy_id].button(g_btnMax).is_pressed = True 
       time.sleep(0.1)
       vjoy[output.vjoy_id].button(g_btnMax).is_pressed = False 
       time.sleep(0.4)

    gremlin.util.log("Calibration routine complete")
