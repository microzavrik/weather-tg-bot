import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram import executor

API_TOKEN = '6702812875:AAHqBs3I7lVqR6qMQYH-LQWogdb2cfXjXoM'
OWM_API_KEY = '3d7b2005a8bd8e2fd677621b86b451e0'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.answer("Welcome to the Weather Bot! Please enter the name of a city to get its weather information.")


@dp.message_handler()
async def get_weather(message: types.Message):
    city = message.text
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        detailed_info = f"🌍 Weather in {city} 🌦️\n"
        
        if "/summary" in message.text:
            detailed_info += f"Temperature: {data['main']['temp']} °C\n" \
                             f"Description: {data['weather'][0]['description']}"
        else:
            detailed_info += f"Temperature: {data['main']['temp']} °C\n" \
                             f"Feels like: {data['main']['feels_like']} °C\n" \
                             f"Humidity: {data['main']['humidity']}%\n" \
                             f"Pressure: {data['main']['pressure']} hPa\n" \
                             f"Description: {data['weather'][0]['description']}"

        await message.answer(detailed_info, parse_mode=ParseMode.HTML)
        
    else:
        await message.answer("City not found. Please enter a valid city name.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)