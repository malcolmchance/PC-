#!/usr/bin/

import sys
import serial
import time

# Instructions and Commands
# =========================
#
# Open a serial port
# ------------------
# prompt> ls /dev/*usb*
# prompt> /dev/cu.usbmodem14721   /dev/tty.usbmodem14721
# prompt> sudo screen /dev/tty.usbmodem147121
# >ver
# >000008

# Commands
# -------
# # Command	    Example	        Description
# 1	ver			ver				Returns current firmware version.
#
# 2	id			id get			Id get reads the module ID. Id set will assign a new ID to the module.
#				id set 			The new ID must be exactly 8 characters in length.
#
# 3	gpio		gpio set x		Sets the GPIO output status to high. Here x is the number of the GPIO.
#								This command accepts GPIO number from 0 -7, total 8 values Please see examples below
#                               gpio set 0 - Sets GPIO 0 to high state
#                               gpio set 4 - Sets GPIO 4 to high state
#
#				gpio clear x	Sets the GPIO output status to low. Here x is the number of the GPIO.
#								This command accepts GPIO number from 0 -7, total 8 values. Please see examples below.
#								gpio clear 0 - Sets GPIO 0 to low state
#								gpio clear 4 - Sets GPIO 4 to low state
#
#				gpio read x		Reads the digital status present at the input mentioned. Here x stands for the number of GPIO.
#								This command accepts GPIO number from 0 -7, total 8 values. The response will be either on
#								or off depending on the current digital state of the GPIO. Please see examples below.
#								gpio read 0 - Reads GPIO 0 status
#								gpio read 4 - Reads GPIO 4 status
#
#				gpio iomask xx	Set mask for selectively update multiple GPIOs with writeall/iodir command. A hexadecimal
#								value(xx) must be specified with desired bit positions set to 0 or 1 with no 0x prepended
#								(eg 02, ff). A 0 in a bit position mask the corresponding GPIO and any update to that GPIO
#								is ignored during writeall/iodir command. A 1 in a bit position will unmask that particular GPIO
#								and any updates using writeall/iodir command will be applied to that GPIO. This mask does not
#								affect the operation of set and clear commands.
#								gpio iomask ff - Unmask all GPIOs
#								gpio iomask 00 - mask all GPIOs.
#
#				gpio iodir xx	Sets the direction of all GPIO in a single operation. A hexadecimal value(xx) must be specified with
#								desired bit positions set to 0 or 1 with no 0x prepended (eg 02, ff). A 0 in a bit position configures
#								that GPIO as output and 1 configures as input. Before using gpio readall/writeall commands, the
#								direction of GPIO must be set using gpio iodir xx command. GPIO direction set by using iodir command
#								will be modified with subsequent set/clear/read commands
#								(only affects the GPIO accessed using these commands).
#								gpio iodir 00 - Sets all GPIO to output
#
#				gpio readall	Reads the status of all GPIO in a single operation. The return value will a hexadecimal number with binary
#								value 1 at bit positions for GPIO in ON state and 0 for GPIO in OFF state. Eg: a return value 00 (binary
#								0000 0000) means all GPIO are OFF. A value ff (binary 1111 1111) means all GPIO are ON.
#								gpio readall - Reads all GPIO status
#
#				gpio  writeall xx	Control all GPIO in a single operation. A hexadecimal value (xx) must be specified with desired bit
#								positions set to 0 or 1. A value 0 at a bit position will turn off the corresponding GPIO. A value 1
#								at a bit position will turn on the corresponding GPIO.
#								gpio writeall ff - Sets all GPIO to high state
#
# 4	adc			adc read x		Reads the analog voltage present at the ADC input mentioned. x stands for the number of ADC input.
#								The response will be a number that ranges from 0 - 1023. Please see examples below.
#								adc read 0 - Reads analog input 0
#								adc read 4 - Reads analog input 4'''
#
# https://docs.numato.com/doc/8-channel-usb-gpio-module-with-analog-inputs/



if (len(sys.argv) < 2):
	print "Usage: gpioread.py <PORT> <GPIONUM>\nEg: gpioread.py /dev/tty.usbmodem14721 0"
    # print "Usage: analogread.py <PORT> <Analog Channel>\nEg: analogread.py COM1 0"
    # type ls /dev/*usb* to find serial port

	sys.exit(0)
else:
	portName = sys.argv[1]
	portNumber = sys.argv[2];

#Open port for communication	
serPort = serial.Serial(portName, 19200, timeout=1)


###############################################################################
#Send "gpio readall" command
###############################################################################
def GPIOport_readall():
    serPort.write("gpio readall" + "\r")
    response = serPort.read(25)
    print response

###############################################################################
#Send "gpio read" command
###############################################################################
def GPIOport_read(gpioNum):
    serPort.write("gpio read "+ str(gpioNum) + "\r")
    response = serPort.read(25)
    print response
    #print response
    if(response[-4] == "1"):
	    print "GPIO " + str(gpioNum) +" is ON"
    elif(response[-4] == "0"):
	    print "GPIO " + str(gpioNum) +" is OFF"


###############################################################################
#Send "adc read" command
#print "Usage: analogread.py <PORT> <Analog Channel>\nEg: analogread.py COM1 0"
###############################################################################
def ADCport_read(analogNum):
    serPort.write("adc read "+ str(analogNum) + "\r")
    response = serPort.read(25)
    print "Read value of port " + str(analogNum) + "(range 0-1023): " + response[12:-3]
    #print "Reply " + response[12:-3]

###############################################################################
#Send GPIO set command
###############################################################################
def GPIOport_set(gpioNum):
    serPort.write("gpio set" +" "+ str(gpioNum) + "\r")
    print "Command sent: gpio set "+ str(gpioNum) + " ..."
    response = serPort.read(25)
    print response

###############################################################################
#Send GPIO clear command
###############################################################################
def GPIOport_clear(gpioNum):
    serPort.write("gpio "+ "clear" +" "+ str(gpioNum) + "\r")
    print "Command sent: gpio clear "+ str(gpioNum) + " ..."
    response = serPort.read(25)

######## Commands ############################

# print "\n############   Read ALL Ports   ############"
# GPIOport_readall()
#
# print "\n############     Read Port 0    ############"
# GPIOport_read(portNumber)

print "\n############     Flash LEDs     ############"

for i in range(3):
    serPort.write("gpio writeall 0 \r")
    time.sleep(.5)


    serPort.write("gpio set 0 \r")
    time.sleep(.5)
    serPort.write("gpio clear 0 \r")
    serPort.write("gpio set 1 \r")
    time.sleep(.5)
    serPort.write("gpio clear 1 \r")
    serPort.write("gpio set 2 \r")
    time.sleep(.5)
    serPort.write("gpio clear 2\r")
    serPort.write("gpio set 3 \r")
    time.sleep(.5)
    serPort.write("gpio clear 3 \r")

    time.sleep(.5)
    serPort.write("gpio writeall 0 \r")

    serPort.write("gpio set 0 \r")
    time.sleep(.5)
    serPort.write("gpio writeall 0 \r")
    time.sleep(.5)
    serPort.write("gpio set 0 \r")
    serPort.write("gpio set 1 \r")
    time.sleep(.5)
    serPort.write("gpio writeall 0 \r")
    time.sleep(.5)
    serPort.write("gpio set 0 \r")
    serPort.write("gpio set 1 \r")
    serPort.write("gpio set 2 \r")
    time.sleep(.5)
    serPort.write("gpio writeall 0 \r")
    time.sleep(.5)
    serPort.write("gpio set 0 \r")
    serPort.write("gpio set 1 \r")
    serPort.write("gpio set 2 \r")
    serPort.write("gpio set 3 \r")
    time.sleep(.5)
    serPort.write("gpio writeall 0 \r")

# def clearAll():
#     serPort.write("gpio writeall 0 \r")
#
# def zero():
#     time.sleep(.5)
#     clearAll()


# def one():
#     time.sleep(.1)
#     print "1"
#     serPort.write("gpio set 0 \r")
#     #serPort.write("gpio set 1 \r")
#     #serPort.write("gpio set 2 \r")
#     #serPort.write("gpio set 3 \r")
#     time.sleep(.5)
#     serPort.write("gpio clear 0 \r")
#     serPort.write("gpio clear 1 \r")
#     serPort.write("gpio clear 2 \r")
#     serPort.write("gpio clear 3 \r")
#
# def two():
#     time.sleep(.1)
#     print "2"
#     #serPort.write("gpio set 0 \r")
#     serPort.write("gpio set 1 \r")
#     #serPort.write("gpio set 2 \r")
#     #serPort.write("gpio set 3 \r")
#     time.sleep(.5)
#     serPort.write("gpio clear 0 \r")
#     serPort.write("gpio clear 1 \r")
#     serPort.write("gpio clear 2 \r")
#     serPort.write("gpio clear 3 \r")
#
# def three():
#     time.sleep(.1)
#     print "3"
#     serPort.write("gpio set 0 \r")
#     serPort.write("gpio set 1 \r")
#     #serPort.write("gpio set 2 \r")
#     #serPort.write("gpio set 3 \r")
#     time.sleep(.5)
#     serPort.write("gpio clear 0 \r")
#     serPort.write("gpio clear 1 \r")
#     serPort.write("gpio clear 2 \r")
#     serPort.write("gpio clear 3 \r")
#
# def four():
#     time.sleep(.1)
#     print "4"
#     #serPort.write("gpio set 0 \r")
#     #serPort.write("gpio set 1 \r")
#     serPort.write("gpio set 2 \r")
#     #serPort.write("gpio set 3 \r")
#     time.sleep(.5)
#     serPort.write("gpio clear 0 \r")
#     serPort.write("gpio clear 1 \r")
#     serPort.write("gpio clear 2 \r")
#     serPort.write("gpio clear 3 \r")
#
# def five():
#     time.sleep(.1)
#     print "5"
#     serPort.write("gpio set 0 \r")
#     #serPort.write("gpio set 1 \r")
#     serPort.write("gpio set 2 \r")
#     #serPort.write("gpio set 3 \r")
#     time.sleep(.5)
#     serPort.write("gpio clear 0 \r")
#     serPort.write("gpio clear 1 \r")
#     serPort.write("gpio clear 2 \r")
#     serPort.write("gpio clear 3 \r")
#
# def six():
#     time.sleep(.1)
#     print "6"
#     #serPort.write("gpio set 0 \r")
#     serPort.write("gpio set 1 \r")
#     serPort.write("gpio set 2 \r")
#     #serPort.write("gpio set 3 \r")
#     time.sleep(.5)
#     serPort.write("gpio clear 0 \r")
#     serPort.write("gpio clear 1 \r")
#     serPort.write("gpio clear 2 \r")
#     serPort.write("gpio clear 3 \r")
#     clearAll()
#
#
# def seven():
#     time.sleep(.1)
#     print "7"
#     serPort.write("gpio set 0 \r")
#     serPort.write("gpio set 1 \r")
#     serPort.write("gpio set 2 \r")
#     #serPort.write("gpio set 3 \r")
#     time.sleep(.5)
#     serPort.write("gpio clear 0 \r")
#     serPort.write("gpio clear 1 \r")
#     serPort.write("gpio clear 2 \r")
#     serPort.write("gpio clear 3 \r")

one()
two()
three()
four()
five()
six()
seven()
clearAll()








serPort.close()
