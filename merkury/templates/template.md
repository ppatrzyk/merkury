# {{ file_name }}

### {{ timestamp }}

{% for chunk in chunks %}
\[_In_\]
```{{ script_type }}
{{ chunk.in }}
```
\[_Out_\]
{% if chunk.html or chunk.markdown %}
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