# Copyright 2021 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import Twist

import rclpy
from rclpy.node import Node

from turtlesim.msg import Pose
from turtlesim.srv import Spawn

import threading
import time

PI = 3.1415926535897
# Setting a default speed of 3 units/sec
speed = 3
angle = 90
clockwise = True


class PointPublisher(Node):

    def __init__(self):
        super().__init__('turtle_tf2_message_broadcaster')

        # Create a client to spawn a turtle
        self.spawner = self.create_client(Spawn, 'spawn')
        # Boolean values to store the information
        # if the service for spawning turtle is available
        self.turtle_spawning_service_ready = False
        # if the turtle was successfully spawned
        self.turtle_spawned = False
        # if the topics of turtle3 can be subscribed
        self.turtle_pose_cansubscribe = True
        # self.turtle_pose_cansubscribe_v2 = 0

        self.timer = self.create_timer(1.0, self.on_timer)
        self.count = 0



    def on_timer(self):
        if self.turtle_spawning_service_ready:
            if self.turtle_spawned:
                self.turtle_pose_cansubscribe = True
            else:
                if self.result.done():

                    self.get_logger().info(
                        f'Successfully spawned 666 {self.result.result().name}')
                    self.turtle_spawned = True

                else:
                    self.get_logger().info('Spawn is not finished')
        else:
            if self.spawner.service_is_ready():
                # Initialize request with turtle name and coordinates
                # Note that x, y and theta are defined as floats in turtlesim/srv/Spawn
                request = Spawn.Request()
                request.name = 'turtle3'
                request.x = float(3)
                request.y = float(3)
                request.theta = float(0)

                request_2 = Spawn.Request()
                request_2.name = 'turtle2'
                request_2.x = float(7)
                request_2.y = float(7)
                request_2.theta = float(0)

                # Call request
                self.result = self.spawner.call_async(request)
                self.result = self.spawner.call_async(request_2)

                self.turtle_spawning_service_ready = True
            else:
                # Check if the service is ready
                self.get_logger().info('Service is not ready')


        # 一隻烏龜跑一個動作
        if self.turtle_pose_cansubscribe:
            self.vel_pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
            self.sub = self.create_subscription(
                Pose, 'turtle1/pose', self.handle_turtle_pose_square, 10)
            self.pub = self.create_publisher(
                PointStamped, 'turtle1/turtle_point_stamped', 10)
            thread = threading.Thread(self.test_second)
            thread.start()

        '''
        # 三隻烏龜
        # self.turtle_pose_cansubscribe = 0
        # self.turtle_pose_cansubscribe_v2 = 0

        # if self.turtle_pose_cansubscribe == 0:

        #     self.vel_pub = self.create_publisher(Twist, 'turtle3/cmd_vel', 10)
        #     self.sub = self.create_subscription(Pose, 'turtle3/pose', self.handle_turtle_pose, 10)
        #     self.pub = self.create_publisher(PointStamped, 'turtle3/turtle_point_stamped', 10)
        #     print("circle")
        #     #time :2s
        #     self.turtle_pose_cansubscribe = self.turtle_pose_cansubscribe + 1

        # elif self.turtle_pose_cansubscribe == 1:
        #     self.vel_pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        #     self.sub = self.create_subscription(Pose, 'turtle1/pose', self.handle_turtle_pose_square, 10)
        #     self.pub = self.create_publisher(PointStamped, 'turtle1/turtle_point_stamped', 10)
        #     #time :2s
        #     self.turtle_pose_cansubscribe_v2 = 1

        # elif self.turtle_pose_cansubscribe_v2 == 1:

        #     self.vel_pub = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)
        #     self.sub = self.create_subscription(Pose, 'turtle2/pose', self.handle_turtle_pose, 10)
        #     self.pub = self.create_publisher(PointStamped, 'turtle2/turtle_point_stamped', 10)

        # self.vel_pub = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)
        # self.sub = self.create_subscription(Pose, 'turtle2/pose', self.handle_turtle_pose, 10)
        # self.pub = self.create_publisher(PointStamped, 'turtle2/turtle_point_stamped', 10)

        # #兩隻烏龜同時跑/選三個動作
        # for i in range(100):
        #     if i%2 == 1:
        #         self.vel_pub = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)
        #         self.sub = self.create_subscription(Pose, 'turtle2/pose', self.handle_turtle_pose, 10)
        #         self.pub = self.create_publisher(PointStamped, 'turtle2/turtle_point_stamped', 10)

        #     else:
        #         self.vel_pub = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)
        #         self.sub = self.create_subscription(Pose, 'turtle2/pose', self.handle_turtle_pose_square, 10)
        #         self.pub = self.create_publisher(PointStamped, 'turtle2/turtle_point_stamped', 10)

        # 沒跑到turtle3
        # thread = threading.Thread(self.test_second)
        # # self.get_logger().info(f'ccc 666 {self.result.result().name}')
        # thread.start()
        '''
    def test_second(self):
        self.vel_pub_2 = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)
        self.sub_2 = self.create_subscription(Pose, 'turtle2/pose', self.handle_turtle_pose_square, 10)
        self.pub_2 = self.create_publisher(PointStamped, 'turtle2/turtle_point_stamped', 10)
        '''
        # # #兩隻烏龜動作
        # if self.turtle_pose_cansubscribe:
        #     for i in range(100):
        #         self.vel_pub = self.create_publisher(Twist, 'turtle3/cmd_vel', 10)
        #         self.sub = self.create_subscription(Pose, 'turtle3/pose', self.handle_turtle_pose_triangle, 10)
        #         self.pub = self.create_publisher(PointStamped, 'turtle3/turtle_point_stamped', 10)

        #         self.turtle_pose_cansubscribe = False
        # else:
        #     self.vel_pub = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)
        #     self.sub = self.create_subscription(Pose, 'turtle2/pose', self.handle_turtle_pose_square, 10)
        #     self.pub = self.create_publisher(PointStamped, 'turtle2/turtle_point_stamped', 10)
        '''
    # 圓形
    # turtle1
    def handle_turtle_pose(self, msg):
        print("circle")
        vel_msg = Twist()
        vel_msg.linear.x = 1.0
        vel_msg.angular.z = 1.0
        self.vel_pub.publish(vel_msg)

        ps = PointStamped()
        ps.header.stamp = self.get_clock().now().to_msg()
        ps.header.frame_id = 'world'
        ps.point.x = msg.x
        ps.point.y = msg.y
        ps.point.z = 0.0
        self.pub.publish(ps)

    # 三角形
    # turtle2
    def handle_turtle_pose_square(self, msg):
        print("square")
        vel_msg = Twist()
        vel_msg.linear.x = 1.0                                                #设置线速度为1m.s，正为前进，负为后退
        vel_msg.linear.y = 0.0
        vel_msg.linear.z = 0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0
        vel_msg.angular.z = 0.0
    	
        self.count = self.count + 1
    	
        while(self.count == 5):
    	    self.count=0
    	    vel_msg.angular.z = 3.14159265358979323846 #转90°
    	
        self.vel_pub.publish(vel_msg)
	 
        ps = PointStamped()
        ps.header.stamp = self.get_clock().now().to_msg()
        ps.header.frame_id = 'world'
        ps.point.x = msg.x
        ps.point.y = msg.y
        ps.point.z = 0.0
        self.pub.publish(ps)

    # 旋轉
    # turtle3
    def rotation(self, msg):
        print("square")

        angular_speed = speed*2*PI/360
        relative_angle = angle*2*PI/360

        vel_msg = Twist()
        vel_msg.linear.x = 1.0  # 设置线速度为1m.s，正为前进，负为后退
        vel_msg.linear.y = 0.0
        vel_msg.linear.z = 0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0
        vel_msg.angular.z = 0.0

        # Checking if our movement is CW or CCW
        if clockwise:
            vel_msg.angular.z = -abs(angular_speed)
        else:
            vel_msg.angular.z = abs(angular_speed)
        # Setting the current time for distance calculus
        ps = PointStamped()
        t0 = self.get_clock().now().to_msg()
        
        current_angle = 0
        while(current_angle < relative_angle):
            
            t1 = self.get_clock().now().to_msg()
            current_angle = angular_speed*(t1-t0)

    	
        self.vel_pub.publish(vel_msg)
	 
        ps = PointStamped()
        ps.header.stamp = self.get_clock().now().to_msg()
        ps.header.frame_id = 'world'
        ps.point.x = msg.x
        ps.point.y = msg.y
        ps.point.z = 0.0
        self.pub.publish(ps)

    #直線
    def line(self, msg):
        print("square")

        angular_speed = speed*2*PI/360
        relative_angle = angle*2*PI/360

        vel_msg = Twist()
        vel_msg.linear.x = 1.0  # 设置线速度为1m.s，正为前进，负为后退
        vel_msg.linear.y = 0.0
        vel_msg.linear.z = 0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0
        vel_msg.angular.z = 0.0

        # Checking if our movement is CW or CCW
        if clockwise:
            vel_msg.angular.z = -abs(angular_speed)
        else:
            vel_msg.angular.z = abs(angular_speed)
        # Setting the current time for distance calculus
        ps = PointStamped()
        t0 = self.get_clock().now().to_msg()
        
        current_angle = 0
        while(current_angle < relative_angle):
            
            t1 = self.get_clock().now().to_msg()
            current_angle = angular_speed*(t1-t0)

    	
        self.vel_pub.publish(vel_msg)
	 
        ps = PointStamped()
        ps.header.stamp = self.get_clock().now().to_msg()
        ps.header.frame_id = 'world'
        ps.point.x = msg.x
        ps.point.y = msg.y
        ps.point.z = 0.0
        self.pub.publish(ps)
def main():
    rclpy.init()
    node = PointPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
    
 