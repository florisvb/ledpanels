#!/usr/bin/env python
from __future__ import division
import roslib
import rospy
import serial
import numpy as N
import numpy as np
import subprocess, signal, os

from ledpanels.msg import MsgPanelsCommand
from ledpanels.srv import *

from std_msgs.msg import *    

import imp, time

def get_localtime():
    lt = time.localtime()
    return lt.tm_hour + lt.tm_min/60. + lt.tm_sec/3600.

def publish_led_command(publisher, led_command):
    publisher.publish(command=led_command[0], 
                      arg1=led_command[1], 
                      arg2=led_command[6], 
                      arg3=led_command[6], 
                      arg4=led_command[6],
                      arg5=led_command[6],
                      arg6=led_command[6],
                      )
    print led_command
    print
                                      
if __name__ == '__main__':

    rospy.init_node('ledpanel_control', anonymous=True)
    publish_to_led_panels = rospy.Publisher('/ledpanels/command', MsgPanelsCommand, latch=True)
    
    # load configuration file
    configuration_filename = os.path.expanduser(rospy.get_param('/ledpanels/configuration_filename'))
    print 'Loading: ', configuration_filename
    ledpanel_configuration = imp.load_source('ledpanel_configuration', configuration_filename)
    config = ledpanel_configuration.LEDPanel_Configuration()
    rospy.sleep(2)

    # run init
    for led_command in config.init_commands:
        publish_led_command(publish_to_led_panels, led_command)


    rospy.sleep(2) 

    # wait until it is local time (within 2 seconds)
    if config.localtime_start != 'now':
        lt = get_localtime()
        while np.abs(lt - config.localtime_start) > .0005:
            #time.sleep(1)
            lt = get_localtime()
            #print lt
    else:
        lt = get_localtime()
        
    # for each interval in config
    for i, interval in enumerate(config.intervals_hrs):
        time.sleep(interval*3600)
        lt = get_localtime()
        led_command = config.commands[i]
        print "Local time: ", lt
        publish_led_command(publish_to_led_panels, led_command)
        
        
        
