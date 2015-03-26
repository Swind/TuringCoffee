require! {
    "components/cookbook_list.js": cookbook_list 
    "components/cookbook_content.js": cookbook_content
}

cookbook = {}

# ================================================================================
#
#   Model 
#
# ================================================================================
class CookbookItem 
    (metadata) ->
        @import(metadata)

    import: (metadata) ->
        @id = metadata["id"] 
        @name = metadata["name"]
        @created_date = @format_date(metadata['date'])
        @estimated_time = metadata["analysis"]["estimatedPrintTime"].toFixed(2)
        @length = metadata["analysis"]["filament"]["tool0"]["length"].toFixed(2)

        if "content" in metadata
            @content = metadata["content"]
        else
            @content = "Empty"

    format_date: (date_time) ->
        dd = new Date(date_time * 1000)
        dd.getFullYear! + '/' + (dd.getMonth! + 1) + "/" + dd.getDate! + " " +
            dd.getHours! + ":" + dd.getMinutes! + ":" + dd.getSeconds!

cookbook.vm = do ->
    vm = {}

    vm.init = ! ->
        vm.cookbooks = m.prop {}
        vm.selected = m.prop {content: ""}

    vm.list = ! ->
        return m.request(
            {
                method: 'GET',
                url: '/plugin/coffee/cookbooks'
            }
        )
        .then((raw_data) ->
            cookbooks = for id, metadata of raw_data
                new CookbookItem(metadata)

            vm.cookbooks(cookbooks)
        )

    vm.select_cookbook = (selected_cookbook) ->
        response = m.request(
            {
                method: 'GET',
                url: '/plugin/coffee/cookbooks/' + selected_cookbook.id
            }
        ).then(vm.selected)

    vm.save_selected_cookbook = ! ->
        m.request(
            {
                method: 'PUT',
                url: '/plugin/coffee/cookbooks/' + vm.selected!.id,
                data: vm.selected!.content 
            }
        )

    vm
# ================================================================================
#
#   View 
#
# ================================================================================
cookbook.view = (ctrl) ->
    [
        (m "div.four.wide.column", {id: "sidebar-wrapper"}, [
            (m "div", {id: "sidebar"}, [ctrl.cookbook_list!])
        ]),
        (m "div.twelve.wide.column", {id: "main-wrapper"}, [
            (m "div", {id: "main"}, [ctrl.cookbook_content!])
        ])
    ]

# ================================================================================
#
#   Controller 
#
# ================================================================================
submodule = (module, args) ->
    return module.view.bind(this, new module.controller(args))

cookbook.controller = ! ->
    cookbook.vm.init!

    @cookbook_list = submodule(cookbook_list, cookbook.vm)
    @cookbook_content = submodule(cookbook_content, cookbook.vm)

module.exports = cookbook
