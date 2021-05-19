import telepot

token = '1469663159:AAGSXGfMgM0lSm1B4nl_l2UVgqHZl5ilk5M'
TelegramBot = telepot.Bot(token)
print(TelegramBot.getUpdates())
