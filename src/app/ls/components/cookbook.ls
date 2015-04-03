cookbook = {}

# ================================================================================
#
#   Model 
#
# ================================================================================
class CookbookItem 
    (name, data) ->
        @name = name
        @description = data["description"]

cookbook.vm = do ->
    vm = {}

    vm.init = ! ->
        vm.cookbooks = m.prop {}

    # Get cookbook list
    vm.list = ! ->
        return m.request(
            {
                method: 'GET',
                url: '/cookbooks'
            }
        )
        .then((raw_data) ->
            cookbooks = for name, data of raw_data
                new CookbookItem(name, data)

            vm.cookbooks(cookbooks)
        )

    vm
# ================================================================================
#
#   View 
#
# ================================================================================
cookbook.view = (ctrl) ->
    generate_card = (cookbook) ->
        m "div.ui.card", [
            (m "div.content", [
                (m "i.right.floated.delete.icon")
                (m "a.header[href='/editor/#{cookbook.name}']", {config: m.route}, cookbook.name)
                (m "div.description" cookbook.description)
            ])
        ]

    cards = (cookbooks) ->
        m "div.ui.three.cards", for cookbook in cookbooks
            generate_card(cookbook)

    [
        (m "div.column", [cards(cookbook.vm.cookbooks!)])
    ]

# ================================================================================
#
#   Controller 
#
# ================================================================================
cookbook.controller = ! ->
    cookbook.vm.init!
    cookbook.vm.list!

module.exports = cookbook
