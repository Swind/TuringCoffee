printer = {}

# ================================================================================
#
#   Model 
#
# ================================================================================
printer.vm = do ->
    vm = {}

    vm.init = ! ->
        vm.barista_status = m.prop {}

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

    vm.go_home = ! ->
        return m.request({
            method: "PUT"
            url: "/printer/home"
        })

    vm.get_barista_status = (handler) ->
        return m.request(
            {
                method: "GET"
                url: "/barista"
            }
        )
        .then(vm.barista_status)
        .then(handler)

    vm.brew = (cookbook_name, action) ->
        return m.request({
            method: "PUT"
            url: "/barista"
            data: {
                "Name": cookbook_name
                "Command": action
            }
        })

    vm

# ================================================================================
#
#   View 
#
# ================================================================================
printer.view = (ctrl) ->
    panel_button = (button_name, onclick) ->
        return (m "div.ui.icon.button" {onclick: onclick}, (m "i.#button_name.icon"))

    generate_move_panel = ! ->
        return (m "table.ui.table.collapsing", [
            (m "tbody" ,[
                (m "tr", [
                    (m "td", panel_button("home"))
                    (m "td", panel_button("arrow.up"))
                    (m "td", panel_button("home"))
                ])

                (m "tr", [
                    (m "td", panel_button("arrow.left"))
                    (m "td", panel_button("home", ctrl.home_onclick))
                    (m "td", panel_button("arrow.right"))
                ])

                (m "tr", [
                    (m "td", panel_button("home"))
                    (m "td", panel_button("arrow.down"))
                    (m "td", panel_button("home"))
                ])
            ])
        ])

    control_button = (button_name, label, onclick) ->
        return (m "div.ui.labeled.icon.button" {onclick: onclick}, [(m "i.#button_name.icon"), label])

    generate_control_panel = ! ->
        return (m "div.ui.vertical.buttons" [
            control_button("play", "Start", ctrl.start_onclick)
            control_button("pause", "Pause")
            control_button("stop", "Stop", ctrl.stop_onclick)
        ])

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
    barista_status_panel = ! ->
        return (m "div", [
            (m "h5.ui.top.attached.header", "Barista Status")
            (m "div.ui.attached.segment", (m "p", printer.vm.barista_status!["State"]))

            (m "h5.ui.attached.header", "Brewing")
            (m "div.ui.attached.segment", (m "p", printer.vm.barista_status!["Now cookbook name"]))

            (m "h5.ui.attached.header", "Now step")
            (m "div.ui.attached.segment", (m "p", printer.vm.barista_status!["Now steps"]))

            (m "h5.ui.attached.header", "Now process")
            (m "div.ui.attached.segment", (m "p", printer.vm.barista_status!["Now process"]))
        ])

    progress_panel = ! ->
        return (m 'div.ui.indicating.progress#process_progress', [
            (m "div.bar")
            (m "div.label", "Process progress")
        ])

    return (m "div.ui.four.column.grid", [
        (m "div.ui.column", [generate_move_panel!])
        (m "div.ui.column", [generate_control_panel!])
        (m "div.ui.column", [barista_status_panel!])
        (m "div.ui.column", [progress_panel!])
    ])

# ================================================================================
#
#   Controller 
#
# ================================================================================
printer.controller = ! ->
    printer.vm.init!

    # Get the route param and load the cookbook content by name
    cookbook_name = m.route.param "name"

    update_progress = (status) ->
        total_cmd = status["Total commands"]
        progress = status["Progress"]

        $('#process_progress').progress({
            percent: (progress/total_cmd) * 100
        })

    setInterval( ! ->
        printer.vm.get_barista_status(update_progress)
    , 1000)

    @start_onclick = ! ->
        printer.vm.brew(cookbook_name, "Start")

    @stop_onclick = ! ->
        printer.vm.brew(cookbook_name, "Stop")

    @home_onclick = ! ->
        printer.vm.go_home()

module.exports = printer
