#!/usr/bin/env python
from Adafruit_BNO055.BNO055 import BNO055
import logging

from time import time
from sensor_msgs.msg import Imu


if __name__ == '__main__':
    # ROS Setup
    rospy.init_node('bno055_imu_node')

    rospy.Publisher('imu', Imu, queue_size = 10)

    # BNO Setup

    bno = BNO055(serial_port='/dev/serial0', rst=18)
    logging.basicConfig(level=logging.DEBUG)

    if not bno.begin():
        raise RuntimeError('The BNO055 is not connected')

    with bno.get_system_status() as status, self_test, error:
        if status == 0x01:
            print('System error: {0}'.format(error))
            print('Datasheet 4.3.59 will clarify the error code.')

    # Read from the device
    seq = 0
    data = Imu()

    rate = rospy.Rate(100)

    while not rospy.is_shutdown():
        # Include if condition if there is a new reading from the device
        # Note that it is not guarenteed that all of these measurements
        # will be from the same buffer.ros
        if True:
            orient_x, orient_y, orient_z, orient_w = bno.read_quaterion()
            acc_x, acc_y, acc_z = bno.read_linear_acceleration()
            ang_vel_x, ang_vel_y, ang_vel_z = bno.read

            data.header.stamp = rospy.Time.now()
            data.header.frame_id = 'imu_link'
            data.header.seq = seq

            data.orientation.w = orient_w
            data.orientation.x = orient_x
            data.orientation.y = orient_y
            data.orientation.z = orient_z

            data.linear_acceleration.x = acc_x
            data.linear_acceleration.y = acc_y
            data.linear_acceleration.z = acc_z


            data.linear_acceleration_covariance[0] = -1
            data.angular_velocity.x = math.radians(ang_vel_x)
            data.angular_velocity.y = math.radians(ang_vel_y)
            data.angular_velocity.z = math.radians(ang_vel_z)
            data.angular_velocity_covariance[0] = -1
            pub_data.publish(data)

            # Work for next loop
            seq += 1
        rate.sleep()