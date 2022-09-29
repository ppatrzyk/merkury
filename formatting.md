---
layout: default
title: Formatting
nav_order: 2
---

# Formatting
{: .no_toc }

By default merkury treats any output as simple print and puts it into `<code>` blocks. There is also a possibility to treat it as either raw HTML or markdown. This is achieved by placing a _magic comment_ after print statement in your script.

## HTML

You need to put a comment `#HTML` after a line that outputs raw HTML.

Example:

```
print("""<img src="https://www.python.org/static/img/python-logo-large.c36dccadd999.png" alt="python">""")
#HTML
```

In addition to writing HTML by hand or using libraries that allow formatting output as HTML, `merkury` provides [utility functions](https://github.com/ppatrzyk/merkury/blob/master/merkury/utils.py) to format **plots** from common libraries. See [plotting docs](https://ppatrzyk.github.io/merkury/plotting.html) for details.

## Markdown

It's also possible to print text formatted in markdown. You need to put magic comment `#MARKDOWN` after print statement.

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
