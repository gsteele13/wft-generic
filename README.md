<!-- #region -->
# Generic driver for WFT instruments

https://windfreaktech.com/

## Installation

You need the package `pyserial`. 

And then you can pip install from the source folder: 

```
pip install .
```

## Aim of the driver

Basic aim:

* To provide robust read / write / query functions for serial communication with WFT devices

Ambitious aim: 

* To parse the help function of the windfreak to create automatically generated "settable" functions
* Main purpose of this aim: to save the reader reading the help and make things more "pythonic"

## Status

Basic aim works!

Ambitious aim: I thought it was working but I can no longer figure out myself how to use my own code. Work in progress. 
'
## Example: Basic usage


First you need to find the WFT device. Probably windows explorer / NImax or some tool like that will help you on windows. 

On mac (and probably linux), the WFT devices show up as a device in /dev/tty.usbXXXXXXX. I usually figure out which one by doing this (usually I have only one usb TTY device on my macbook):

```
import glob
devs = glob.glob("/dev/tty.usb*")
devs
```

I can then create a WFT instance using:

```
port = "/dev/tty.usbmodem206C34714E561"
wft = WFT(port)
```

And then this function is useful:

```
wft.help()
```

on my SynthHD gives:

```
C  %d  Control Channel (A(0) or B(1))   (0)
f  %f  RF Frequency Now (MHz) 1000.00000000,  (1000.000000)
W  %f  RF Power (dBm) 0.000,  (0.000000)
V  %d  Amp Calibration success?  (1)
Z  %d  Temperature Comp (0=none, 1=on set, 2=1sec, 3=10sec) 3,  (3)
a  %d  VGA DAC Setting (0=min, 4000=max) 724,  (711)
~  %f  RF Phase Step (0=minimum, 360.0=maximum) 0.0000,  (0.000000)
h  %d  RF High(1) or Low(0) Power 1,  (1)
E  %d  PLL Chip En On(1) or Off(0) 1,  (0)
U  %d  PLL charge pump current 5,  (5)
b  %d  REF Doubler On(1) or Off(0) 0,  (0)
i  %f  Channel spacing (Hz) 100.000,  (100.000000)
x  %d  Reference (external=0, int 27MHz=1, int 10MHz=2)  (1)
*  %f  PLL reference frequency (MHz)  (27.000000)
l  %f  Sweep lower frequency (MHz) 1000.00000000,  (1000.000000)
u  %f  Sweep upper frequency (MHz) 5000.00000000,  (5000.000000)
s  %f  Sweep step size (MHz/%) 200.00000000,  (200.000000)
t  %f  Sweep step time (mS) 1.000,  (1.000000)
[  %f  Sweep amplitude low (dBm) 0.000,  (0.000000)
]  %f  Sweep amplitude high (dBm) 0.000,  (0.000000)
^  %d  Sweep direction (up=1 / down=0) 1,  (1)
k  %f  Sweep differential seperation (MHz)  (1.000000)
n  %d  Sweep differential: (0=off, 1=ChA-DiffFreq, 2=ChA+DiffFreq)   (0)
X  %d  Sweep type (lin=0 / tab=1 / %=2) 0,  (0)
g  %d  Sweep run (on=1 / off=0)  (0)
c  %d  Sweep set continuous mode  (0)
w  %d  Enable trigger: (0=software, 1=sweep, 2=step, 3=hold all, ..)  (0)
Y  %d  Trigger Polarity (active low=0 / active high=1)  (0)
F  %d  AM step time (uS)  (20)
q  %d  AM # of cycle repetitions  (65)
A  %d  AM Run Continuous (on=1 / off=0)  (0)
P  %d  Pulse On time (uS) 1,  (1)
O  %d  Pulse Off time (uS) 10,  (10)
R  %d  Pulse # of repetitions 10,  (10)
:  %d  Pulse Invert signal (on=1 / off=0) 0,  (0)
G      Pulse Run one burst
j  %d  Pulse continuous mode  (0)
<  %d  FM Frequency (Hz) 1000,  (1000)
>  %d  FM Deviation (Hz) 100000,  (100000)
,  %d  FM # of repetitions 100,  (100)
;  %d  FM Type (sinusoid=0 / chirp=1) 0,  (0)
/  %d  FM continuous mode  (0)
p  %d  Phase lock status (lock=1 / unlock=0) 1,  (0)
z  %f  Temperature in degrees C  (33.000000)
v  %f  Show version (0=FW, 1=HW, 2=Model) 3.21,  (2.060000)
+      Model Type
-  %d  Serial Number  (1418)
e      Write all settings to eeprom
?      help
```

And from there I can do things like set  frequencies:

```
wft.write("f10.002")
```

and check their values:

```
wft.query("f?")
```

That's the basics!
<!-- #endregion -->
