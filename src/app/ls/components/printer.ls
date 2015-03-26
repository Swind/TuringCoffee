printer = {}

# ================================================================================
#
#   Model 
#
# ================================================================================

printer.control = do ->
    control = {}

    # Send command to OctoPrint to control printhead
    control.printhead_request = (payload) ->
        return m.request(
            {
                method: "POST",
                url: "/api/printer/printhead",
                data: payload
            }
        )

    # PrintHead Commands
    control.printhead_cmds = {}
    control.printhead_cmds.jog = (x=0, y=0, z=0) ->
        payload = {
            "command": "jog", 
            "x": x,
            "y": y,
            "z": z
        }

        return control.printhead_request(payload)

    control.printhead_cmds.home = (axes) ->
        payload = {
            "command": "home",
            "axes": axes
        }

        return control.printhead_request(payload)

    # PrintHead alias 
    control.x = {}
    control.x.jog = (x) -> return control.printhead_cmds.jog(x, 0, 0)
    control.x.home = ! -> return control.printhead_cmds.home("[x]")

    control.y = {}
    control.y.jog = (y) -> return control.printhead_cmds.jog(0, y, 0)
    control.y.home = ! -> return control.printhead_cmds.home("[y]")

    control.z = {}
    control.z.jog = (z) -> return control.printhead_cmds.jog(0, 0, z)
    control.z.home = ! -> return control.printhead_cmds.home("[z]")

    return control

# ================================================================================
#
#   View 
#
# ================================================================================

icon_button = (icon_name, onclick) ->
    return (m "div.ui.icon.button", {onclick: onclick}, [
        (m "i.#icon_name.icon")
    ])

printer.view = (ctrl) ->
    (m "div.row",[
        icon_button("right.arrow"),
        icon_button("up.arrow"),
        icon_button("down.arrow"),
        icon_button("left.arrow"),
        icon_button("home.arrow")
    ])

printer.controller = ! ->
    return

module.exports = printer
