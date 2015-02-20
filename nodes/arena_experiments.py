#!/usr/bin/env python
from __future__ import division
import roslib
import rospy
import serial
import numpy as N
import subprocess, signal, os

from ledpanels.msg import MsgPanelsCommand
from ledpanels.srv import *

from std_msgs.msg import *    
    
class LEDArena:
    def __init__(self):
        self.publish_to_led_panels = rospy.Publisher('/ledpanels/command', MsgPanelsCommand, latch=True)
        self.publish_pattern_name = rospy.Publisher('/ledpanels/pattern', String, queue_size=3)
        rospy.sleep(2)
        self.publish_to_led_panels.publish(command='ctr_reset')
        rospy.sleep(5)
        
    def run_closed_loop_pattern(self, pattern_id, xgain=-10, ypos=0, pattern_name='pattern_name'):
        self.publish_to_led_panels.publish(command='stop')
        rospy.sleep(1)
        self.publish_to_led_panels.publish(command='set_pattern_id', arg1=pattern_id)
        rospy.sleep(1)
        self.publish_to_led_panels.publish(command='set_position', arg1=48, arg2=ypos)
        rospy.sleep(1)
        self.publish_to_led_panels.publish(command='send_gain_bias', arg1=xgain, arg2=0, arg3=0, arg4=0)
        rospy.sleep(1)
        self.publish_to_led_panels.publish(command='set_mode', arg1=1, arg2=0)
        rospy.sleep(1)
        self.publish_to_led_panels.publish(command='start')
        self.publish_pattern_name.publish(pattern_name)
        
    def start_rosbag_recording(self, topics, directory='~/'):
        directory = os.path.expanduser(directory)
        topics_with_spaces = [topic + ' ' for topic in topics]
        command = 'rosbag record ' + ''.join(topics_with_spaces)
        print 'rosbag record command: ', command
        self.rosbag_process_id = subprocess.Popen(command, stdin=subprocess.PIPE, shell=True, cwd=directory)
        print 'recording bagfile for: ', topics
        print 'to directory: ', directory
        print 
        
    def stop_rosbag_recording(self):
        # kill process and children
        p = self.rosbag_process_id
        ps_command = subprocess.Popen("ps -o pid --ppid %d --noheaders" % p.pid, shell=True, stdout=subprocess.PIPE)
        ps_output = ps_command.stdout.read()
        retcode = ps_command.wait()
        assert retcode == 0, "ps command returned %d" % retcode
        for pid_str in ps_output.split("\n")[:-1]:
                os.kill(int(pid_str), signal.SIGINT)
        p.terminate()
        print 'rosbag recording STOPPED'
        

if __name__ == '__main__':
    
    # example: run closed loop stripe fixation
    stripe_pattern_id = rospy.get_param('/ledpanels/stripe_pattern_id', 16)
    
    rospy.init_node('experiment_controller')
    LEDArena = arena_experiments.LEDArena()
    LEDArena.run_closed_loop_pattern(stripe_pattern_id, ypos=0, pattern_name='stripe')
    
