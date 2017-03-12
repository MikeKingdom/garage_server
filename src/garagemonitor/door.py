import logging
log_format = '%(levelname)s | %(asctime)-15s | %(message)s'
logging.basicConfig(format=log_format, level=logging.DEBUG)
import RPi.GPIO as GPIO
#import GPIOStub as GPIO
import time

class Door(object):

        def __init__(self, topLimitPin, bottomLimitPin, closePin):
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(topLimitPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(bottomLimitPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(closePin, GPIO.OUT)
                GPIO.output(closePin, True)
                print 'Door init topLimitPin={} bottomLimitPin={}, closePin={}'.format(topLimitPin, bottomLimitPin, closePin)
                self.topLimitPin = topLimitPin
                self.bottomLimitPin = bottomLimitPin
                self.closePin = closePin
                return

        def getState(self):
                top = GPIO.input(self.topLimitPin)
                bottom = GPIO.input(self.bottomLimitPin)
                if top == 0:
                        state = 'open'
                elif bottom == 0:
                        state = 'closed'
                else:
                        state = 'middle'
                print 'Door getState top={}, bottom={} state={}'.format(top, bottom, state)
                return state

        def __triggerDoor(self):
                GPIO.output(self.closePin, False)
                time.sleep(1)
                GPIO.output(self.closePin, True)

        def close(self):
                print 'Door close'
                self.__triggerDoor();

        def open(self):
                print 'Door open'
                self.__triggerDoor();
