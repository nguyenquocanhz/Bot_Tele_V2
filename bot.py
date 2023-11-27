import telebot
import requests
import json
import logging
from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(bot_token, threaded=False)

url = {

    'replace': 'https://shopkcff.com/js/plugin/js/1.php',
    'view' : 'https://shopkcff.com/js/plugin/js/1.php?act=view'
}
replace = url['replace']
view = url['view']

params = {
    'partner_id': '2761789661',
    'partner_key': '7ff3c5fee070a37d12b26f838fb35261'
}

params1 = {
    'partner_id': '29786780548',
    'partner_key': '31582b01caee025e87d56701111ee07f'
}


logging.basicConfig(
    level=logging.INFO,
    filename='bot.log',
    format='%(asctime)s [%(levelname)s] %(message)s'
)

@bot.message_handler(commands=['id', 'view', 'view1', 'shopkcff_3', 'shopkcff_4', 'napthe5giay_3', 'napthe5giay_4'])
def handle_command(message):
    command = message.text.split('/')[1]

    if command in ['shopkcff_3', 'shopkcff_4']:
        if command == 'shopkcff_4':
            response = requests.get(replace, params=params1)
        else:
            response = requests.get(replace, params=params)
        response_content = response.json()

    elif command == 'view':
        response = requests.get(view)
        response_content = response.json()
        
    elif command == 'id':
        bot.reply_to(message, f"Chat ID của bạn là: {message.chat.id}")
        return

    else:
        bot.reply_to(message, 'Lệnh không hợp lệ.')
        return

    if response_content['status'] == 'success':
        response_message = f"{response_content['message']}\npartner_id: {response_content['partner_id']}\npartner_key: {response_content['partner_key']}" + "\n"
    else:
        response_message = response_content['message']

    with open('response.txt', 'a') as file:
        file.write(json.dumps(response_content))

    bot.reply_to(message, response_message)
    logging.info(f"Command '{command}' processed successfully.")

def main():
    print('Bot đang chạy.....')
    bot.infinity_polling()  # Sử dụng infinity_polling() thay cho polling() để sử dụng mô hình long polling

if __name__ == '__main__':
    while True:
        command = input("Nhập lệnh (start/stop/restart): ")
        if command == 'start':
            logging.info('Bot running.')
            main()
            print('Bot đang chạy.....')
            while True:
                update = bot.get_updates()[-1]  # Lấy thông báo mới nhất
                bot.process_new_messages([update])  # Xử lý thông báo
                command = input("Nhập lệnh (start/stop/restart): ")
                if command == 'stop':
                    bot.stop_polling()
                    break
                elif command == 'restart':
                    bot.stop_polling()
                    main()
                    print('Bot đang chạy.....')
        elif command == 'stop':
            bot.stop_polling()
            break
        elif command == 'restart':
            bot.stop_polling()
            main()
            print('Bot đang chạy.....')
            
        else:
            print('Lệnh không hợp lệ. Vui lòng thử lại.')

    # Dòng mã dưới đây sẽ được thực thi khi bot dừng chạy
    print('Bot đã dừng.')
    logging.info('Bot đã dừng chạy.')
    input('Nhấn Enter để thoát.')




