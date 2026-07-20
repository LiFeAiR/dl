📊 Подсчёт рыбы:
{% for key, stat in stats.items() -%}
{% if key == "huge" -%}
    {% set key_title = "Огромная³" -%}
{% elif key == "big" -%}
    {% set key_title = "Большая²" -%}
{% elif key == "small" -%}
    {% set key_title = "Мелкая¹" -%}
{% endif -%}
{% if key != "all" -%}
{{ key_title }}: {{ stat.count }} (+{{ stats1[key].count - stat.count }}) шт. = {{ stat.total }} (+{{ stats1[key].total - stat.total }})
{% for key1, item in calc1[key].items() -%}
└ {{item.name}}x{{item.count}} (+{% if key1 in calc[key] %}{{item.count - calc[key][key1].count}}{% else %}{{item.count}}{% endif %})
{% endfor -%}
{% endif -%}
{% endfor %}
🐟 Было рыбы: {{stats.all.count}} шт., стало рыбы: {{stats1.all.count}} шт.
💰 Общая стоимость: было - {{stats.all.total}}, стало - {{stats1.all.total}}