from flask import Flask
from flask import jsonify, Response, render_template, abort, make_response
from flask import request

from cookbook_manager import CookbookManager

from barista import Barista

import json
import httplib
from threading import Thread

from utils import channel
from utils import json_config

# ===============================================================================
#
# Global Variables
#
# ===============================================================================

app = Flask(__name__)
cmgr = CookbookManager()
config = json_config.parse_json("config.json")

barista = Barista()

@app.route("/")
def index():
    pass

# ===============================================================================
#
# Cookbook Manager API
#
# ===============================================================================
@app.route("/cookbooks", methods=["GET"])
def list_cookbooks():
    """
    {
        "cookbooks": ["cookbook1", "cookbook2", "cookbook3"]
    }
    """
    cookbooks = cmgr.list()
    return jsonify({"cookbooks": cookbooks})

@app.route("/cookbooks/<string:name>", methods=["GET"])
def read_cookbook(name):
    """
    {
        "name": "cookbook1",
        "date": "",
        "description": ""
    }
    """
    return cmgr.read(name)

@app.route("/cookbooks/<string:name>", methods=["PUT"])
def update_cookbook(name):
    """
    {
        "name": "new_cookbook_name"
    }
    """
    if request.data:
        params = json.loads(request.data)
    else:
        params = {}

    if "name" in params:
        new_name = params["name"]
        cmgr.rename(name, new_name)
    else:
        # If no name params in the params, create a new cookbook
        cmgr.update(name)

    resp = make_response()
    resp.status_code = httplib.CREATED

    return resp

@app.route("/cookbooks/<string:name>/content", methods=["GET"])
def read_cookbook_content(name):
    content = cmgr.read(name)
    return content

@app.route("/cookbooks/<string:name>/content", methods=["PUT"])
def update_cookbook_content(name):
    new_content = request.data
    cmgr.update(name, new_content)

    resp = make_response()
    resp.status_code = httplib.OK

    return resp

@app.route("/cookbooks/<string:name>", methods=["DELETE"])
def delete_cookbook(name):
    cmgr.delete(name)

    resp = make_response()
    resp.status_code = httplib.NO_CONTENT

    return resp

# ===============================================================================
#
# Barista API
#
# ===============================================================================
@app.route("/barista", methods=["GET"])
def get_barista_status():
    """
    {
        "State": "Brewing",
        "Now steps": "Step title",
        "Now steps index": 3,
        "Now process": "Process title",
        "Now process index": 1,
        "Now cookbook name": "Test",
        "Temperature": 90,
        "Is water full": true,
        "Total commands": 1000,
        "Progress": 834
    }
    """

    status = {
        "State": barista.state,
        "Now steps": barista.now_step,
        "Now steps index": barista.now_step_index,
        "Now process": barista.now_process,
        "Now process index": barista.now_process_index,
        "Now cookbook name": barista.now_cookbook_name,
        "Temperature": barista.heater_temperature,
        "Is water full": barista.is_water_full,
        "Total commands": barista.total_cmd,
        "Progress": barista.printer_progress
    }

    return jsonify(status)

@app.route("/barista", methods=["PUT"])
def brew():
    """
    {
        "Command": "Start|Pause|Resume|Stop",
        "Name": "Cookbook"
    }
    """
    params = json.loads(request.data)

    cmd = params["Command"]
    name = params["Name"]

    app.logger.debug("{} {} ...".format(cmd, name))

    if cmd == "Start":
        barista.brew(name)

    resp = make_response()
    resp.status_code = httplib.OK

    return resp

# ===============================================================================
#
# Printer API
#
# ===============================================================================
@app.route("/printer", methods=["GET"])
def get_printer_status():
    """
    {
        "state": "Printing",
        "progress": 198,
        "total": 3000
    }
    """
    status = {
        "state": barista.printer_state_string,
        "progress": barista.printer_progress,
        "total": barista.total_cmd
    }

    return jsonify(status)

@app.route("/printer/jog", methods=["PUT"])
def control_printer():
    """
    {
        "X": 0,
        "Y": 0,
        "Z": 0,
        "E1": 100,
        "E2": 100,
        "F": 100
    }
    """
    params = json.loads(request.data)
    barista.printer_jog(params["X"],
                        params["Y"],
                        params["Z"],
                        params["E1"],
                        params["E2"],
                        params["F"])

    resp = make_response()
    resp.status_code = httplib.CREATED

    return resp
# ===============================================================================
#
# Heater API
#
# ===============================================================================
@app.route("/heater", methods=["GET"])
def get_heater_status():
    pass

@app.route("/heater", methods=["PUT"])
def control_heater():
    """
    {
        "Set Point": 80
    }
    """
    pass

# ===============================================================================
#
# Refill API
#
# ===============================================================================
@app.route("/refill", methods=["GET"])
def get_refill_status():
    return jsonify({"full": barista.is_water_full})

@app.route("/refill", methods=["PUT"])
def control_refill():
    """
    {
        "Command": "Start|Stop"
    }
    """
    pass
