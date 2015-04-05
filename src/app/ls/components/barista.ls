require! {
    "components/heater.js": heater 
    "components/printer.js": printer 
}

barista = {}

# ================================================================================
#
#   Model 
#
# ================================================================================

# ================================================================================
#
#   View 
#
# ================================================================================
barista.view = (ctrl) ->
    [
        (m "div.column", [ctrl.heater_chart!])
        (m "div.column", [ctrl.printer!])
    ]
# ================================================================================
#
#   Controller 
#
# ================================================================================
submodule = (module, args) ->
    return module.view.bind(this, new module.controller(args))

barista.controller = ! ->
    @heater_chart = submodule(heater, {})
    @printer = submodule(printer, {})

module.exports = barista
