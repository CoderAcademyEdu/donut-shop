from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import rpyc


class DonutUI():

    def __init__(self):

        self.app = QApplication([])

        connect_panel = self.create_connect_panel()

        window = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(connect_panel)
        window.setLayout(layout)
        window.show()


        self.main_layout = layout

        self.window = window

    def create_connect_panel(self):

        # Create a panel widget (a QFrame) which will contain all
        # widgets relating to this device, within a border
        panel = QFrame()
        panel.setFrameShape(QFrame.Panel)
        layout = QVBoxLayout()
        panel.setLayout(layout)

        lbl_ip_address = QLabel('Enter IP address or hostname:')
        inp_ip_address = QLineEdit()
        inp_ip_address.setText('127.0.0.2')
        btn_connect = QPushButton('Link new device')

        layout.addWidget(lbl_ip_address)
        layout.addWidget(inp_ip_address)
        layout.addWidget(btn_connect)

        def connect():
            hostname = inp_ip_address.text()

            # RPC connection is created here
            connection = rpyc.classic.connect(hostname)

            # Takes the _remote_ object my_device and makes a local proxy
            device = connection.modules.__main__.my_device

            # Creates a device panel to control this device
            self.add_device_panel(device)

        # set button behaviour
        btn_connect.clicked.connect(connect)

        return panel

    def add_device_panel(self, device):

        # Create a panel widget (a QFrame) which will contain all
        # widgets relating to this device, within a border
        panel = QFrame()
        panel.setFrameShape(QFrame.Box)

        # Create a layout to hold the widgets in this panel
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # All devices have a name
        # (polymorphism is being used here)
        lbl_name = QLabel('Device: ' + device.get_name())

        # All devices have a description of their contents
        # (polymorphism is being used here)
        lbl_label = QLabel(device.get_label())

        # Add these widgets to the layout
        layout.addWidget(lbl_name)
        layout.addWidget(lbl_label)

        # These ifs and elifs determine whether we have a
        # SwitchDevice object, a WriteableDevice object,
        # or a ReadableDevice object.

        if hasattr(device, 'turn_on'):

            # Add widgets to the layout appropriate for a switch object
            rad_on = QRadioButton(device.get_on_label())
            rad_off = QRadioButton(device.get_off_label())
            layout.addWidget(rad_on)
            layout.addWidget(rad_off)

            # Read the current device status and select the right
            # radio button
            # NOTE: this only happens once when the panel is created
            if device.read() == True:
                rad_on.setChecked(True)
            else:
                rad_off.setChecked(True)

            # Set up button behaviour
            def rad_change():
                if rad_on.isChecked():
                    device.turn_on()
                else:
                    device.turn_off()

            rad_on.toggled.connect(rad_change)

        elif hasattr(device, 'write'):

            # Add widgets to the layout appropriate for a writeable object
            inp_value = QLineEdit()
            # (initial input box text contains current device value,
            #  by calling device.read() )
            inp_value.setText(str(device.read()))

            btn_set = QPushButton('Set new value')

            layout.addWidget(inp_value)
            layout.addWidget(btn_set)


            # Set up button behaviour
            def set_value():
                device.write(inp_value.text())

            btn_set.clicked.connect(set_value)

        elif hasattr(device, 'read'):

            # Add widgets to the layout appropriate for a readable object
            # (initial label text contains current device value,
            #  by calling device.read() )
            lbl_value = QLabel(str(device.read()))
            layout.addWidget(lbl_value)

        # All widgets have been added, add entire panel to main app window
        self.main_layout.addWidget(panel)



    def run(self):
        self.app.exec_()
