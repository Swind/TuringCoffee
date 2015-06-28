#Attach ready event

sidebar = {}

console.log 'load sidebar script...'

sidebar.ready = ! ->

    <- $ \.setting.item .on \click
    console.log 'button be clicked'
    $ \.setting.sidebar .sidebar \toggle


$ document .ready(sidebar.ready)
