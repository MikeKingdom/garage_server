from flask import Flask, render_template
from garagemonitor import app
from garagemonitor.garage import state, setState

print 'views'

@app.route('/')
def index():
        return render_template('index.html', state=state)
