## Используемая информация

База имен
1. https://mydata.biz/ru/catalog/databases/names_db

XML
1. https://codecamp.ru/blog/python-manipulating-xml/
1. https://riptutorial.com/ru/python/example/25995

plotly|Dash
1. https://dash.plotly.com/



docker docs
1. https://docs.docker.com/develop/develop-images/dockerfile_best-practices/https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

## Docker
#### Собираем images
```powershell
docker build -t local/2gis:v1 .
```

#### Запускаем контейнер
```powershell
docker run -v {путь к папке csv с результатами расчета}:/app/csv --name 2gis -p 127.0.0.1:8000:8000/tcp local/2gis:v1
```
{путь к папке csv с результатами расчета} - /C/Users/Mashk/PycharmProjects/2gis_ex/csv(пример)

#### Можно стянуть готовый images и запустить
```powershell
docker pull mashkovdm/2gis:v1 & docker run -v {путь к папке csv с результатами расчета}:/app/csv --name 2gis -p 127.0.0.1:8000:8000/tcp mashkovdm/2gis:v1
```
{путь к папке csv с результатами расчета} - /C/Users/Mashk/PycharmProjects/2gis_ex/csv(пример)
## График 
Данные о кол-ве рабочего времени в разрезе людей и времени доступен по [ссылке](http://127.0.0.1:8000/)
## CLI
Сформировать данные в файл 'sample.xml' по 7 людям в интервале дат '2020-01-01' - '2020-09-30'. 
После этого обновите страницу графика, данные обновятся.

```docker exec -it 2gis python func.py generate_fake_data --file_name='sample.xml' --unique_person_count=7 --start_date='2020-01-01' --end_date='2020-09-30'```

Рассчитать общее кол-во часов для каждого человека из списка names в интервале дат в интервале дат '2020-01-01' - '2020-09-30' 

```docker exec -it 2gis python func.py calc_work_time  --names=['Абаханум','Аанжелла','Абам'] --start_date='2020-01-01' --end_date='2020-09-30'```

 
