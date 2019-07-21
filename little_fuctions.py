def get_suggests(user_storage):
    if "suggests" in user_storage.keys():
        suggests = []
        for suggest in user_storage['suggests']:
            if type(suggest) != list:
                suggests.append({'title': suggest, 'hide': True})
            else:
                print(suggest)
                suggests.append({'title': suggest[0], "url": suggest[1], 'hide': False})
                print(suggests)
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


def get_mode(id, database):
    return database.get_entry("users_info", ['mode'], {'request_id': id})[0][0]


def update_mode(id, mode, database):
    database.update_entries('users_info', id, {'mode': mode}, update_type='rewrite')
    return True


def hello(id, database):
    from random import choice
    return choice(aliceAnswers["helloTextVariations"]["gender"]).format("Имя")