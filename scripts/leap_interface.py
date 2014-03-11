#################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.                #
# Leap Motion proprietary and confidential. Not for distribution.               #
# Use subject to the terms of the Leap Motion SDK Agreement available at        #
# https://developer.leapmotion.com/sdk_agreement, or another agreement          #
# between Leap Motion and you, your company or other organization.              #
#################################################################################

#################################################################################
# Altered LEAP example by Florian Lier, you need to have the LEAP SDK installed #
# for this to work properly ;)                                                  #
# This interface provides access to the LEAP MOTION hardware, you will need to  #
# have the official LEAP MOTION SDK installed in order to load the shared       #
# provided with the SDK.                                                        #
#################################################################################

import sys
import time
# Set (append) your PYTHONPATH properly, or just fill in the location of your LEAP
# SDK folder, e.g., ../LeapSDK/lib where the Leap.py lives and /LeapSDK/lib/x64 or
# x86 where the *.so files reside.
<<<<<<< HEAD
#sys.path.append("/home/flier/Projects/Ongoing/Leap_Developer/LeapSDK/lib")
#sys.path.append("/home/flier/Projects/Ongoing/Leap_Developer/LeapSDK/lib/x64")
=======
sys.path.append("/home/sam/LeapDeveloperKit/LeapSDK/lib")
sys.path.append("/home/sam/LeapDeveloperKit/LeapSDK/lib/x64")
>>>>>>> master
import threading
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class LeapInterface(Leap.Listener):
    def on_init(self, controller):
        # These variables as probably not thread safe
        # TODO: Make thread safe ;)
        self.hand           = [0,0,0]
        self.hand_direction = [0,0,0]
        self.hand_normal    = [0,0,0]
        self.hand_palm_pos  = [0,0,0]
        self.hand_pitch     = 0.0
        self.hand_yaw       = 0.0
        self.hand_roll      = 0.0
        self.finger_data = []
        print "Initialized Leap Motion Device"

    def on_connect(self, controller):
        print "Connected to Leap Motion Controller"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected Leap Motion"

    def on_exit(self, controller):
        print "Exited Leap Motion Controller"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        '''
        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        '''
        
        if not frame.hands.is_empty:
            # Get the first hand
            self.hand = frame.hands[0]

            # Check if the hand has any fingers
            fingers = self.hand.fingers
            self.finger_data = []
            if not fingers.is_empty:
                for finger in (f for f in fingers if f.is_finger) :
                    pos = finger.tip_position
                    vel = finger.tip_velocity
                    direction = finger.direction
                    self.finger_data.append({'pos':pos, 'vel':vel, 'dir':direction})

            # Get the hand's sphere radius and palm position
            # print "Hand sphere radius: %f mm, palm position: %s" % (self.hand.sphere_radius, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = self.hand.palm_normal
            direction = self.hand.direction
            pos = self.hand.palm_position

            self.hand_direction[0] = direction.x
            self.hand_direction[1] = direction.y
            self.hand_direction[2] = direction.z
            self.hand_normal[0]    = normal.x
            self.hand_normal[1]    = normal.y
            self.hand_normal[2]    = normal.z
            self.hand_palm_pos[0]  = pos.x
            self.hand_palm_pos[1]  = pos.y
            self.hand_palm_pos[2]  = pos.z
            self.hand_pitch        = direction.pitch * Leap.RAD_TO_DEG
            self.hand_yaw          = normal.yaw * Leap.RAD_TO_DEG
            self.hand_roll         = direction.roll * Leap.RAD_TO_DEG

            # Calculate the hand's pitch, roll, and yaw angles
            print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees, %d fingers" % (self.hand_pitch, self.hand_roll, self.hand_yaw, len(self.finger_data))

            '''
            # Gestures
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)

                    # Determine clock direction using the angle between the pointable and the circle normal
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
                        clockwiseness = "clockwise"
                    else:
                        clockwiseness = "counterclockwise"

                    # Calculate the angle swept since the last frame
                    swept_angle = 0
                    if circle.state != Leap.Gesture.STATE_START:
                        previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                        swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                    print "Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                            gesture.id, self.state_string(gesture.state),
                            circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    print "Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                            gesture.id, self.state_string(gesture.state),
                            swipe.position, swipe.direction, swipe.speed)

                if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                    keytap = KeyTapGesture(gesture)
                    print "Key Tap id: %d, %s, position: %s, direction: %s" % (
                            gesture.id, self.state_string(gesture.state),
                            keytap.position, keytap.direction )

                if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                    screentap = ScreenTapGesture(gesture)
                    print "Screen Tap id: %d, %s, position: %s, direction: %s" % (
                            gesture.id, self.state_string(gesture.state),
                            screentap.position, screentap.direction )

        if not (frame.hands.empty and frame.gestures().empty):
            print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
    '''

class Runner(threading.Thread):

    def __init__(self,arg=None):
        threading.Thread.__init__(self)
        self.arg=arg
        self.listener = LeapInterface()
        self.controller = Leap.Controller()
        self.controller.add_listener(self.listener)
    
    def __del__(self):
        self.controller.remove_listener(self.listener)

    @property
    def hand_direction(self):
        return self.listener.hand_direction

    @property
    def hand_normal(self):
        return self.listener.hand_normal

    @property
    def hand_palm_pos(self):
        return self.listener.hand_palm_pos

    @property
    def hand_roll(self):
        return self.listener.hand_roll

    @property
    def hand_pitch(self):
        return self.listener.hand_pitch

    @property
    def hand_yaw(self):
        return self.listener.hand_yaw

    @property
    def finger_data(self):
        return self.listener.finger_data

    def run (self):
        while True:
            # Save some CPU time
            time.sleep(0.001)

