# {{ file_name }}

### {{ timestamp }}

{% for chunk in chunks %}
#### Input
```{{ script_type }}
{{ chunk.in }}
```
#### Output
{% if chunk.html %}
HTML output not supported.
{% elif chunk.markdown %}
{{ chunk.out }}
{% else %}
```{{ script_type }}
{{ chunk.out }}
```
{% endif %}
---
{% endfor %}

_Script triggered by {{ author }} on {{ timestamp }}, ran in {{ duration }}ms_

_Report generated with [Merkury](https://github.com/ppatrzyk/merkury) v{{ version }}._