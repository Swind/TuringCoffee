cookbook_content = {}
# ================================================================================
#
#   CodeMirror Editor 
#
# ================================================================================
codemirror_editor = (mode, value, opts) ->
    setup_codemirror = (elem, isInitialized, ctx) ->
        editor = ctx.CodeMirror

        if !isInitialized
            editor = CodeMirror(elem, {
                value: value!.content,
                lineNumbers: true,
                mode: mode
            })

            ctx.last_value = value!.content
            ctx.CodeMirror = editor

            do
                (editor, changeObj) <-! editor.on "change"
                m.startComputation!
                value!.content = editor.getValue!
                ctx.last_value = value!.content
                m.endComputation!

            do
                <- setTimeout _, 0
                editor.refresh!
        else
            if ctx.last_value != value!.content
                ctx.last_value = value!.content
                editor.setValue value!.content

    opts = opts || {}
    opts.config = setup_codemirror

    return m "div\#cookbook-content", opts

# ================================================================================
#
#   View 
#
# ================================================================================
cookbook_content.view = (ctrl) -> [
        m("div.ui.header", ctrl.vm.selected!.id),
        m("div.ui.button", "Print"),
        m("div.ui.button", {onclick: ! -> ctrl.vm.save_selected_cookbook!}, "Save"),
        m("div.ui.button", "Delete"),
        codemirror_editor("markdown", ctrl.vm.selected, {})]

# ================================================================================
#
#   View Model 
#
# ================================================================================
cookbook_content.controller = (vm) ->
    @vm = vm

    this

module.exports = cookbook_content
