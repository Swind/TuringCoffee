from flask import Flask
from flask import jsonify, Response, render_template, abort
from flask import request

from cookbook_manager import CookbookManager

# ===============================================================================
#
# Global Variables
#
# ===============================================================================

app = Flask(__name__)
cmgr = CookbookManager()

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
    return jsonify(cookbooks)

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
    new_content = request.data

@app.route("/cookbooks/<string:name>/content", methods=["GET"])
def read_cookbook_content(name):
    pass

@app.route("/cookbooks/<string:name>/content", methods=["PUT"])
def update_cookbook_content(name):
    pass

@app.route("/cookbooks/<string:name>", methods=["DELETE"])
def delete_cookbook(name):
    pass

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
    pass

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
    pass

@app.route("/refill", methods=["PUT"])
def control_refill():
    """
    {
        "Command": "Start|Stop"
    }
    """
    pass
