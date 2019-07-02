# -*- coding: utf-8 -*-

"""A demonstration of Comet streaming functionality using Sijax."""

import os, sys
from cloud import Server
from multiprocessing import Process, Pipe

path = os.path.join('.', os.path.dirname(__file__), '../')
sys.path.append(path)

from flask import Flask, g, render_template
import flask_sijax

usage = ''

app = Flask(__name__)

# The path where you want the extension to create the needed javascript files
# DON'T put any of your files in this directory, because they'll be deleted!
app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

# You need to point Sijax to the json2.js library if you want to support
# browsers that don't support JSON natively (like IE <= 7)
app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'

flask_sijax.Sijax(app)

def get_usage():
    global usage

    if usage_conn.poll():
        usage = usage_conn.recv()

    return usage

def comet_do_work_handler(obj_response, sleep_time):
    import time

    global usage

    colors = {'': '#DCDCDC',
              0.0: '#006400',
              50.0: '#FFFF00',
              100.0: '#8B0000'}

    color_pos = 0
    while True:
        get_usage()

        obj_response.css('#progress', 'background-color', colors[usage])

        # Yielding tells Sijax to flush the data to the browser.
        # This only works for Streaming functions (Comet or Upload)
        # and would not work for normal Sijax functions
        yield obj_response

        time.sleep(sleep_time)

        if color_pos == 0:
            color_pos = 1
        else:
            color_pos = 0

@app.before_first_request
def create_server():
    parent_conn, child_conn = Pipe()
    server = Server(child_conn)
    print('Server is up')
    global p
    p = Process(target=server.run)
    p.start()

    print("Done")

    # set the global usage conn
    global usage_conn
    usage_conn = parent_conn

@app.route('/shutdown', methods=['POST'])
def shutdown():
    print("Joinning")
    p.join()

@flask_sijax.route(app, "/")
def index():
    if g.sijax.is_sijax_request:
        # The request looks like a valid Sijax request
        # Let's register the handlers and tell Sijax to process it
        g.sijax.register_comet_callback('do_work', comet_do_work_handler)
        return g.sijax.process_request()

    return render_template('comet.html')

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True, port=8080)
