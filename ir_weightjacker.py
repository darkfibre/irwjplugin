import gremlin
from gremlin.user_plugin import *

mode = ModeVariable("Mode", "Mode in which to use these settings")

output = VirtualInputVariable(
    "Output Device",
    "vJoy device to use as the output, must have 40 buttons",
    [gremlin.common.InputType.JoystickWrapper]
)

minWJbutton = PhysicalInputVariable(
    "Min WJ Button",
    "Button that sets the weight jacker to the minimum value",
    [gremlin.common.InputType.JoystickButton]
)

midWJbutton = PhysicalInputVariable(
    "Mid WJ Button",
    "Button that sets the weight jacker to the middle value",
    [gremlin.common.InputType.JoystickButton]
)

maxWJbutton = PhysicalInputVariable(
    "Max WJ Button",
    "Button that sets the weight jacker to the maximum value",
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

minDefault = IntegerVariable("Default min WJ", "Default value for minimum WJ", -20, -20, 0)

midDefault = IntegerVariable("Default mid WJ", "Default value for middle WJ", 0, -19, 19)

maxDefault = IntegerVariable("Default max WJ", "Default value for maximum WJ", 20, 0, 20 )

g_wjValues = [ minDefault.value, midDefault.value, maxDefault.value ]
g_wjCurrent = 1 # 0 = min, 1 = mid, 2 = max

decorator_min = minWJbutton.create_decorator(mode.value)
decorator_mid = midWJbutton.create_decorator(mode.value)
decorator_max = maxWJbutton.create_decorator(mode.value)
decorator_inc = incWJbutton.create_decorator(mode.value)
decorator_dec = decWJbutton.create_decorator(mode.value)

@decorator_min.button(minWJbutton.input_id)
def minWJbtn(event, vjoy):
    global g_wjCurrent
    g_wjCurrent = 0
    buttonId = gremlin.util.clamp((g_wjValues[g_wjCurrent]+20),0,40)
    vjoy[output.vjoy_id].button(buttonId).is_pressed = event.is_pressed


@decorator_mid.button(midWJbutton.input_id)
def midWJbtn(event, vjoy):
    global g_wjCurrent
    g_wjCurrent = 1
    buttonId = gremlin.util.clamp((g_wjValues[g_wjCurrent]+20),0,40)
    vjoy[output.vjoy_id].button(buttonId).is_pressed = event.is_pressed

@decorator_max.button(maxWJbutton.input_id)
def maxWJbtn(event, vjoy):
    global g_wjCurrent
    g_wjCurrent = 2
    buttonId = gremlin.util.clamp((g_wjValues[g_wjCurrent]+20),0,40)
    vjoy[output.vjoy_id].button(buttonId).is_pressed = event.is_pressed

@decorator_inc.button(incWJbutton.input_id)
def incWJbtn(event, vjoy):
    global g_wjValues
    g_wjValues[g_wjCurrent] += adjustmentSize.value
    buttonId = gremlin.util.clamp((g_wjValues[g_wjCurrent]+20),0,40)
    vjoy[output.vjoy_id].button(buttonId).is_pressed = event.is_pressed

@decorator_dec.button(decWJbutton.input_id)
def decWJbtn(event, vjoy):
    global g_wjValues
    g_wjValues[g_wjCurrent] -= adjustmentSize.value
    buttonId = gremlin.util.clamp((g_wjValues[g_wjCurrent]+20),0,40)
    vjoy[output.vjoy_id].button(buttonId).is_pressed = event.is_pressed
