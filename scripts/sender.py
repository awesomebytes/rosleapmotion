#!/usr/bin/env python
__author__ = 'flier'
import rospy
import leap_interface
from leap_motion.msg import leap
from leap_motion.msg import leapros
from leap_motion.msg import Finger

# Obviously, this method publishes the data defined in leapros.msg to /leapmotion/data
def sender():
    li = leap_interface.Runner()
    li.setDaemon(True)
    li.start()
    # pub     = rospy.Publisher('leapmotion/raw',leap)
    pub_ros   = rospy.Publisher('leapmotion/data',leapros)
    rospy.init_node('leap_pub')

    while not rospy.is_shutdown():
        hand_direction_ = li.hand_direction
        hand_normal_    = li.hand_normal
        hand_palm_pos_  = li.hand_palm_pos
        hand_pitch_     = li.hand_pitch
        hand_roll_      = li.hand_roll
        hand_yaw_       = li.hand_yaw

        msg = leapros()
        msg.direction.x = hand_direction_[0]
        msg.direction.y = hand_direction_[1]
        msg.direction.z = hand_direction_[2]
        msg.normal.x = hand_normal_[0]
        msg.normal.y = hand_normal_[1]
        msg.normal.z = hand_normal_[2]
        msg.palmpos.x = hand_palm_pos_[0]
        msg.palmpos.y = hand_palm_pos_[1]
        msg.palmpos.z = hand_palm_pos_[2]
        msg.ypr.x = hand_yaw_
        msg.ypr.y = hand_pitch_
        msg.ypr.z = hand_roll_
        
        # add finger data for each finger
        
        msg.fingers = []
        finger_data = li.finger_data
        for finger in finger_data:
            finger_msg = Finger()
            
            finger_msg.position.x = finger['pos'][0]
            finger_msg.position.y = finger['pos'][1]
            finger_msg.position.z = finger['pos'][2]
            
            finger_msg.velocity.x = finger['vel'][0]
            finger_msg.velocity.x = finger['vel'][1]
            finger_msg.velocity.x = finger['vel'][2]
            
            finger_msg.direction.x = finger['dir'][0]
            finger_msg.direction.y = finger['dir'][1]
            finger_msg.direction.z = finger['dir'][2]
            
            msg.fingers.append(finger_msg)

        # We don't publish native data types, see ROS best practices
        # pub.publish(hand_direction=hand_direction_,hand_normal = hand_normal_, hand_palm_pos = hand_palm_pos_, hand_pitch = hand_pitch_, hand_roll = hand_roll_, hand_yaw = hand_yaw_)
        pub_ros.publish(msg)
        # Save some CPU time, circa 100Hz publishing.
        rospy.sleep(0.01)


if __name__ == '__main__':
    try:
        sender()
    except rospy.ROSInterruptException:
        pass
