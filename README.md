# irwjplugin - An iRacing Weight Jacker plugin for Joystick Gremlin

This is a plugin for Joystick Gremlin to simplify the usage of the weight jacker in iRacing. It enables you to configure button assignments to instantly select minimum, maximum, and a middle WJ setting. Additional hotkeys can be bound to increment or decrement the selected values on the fly. The new value will be remembered, so it will be instantly re-selected when you press the min/mid/max button again.

This provides maximum flexibility with the fewest possible button assignments.

### Prerequisites ####

Download and install [vJoy](https://github.com/shauleiz/vJoy/releases) and [Joystick Gremlin](https://whitemagic.github.io/JoystickGremlin/download/)

Run the "Configure vJoy" utility and configure your vJoy device to have at least **41 buttons.** You do not need any other options enabled for the device, another reboot will likely be required after configuring vJoy.

### Setup Instructions ###

* Run Joystick Gremlin and go to the **plugins** tab.
* Add a plugin, and select the ir_weightjacker.py file you have downloaded.
* Click on the small gear to configure the plugin.
	* Make sure the correct vJoy device is selected
	* Click on each of the button assignments and press the button(s) on your controller to assign them
	* Leave the other values as default for now
* Click on the **Activate** button on the toolbar to enable the remapping/configuration
* Optional: Launch **vJoy Monitor** and verify the buttons on the vJoy device are triggered as you press different buttons.
* iRacing Setup
	* Launch iRacing and go to options / controls
	* Select the right rear spring offset, set the type of **Rotary Encoder**
	* Press the button on your wheel assigned to **Minimum** WJ, followed by the button assigned to **Maximum** WJ. You should see iRacing show the **0-40** in the calibration dialog.
	* Click **Done**

That's about it.
