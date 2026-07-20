# DL PLAYING BOT

## CONFIG

[config.yaml](config.yaml)

Заполните файл данными полученными из
https://my.telegram.org/apps

```yaml
accounts:
  - name: _some_name_
    api_id: _some_api_id_
    api_hash: _some_api_hash_
```

## USING

* Рыбалка
    * `python dl/main.py -j fishing -a _some_name_`
* Атака
    * `python dl/main.py -j fighting -a _some_name_`
* Совместная атака на мобов
    * `python dl/main.py -j party -a _some_name_`
* Различные калькуляторы
  * `python calc.py`