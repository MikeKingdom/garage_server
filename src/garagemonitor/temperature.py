import logging
log_format = '%(levelname)s | %(asctime)-15s | %(message)s'
logging.basicConfig(format=log_format, level=logging.DEBUG)
import os
import glob
import time

class Temperature(object):

        def __init__(self):
                print 'Temperature initializing one wire'
                os.system('modprobe w1-gpio')
                os.system('modprobe w1-therm')

                base_dir = '/sys/bus/w1/devices/'
                device_folders = glob.glob(base_dir + '28*')
                if len(device_folders) > 0:
                    self.device_file = device_folders[0] + '/w1_slave'
                    print 'Temperature device is ' + self.device_file
                else :
                    self.device_file = None
                return

        def __readTemp(self):
                if self.device_file is None:
                    lines = None
                else :
                    print 'Temperature opening ' + self.device_file
                    f = open(self.device_file, 'r')
                    lines = f.readlines()
                    f.close()
                return lines

        def readTemp(self):
                return self.__readTemp()

        def getTemperature(self):
                print 'Temperature getting temperature'
                lines = self.__readTemp()
                if lines is None  :
                    temp_c = 0.0
                    temp_f = 0.0
                else :
                    print 'Temperature line 0 - ' + lines[0]
                    print 'Temperature line 1 - ' + lines[1]
                    while lines[0].strip()[-3:] != 'YES':
                        time.sleep(0.2)
                        lines = self.__readTemp()
                    equals_pos = lines[1].find('t=')
                    if equals_pos != -1:
                        temp_string = lines[1][equals_pos + 2:]
                        temp_c = float(temp_string) / 1000.0
                        temp_f = temp_c * 9.0 / 5.0 + 32.0
                print 'Temperature getTemperature temp_c={} temp_f={}'.format(temp_c, temp_f)
                return temp_c, temp_f
