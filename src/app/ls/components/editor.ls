cookbook_content = {}
# ================================================================================
#
#   CodeMirror Editor 
#
# ================================================================================
codemirror_editor = (value, opts) ->

    setup_codemirror = (elem, isInitialized, ctx) ->

        editor = ctx.CodeMirror

        if !isInitialized
            editor = CodeMirror(elem, {
                value: value!,
                lineNumbers: true,
                mode: "markdown", 
                lineWrapping: true,
                viewportMargin: Infinity
            })

            ctx.last_value = value!
            ctx.CodeMirror = editor

            do
                (editor, changeObj) <-! editor.on "change"
                m.startComputation!
                value(editor.getValue!)
                ctx.last_value = value!
                m.endComputation!

            do
                <- setTimeout _, 0
                editor.refresh!
        else
            if ctx.last_value != value!
                ctx.last_value = value!
                editor.setValue value!

    opts = opts || {}
    opts.config = setup_codemirror

    return m "div\#cookbook-content", opts

codemirror_toolbar = ! -> 

    setup_codemirror = (elem, isInitialized, ctx) ->

        editor = ctx.CodeMirror

# ================================================================================
#
#   View 
#
# ================================================================================
cookbook_content.view = (ctrl) -> 
    (m "div.column", {id: "editor"}, [codemirror_editor(cookbook_content.vm.content, {})])

# ================================================================================
#
#   Controller and View Model 
#
# ================================================================================
cookbook_content.vm = do ->
    vm = {}

    vm.init = ! ->
        vm.name = m.prop ""
        vm.content = m.prop "" 

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

    @cookbook_name = m.route.param "name"
    cookbook_content.vm.load_content(@cookbook_name)


module.exports = cookbook_content
