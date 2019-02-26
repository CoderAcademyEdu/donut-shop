# Donut shop

## Usage

In 4 separate terminals, run:

    cd remote
    ./donut_machine.py
  
    cd remote
    ./sweetness.py
  
    cd remote
    ./icing_control.py
  
    cd local
    ./main.py

Then in the GUI you can connect to

* 127.0.0.2
* 127.0.0.3
* 127.0.0.4

## Source code

* local/donut\_ui.py
  * contains the GUI for the Donut shop console
* local/drag\_drop\_container.py
  * is unfinished! You don't need to make one, you can copy the one from the drag and drop example.
* remote/rpyc\_classic.py
  * BOILERPLATE CODE, leave it. You don't need to read this file.
* remote/device.py
  * abstract class that all devices inherit from
  * creates a method that returns a device name
* remote/switch\_device.py
  * abstract class that "on/off" or other two-option devices can inherit from
* remote/readable\_device.py
  * a device that has a read-only value (such as a thermometer)
* remote/writeable\_device.py
  * a device that has a read-write value (such as an air conditioner temperature)
* everything else in the `remote` directory:
  * these files simulate the actual devices themselves
  * they all inherit directly from another class and indirectly from device.py

## donut\_ui.py

* In `__init__` method
  * The usual stuff happens here
  * A drag and drop container needs to be created here instead of a `window`
* In `def connect():` function definition
  * this is where the RPC link is created
  * `connection = rpyc.classic.connect(hostname)` sets up an RPC link
  * `device = connection.modules.__main__.my_device` is where an object within the IOT device is "assigned" to the variable `device`.
  * This basically means that any method called on `device` will _actually_ run on the server (i.e. the device) which can of course run on a different machine
  * For example, with the `donut_machine` server, the variable `my_device` in `icing_control.py` is also getting assigned to the `device` variable in donut\_ui.py
  * `device` is thus a _proxy object_ and so you can say that accessing its methods is using the **proxy object design pattern**.
  * you will notice that `device` is passed into the `add_device_panel()` method. This allows `add_device_panel` to use the device and call its methods.
