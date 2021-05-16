import asyncio
import time

# Мои
import KeyBoards
from State import NewProduce
from messages import MESSAGES
from MemberBase import PublicDirector
#
import aiogram
from aiogram import Bot, types
from aiogram.utils import executor, markdown
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


storage = MemoryStorage()
loop = asyncio.get_event_loop()
bot = Bot(token='')
dp = Dispatcher(bot, storage=storage, loop=loop)

PAYMENTS_PROVIDER_TOKEN = ''


@dp.message_handler(commands='start')
async def StartHandler(message: types.Message):
    await bot.send_message(message.from_user.id, MESSAGES['start'])


@dp.message_handler(commands='buy')
async def For_Sell(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['page'] = len(PublicDirector.DownloadProduces())-1
    await bot.send_message(message.chat.id, MESSAGES['main'], reply_markup=KeyBoards.next_list(data['page']))


@dp.callback_query_handler(lambda c: c.data == 'next')
async def NextList(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['page'] -= 9
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                        reply_markup=KeyBoards.next_list(data['page']))


@dp.callback_query_handler(lambda c: c.data == 'back')
async def NextList(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['page'] += 9
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                        reply_markup=KeyBoards.next_list(data['page']))


@dp.message_handler(commands='new')
async def Add_produce(message: types.Message):
    await NewProduce.name.set()
    await bot.send_message(message.chat.id, 'Введите название товара')


@dp.message_handler(state=NewProduce.name)
async def Add_produce_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await NewProduce.description.set()
    await bot.send_message(message.chat.id, 'Введите описание товара')


@dp.message_handler(state=NewProduce.description)
async def Add_produce_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await NewProduce.coast.set()
    await bot.send_message(message.chat.id, 'Введите цену товара в рублях')


@dp.message_handler(state=NewProduce.coast)
async def Add_produce_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['coast'] = int(message.text)*100
    await NewProduce.photo_url.set()
    await bot.send_message(message.chat.id, 'Пришлите ссылку на фото товара')


@dp.message_handler(state=NewProduce.photo_url)
async def Add_produce_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo_url'] = message.text
    await NewProduce.start_parameter.set()
    await bot.send_message(message.chat.id, 'Пришлите start_parameter товара')


@dp.message_handler(state=NewProduce.start_parameter)
async def Add_produce_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['start_parameter'] = message.text
    await NewProduce.payload.set()
    await bot.send_message(message.chat.id, 'Пришлите payload товара')


@dp.message_handler(state=NewProduce.payload)
async def Add_produce_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['payload'] = message.text
    PublicDirector().AddProduce(data['name'], data['description'], data['coast'],
                                data['photo_url'], data['start_parameter'], data['payload'])
    await bot.send_message(message.chat.id, 'Готово')
    await state.finish()


@dp.callback_query_handler()
async def ButtonPay(callback: types.CallbackQuery):
    # for handler inline_button, name button =  callback.data
    name = callback.data
    id, title, description, amount, photo_url, start_parameter, payload = PublicDirector.DownloadProduce(name)
    if amount > 200*100:
        amount = 100.01*100
    PRICE = types.LabeledPrice(label=title, amount=int(amount))
    await bot.send_invoice(callback.from_user.id,
                           title=title,
                           description=description,
                           provider_token=PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',
                           is_flexible=False,
                           photo_url=photo_url,
                           prices=[PRICE],
                           start_parameter=start_parameter,
                           payload=payload
                           )


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.message.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    print(message.from_user)
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    await bot.send_message(message.chat.id, 'suc')


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop)
