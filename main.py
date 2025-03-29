from telebot import TeleBot, types
from random import choice
import Mafia.db as db , time

bot = TeleBot('7873989281:AAHmUN2s0R5LVsoqIwoM_ots_js7CTXMurU')

game =False
group_id = None
night = False


def game_loop(message):
    global night , game
    bot.send_message(message.chat.id, 'Добро пожаловать в игру!\nЕсли вы мафия то испальзуете команду ')
    bot.send_message(message.chat.id, 'Игра начнеться через 20 секунд!')
    time.sleep(10)
    while True:
        if not night:
            bot.send_message(message.chat.id, 'Город засыпает! , Просыпаеться мафия!')
        else:
            bot.send_message(message.chat.id, 'Город просыпаеться! , Засыпает мафия !')
        db.clear_db(dead = False)
        if db.chec_winer() == 'mafia':
            bot.send_message(message.chat.id, 'Мафия победила!')
            game =False
            return
        elif db.chec_winer() == 'citizen':
            bot.send_message(message.chat.id, 'Челены победили!')
            game =False
            return

        night = not night
        alive_players = db.get_alive_players()
        fgfg = '\n'.join(alive_players)
        plaers =f'Живые игроки: \n{fgfg}'
        bot.send_message(message.chat.id,plaers)
        
        time.sleep(20)


@bot.message_handler(commands=['mafia'])
def mafia(message):
    if not game:
        global group_id
        group_id = message.chat.id
        db.new_game()
        bot.send_message(message.chat.id, 'Если Ты хочешь потерять друзей то намиши "готов" мне в лс')\
        
@bot.message_handler(func=lambda message: message.text == 'готов'and message.chat.type == 'private')
def ready(message):
    bot.send_message(group_id, f'{message.from_user.first_name} готов к игре!')
    bot.send_message(message.from_user.id, 'Ты в игре!')
    db.insert_player(message.from_user.id, message.from_user.first_name)
    

@bot.message_handler(commands=['play'])
def start_game(message):
    global game
    players_amount = db.players_amount()
    if players_amount >= 5 and not game:
        db.set_roles(players_amount)
        players_roles = db.get_players_roles()
        mafia_usernames = db.get_mafia_usernames()
        for player_id , role in players_roles:
            if player_id > 5:
                bot.send_message(player_id, f'Твоя роль {role}')
                if role =='mafia':
                    bot.send_message(player_id,f'Все челены мафии: \n {mafia_usernames}')
        game = True
        bot.send_message(message.chat.id, 'Игра началась!')
        db.clear_db(dead=True)
        game_loop(message)
        return
    bot.send_message(message.chat.id, 'Недостаточно игроков!  Добавляем ботов...')
    for i in range(5 - players_amount):
        bot_name = f'bot{i}'
        db.insert_player(i, bot_name)
        bot.send_message(group_id, f'Бот {bot_name} добавлен!')
    start_game(message)
    

@bot.message_handler(commands=['kill'])
def kill(message):
    username = message.text.replace('/kill ', '')
    alive_players = db.get_alive_players()
    mafia_usernames = db.get_mafia_usernames()
    if night and message.from_user.first_name in mafia_usernames:
        if not username in alive_players:
            bot.send_message(message.chat.id, 'Такого игрока нет!')
            return
        db.kill(username)


@bot.message_handler(commands=['kick'])
def kick(message):
    username = message.text.replace('/kill ', '')
    alive_players = db.get_alive_players()
    if not night:
        if not username in alive_players:
            bot.send_message(message.chat.id, 'Такого игрока нет!')
            return
        vote = db.vote('citizen_vote', username, message.from_user.id)
        if vote:
            bot.send_message(message.chat.id, 'Ваш голос учитан!')
            return
        bot.send_message(message.chat.id, 'Вы не можете голосовать!')
        return
    bot.send_message(message.chat.id, 'Сейчас ночь ты не можешь голосовать!')
    bot.polling(non_stop = True)


if __name__ == '__main__':
    bot.polling(non_stop = True) 
