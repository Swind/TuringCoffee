require! {
    "components/temperature.js": temperature 
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
        (m "div.column", [ctrl.temperature_chart!])
    ]
# ================================================================================
#
#   Controller 
#
# ================================================================================
submodule = (module, args) ->
    return module.view.bind(this, new module.controller(args))

barista.controller = ! ->
    @temperature_chart = submodule(temperature, {})

module.exports = barista 
