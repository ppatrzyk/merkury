function change_theme() {
    var theme = document.getElementById("dark-light-mode").checked ? "light" : "dark";
    var html = document.getElementsByTagName("html")[0];
    var prism_dark = document.getElementById("prism-dark");
    var prism_light = document.getElementById("prism-light");
    html.setAttribute("data-theme", theme);
    if (theme == "light") {
        prism_light.removeAttribute("media")
        prism_dark.setAttribute("media", "max-width: 1px")
    } else {
        prism_dark.removeAttribute("media")
        prism_light.setAttribute("media", "max-width: 1px")
    }
}
