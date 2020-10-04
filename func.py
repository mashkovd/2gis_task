import xml.etree.cElementTree as ET
import fire
import pandas as pd
import random
from datetime import datetime
import xmlschema

RESULT_FILE_NAME = './csv/result.csv'


def generate_fake_data(file_name='sample.xml', start_date='2020-01-01', end_date='2020-09-30', unique_person_count=12):
    """
    Функция формирует тестовые данные, необходимые для расчета рабочего времени
    в разрезе людей и времени

    Args:
        file_name: название файла
        start_date (``str``): начальная дата формирования данных
        end_date (``str``): конечная дата формирования данных
        unique_person_count (``int``): кол-во уникальных имен/идентификаторов
    Returns:

        файл c названием file_name в формате xml
    """
    tree = ET.parse('russian_names.xml')
    root = tree.getroot()
    names = root[1].findall('Surnames/russian_names/Name')

    people = ET.Element('people')

    for name in names[:unique_person_count]:
        for time in pd.date_range(start_date, end_date, freq='B'):
            person = ET.Element('person')
            person.set('full_name', name.text)
            start = ET.Element('start')
            end = ET.Element('end')
            start.text = time.replace(hour=random.randint(7, 11),
                                      minute=random.randint(0, 59),
                                      second=random.randint(0, 59),
                                      ).strftime("%d-%m-%Y %H:%M:%S")
            end.text = time.replace(hour=random.randint(15, 19),
                                    minute=random.randint(0, 59),
                                    second=random.randint(0, 59),
                                    ).strftime("%d-%m-%Y %H:%M:%S")

            person.append(start)
            person.append(end)
            people.append(person)

    tree = ET.ElementTree(people)
    tree.write(file_name, encoding='utf-8', xml_declaration=True)


def get_data_per_person(file_name='sample.xml', start_date='2020-01-01', end_date='2020-09-30',
                        names=None, ):
    """

    Args:
        file_name (``str``): название файла
        start_date (`str`):  начальная дата для выборки
        end_date (`str`): конечная дата для выборки
        names (`list`): список имен/идентификаторов

    Returns:
        (``pd.DataFrame``, mess): DataFrame c расчетными данными

    """

    mess = ''
    sample_schema = xmlschema.XMLSchema('sample.xsd')
    # TODO Ресурсоемкая операция. Требуется уточнить необходимость проверки xml на валидность
    # if not sample_schema.is_valid(file_name):
    #     mess = 'Некорректный формат xml'

    start_date_from = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_to = datetime.strptime(end_date, "%Y-%m-%d").date()
    data_per_person = []
    data_start_end_time = {}
    for event, elem in ET.iterparse(file_name):

        if elem.tag in ('start', 'end'):
            # TODO Попробовать поискать варианты без вызова функции strptime
            time_from_text = datetime.strptime(elem.text, '%d-%m-%Y %H:%M:%S').date()
            if start_date_from <= time_from_text <= end_date_to:
                data_start_end_time.update({elem.tag: datetime.strptime(elem.text, '%d-%m-%Y %H:%M:%S')})

        elif elem.tag == 'person' and data_start_end_time and (
                names and elem.attrib.get('full_name') in names or names is None):
            work_time = data_start_end_time.get('end') - data_start_end_time.get('start')
            data_per_person.append({'work_time': work_time.seconds,
                                    'date': data_start_end_time.get('end').date(),
                                    'full_name': f"{elem.attrib.get('full_name')}"
                                    }
                                   )
            data_start_end_time = {}
        elem.clear()

    df_grouped = pd.DataFrame()
    if data_per_person:
        df = pd.DataFrame(data_per_person)
        df_grouped = df.groupby(['full_name']).sum()
        df_grouped['work_time'] = round(df_grouped['work_time'] / 3600, 2)

    return df_grouped, mess


def calc_work_time(file_name='sample.xml', start_date='2020-01-01', end_date='2020-09-30',
                   names=None, ):
    f"""

    Args:
        file_name (``str``): название файла
        start_date (`str`):  начальная дата для выборки
        end_date (`str`): конечная дата для выборки
        names (`list`): список имен/идентификаторов

    Returns:

        Формирует файл result.csv с результатом расчета общего времени пребывания людей из списка {names}
        в интервале дат {start_date} и {end_date} из файла {calc_work_time}
        
    """
    df, _ = get_data_per_person(file_name=file_name,
                                start_date=start_date,
                                end_date=end_date, names=names)

    df.loc['Итого'] = df['work_time'].sum()
    print(f'{df.tail(10)}\n'
          f'В файле {RESULT_FILE_NAME} результаты расчета')
    df.to_csv(RESULT_FILE_NAME)


if __name__ == '__main__':
    fire.Fire()
