function change_theme() {
    var html = document.getElementsByTagName("html")[0];
    var prism_dark = document.getElementById("prism-dark");
    var prism_light = document.getElementById("prism-light");
    var current_theme = html.getAttribute("data-theme");
    if (current_theme == "dark") {
        html.setAttribute("data-theme", "light")
        prism_light.removeAttribute("media")
        prism_dark.setAttribute("media", "max-width: 1px")
    } else {
        html.setAttribute("data-theme", "dark")
        prism_dark.removeAttribute("media")
        prism_light.setAttribute("media", "max-width: 1px")
    }
}
