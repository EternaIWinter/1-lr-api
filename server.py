from flask import Flask, request
from flask_restful import Api
import psycopg2
from psycopg2 import Error
app = Flask(__name__)
api = Api(app)
try:
    connection = psycopg2.connect(  user="postgres", 
                                    password="174QcT",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="game")
except (Exception, Error) as err:
    print("Ошибка при работе с PostgreSQL", err)

def get_game_id(name, flag_select = 0):
    if flag_select == 0:
        cursor = connection.cursor()
        cursor.execute(f'''SELECT "Game_Id" FROM public.name WHERE "name" = '{name}'; ''')
        Game_Id = cursor.fetchone()
        cursor.close()
        return Game_Id
    else:
        cursor = connection.cursor()
        cursor.execute(f'''SELECT "Game_Id" FROM public.name ORDER BY "Game_Id" DESC LIMIT 1; ''')
        Game_Id = cursor.fetchone()
        cursor.close()
        return Game_Id

def basics_delete(Game_Id, table_name):
    cursor = connection.cursor()
    cursor.execute(f'''DELETE FROM public.{table_name} WHERE "Game_Id"={int(Game_Id[0])};''')
    connection.commit()
    cursor.close()
    return 1

def basics_insert(insert_object, insert_value, table_name):
    cursor = connection.cursor()
    cursor.execute(f'''INSERT INTO public.{table_name} ({insert_object}) VALUES ({insert_value});''')
    connection.commit()
    cursor.close()
    return 1

def basics_select(Game_Id, select_object, table_name):
    cursor = connection.cursor()
    cursor.execute(f'SELECT {select_object} FROM public.{table_name} WHERE "Game_Id"={int(Game_Id[0])};')
    connection.commit()
    result = cursor.fetchone()
    cursor.close()
    return result
    
@app.route('/games/<name>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def api_perform(name):
    if request.method == 'GET':
        try:
            Game_Id = get_game_id(name)
            result = basics_select(Game_Id, 'description', 'description')
            result += basics_select(Game_Id, '"RAM", "Processor", "Hard_Disk"', '"System_Requirements"')
            result += basics_select(Game_Id, '"Price"', '"Price"')
            result += basics_select(Game_Id, '"Series_name"', '"Series"')
            return {'descrip': result[0], 'RAM': result[1], 'Processor': result[2], 'Hard_Disk': result[3], 'Price': result[4], 'Series_name': result[5]}
        except (Exception, Error) as err:
            print("Ошибка при работе с PostgreSQL", err)
            return {"error": str(err)}

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            Game_Id = get_game_id(name)
            cursor = connection.cursor()
            cursor.execute(f'''UPDATE public.description SET "description"='{data["descrip"]}' WHERE "Game_Id"={int(Game_Id[0])};''')
            connection.commit()
            cursor.close()
            return {'answer': 'Обновление успешно'}
        except (Exception, Error) as err:
            print("Ошибка при работе с PostgreSQL", err)
            return {"error": str(err)}

    elif request.method == 'DELETE':
        try:
            Game_Id = get_game_id(name)
            basics_delete(Game_Id, 'name')
            basics_delete(Game_Id, 'description')
            basics_delete(Game_Id, '"System_Requirements"')
            basics_delete(Game_Id, '"Series"')
            basics_delete(Game_Id, '"Price"')
            return {'answer': 'Удаление успешно'}
        except (Exception, Error) as err:
            print("Ошибка при работе с PostgreSQL", err)
            return {"error": str(err)}
        
    elif request.method == 'POST':
        try:
            data = request.get_json()
            Game_Id = get_game_id(name, 1)
            cursor = connection.cursor()
            basics_insert('"Game_Id", "name", "genre"', f"{int(Game_Id[0]) + 1}, '{name}', '{data['genre']}'", 'name')
            basics_insert('"Game_Id"', f"{int(Game_Id[0]) + 1}", 'description')
            basics_insert('"Game_Id"', f"{int(Game_Id[0]) + 1}", '"System_Requirements"')
            basics_insert('"Game_Id"', f"{int(Game_Id[0]) + 1}", '"Series"')
            cursor.execute(f'''SELECT "Id" FROM public."Price" ORDER BY "Game_Id" DESC LIMIT 1; ''')
            Id = cursor.fetchone()
            basics_insert('"Game_Id", "Id"', f"{int(Game_Id[0]) + 1}, {int(Id[0]) + 1}", '"Price"')
            cursor.close() 
            return {'answer': 'Добавление успешно'}
        except (Exception, Error) as err:
            print("Ошибка при работе с PostgreSQL", err)
            return {"error": str(err)}
if __name__ == '__main__':
    app.run(debug=True)