#Attach ready event

sidebar = {}

sidebar.ready = ! ->

    # Set the header "menu" click action.
    # When "menu" be clicked, the sidebar will be shown
    <- $ \.setting.item .on \click
    $ \.setting.sidebar .sidebar \toggle




$ document .ready(sidebar.ready)
