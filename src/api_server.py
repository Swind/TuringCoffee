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
@app.route("/cookbooks", method=["GET"])
def list_cookbooks(self):
    """
    {
        "cookbooks": ["cookbook1", "cookbook2", "cookbook3"]
    }
    """
    cookbooks = cmgr.list()
    return jsonify(cookbooks)

@app.route("/cookbooks/<str:name>", method=["GET"])
def read_cookbook(self, name):
    """
    {
        "name": "cookbook1",
        "date": "",
        "description": ""
    }
    """
    return cmgr.read(name)

@app.route("/cookbooks/<str:name>", method=["PUT"])
def update_cookbook(self, name):
    """
    {
        "name": "new_cookbook_name"
    }
    """
    new_content = request.data

@app.route("/cookbooks/<str:name>/content", method=["GET"])
def read_cookbook_content(self, name):
    pass

@app.route("/cookbooks/<str:name>/content", method=["PUT"])
def update_cookbook_content(self, name):
    pass

@app.route("/cookbooks/<str:name>", method=["DELETE"])
def delete_cookbook(self, name):
    pass

# ===============================================================================
#
# Printer API
#
# ===============================================================================
@app.route("/printer", method=["GET"])
def get_printer_status(self):
    pass

@app.route("/printer", method=["PUT"])
def print_cookbook(self):
    """
    {
        "Command": "Start|Pause|Resume|Stop",
        "Cookbook Name": "Cookbook"
    }
    """
    pass

@app.route("/printer/jog", method=["PUT"])
def control_printer(self):
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
@app.route("/heater", method=["GET"])
def get_heater_status(self):
    pass

@app.route("/heater", method=["PUT"])
def control_heater(self):
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
@app.route("/refill", method=["GET"])
def get_refill_status(self):
    pass

@app.route("/refill", method=["PUT"])
def control_refill(self):
    """
    {
        "Command": "Start|Stop"
    }
    """
    pass
