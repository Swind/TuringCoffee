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

    generate_buttons = (cookbook) ->
        m "div.buttons" {config: ctrl.button_config} [
            (m "div.button.button-edit" {
                onclick: ctrl.brew_onclick.bind cookbook
            } "Edit")
            (m "div.button.button-brew" {
                onclick: ctrl.brew_onclick.bind cookbook
            } "Brew")
        ]

    generate_card = (cookbook) ->
        m "div.col-xs-12.col-sm-4.col-md-3.col-lg-2", [
            (m "div.card[href='/editor/#{cookbook.name}']",
            {
                config: m.route
                onclick: ctrl.card_onclick
            },
            [
                (m "div.header", cookbook.name)
                (m "div.divider")
                (m "div.description" cookbook.description)
                (generate_buttons cookbook)
            ])
        ])

    cards = (cookbooks) ->
        m "div", for cookbook in cookbooks
            generate_card(cookbook)

    [
        (m "div.row.card-container", [cards(cookbook.vm.cookbooks!)])
    ]

# ================================================================================
#
#   Controller 
#
# ================================================================================
cookbook.controller = ->
    cookbook.vm.init!
    cookbook.vm.list!

    ctrl = {}
    ctrl.card_onclick = (e) !->
        btns = document.getElementsByClassName 'buttons'

        for btn in btns
            btn.style.display = 'none'

        for child in this.children
            if child.className is 'buttons'
                child.style.display = 'flex'

    ctrl.button_config = (element, isInit) !->
        if isInit is false
            element.style.display = 'none'

    ctrl.brew_onclick = ->
        m.route "/brew/#{this.name}"

    ctrl.edit_onclick = ->
        m.route "/editor/#{this.name}"

    ctrl

module.exports = cookbook
