def get_suggests(user_storage):
    if "suggests" in user_storage.keys():
        suggests = []
        for suggest in user_storage['suggests']:
            if type(suggest) != list:
                suggests.append({'title': suggest, 'hide': True})
            else:
                suggests.append({'title': suggest[0], "url": suggest[1], 'hide': False})
    else:
        suggests = []

    return suggests, user_storage


def IDontUnderstand(response, user_storage, answer):
    import random
    message = random.choice(answer)
    response.set_text(message)
    response.set_tts(message + "Доступные команды: {}.".format(" ,".join(user_storage['suggests'])))
    buttons, user_storage = get_suggests(user_storage)
    response.set_buttons(buttons)
    return response, user_storage


def read_answers_data(name):
    import json
    with open(name+".json", encoding="utf-8") as file:
        data = json.loads(file.read())
        return data


aliceAnswers = read_answers_data("data/answers_dict_example")


def get_mode(user_id, database):
    return database.get_entry("users_info", ['mode'], {'request_id': user_id})[0][0]


def update_mode(user_id, mode, database):
    database.update_entries('users_info', user_id, {'mode': mode}, update_type='rewrite')
    return True


def isequal(text, pattern):
    import synonyms
    return text.capitalize().strip('.,?!').replace('ё', 'е') in synonyms.synonyms[pattern]


def get_lasts(user_id, database):
    return database.get_entry("users_info", ['last_text'], {'request_id': user_id})[0][0],\
            database.get_entry("users_info", ['last_speech'], {'request_id': user_id})[0][0],\
            database.get_entry("users_info", ['last_buttons'], {'request_id': user_id})[0][0].split('#')

def hello():
    import random
    return random.choice(['Привет. Выбери игру.',
                          'Привет. Во что играем сегодня?',
                          'Привет. Я джала тебя. С чего начнем?'])