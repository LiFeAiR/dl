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
{% if stat.diff.count > 0 -%}
 {% set p ="+" -%}
{% else -%}
 {% set p ="" -%}
{% endif -%}
{{ key_title }}: {{ stat.cur.count }} {% if stat.diff.count != 0 %}({{ p }}{{ stat.diff.count }}){% endif %} шт. = {{ stat.cur.total }} {% if stat.diff.count != 0 %}({{ p }}{{ stat.diff.total }}){% endif %}
{% for key1, item in calc[key].items() -%}
└ {{item.name}}x{{item.cur}} {% if item.diff != 0 %}({% if item.diff > 0 %}+{% endif %}{{item.diff}}){% endif %}
{% endfor -%}
{% endif -%}
{% endfor %}
{% if stats.all.diff.count > 0 -%}
 {% set p ="увеличилось на" -%}
{% else -%}
 {% set p ="уменьшилось на" -%}
{% endif -%}
🐟 Было рыбы: {{stats.all.prev.count}} шт., стало рыбы: {{stats.all.cur.count}} шт.{% if stats.all.diff.count != 0 %}, {{p}} {{stats.all.diff.count|abs}} шт.{% endif %}
💰 Общая стоимость: было - {{stats.all.prev.total}}, стало - {{stats.all.cur.total}}{% if stats.all.diff.count != 0 %}, {{p}} {{stats.all.diff.total|abs}}{% endif %}