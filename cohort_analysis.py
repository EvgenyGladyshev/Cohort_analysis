import pandas as pd

# Считываем csv файл по вложенному бюджету

df_spent = pd.read_csv('spent.csv')

# Считаем сколько денег было потрачено по когортам и источникам
# Поскольку в данных представлены уже с разбивкой по месяцу и источнику, то просто сортируем их
df_spent = df_spent.sort_values(['Когорта', 'Источник'])

# Добавляем дату из когорт для дальнейшего соединения
df_spent['Дата'] = df_spent['Когорта']

# Так как источников несколько, то выбираем тот, который хотим исследовать
# То есть просто меняем в фильтре название источника, чтобы посмотреть отдельные покупки по ним
# Чтобы посмотреть общие значения, убираем этот фильтр

# Фильтры: ВК, Инстаграм, Яндекс, Телеграм
# ВАЖНО: для анализа важно не забывать менять фильтры как в df_spent, так и в df_data

df_spent = df_spent[df_spent['Источник']=='ВК']

# Создаем отдельный таблицу из одного столбца для когорт
cohorts_spent = (df_spent['Когорта']).to_frame(name='cohorts_spent')

# Создаем отдельный таблицу из одного столбца для месяцев покупки
dates_spent = (df_spent['Дата']).to_frame(name='dates_spent')

# Соединяем обе таблицы декартновым произведением
# Таким образом, у нас будет для каждой когорты все месяцы покупок
dates_cohorts_spent = dates_spent.merge(cohorts_spent, how='cross')

# Объединяем полученную таблицу когорт и дат покупок с таблицей вложенных инвестиций
df_spent = df_spent.merge(dates_cohorts_spent, how='right', left_on=['Когорта', 'Дата'], right_on=['cohorts_spent', 'dates_spent'])

# Заполняем столбец 'Потрачено' вместо NaN потраченной суммой на тот или иной месяц
df_spent['Потрачено'] = df_spent.groupby('cohorts_spent')['Потрачено'].transform('first')



# Считываем csv файл по покупкам клиентов
df_data = pd.read_csv('data.csv', dtype={'карта клиента': str})

# Отсортировали данные по клиенту и дате покупки
df_data = df_data.sort_values(['карта клиента', 'Дата покупки'])

# Так как один клиент может прийти только из одного источника, приводим данные по источнику к корректному виду
df_data['корректный_источник'] = df_data.groupby('карта клиента')['Источник'].transform('first')

# Разделили пользователей на когорты, а также добавили столбец с годом и месяцем покупок
df_data['cohort'] = pd.to_datetime(df_data.groupby('карта клиента')['Дата покупки'].transform('min')).dt.strftime('%Y-%m')
df_data['ym'] = pd.to_datetime(df_data['Дата покупки']).dt.strftime('%Y-%m')

# Так как источников несколько, то выбираем тот, который хотим исследовать
# То есть просто меняем в фильтре название источника, чтобы посмотреть отдельные покупки по ним
# Чтобы посмотреть общие значения, убираем этот фильтр
# Фильтры: ВК, Инстаграм, Яндекс, Телеграм

df_data = df_data[df_data['корректный_источник'] == 'ВК']

# Отдельно посчитаем сколько клиентов пришло из каждого источника с разбивкой на когорты и на источник
cohort_clients = df_data.groupby('cohort')['карта клиента'].nunique().reset_index()

# Посчитали суммы покупок каждой когорты в каждом месяце
df_data = df_data.groupby(['cohort', 'ym'])['сумма покупки'].agg('sum').reset_index()

# Посчитали куммулятивный итог (LTV) по когортам
df_data['LTV'] = df_data.sort_values(['cohort', 'ym']).groupby('cohort')['сумма покупки'].agg('cumsum')

# Создаем отдельный таблицу из одного столбца для когорт
cohorts_data = df_data['cohort']
# Убираем дубликаты
cohorts_data = (cohorts_data.drop_duplicates()).to_frame(name='cohorts_data')

# Создаем отдельный таблицу из одного столбца для месяцев покупки
dates_data = df_data['ym']
# Убираем дубликаты 
dates_data = (dates_data.drop_duplicates()).to_frame(name='dates_data')

# Соединяем обе таблицы декартновым произведением
# Таким образом, у нас будет для каждой когорты все месяцы покупок
dates_cohorts_data = dates_data.merge(cohorts_data, how='cross')

# Объединяем полученную таблицу когорт и дат покупок с таблицей покупок юзеров
# Формируем итоговую таблицу для анализа LTV
df_data = df_data.merge(dates_cohorts_data, how='right', left_on=['cohort', 'ym'], right_on=['cohorts_data', 'dates_data'])

# Добавляем к таблице с покупками юзеров столбец вложенных инвестиций для анализа
df_data['Потрачено'] = df_spent['Потрачено']

# Добавляем столбец ROMI для понимания окупаемости вложенных средств
df_data['ROMI'] = round((df_data['LTV']-df_data['Потрачено'])/df_data['Потрачено']*100, 2)

# Создаем таблицу LTV
LTV = df_data.pivot_table(index=['cohorts_data', 'Потрачено'], columns='dates_data', values='LTV' , aggfunc='max').fillna('')
print(LTV)

# Создаем таблицу ROMI
ROMI = df_data.pivot_table(index=['cohorts_data', 'Потрачено'], columns='dates_data', values='ROMI').fillna('')
print(ROMI)