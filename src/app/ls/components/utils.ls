format_date = (date_time) ->
    dd = new Date(date_time * 1000)
    dd.getFullYear! + '/' + (dd.getMonth! + 1) + "/" + dd.getDate! + " " +
        dd.getHours! + ":" + dd.getMinutes! + ":" + dd.getSeconds!

submodule = (module, args) ->
    return module.view.bind(this, new module.controller(args))

