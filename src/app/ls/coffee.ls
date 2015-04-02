require! {
    "components/cookbook.js": cookbook
    "components/barista.js": barista 
}

m.route (document.getElementById "wrapper"), "/", {
    "/": cookbook,
    "/barista": barista 
}
