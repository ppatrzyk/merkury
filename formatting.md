---
layout: default
title: Formatting
nav_order: 2
---

# Formatting
{: .no_toc }

Merkury processes files with any python code and by default treats output as standard text. However, in some cases you might want to render code output as [raw html](#html) or treat program output as [markdown](#markdown). This section provides an overview on how to do it.

1. TOC
{:toc}

## HTML

You need to put a comment `#HTML` after a line that outputs raw HTML.

Example:

```
print("""<img src="https://www.python.org/static/img/python-logo-large.c36dccadd999.png" alt="python">""")
#HTML
```

## Markdown

You need to put a comment `#MARKDOWN` after a line that outputs markdown text.

Example:

```
print("""
# I'm a markdown header

List:

* l1
* l2

""")
#MARKDOWN
```
