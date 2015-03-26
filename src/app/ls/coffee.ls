require! {
    "components/cookbook.js": cookbook
    "components/printer.js": printer
}

m.route (document.getElementById "wrapper"), "/", {
    "/": cookbook,
    "/printer": printer
}
