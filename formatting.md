---
layout: default
title: Formatting
nav_order: 2
---

# Formatting
{: .no_toc }

In produced report, code will be broken into sections. Each section ends with a statement printing some output (e.g., `print()`). You can give titles to each section by placing _magic comment_ - `#TITLE <your_section_title>` for python, `--TITLE <your_section_title>` for SQL - after line that produces output.

### Python

When it comes to report formatting, there are 3 types of outputs in a Python script: Standard `<code>` block (default), HTML, or Markdown.

By default _merkury_ treats any output as standard code print and puts it into `<code>` blocks. If your output is actually HTML or Markdown, you need to indicate that by placing a _magic comment_ after print statement in your script.

#### HTML

You need to put a comment `#HTML` after a line that outputs raw HTML. For example:

```
print(pandas_df.to_html(border=0))
#HTML
```

In addition to writing HTML by hand or using libraries that allow formatting output as HTML, _merkury_ provides [utility functions](merkury/utils.py) to format **plots** from common libraries. See [plotting docs](https://ppatrzyk.github.io/merkury/plotting.html) for details.

#### Markdown

It's also possible to render text formatted in markdown. You need to put magic comment `#MARKDOWN` after print statement.

For example:

```
print("""
# I'm a markdown header

List:

* l1
* l2

""")
#MARKDOWN
```

### SQL

Outputs from all queries will be formatted as a HTML tables.
