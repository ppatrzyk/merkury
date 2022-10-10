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

function random_str() {return (Math.random() + 1).toString(36).substring(2);} // https://stackoverflow.com/a/8084248

function make_table(table) {
    var body = table.getElementsByTagName("tbody")[0];
    body.classList.add("list");
    var headers = Array.from(table.getElementsByTagName("th"));
    header_classes = headers.map(header => `${header.textContent.replace(/\s/g, "")}_${random_str()}`);
    headers.forEach((header, i, _headers) => {
        var sort_button = document.createElement("button");
        sort_button.classList.add("sort");
        sort_button.setAttribute("data-sort", header_classes[i]);
        sort_button.innerText = header.innerText;
        header.innerText = "";
        // TODO think about best format of this
        // Either adjust button style or put next to text as "sort"?
        // sort_button.innerText = "sort";
        header.appendChild(sort_button);
        // header.replaceWith(sort_button);
    });
    var cells = Array.from(table.getElementsByTagName("td"));
    cells.forEach((cell, i, _cells) => {
        cell.classList.add(header_classes[i % header_classes.length]);
    });
    var current_parent = table.parentNode;
    var div_parent = document.createElement("div");
    div_parent.id = random_str();
    current_parent.replaceChild(div_parent, table);
    search_input = document.createElement("input")
    search_input.classList.add("search")
    search_input.setAttribute("placeholder", "Search")
    // TODO pagination better style or remove
    pagination = document.createElement("ul")
    pagination.classList.add("pagination")
    div_parent.appendChild(search_input);
    div_parent.appendChild(table);
    div_parent.appendChild(pagination);
    var list_js_opts = {valueNames: header_classes, page: 10, pagination: true}
    var table_listjs = new List(div_parent.id, list_js_opts);
}

function interactive_tables() {
    var tables = Array.from(document.getElementsByTagName("table"));
    tables.forEach(table => {
        try {
            make_table(table);
        } catch (error) {
            console.warn(`Failed to make table interactive: ${error.message}`);
        }
    });
}

document.addEventListener("DOMContentLoaded", interactive_tables);
