
{% if table %}
{% for x in table %}{{ x.0 }} {{ x.1 }} hr  {{ x.2 }}%
{% endfor %}
{% else %}
No table given
{% endif %}