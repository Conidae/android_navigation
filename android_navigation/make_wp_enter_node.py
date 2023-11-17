import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
import pandas as pd
import os


class MakeWpEnter(Node):
    def __init__(self,filename):
        super().__init__('make_wp_enter_node')
        self.sub=self.create_subscription(NavSatFix,'gps/fix',self.callback,1)
        self.csv_filename= filename
        self.csv_data=pd.DataFrame(columns=['Latitude','Longitude'])
        self.c=1
        print('initialized!')

    def callback(self,gps_msg):
        self.latitude=gps_msg.latitude
        self.longitude=gps_msg.longitude
        if self.c!=1:
            self.save_to_csv(self.latitude,self.longitude)

        input(f'{self.c}times press Enter to save to CSV')==''
        print(f'{self.c}s waipoint is {self.latitude},{self.longitude}')
        self.c+=1
        print('------------------------------')

    def save_to_csv(self,latitude,longitude):
        new_row=pd.DataFrame({'Latitude':[latitude],'Longitude':[longitude]})
        self.csv_data=pd.concat([self.csv_data,new_row],ignore_index=True)
        self.csv_data.to_csv(self.csv_filename,index=False,header=False)
        print('saved!!')
        print('------------------------------')

def main():
    rclpy.init()

    csv_filename='~/Downloads/marker_position_enter.csv'
    node = MakeWpEnter(csv_filename)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('key interrupted')
    
    node.destroy_node
    rclpy.shutdown
    print('program end')