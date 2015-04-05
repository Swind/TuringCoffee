printer = {}

# ================================================================================
#
#   Model 
#
# ================================================================================
printer.vm = do ->
    vm = {}
    vm.jog = (x=null, y=null, z=null, e1=null, e2=null, f=null) ->
        data = {
            "X": x,
            "Y": y,
            "Z": z,
            "E1": e1,
            "E2": e2,
            "F": f
        }

        return m.request(
            {
                method: "PUT"
                url: "/printer/jog"
                data: data
            }
        )

    vm

# ================================================================================
#
#   View 
#
# ================================================================================
printer.view = (ctrl) ->
    panel_button = (button_name, onclick) ->
        return (m "div.column", (m "div.ui.icon.button" {onclick: onclick}, (m "i.#button_name.icon")))

    generate_control_panel = ! ->
        return (m "div.ui.three.column.grid.middle.padded.aligned.internally.celled", [
            (m "div.row", [
                panel_button("home")
                panel_button("arrow.up")
                panel_button("home")
            ])

            (m "div.row", [
                panel_button("arrow.left")
                panel_button("home")
                panel_button("arrow.right")
            ])

            (m "div.row", [
                panel_button("home")
                panel_button("arrow.down")
                panel_button("home")
            ])
        ])

    return (m "div.ui.four.column.grid", [
        (m "div.ui.column", [generate_control_panel!])
    ])

# ================================================================================
#
#   Controller 
#
# ================================================================================
printer.controller = ! ->
    return

module.exports = printer
