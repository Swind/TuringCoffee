cookbook_list = {}

# ================================================================================
#
#   View and Controller
#
# ================================================================================
#
cookbook_list.view = (ctrl) ->

    generate_item = (cookbook) ->
        m "div.ui.item", {id: "cookbook-item", onclick: ! -> ctrl.select_cookbook(cookbook)},[
            (m "div.content", [
                (m "a.header" cookbook.id),
                (m "div.meta" cookbook.created_date),
                (m "div.description", [
                    (m "div" cookbook.estimated_time),
                    (m "div" cookbook.length)
                ])
            ])
        ]

    m "div.ui.items.divided", for cookbook in ctrl.vm.cookbooks!
        generate_item(cookbook)

cookbook_list.controller = (vm) ->
    @vm = vm
    @vm.list!

    @select_cookbook = (selected_cookbook) ->
        @vm.select_cookbook(selected_cookbook)

    this

module.exports = cookbook_list
