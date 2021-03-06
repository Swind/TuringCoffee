require! {
    "components/cookbook.js": cookbook
    "components/barista.js": barista
    "components/editor.js": editor
}

m.route (document.getElementById "wrapper"), "/", {
    "/": cookbook
    "/editor/:name": editor
    "/brew/:name": barista
}
