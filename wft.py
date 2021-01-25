import serial
from time import sleep

class WFT:
    def __init__(self, port, timeout=0.01):
        self.s = serial.Serial(port, timeout=timeout)
        self.value = {}
        self.command_char = {}
        self.command_fmt = {}
        self.parse_settings()
    def write(self, msg):
        self.s.write(msg.encode('ascii', 'ignore'))
    def read(self):
        # No handshaking or msg term, so just read until timeout (10 ms)...
        # smarter in the future: keep reading in blocks until we reach a timeout,
        # then we can also maybe make the timeout smaller
        return self.s.read(10000).decode('utf-8')
    def query(self,msg):
        self.write(msg)
        # some commands, in particular firmware and model, take some time...
        # (could hard code a list of slow commands if we want...)
        # (but a 50 ms sleep is a safe solution...)
        sleep(0.05) 
        return self.read()
    def parse_settings(self):
        s = self.query("?")
        lines = s.splitlines()[:-2] # always sends a final blank line? 
        for l in lines:
            key = " ".join(l.split(" ")[:-1])[3:] # reverse engineered...
            # One problem: there are 3 types of commands:
            #
            # (A) set a value (eg f, a), 1 paramter, no data returned
            # (B) read a value (eg v, +, -), no parameters, data returned
            # (C) execute a command (eg b), no parameters, no data returned
            #
            # Aside from guessing, there is no way to figure out what types
            # of commands they are...
            #
            # And, furthermore, the parameters might be ints or floats,
            # and aside from reading PDFs, or maybe guessing from 
            # the settings as they are printed, there is no way to know what 
            # they need
            # 
            # Although, if I trust that they have always used a decimal place
            # for any parameters that should be floats, then there could be
            # a solution
            #
            self.command_char[key] = l[0]
            val_string = l.split(" ")[-1]
            try: 
                float(val_string) # this will fail if it is not a float 
                if "." in val_string: # float
                    self.value[key] = float(val_string)
                    self.command_fmt = "%f"
                else: # int
                    self.value[key] = int(val_string)
                    self.command_fmt = "%d"
            except ValueError:
                # for commands of type (C), this will be empty
                self.value[key] = self.query(l[0]) 
                self.command_fmt = ""

# # Basic test
# import glob
# devs = glob.glob("/dev/tty.usb*")
# devs
#
# port = "/dev/tty.usbmodem123451"
# wft = WFT(port)
# wft.read()

# # Update github folder
#
# # ! cp wft.py /Users/gsteele/Documents/GitHub/wft-generic/