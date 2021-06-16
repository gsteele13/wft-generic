import serial
from time import sleep

# +
class setting_dict(dict):
    def __init__(self, wft):
        self.wft = wft
    def update_key(self,key,value): # used only when fetching
        super().__setitem__(key, value)
    def __setitem__(self, key, value):
        super().__setitem__(key, value) 
        fmt = self.wft.command_fmt[key]
        char = self.wft.command_char[key]
        if fmt == "":
            self.write(char)
        else:
            cmd = ("%s" + fmt) % (char, value)
            self.wft.write(cmd)
        self.wft.parse_settings()
    def __getitem__(self, key):
        return super().__getitem__(key)
        
class WFT:        
    def __init__(self, port, timeout=0.01, debug=False):
        self.debug = debug
        self.s = serial.Serial(port, timeout=timeout)
        self.setting = setting_dict(self)
        self.command_char = {}
        self.command_fmt = {}
        self.parse_settings()
    def write(self, msg):
        if self.debug:
            print("sending command", msg)
        self.s.write(msg.encode('ascii', 'ignore'))
        sleep(0.05) # sometimes getting errors...
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
    def help(self):
        self.parse_settings()
        for k in self.setting.keys():
            s = self.command_char[k]
            if self.command_fmt[k] != "":
                s += "  " + self.command_fmt[k]
            else:
                s += "    "   
            s += "  " + k
            if self.command_fmt[k] != "":
                s += "  (" + (self.command_fmt[k] % self.setting[k]) +")"
            print(s)
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
                    self.setting.update_key(key, float(val_string))
                    self.command_fmt[key] = "%f"
                else: # int
                    self.setting.update_key(key, int(val_string))
                    self.command_fmt[key] = "%d"
            except ValueError:
                # for commands of type (C), this will be empty
                self.setting.update_key(key, val_string)
                self.command_fmt[key] = ""
# -

# # Basic test
# import glob
# devs = glob.glob("/dev/tty.usb*")
# devs
#
# port = "/dev/tty.usbmodem123451"
# wft = WFT(port)

# wft.help()

# wft.parse_settings()

# wft.help()

# # Update github folder
#
# # ! cp wft.py /Users/gsteele/Documents/GitHub/wft-generic/
