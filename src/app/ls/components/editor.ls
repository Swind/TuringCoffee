cookbook_content = {}
# ================================================================================
#
#   View 
#
# ================================================================================
cookbook_content.view = (ctrl) -> [
    (m "div.column", {id: "editor"}, [
        (m "div.ui.buttons", [
            (m "div.ui.icon.button", [(m "i.save.icon"), "Save"]),
            (m "div.ui.icon.button", [(m "i.print.icon"), "Print"])
        ]),
        (m "div.ui.buttons", [
            (m "div.ui.icon.button", (m "i.header.icon")),
            (m "div.ui.icon.button", (m "i.code.icon")),
            (m "div.ui.icon.button", (m "i.list.icon")),
            (m "div.ui.icon.button", (m "i.ordered.list.icon")),
        ]),
        (m 'div#cookbook-content' {config: ctrl.config_editor})
    ])
]

# ================================================================================
#
#   Controller and View Model 
#
# ================================================================================
cookbook_content.vm = do ->
    vm = {}

    # Create the cookbook name and content properties
    # These will be used by codemirror editor and toolbar
    vm.init = ! ->
        vm.name = m.prop ""
        vm.content = m.prop ""

    # Send a request to get the cookbook content and update the content to trigger the editor refresh 
    vm.load_content = (name) ->
        return m.request(
            {
                method: 'GET',
                url: "/cookbooks/#name/content"
                deserialize: (value) -> value
            }
        )
        .then((content) ->
            vm.content(content)
        )

    vm

cookbook_content.controller = ! ->
    cookbook_content.vm.init!

    # Get the route param and load the cookbook content by name
    @cookbook_name = m.route.param "name"
    cookbook_content.vm.load_content(@cookbook_name)

    # Create Codemirror editor and save the editor instance to the view model 
    @config_editor = (elem, isInitialized, ctx) ->
        cookbook_content.vm.editor = CodeMirror(elem, {
            value: cookbook_content.vm.content!,
            lineNumbers: true,
            mode: "markdown",
            lineWrapping: true,
            viewportMargin: Infinity
        })

module.exports = cookbook_content
