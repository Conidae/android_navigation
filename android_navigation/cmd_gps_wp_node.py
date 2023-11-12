import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import pandas as pd
from geographic_msgs.msg import GeoPoint
from geometry_msgs.msg import Point
from robot_localization.srv import FromLL
import math
from tf_transformations import quaternion_from_euler

#waypoint
import time
from copy import deepcopy
from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

class Cmd_gps_wp_node(Node):
	def __init__(self):
		super().__init__('cmd_gps_wp_node')
		print('iniciarised')
		self.client=self.create_client(FromLL,'fromLL')#create client
		while not self.client.wait_for_service(timeout_sec=1.0):
			print('wait created service')
		print('create.client')
		self.request= FromLL.Request()
		
	def send_request(self,point):
		self.request.ll_point.latitude =point[0]
		self.request.ll_point.longitude =point[1]
		self.request.ll_point.altitude =0.0
		self.future=self.client.call_async(self.request)
		rclpy.spin_until_future_complete(self,self.future)
		return self.future.result()		
		
	def receive_csv(self,csv_file):#CSVから緯度経度listを取得
		data = pd.read_csv(csv_file, header=None)
		waypoint_list = [(row[0], row[1]) for index, row in data.iterrows()]
		return waypoint_list

	def make_waypoint(self):
		before_points=self.receive_csv('~/Downloads/marker_positions.csv')
		print('start make_waypoint')
		output_list=[]
		waypoints=[]
		for bedore_point in before_points:
			response=self.send_request(point=bedore_point)
			output_list.append([response.map_point.x,response.map_point.y,response.map_point.z])

		for i in range(len(output_list)):
			if i<len(output_list)-1:
				pose=math.atan2(output_list[i+1][1]-output_list[i][1],output_list[i+1][0]-output_list[i][0])
			else:
				pose=0
			x,y,z,w=quaternion_from_euler(0,0,pose,'ryxz')
			waypoints.append([output_list[i][0],output_list[i][1],0,x,y,z,w])
		print(waypoints)
		return waypoints
	
	def waypoint_nav(self,waypoints):
			navigator = BasicNavigator()
			inspection_points=[]
			while rclpy.ok():
				inspection_pose = PoseStamped()
				inspection_pose.header.frame_id = 'map'
				inspection_pose.header.stamp = navigator.get_clock().now().to_msg()
				for pt in waypoints:
					inspection_pose.pose.position.x = pt[0]
					inspection_pose.pose.position.y = pt[1]
					inspection_pose.pose.orientation.z = pt[5]
					inspection_pose.pose.orientation.w = pt[6]
					inspection_points.append(deepcopy(inspection_pose))
				nav_start = navigator.get_clock().now()
				navigator.followWaypoints(inspection_points)
					# Do something during our route (e.x. AI to analyze stock information or upload to the cloud)
					# # Simply print the current waypoint ID for the demonstation
				i = 0
				while not navigator.isTaskComplete():
					i = i + 1
					feedback = navigator.getFeedback()
					if feedback and i % 5 == 0:
						print('Executing current waypoint: ' +
							str(feedback.current_waypoint + 1) + '/' + str(len(inspection_points)))
				result = navigator.getResult()
				if result == TaskResult.SUCCEEDED:
					print('Inspection of shelves complete! Returning to start...')
				elif result == TaskResult.CANCELED:
					print('Inspection of shelving was canceled. Returning to start...')
					exit(1)
				elif result == TaskResult.FAILED:
					print('Inspection of shelving failed! Returning to start...')
				# go back to start
				# initial_pose.header.stamp = navigator.get_clock().now().to_msg()
				# navigator.goToPose(initial_pose)
				while not navigator.isTaskComplete:
					pass


def main(args=None):
	rclpy.init(args=args)
	node = Cmd_gps_wp_node()
	waypoints=node.make_waypoint()
	node.waypoint_nav(waypoints=waypoints)

	node.destroy_node()
	# Destroy the node explicitly
	# (optional - otherwise it will be done automatically
	# when the garbage collector destroys the node object)
	rclpy.shutdown()
