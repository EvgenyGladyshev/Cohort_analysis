# Описание задачи

В течение года проводились рекламные кампании в разных каналах по привлечению новых клиентов интернет-аптеки. По окончании года нужно было принять решение - какие каналы привлечения показали себя хорошо и их стоит масштабировать, а какие нужно менять/убирать.

## Что было сделано

Было предложено провести когортный анализ LTV/ROMI в рамках данной работы.

1. Собраны данные о транзакциях клиентов, сформированы когорты по месяцам.
2. Рассчитаны LTV и ROMI для каждой когорты по месяцам с разбивкой на каналы.
3. Сформированы выводы об окупаемости рекламных кампаний и каналов привлечения.

## Данные для работы
- [Данные по продажам с вебинара](https://github.com/EvgenyGladyshev/Cohort_analysis/blob/master/spent.csv)
- [Данные по канал](https://raw.githubusercontent.com/EvgenyGladyshev/Cohort_analysis/refs/heads/master/data.csv)
- [Код проведения когортного анализа](https://github.com/EvgenyGladyshev/Cohort_analysis/blob/master/cohort_analysis.py) (в строке `21` и `59` меняем источник на *ВК, Инстаграм, Яндекс или Телеграм* для изменения источника)
- [Бизнес-выводы и рекомендации](https://github.com/EvgenyGladyshev/Cohort_analysis/blob/master/insights.md)

## Запуск скрипта

```sh
# Создаем виртуальное окружение
python -m venv cohort_analysis

# Активируем виртуальное окружение
./cohort_analysis/scripts/activate # source cohort_analysis/bin/activate для Linux

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем скрипт
python cohort_analysis.py
```