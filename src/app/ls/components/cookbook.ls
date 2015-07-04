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
        (m "div.col-md-3", [
            (m "div.thumbnail", [
                (m "img" {"data-src": "holder.js/300x200"})
                (m "div.caption", [
                    (m "h4", cookbook.name)
                    (m "p", cookbook.description)
                    (m "p", [
                        (m "a.btn.btn-info[href='/editor/#{cookbook.name}']", {role: "button", config: m.route}, "Edit")
                        (m "a.btn.btn-default[href='#']", {role: "button"}, "Brew")
                    ])
                ])
            ])
        ])

    cards = (cookbooks) ->
        m "div", for cookbook in cookbooks
            generate_card(cookbook)

    [
        (m "div", [
            (m "div.center-block", [
                cards(cookbook.vm.cookbooks!)
            ])
        ])
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
