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
{{ key_title }}: {{ stat.count }} шт. = {{ stat.total }}
{% for key1, item in calc[key].items() -%}
└ {{item.name}}x{{item.count}}
{% endfor -%}
{% endif -%}
{% endfor %}
🐟 Всего рыбы: {{stats.all.count}} шт.
💰 Общая стоимость: {{stats.all.total}}