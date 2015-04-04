temperature = {}

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
temperature.view = (ctrl) ->
    (m '#plot[style=height:400px]', {config: ctrl.config_chart})

# ================================================================================
#
#   Controller 
#
# ================================================================================
temperature.controller = ! ->
    @config_chart = (elem, isInitialized, ctx) ->
        chart = ctx.Chart

        if not isInitialized
            ctx.chart = new Highcharts.Chart(
                chart : {
                    type: 'spline'
                    renderTo: 'plot'
                    animation: Highcharts.svg
                    marginRight: 10
                    events: {
                        load: ! ->
                            series = @series[0]
                            setInterval( ! -> 
                                x = (new Date!).getTime!
                                y = Math.random!

                                series.addPoint([x, y], true, true)
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
                        text: "Value"
                    }
                    plotLines: [{
                        value: 0
                        width: 1
                        color: "#808080"
                    }]
                }
                legend: {
                    enabled: false
                }
                exporting: {
                    enabled: false
                }
                series: [{
                    name: "Random data"
                    data: do ->
                        data = []
                        time = (new Date!).getTime!

                        for i from -19 to 0
                            data.push({
                                x: time + i * 1000
                                y: Math.random()
                            })

                        data
                }]
            )
        return

module.exports = temperature 
