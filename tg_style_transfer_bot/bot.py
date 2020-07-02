import styletransfer
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token='609613235:AAFI7eyxr9scD933I30fq6shWhOHwr6596Q')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nЯ бот, который может переносить стиль с одной картинки на другую! Для более подробной информации напиши /help")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('''Для работы необходимо отправить две картинки:\n1. Картинка контент (ее будем обрабатывать). При отправке обязательно сделать подпись content\n2. Картинка стиль (с нее переносим стиль). При отправке обязательно сделать подпись style\n3. После отправки двух картинок пишем /go для начала работы\n Для корректной работы рекомендуется выбирать картинки, где действительно есть какой-то особый стиль.\nНапример, картины художников''')


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def process_photo_command(message: types.Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    src = 'image_' + message.caption +'.jpg'
    await bot.download_file(file_path, src)


@dp.message_handler(commands=['go'])
async def send_styled_photo_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Бот начал обработку картинок, среднее время ожидания: 5-10 минут.")
    content_img = await styletransfer.image_loader("image_content.jpg")
    style_img = await styletransfer.image_loader("image_style.jpg")
    output = styletransfer.StyleTransfer(content_img, style_img, content_img.clone()).run_style_transfer()
    await styletransfer.save_img('output.png', output)
    await bot.send_photo(message.from_user.id, open('output.png', 'rb'),
                         reply_to_message_id=message.message_id)



@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)
