heater = {}

# ================================================================================
#
#   Model 
#
# ================================================================================
heater.vm = do ->
    vm = {}

    vm.init = ! ->
        vm.heater_status = m.prop {}
        vm.refill_status = m.prop {"full": false} 
        vm.input_temperature = m.prop 0

    vm.get_heater_status = (handler) ->
        return m.request(
            {
                method: "GET",
                url: "/heater"
            }
        )
        .then(vm.heater_status)
        .then(handler)

    vm

# ================================================================================
#
#   View 
#
# ================================================================================
heater.view = (ctrl) ->
    generate_heater_statistic = (key, label_name) ->
        return (m 'div.ui.statistic', [
            (m 'div.text.value', heater.vm.heater_status![key])
            (m 'div.label', label_name)
        ])

    (m "div.ui.two.column.grid", [
        (m 'div.ui.column#plot', {config: ctrl.config_chart})
        (m 'div.ui.column.large.horizontal.statistics', [
            generate_heater_statistic("temperature", "Temperature")
            generate_heater_statistic("set_point", "Set Point")
            generate_heater_statistic("duty_cycle", "Duty Cycle")
            generate_heater_statistic("is_water_full", "Water Level")
            (m "div.ui.action.input", [
                (m "input" {type: "text", onchange: m.withAttr("value", heater.vm.input_temperature)})
                (m "button.ui.button" {onclick: ctrl.set_temperature},"Set Temperature")
            ])
        ])
    ])

# ================================================================================
#
#   Controller 
#
# ================================================================================
heater.controller = ! ->
    heater.vm.init!

    @set_temperature = ! ->
        return m.request({
            method: "PUT"
            url: "/heater"
            data: {
                "Set Point": heater.vm.input_temperature!
            }
        })

    @config_chart = (elem, isInitialized, ctx) ->
        chart = ctx.Chart

        update_heater_status = (temperature_series, set_point_series, duty_cycle_series) ->
            handler = ! ->
                latest = heater.vm.heater_status!

                temperature = latest["temperature"]
                set_point = latest["set_point"]
                duty_cycle = latest["duty_cycle"]
                update_time = latest["update_time"]

                temperature_series.addPoint([update_time, temperature], true, false)
                set_point_series.addPoint([update_time, set_point], true, false)
                duty_cycle_series.addPoint([update_time, duty_cycle], true, false)

            heater.vm.get_heater_status(handler)

        if not isInitialized
            ctx.chart = new Highcharts.Chart(
                chart : {
                    type: 'spline'
                    renderTo: 'plot'
                    animation: Highcharts.svg
                    marginRight: 10
                    events: {
                        load: ! ->
                            temperature_series = @series[0]
                            set_point_series = @series[1]
                            duty_cycle_series = @series[2]

                            setInterval( ! ->
                                update_heater_status(
                                    temperature_series,
                                    set_point_series,
                                    duty_cycle_series)
                            , 1000)
                    }
                }
                title: {
                    text: "Live random data"
                }
                xAxis: {
                    type: "datetime"
                    tickPixelInterval: 150
                }
                yAxis: {
                    title: {
                        text: "Temperature (C)"
                    }
                    plotLines: [{
                        value: 0
                        width: 1
                        color: "#808080"
                    }]
                }
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle',
                    borderWidth: 0
                }
                exporting: {
                    enabled: false
                }
                series: [{
                    name: "Temperature"
                    data: []
                },
                {
                    name: "Set Points"
                    data: []
                },
                {
                    name: "Duty Cycle"
                    data: []
                }
                ]
            )
        return


module.exports = heater
