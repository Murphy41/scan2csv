#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
import csv
import os
import math

class Scan2CSV:
    def __init__(self):
        self.csv_file = None
        self.csv_writer = None

        rospy.init_node('scan2csv', anonymous=True)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.create_csv_file()

    def create_csv_file(self):
        output_dir = rospy.get_param('~output_dir', os.getcwd())
        filename = os.path.join(output_dir, 'scan.csv')

        self.csv_file = open(filename, 'w')
        self.csv_writer = csv.writer(self.csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.csv_writer.writerow(['Timestamp', 'Angle', 'Range', 'X', 'Y'])

        rospy.loginfo(f"Saving LiDAR scan data to {filename}")

    def scan_callback(self, scan_data):
        timestamp = rospy.get_time()
        angle_increment = scan_data.angle_increment

        for i, range_val in enumerate(scan_data.ranges):
            if not math.isinf(range_val):
                angle = scan_data.angle_min + (i * angle_increment)
                x = range_val * math.cos(angle)
                y = range_val * math.sin(angle)
                self.csv_writer.writerow([timestamp, angle, range_val, x, y])

    def run(self):
        rospy.spin()
        self.csv_file.close()

if __name__ == '__main__':
    try:
        scan2csv = Scan2CSV()
        scan2csv.run()
    except rospy.ROSInterruptException:
        pass
