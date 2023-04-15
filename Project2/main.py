import telebot
import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote
from bs4 import BeautifulSoup

# Initialize Telebot with your Telegram Bot API token
bot = telebot.TeleBot('5667223037:AAGapBv_L-CSsev4vvQrrCV4uqYbMKx6b-Y')


def search_and_send(query, chat_id):
    # Build the Google search URL
    url = f'https://www.google.com/search?q={query}&gl=us&hl=en'
    # Make the HTTP request to the Google search page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    req = Request(url, headers=headers)
    response = urlopen(req)

    # Parse the HTML response and retrieve the first 3 results
    soup = BeautifulSoup(response, 'html.parser')
    #results = [a['href'][7:] for a in soup.find_all('a', href=True) if a['href'].startswith('/url?q=')][:3]
    results = [result.get('href') for result in soup.select('.yuRUbf a')[:3]]
    print(results)
    # Send the results to the user via Telegram
    for result in results:
        bot.send_message(chat_id, result)

    # Save the results to a JSON file
    with open('search_results.json', 'a') as f:
        json.dump({query: results}, f)


# Handle incoming messages from Telegram
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hello! Please enter what you would like to search.')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    chat_id = message.chat.id

    # Search Google and send the results
    search_and_send(user_input, chat_id)


# Start the bot
bot.polling()
