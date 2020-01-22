#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   appCam.py
#  
#   PiCam Local Web Server with Flask
# 

from flask import Flask, render_template, Response
app = Flask(__name__)

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera
import time

@app.route("/")
def index():
    timeNow = time.asctime( time.localtime(time.time()) )
    
    templateData = {
      'time': timeNow
    }
    return render_template('index.html', **templateData)
    
@app.route('/camera')
def cam():
    """Video streaming home page."""
    timeNow = time.asctime( time.localtime(time.time()) )
    templateData = {
      'time': timeNow
    }
    return render_template('camera.html', **templateData)
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)