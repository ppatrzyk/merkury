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

function interactive_tables() {
    console.log("interactive_tables called");
    var tables = Array.from(document.getElementsByTagName("table"));
    tables.forEach(table => {
        // todo tryexcept that
        table.insertAdjacentHTML("beforebegin", '<input class="search" placeholder="Search" />');
        var body = table.getElementsByTagName("tbody")[0];
        body.classList.add('list');
        var options = {
        valueNames: [ 'name', 'born' ]
        };
        var table_listjs = new List('users', options);
        // todo all column heads into sort buttons
        // https://listjs.com/examples/table/
    });
}

document.addEventListener("DOMContentLoaded", interactive_tables);
