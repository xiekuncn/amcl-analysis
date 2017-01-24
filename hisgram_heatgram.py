#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
import math
from matplotlib import pyplot as plt
from amcl.msg import PoseWithWeightArray
from flask import Flask, url_for
import os 

app = Flask(__name__)
image_format = "png"

def callback(msg):
    print "new data",msg.iterate_time
    figure_name = "%d-1" % msg.iterate_time
    plt.figure(figure_name)
    weights = np.array(msg.weights)
    bins = np.linspace(0, 
                       0.1,
                       20)
    plt.xlim([-0.01, 0.11])
    plt.hist(weights, bins=bins, alpha=0.5)
    plt.title("iterate time {}\nmin = {} max = {}\nparticle count = {}".
              format(msg.iterate_time, 
                     min(weights), 
                     max(weights),
                     len(weights)))
    plt.xlabel("weight")
    plt.ylabel("count")
    plt.savefig('static/' + figure_name + "." + image_format)
    
    figure_name = "%d-2" % msg.iterate_time
    plt.figure(figure_name)
    plt.xlim([-10, 10])
    plt.ylim([-10, 10])
    plt.xlabel("x")
    plt.ylabel("y")
    poses = np.array([[pose.position.x, pose.position.y] for pose in  msg.poses])
    plt.scatter(poses[:,0], poses[:,1], c=weights)
    plt.savefig('static/' + figure_name + "." + image_format)
    
def compare(x, y):
    x1 = x.split("-")
    y1 = y.split("-")

    if x1[0] == y1[0]:
        x1 = x1[1].split('.')[0]
        y1 = y1[1].split('.')[0]
    else:
        x1 = x1[0]
        y1 = y1[0]
    return int(x1) - int(y1)

@app.route("/")
def main_page():
    images = os.listdir("./static/")
    images = [image for image in images if image.endswith(image_format)]
    images = sorted(images, cmp=compare)    
    ret = ""
    for image in images:
        ret = '''{}\n <img src="{}" />'''.format(ret, url_for('static', filename=image))
    return ret

if __name__ ==  "__main__":
    rospy.init_node("jupyter_node")
    rospy.Subscriber("pose_with_weight_array", PoseWithWeightArray, callback)
    app.run()
