#!/usr/bin/python
from flask import Flask, render_template, request, send_file, jsonify
from door import Door
from temperature import Temperature
import os

app = Flask(__name__)
mainDoor = Door(topLimitPin=18, bottomLimitPin=23, closePin=24)
tempSensor = Temperature()


def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

@app.route('/', methods=['GET', 'POST'])
def index():
        if request.method == 'POST':
                newState = request.form['state']
                if newState == 'closed' and mainDoor.getState() == 'open':
                        mainDoor.close()
                        app.logger.info('Closing garage door from /')
                        return render_template('index.html', state='closing');
        deg_c, deg_f = tempSensor.getTemperature()

        return render_template('index.html', state=mainDoor.getState(), temperature='{:3.1f}'.format(deg_f))

@app.route('/rest/garage', methods=['GET', 'POST'])
def garage():
        if request.method == 'POST':
                content = request.json
                newState = content['state']
                if newState == 'closed':
                        mainDoor.close()
                        app.logger.info('Closing garage door from /rest/garage')
        deg_c, deg_f = tempSensor.getTemperature()

        if request_wants_json():
                return '{{"state":"{}", "temperature":{:3.1f} }}'.format(mainDoor.getState(), deg_f)
        return 'Garage door is {}\nTemperature is {:3.1f}F'.format(mainDoor.getState(), deg_f)

@app.route('/rest/garage/open', methods=['GET', 'POST'])
def open_garage():
        mainDoor.open()
        app.logger.info('Opening garage door from /rest/garage/open')

        if request_wants_json():
                return '{"state":"' + mainDoor.getState() + '"}'
        return 'Changing state to ' + mainDoor.getState()

@app.route('/get_image')
def get_image():
    os.system('raspistill -vf -hf -w 640 -h 480 -a 1036 -ae +25+25 -o /tmp/cam.jpg')
    return send_file('/tmp/cam.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')
