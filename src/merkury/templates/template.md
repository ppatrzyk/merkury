# {{ title }}

### {{ timestamp }}

{% if toc %}
## Contents
{% for chunk in chunks %}
{% if chunk.title is not none %}
{{ chunk.number }}. {{ chunk.title }}
{% else %}
{{ chunk.number }}. Chunk {{ chunk.number }}
{% endif %}
{% endfor %}
{% endif %}

{% for chunk in chunks %}

{% if chunk.title is not none %}
## {{ chunk.title }}
{% endif %}

_In_ \[{{ chunk.number }}\]
```python
{{ chunk.in }}
```
_Out_ \[{{ chunk.number }}\]
{% if chunk.html or chunk.markdown %}
{{ chunk.out }}
{% else %}
```python
{{ chunk.out }}
```
{% endif %}
---
{% endfor %}

_Script {{ file_name }} triggered by {{ author }} on {{ timestamp }}, ran in {{ duration }}ms_

_Report generated with [Merkury](https://github.com/ppatrzyk/merkury) v{{ version }}._