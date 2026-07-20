📊 Подсчёт рыбы:
{% for key, stat in stats.items() -%}
{% if key == "huge" -%}
Огромная³: {{ stat.count }} шт. = {{ stat.total }}
{% elif key == "big" -%}
Большая²: {{ stat.count }} шт. = {{ stat.total }}
{% elif key == "small" -%}
Мелкая¹: {{ stat.count }} шт. = {{ stat.total }}
{% endif -%}
{% for item in calc[key] -%}
└ {{item.name}}x{{item.count}}
{% endfor -%}
{% endfor %}
🐟 Всего рыбы: {{stats.all.count}} шт.
💰 Общая стоимость: {{stats.all.total}}