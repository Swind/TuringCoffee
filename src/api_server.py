from flask import Flask
from flask import jsonify, Response, render_template, abort, make_response
from flask import request

from cookbook_manager import CookbookManager

from chef import Chef

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

chef = Chef()

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
# Printer API
#
# ===============================================================================
@app.route("/printer", methods=["GET"])
def get_printer_status():
    pass

@app.route("/printer", methods=["PUT"])
def print_cookbook():
    """
    {
        "Command": "Start|Pause|Resume|Stop",
        "Cookbook Name": "Cookbook"
    }
    """
    params = json.loads(request.data)

    cmd = params["Command"]
    name = params["Cookbook Name"]

    app.logger.debug("{} {} ...".format(cmd, name))

    if cmd == "Start":
        chef.cook(name)

    resp = make_response()
    resp.status_code = httplib.OK

    return resp

@app.route("/printer/jog", methods=["PUT"])
def control_printer():
    """
    {
        "X": 0,
        "Y": 0,
        "Z": 0,
        "E1": 100,
        "E2": 100
    }
    """
    pass
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
    return jsonify({"full": chef.is_water_full})

@app.route("/refill", methods=["PUT"])
def control_refill():
    """
    {
        "Command": "Start|Stop"
    }
    """
    pass
