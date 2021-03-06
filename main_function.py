# coding: utf-8
from __future__ import unicode_literals
import little_fuctions
from card_template import *
silence = ' <speaker audio="dialogs-upload/a8485d59-e259-4a1d-b7d2-01f329fcc983/ad41fb6a-4909-4bd7-bc5c-1f855aa37209.opus">'


def message_return(response, user_storage, text, speech, buttons, mode, user_id, database):
    little_fuctions.update_mode(user_id, mode, database)
    text = text.replace('+', '')
    if not (text.endswith('.') or text.endswith('!') or text.endswith('?')):
        text += '.'
    response.set_text(text)
    response.set_tts(speech + silence*little_fuctions.get_silent(user_id, database))
    user_storage["suggests"] = buttons
    database.update_entries('users_info', user_id, {'last_buttons': '#'.join(buttons)}, update_type='rewrite')
    buttons, user_storage = little_fuctions.get_suggests(user_storage)
    if mode == "":
        user_storage["card"] = start_card(little_fuctions.get_color(user_id, database))
        user_storage["card"]["header"]["text"] = text
        response.set_card(user_storage["card"])
    elif mode == 'settings':
        user_storage["card"] = settings(little_fuctions.get_color(user_id, database), user_id, database)
        user_storage["card"]["header"]["text"] = text
        response.set_card(user_storage["card"])
    elif mode == "yesno>main":
        user_storage["card"] = yesno_card(little_fuctions.get_color(user_id, database), user_id, database)
        user_storage["card"]["header"]["text"] = text
        response.set_card(user_storage["card"])
    elif mode == "croco>main":
        user_storage["card"] = croco_card(little_fuctions.get_color(user_id, database))
        user_storage["card"]["header"]["text"] = text
        response.set_card(user_storage["card"])
    elif mode == "Inever>main":
        user_storage["card"] = inever_card(little_fuctions.get_color(user_id, database))
        user_storage["card"]["header"]["text"] = text
        response.set_card(user_storage["card"])
    elif mode == "croco>difficulty":
        user_storage["card"] = croco_diff_card(little_fuctions.get_color(user_id, database))
        user_storage["card"]["header"]["text"] = text
        response.set_card(user_storage["card"])
    else:
        response.set_buttons(buttons)
    database.update_entries('users_info', user_id, {'last_text': text}, update_type='rewrite')
    database.update_entries('users_info', user_id, {'last_speech': speech}, update_type='rewrite')
    return response, user_storage


def idk_return(response, user_storage, user_id, database, mode, comment = ''):
    last_text, last_speech, last_buttons = little_fuctions.get_lasts(user_id, database)
    if comment == 'again':
        text = last_text
        speech = last_speech
    elif comment:
        text = comment
        speech = comment
    else:
        text = little_fuctions.idk() + '\n\n{}'.format(last_text)
        speech = little_fuctions.idk() + '\n\n{}'.format(last_speech)
    buttons = last_buttons
    text = text.replace('+', '')
    response.set_text(text)
    response.set_tts(speech + silence  * little_fuctions.get_silent(user_id, database))
    user_storage["suggests"] = buttons
    buttons, user_storage = little_fuctions.get_suggests(user_storage)
    if mode == "":
        user_storage["card"] = start_card(little_fuctions.get_color(user_id, database))
        user_storage["card"]["header"]["text"] = text
        response.set_card(user_storage["card"])
    elif mode == 'settings':
        user_storage["card"] = settings(little_fuctions.get_color(user_id, database), user_id, database)
        user_storage["card"]["header"]["text"] = text
        response.set_card(user_storage["card"])
    elif mode == "yesno>main":
        user_storage["card"] = yesno_card(little_fuctions.get_color(user_id, database), user_id, database)
        response.set_card(user_storage["card"])
    elif mode == "croco>main":
        user_storage["card"] = croco_card(little_fuctions.get_color(user_id, database))
        user_storage["card"]["header"]["text"] = text
        response.set_card(user_storage["card"])
    elif mode == "Inever>main":
        user_storage["card"] = inever_card(little_fuctions.get_color(user_id, database))
        user_storage["card"]["header"]["text"] = text
        response.set_card(user_storage["card"])
    elif mode == "croco>difficulty":
        user_storage["card"] = croco_diff_card(little_fuctions.get_color(user_id, database))
        user_storage["card"]["header"]["text"] = text
        response.set_card(user_storage["card"])
    else:
        response.set_buttons(buttons)
    return response, user_storage


def handle_dialog(request, response, user_storage, database):
    if not database.get_entry("users_info", ['new'], {'request_id': request.user_id}):
        database.add_entries("users_info", {"request_id": request.user_id})
    if not user_storage:
        user_storage = {"suggests": []}
    if "command" in request.request.keys():
        input = request.command
    else:
        input = request.payload
    user_id = request.user_id
    is_first_time = request.is_new_session
    if is_first_time:
        text = 'Вас приветствует Игротека - спутник дружеских компаний. Надеюсь, мы с вами поладим. ' \
               'Выберите игру - и мы начнем.'
        speech = text
        mode = ''
        buttons = []
        return message_return(response, user_storage, text, speech, buttons, mode, user_id, database)
    else:
        mode = little_fuctions.get_mode(user_id, database)

    if little_fuctions.isequal(input, 'В начало'):
        mode = ''
        input = ''

    games = ['Данетки', 'Я никогда не', 'Крокодил']

    if little_fuctions.isequal(input, 'Помощь'):
        text = 'В этом навыке все просто! Выбери игру и скажи "начать". ' \
               'Правила ты сможешь посмотреть в меню игры. Желаю хорошо провести время!'
        speech = text
        buttons = games[:]
        mode = ''
        return message_return(response, user_storage, text, speech, buttons, mode, user_id, database)
    elif little_fuctions.isequal(input, 'Еще раз'):
        return idk_return(response, user_storage, user_id, database, mode, 'again')
    elif mode.startswith('yesno') or (mode == '' and little_fuctions.isequal(input, 'Данетки')):
        import yes_no_puzzle
        succes = yes_no_puzzle.start(input, user_id, database)
        if succes:
            return message_return(response, user_storage, *succes, user_id, database)
        else:
            return idk_return(response, user_storage, user_id, database, mode)
    elif mode.startswith('Inever') or (mode == '' and little_fuctions.isequal(input, 'Я никогда не')):
        import I_have_never_ever
        succes = I_have_never_ever.start(input, user_id, database)
        if succes:
            return message_return(response, user_storage, *succes, user_id, database)
        else:
            return idk_return(response, user_storage, user_id, database, mode)
    elif mode.startswith('croco') or (mode == '' and little_fuctions.isequal(input, 'Крокодил')):
        import croco
        succes = croco.start(input, user_id, database)
        if succes:
            return message_return(response, user_storage, *succes, user_id, database)
        else:
            return idk_return(response, user_storage, user_id, database, mode)
    elif mode == 'settings' and little_fuctions.isequal(input, 'Сменить цвета'):
        little_fuctions.update_color(little_fuctions.get_color(user_id, database) + 1, user_id, database)
        if (little_fuctions.get_color(user_id, database) + default_color) % colors in blocked_colors:
            little_fuctions.update_color(little_fuctions.get_color(user_id, database) + 1, user_id, database)
        text = little_fuctions.go_color()
        speech = text
        mode = 'settings'
        buttons = []
        return message_return(response, user_storage, text, speech, buttons, mode, user_id, database)
    elif mode == 'settings' and little_fuctions.isequal(input, 'Тихий режим'):
        little_fuctions.update_silent(1 - little_fuctions.get_silent(user_id, database), user_id, database)
        return idk_return(response, user_storage, user_id, database, mode, 'Поняла вас, Сэр!')
    elif (mode == '' and little_fuctions.isequal(input, 'Настройки')) or mode == 'settings':
        mode = 'settings'
        text = little_fuctions.go_settings()
        speech = text
        buttons = []
        return message_return(response, user_storage, text, speech, buttons, mode, user_id, database)
    elif mode == '' and little_fuctions.isequal(input, 'Другая игра'):
        import other_games, random
        mode = ''
        used = little_fuctions.get_set(user_id, database)
        if len(used) == len(other_games.data):
            used = set()
        mediator = set(other_games.data).difference(used)
        text = random.choice(list(mediator))
        used.add(text)
        little_fuctions.update_set(used, user_id, database)
        speech = text
        buttons = []
        return message_return(response, user_storage, text, speech, buttons, mode, user_id, database)
    elif mode == '':
        text = little_fuctions.hello()
        speech = text
        mode = ''
        buttons = []
        little_fuctions.update_set(set(), user_id, database)
        return message_return(response, user_storage, text, speech, buttons, mode, user_id, database)
    else:
        return idk_return(response, user_storage, user_id, database, mode)
