#!/usr/bin/env python

#Connects to an RTKRCV server stream which outputs an XYZ-ECEF RTK solution. 
#This solution message is parsed into its component and transmitted over 
#individual ROS topics

import rospy
import numpy as np
from std_msgs.msg import String
import socket
from sensor_msgs.msg import Imu, NavSatFix, NavSatStatus
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, Point, Pose, PoseStamped

def getMsg():
	
	pub_navsat = rospy.Publisher('/rtklib/rover', NavSatFix)
	pub_pose = rospy.Publisher('/rtklib/pose', PoseStamped)
	
	#Initialize the RTKLIB ROS node	
	rospy.init_node('rtklib_messages', anonymous=True)
	
	#Define the publishing frequency of the node
	rate = rospy.Rate(10)
	
	#Create a socket
	sock = socket.socket()
	
	#Get the address of the local host
	host = socket.gethostname()
	
	#Connect to the RTKRCV server that is bound to port xxxx
	port = 5801
	sock.connect((host,port))
	
	e2 = 6.69437999014e-3
	a = 6378137.0
	
	while not rospy.is_shutdown():
		
		navsat = NavSatFix()
		ecef_xyz = Point()
		ecef_pose = Pose()
		ecef_stampedPose = PoseStamped()
		
		ecef_stampedPose = 
		navsat.header.stamp = rospy.Time.now()
		
		#Get the position message from the RTKRCV server
		msgStr = sock.recv(1024)
		
		#Split the message
		msg = msgStr.split()
		
		navsat.latitude = float(msg[2])
		navsat.longitude = float(msg[3])
		navsat.altitude = float(msg[4])
		
		N = 1.0*a/np.sqrt(1-e2*(np.sin(float(msg[2])*np.pi/180.0)**2))
		
		ecef_xyz.x = (N+float(msg[4]))*np.cos(float(msg[2])*np.pi/180.0)*np.cos(float(msg[3])*np.pi/180.0)
		ecef_xyz.y = (N+float(msg[4]))*np.cos(float(msg[2])*np.pi/180.0)*np.sin(float(msg[3])*np.pi/180.0)
		ecef_xyz.z = (N*(1-e2)+float(msg[4]))*np.sin(float(msg[2])*np.pi/180.0)
		
		ecef_pose.position = ecef_xyz
		ecef_stampedPose.pose = ecef_pose
		
		pub_navsat.publish(navsat)
		pub_pose.publish(ecef_stampedPose)
		
		rate.sleep()
		
	#Create a list of ROSTopic names
	#topicList = ['dow', 'gpst', 'latitude', 'longitude', 'height', 'check', 'sats', 
	#'dxx', 'dyy', 'dzz', 'dxy', 'dyz', 'dxz', 'delay', 'ftest']

if __name__ == '__main__':
	try:
		#Run the publisher
		getMsg()
	except rospy.ROSInterruptException:
		pass
