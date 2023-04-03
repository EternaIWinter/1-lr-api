import requests
from time import sleep
menu = """\n    1 - Посмотреть описание игры 
    2 - Посмотреть требования к игре
    3 - Посмотреть цену на игру
    4 - Посмотреть из какой серии игра
    5 - Удалить игру
    6 - Добавить игру
    7 - Изменить описание игры
    8 - Выйти \n
            """
api_path = f'http://127.0.0.1:5000/games/'
exit_flag = True
while exit_flag:
    print(menu)
    try:
        menu_choiсe = int(input())
    except(Exception) as err:
        print(err)
    if menu_choiсe == 1:
        answer = requests.get(api_path+input("Введите название игры: "))
        try:
            print(answer.json()['descrip'])
        except:
            print(answer.json()['error'])
    elif menu_choiсe == 2:
        answer = requests.get(api_path+input("Введите название игры: "))
        try:
            print(f"ОЗУ - {answer.json()['RAM']}  Процессор - {answer.json()['Processor']}  Места на диске - {answer.json()['Hard_Disk']}")
        except:
            print(answer.json()['error'])
    elif menu_choiсe == 3:
        answer = requests.get(api_path+input("Введите название игры: "))
        try:
            print(answer.json()['Price'])
        except:
            print(answer.json()['error'])
    elif menu_choiсe == 4:
        answer = requests.get(api_path+input("Введите название игры: "))
        try:
            print(answer.json()['Series_name'])
        except:
            print(answer.json()['error'])
    elif menu_choiсe == 5:
        name = input("Введите название игры: ")
        answer = requests.delete(api_path+name)
        try:
            print(answer.json()['answer'])
        except:
            print(answer.json()['error'])
    elif menu_choiсe == 6:
        name = input("Введите название игры: ")
        ToSend = {'genre': input('Введите жанр игры: ')}
        answer = requests.post(api_path+name, json=ToSend)
        try:
            print(answer.json()['answer'])
        except:
            print(answer.json()['error'])
    elif menu_choiсe == 7:
        name = input("Введите название игры: ")
        ToSend = {'descrip': input('Введите новое описание игры: ')}
        answer = requests.put(api_path+name, json=ToSend)
        try:
            print(answer.json()['answer'])
        except:
            print(answer.json()['error'])
    if menu_choiсe == 8:
        exit_flag = False
        print('Удачи!')
        sleep(1)
    menu_choiсe = 0