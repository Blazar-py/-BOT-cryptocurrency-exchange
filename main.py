import re
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from bs4 import BeautifulSoup as BS

bot = Bot(token="TOKEN_FROM_BOTFATHER", parse_mode='HTML')
admin_id = 1512300383

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserInformation(StatesGroup):
    user_give = State()
    user_take = State()
    user_count_give = State()
    user_count_take = State()
    user_wallet = State()
    wait = State()
    izm_wallet = State()
    reklama_send = State()
    procent = State()
    wait_add = State()
    wait_add_wallet = State()


database = open("users_id.txt", "r", encoding="utf-8")
datausers = set()
for line in database:
    datausers.add(line.strip())
database.close()

bitcoin_wallet = 'btc111'
ethereum_wallet = 'eth222'
tether_wallet = 'tether333'
toncoin_wallet = 'toncoin444'
solana_wallet = 'solonaaaa'
dogecoin_wallet = 'dog'

procent = 0


other1 = 'dogecoin'
other2 = 'solana'
other3 = 'NONE'
other4 = 'NONE'
other5 = 'NONE'
other6 = 'NONE'
other7 = 'NONE'
other8 = 'NONE'
other9 = 'NONE'


keyboard_main_ru = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1_ru = types.KeyboardButton(text="Exchange Rates")
button2_ru = types.KeyboardButton(text="Exchange")
button3_ru = types.KeyboardButton(text="Support")
keyboard_main_ru.add(button1_ru, button2_ru, button3_ru)

keyboard_cancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_cancel = types.KeyboardButton(text="🔺 Cancel 🔺")
keyboard_cancel.add(button_cancel)

crypto = ['bitcoin', 'ethereum', 'tether', 'toncoin', 'solana', 'dogecoin']


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    file = open('users_id.txt', 'r')
    text = file.read()
    if not str(message.from_user.id) in text:
        all_id = open("users_id.txt", "a", encoding="utf-8")
        all_id.write(str(f"{message.from_user.id}\n"))
        datausers.add(message.from_user.id)
        inlinekeyboard_lang = types.InlineKeyboardMarkup()
        inlinekeyboard_lang.add(types.InlineKeyboardButton(text="🇬🇧 English", callback_data="ru_start"))
        await message.answer(f'Hello {message.from_user.username}! For working with changer bot select your language.', reply_markup=inlinekeyboard_lang)
    else:
        await message.answer(f'Hello again!', reply_markup=keyboard_main_ru)
        

@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if message.from_user.id == admin_id:
        inlinekeyboard_admin = types.InlineKeyboardMarkup()
        inlinekeyboard_admin.add(types.InlineKeyboardButton(text="Редактировать наценку", callback_data="redakt_nacenka"))
        inlinekeyboard_admin.add(types.InlineKeyboardButton(text="Добавить крипту", callback_data="add_crypto"))
        inlinekeyboard_admin.add(types.InlineKeyboardButton(text="Редактировать наши кошельки", callback_data="izm_wallet"))
        inlinekeyboard_admin.add(types.InlineKeyboardButton(text="Отправить рассылку", callback_data="reklama"))
        inlinekeyboard_admin.add(types.InlineKeyboardButton(text="Выйти из админ панели", callback_data="exit_adm"))
        await message.answer('Вы вошли в админ панель', reply_markup=inlinekeyboard_admin)


@dp.callback_query_handler(text="ru_start")
async def send(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer('The language was successfully selected\nTo work with the currency exchanger, use the buttons', reply_markup=keyboard_main_ru)


@dp.message_handler(content_types=['text'])
async def message(message: types.Message):
    if message.text == 'Exchange Rates':
        msg = f'<b>Exchange Rates:</b>\n\n'
        for i in crypto:
            r = requests.get(f"https://coinmarketcap.com/currencies/{i}/")
            html = BS(r.content, 'html.parser')
            price = html.find("div", class_="priceValue").text
            price2 = float(re.sub("[$,]", "", price))
            msg += f'{i} - {price2}$\n'
        await message.answer(msg)
    elif message.text == 'Support':
        await message.answer('Support: @BlazarPython')
    elif message.text == 'Exchange':
        msg = f'<b>Exchange Rates:</b>\n\n'
        for i in crypto:
            r = requests.get(f"https://coinmarketcap.com/currencies/{i}/")
            html = BS(r.content, 'html.parser')
            price = html.find("div", class_="priceValue").text
            price2 = float(re.sub("[$,]", "", price))
            msg += f'{i} - {price2}$\n'
        msg += '\nSelect the cryptocurrency you want to <u>give away</u>:'
        inlinekeyboard_give = types.InlineKeyboardMarkup()
        inlinekeyboard_give.add(types.InlineKeyboardButton(text="Bitcoin", callback_data="bitcoin_give"))
        inlinekeyboard_give.add(types.InlineKeyboardButton(text="Ethereum", callback_data="ethereum_give"))
        inlinekeyboard_give.add(types.InlineKeyboardButton(text="tether", callback_data="tether_give"))
        inlinekeyboard_give.add(types.InlineKeyboardButton(text="Toncoin", callback_data="toncoin_give"))
        for i in range(1, 9):
            name = globals().get(f"other{i}")
            if name != 'NONE':
                inlinekeyboard_give.add(types.InlineKeyboardButton(text=f'{name}', callback_data=f'{name}_give'))
        await message.answer(msg, reply_markup=inlinekeyboard_give)
    else:
        await message.answer('Your request is not clear')


@dp.callback_query_handler(regexp=r'^\w+_give')
async def send(call: types.CallbackQuery, state: FSMContext, regexp):
    await call.answer()
    await call.message.delete()
    name = regexp.group()[:-5]
    await state.update_data(user_give=f'{name}')
    inlinekeyboard_give = types.InlineKeyboardMarkup()
    inlinekeyboard_give.add(types.InlineKeyboardButton(text="Bitcoin", callback_data="bitcoin_takes"))
    inlinekeyboard_give.add(types.InlineKeyboardButton(text="Ethereum", callback_data="ethereum_takes"))
    inlinekeyboard_give.add(types.InlineKeyboardButton(text="tether", callback_data="tether_takes"))
    inlinekeyboard_give.add(types.InlineKeyboardButton(text="Toncoin", callback_data="toncoin_takes"))
    for i in range(1, 9):
        name2 = globals().get(f"other{i}")
        if name2 != 'NONE' and name2 != name:
            inlinekeyboard_give.add(types.InlineKeyboardButton(text=f'{name2}', callback_data=f'{name2}_takes'))
    await call.message.answer(f'You give away: <b>{name}</b>\nNow choose which currency you want to <u>receive</u>:', reply_markup=inlinekeyboard_give)


@dp.callback_query_handler(regexp=r'^\w+_takes')
async def send(call: types.CallbackQuery, state: FSMContext, regexp):
    await call.answer()
    await call.message.delete()
    name = regexp.group()[:-6]
    await state.update_data(user_take=f'{name}')
    data = await state.get_data()
    await call.message.answer(f'You make an exchange:\n<b>{data["user_give"]}</b> ➡ <b>{data["user_take"]}</b> .\n\n'
                              f'Now enter the amount you want to pay (in {data["user_give"]})', reply_markup=keyboard_cancel)
    await UserInformation.user_count_give.set()


@dp.message_handler(state=UserInformation.user_count_give)
async def send_count(message: types.Message, state: FSMContext):
    if message.text == '🔺 Cancel 🔺':
        await state.finish()
        await message.answer('Operation canceled', reply_markup=keyboard_main_ru)
    else:
        s = float(message.text)
        if 0 < s <= 10000000000:
            await state.update_data(user_count_give=message.text)
            data = await state.get_data()
            r = requests.get(f"https://coinmarketcap.com/currencies/{data['user_give']}/")
            html = BS(r.content, 'html.parser')
            price = html.find("div", class_="priceValue").text
            give = float(re.sub("[$,]", "", price))
            r2 = requests.get(f"https://coinmarketcap.com/currencies/{data['user_take']}/")
            html2 = BS(r2.content, 'html.parser')
            price2 = html2.find("div", class_="priceValue").text
            take = float(re.sub("[$,]", "", price2))
            count = float(data['user_count_give'])
            itog = give * count / take
            itog2 = itog - (itog * (procent / 100))
            await state.update_data(user_count_take=itog2)
            await message.answer(f'Are you going to exchange {data["user_give"]}: [ {data["user_count_give"]} ] for {data["user_take"]}: [ {itog2} ]\n\n'
                                 f'Now we need <u>your</u> wallet<b> {data["user_take"]}</b>\nPlease enter it:')
            await UserInformation.user_wallet.set()
        else:
            await message.answer('Minimum: 0\nMaximum: 10000000000')


@dp.message_handler(state=UserInformation.user_wallet)
async def send_wallet(message: types.Message, state: FSMContext):
    global wallet
    if message.text == '🔺 Cancel 🔺':
        await state.finish()
        await message.answer('Operation canceled', reply_markup=keyboard_main_ru)
    else:
        if len(message.text) > 10:
            await state.update_data(user_wallet=message.text)
            data = await state.get_data()
            give = data['user_give']
            wallet = globals().get(f"{give}_wallet")
            keyboard_check = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1_check = types.KeyboardButton(text="Paid")
            button2_check = types.KeyboardButton(text="Cancel")
            keyboard_check.add(button1_check, button2_check)
            await message.answer(f'<b>Success!</b>\n\nLets double-check everything:\n\n'
                                 f'1. You transfer [ {data["user_count_give"]} ] {data["user_give"]} to wallet <code>{wallet}</code>\n'
                                 f'2. We transfer to you [ {data["user_count_take"]} ] {data["user_take"]} to your wallet: <code>{data["user_wallet"]}</code>'
                                 f'\n\nMake sure that everything is correct, fulfill the conditions and click the "Paid".', reply_markup=keyboard_check)
            await UserInformation.wait.set()
        else:
            await message.answer('Error!\nYou entered your wallet incorrectly!\nRepeat:')

        @dp.message_handler(state=UserInformation.wait)
        async def wait(message: types.Message, state: FSMContext):
            if message.text == 'Cancel':
                await state.finish()
                await message.answer('The operation has been cancelled.', reply_markup=keyboard_main_ru)
            elif message.text == 'Paid':
                data = await state.get_data()
                inlinekeyboard_proverka = types.InlineKeyboardMarkup()
                inlinekeyboard_proverka.add(types.InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"okey_{message.from_user.id}"))
                inlinekeyboard_proverka.add(types.InlineKeyboardButton(text="⛔ Удалить", callback_data=f"delete_{message.from_user.id}"))
                await message.answer('Excellent!\nWait for confirmation from the administration.\n\nYou will receive a notification in this bot.', reply_markup=keyboard_main_ru)
                await bot.send_message(admin_id, f'<b>‼ Новая заявка на обмен ‼</b>\n\n'
                                                 f'             <b>{data["user_give"]}</b> ➡ <b>{data["user_take"]}</b>\n'
                                                 f'Пользователь: {message.from_user.username} (id: <code>{message.from_user.id}</code> )\n\n'
                                                 f'Данные: {message.from_user.username} должен был перевести [ {data["user_count_give"]} ] {data["user_give"]} '
                                                 f'на наш кошелёк: <code>{wallet}</code>\n\n'
                                                 f'Если всё верно, то переведите [ {data["user_count_take"]} ] {data["user_take"]} на его кошелёк: '
                                                 f'<code>{data["user_wallet"]}</code>', reply_markup=inlinekeyboard_proverka)
                await state.finish()


@dp.callback_query_handler(regexp=r'^okey_\d+')
async def send(call: types.CallbackQuery, regexp):
    await call.answer()
    await call.message.delete()
    id_usera = (regexp.group())[5:]
    await bot.send_message(id_usera, f'⚠ You were approved in the last exchange ✅\n\nIf the crypto was not received - contact support')


@dp.callback_query_handler(regexp=r'^delete_\d+')
async def send(call: types.CallbackQuery, regexp):
    await call.answer()
    await call.message.delete()
    id_usera = (regexp.group())[7:]
    await bot.send_message(id_usera, f'⚠ Sorry, but your last exchange was denied ⚠')
    
#============================= АДМИНКА
@dp.callback_query_handler(text="back_admin")
async def send(call: types.CallbackQuery):
    if call.from_user.id == admin_id:
        await call.answer()
        await call.message.delete()
        inlinekeyboard_admin = types.InlineKeyboardMarkup()
        inlinekeyboard_admin.add(types.InlineKeyboardButton(text="Редактировать наценку", callback_data="redakt_nacenka"))
        inlinekeyboard_admin.add(types.InlineKeyboardButton(text="Добавить крипту", callback_data="add_crypto"))
        inlinekeyboard_admin.add(types.InlineKeyboardButton(text="Редактировать наши кошельки", callback_data="izm_wallet"))
        inlinekeyboard_admin.add(types.InlineKeyboardButton(text="Отправить рассылку", callback_data="reklama"))
        inlinekeyboard_admin.add(types.InlineKeyboardButton(text="Изменить текста бота", callback_data='text_edit'))
        inlinekeyboard_admin.add(types.InlineKeyboardButton(text="Выйти из админ панели", callback_data="exit_adm"))
        await call.message.answer('Вы вернулись в админ-панель', reply_markup=inlinekeyboard_admin)


@dp.callback_query_handler(text="exit_adm")
async def send(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()


@dp.callback_query_handler(text="redakt_nacenka")
async def send(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()
    inlinekeyboard_nacenka = types.InlineKeyboardMarkup()
    inlinekeyboard_nacenka.add(types.InlineKeyboardButton(text="Процентная наценка", callback_data='procent'))
    inlinekeyboard_nacenka.add(types.InlineKeyboardButton(text="Назад в админ-панель", callback_data='back_admin'))
    await call.message.answer(f'Сейчас наценка:\n\nПроцентная: {procent}%\n\nВыберите способ наценки:', reply_markup=inlinekeyboard_nacenka)
    @dp.callback_query_handler(text="procent")
    async def send(call: types.CallbackQuery):
        await call.answer()
        await call.message.delete()
        await call.message.answer('Введите процент наценки числом\nНапример: "5" - наценка на 5%\n"0.5" - наценка на 0.5%:')
        await UserInformation.procent.set()
        @dp.message_handler(state=UserInformation.procent)
        async def wait(message: types.Message, state: FSMContext):
            global procent
            try:
                s = float(message.text)
                procent = s
                inlinekeyboard_back = types.InlineKeyboardMarkup()
                inlinekeyboard_back.add(types.InlineKeyboardButton(text="Назад в админ-панель", callback_data='back_admin'))
                await message.answer(f'<b>Успешно!</b>\nПроцентная наценка в: {s}%',reply_markup=inlinekeyboard_back)
                await state.finish()
            except:
                await message.answer('Неверно введено число!\nПопробуйте снова:')

                
@dp.callback_query_handler(text="izm_wallet")
async def send(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()
    inlinekeyboard_wallet = types.InlineKeyboardMarkup()
    for i in crypto:
        inlinekeyboard_wallet.add(types.InlineKeyboardButton(text=f"{i}", callback_data=f'{i}_editwlt'))
    inlinekeyboard_wallet.add(types.InlineKeyboardButton(text="Назад в админ-панель", callback_data='back_admin'))
    await call.message.answer('Выберите для какой криптовалюты изменить кошелёк:', reply_markup=inlinekeyboard_wallet)
    @dp.callback_query_handler(regexp=r'^\w+_editwlt')
    async def send(call: types.CallbackQuery, regexp):
        global name_izmen
        await call.answer()
        await call.message.delete()
        name_izmen = regexp.group()[:-8]
        await call.message.answer(f'Вы выбрали: {name_izmen}.\nТеперь введите ваш новый кошелек для принятия этой валюты:')
        await UserInformation.izm_wallet.set()
        @dp.message_handler(state=UserInformation.izm_wallet)
        async def wait(message: types.Message, state: FSMContext):
            inlinekeyboard_back = types.InlineKeyboardMarkup()
            inlinekeyboard_back.add(types.InlineKeyboardButton(text="Назад в админ-панель", callback_data='back_admin'))
            var = {f'{name_izmen}_wallet': message.text}
            globals().update(var)
            await message.answer('Успешно!', reply_markup=inlinekeyboard_back)
            await state.finish()


@dp.callback_query_handler(text='reklama')
async def send(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer('Введите текст, который получат все пользователи бота:')
    await UserInformation.reklama_send.set()
    @dp.message_handler(state=UserInformation.reklama_send)
    async def reklama(message: types.Message, state: FSMContext):
        global reklama_sendes631
        inlinekeyboard_reklama = types.InlineKeyboardMarkup()
        inlinekeyboard_reklama.add(types.InlineKeyboardButton(text="❌ Нет, не отправлять", callback_data="back_admin"))
        inlinekeyboard_reklama.add(types.InlineKeyboardButton(text="✅ Да, отправляем", callback_data="confirm_reklama"))
        reklama_sendes631 = message.text
        await message.answer(f'Вы уверены что желаете отправить данное сообщение:\n\n{message.text}', reply_markup=inlinekeyboard_reklama)
        await state.finish()
    @dp.callback_query_handler(text='confirm_reklama')
    async def send(call: types.CallbackQuery):
        await call.answer()
        await call.message.delete()
        inlinekeyboard_back = types.InlineKeyboardMarkup()
        inlinekeyboard_back.add(types.InlineKeyboardButton(text="Назад в админ-панель", callback_data='back_admin'))
        for user in datausers:
            try:
                await bot.send_message(user, reklama_sendes631)
            except:
                print(f'[ {user} ] - некорректный юзер. Советую удалить из базы этот id.')
                pass
        await call.message.answer("Сообщение успешно разослано!", reply_markup=inlinekeyboard_back)


@dp.callback_query_handler(text='add_crypto')
async def send(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer('Отправьте ссылку на крипту с сайта\ncoinmarketcap.com')
    await UserInformation.wait_add.set()
    @dp.message_handler(state=UserInformation.wait_add)
    async def add(message: types.Message, state: FSMContext):
        global other1
        global other2
        global other3
        global other4
        global other5
        global other6
        global other7
        global other8
        global other9
        r = requests.get(f"{message.text}")
        html = BS(r.content, 'html.parser')
        name = html.find("span", class_="sc-1eb5slv-0").text.lower()
        r2 = requests.get(f"{message.text}")
        html2 = BS(r2.content, 'html.parser')
        price = html2.find("div", class_="priceValue").text
        price2 = float(re.sub("[$,]", "", price))
        for i in range(1, 9):
            names = globals().get(f"other{i}")
            if names == 'NONE':
                var = {f'other{i}': name}
                globals().update(var)
                globals()[f'{name}_price'] = price2
                await state.update_data(wait_add=f'{name}')
                break
        await message.answer('Теперь введите ваш кошелёк этой валюты:')
        await UserInformation.wait_add_wallet.set()
        @dp.message_handler(state=UserInformation.wait_add_wallet)
        async def add(message: types.Message, state: FSMContext):
            global crypto
            data = await state.get_data()
            name_add = data['wait_add']
            globals()[f'{name_add}_wallet'] = message.text
            inlinekeyboard_back = types.InlineKeyboardMarkup()
            inlinekeyboard_back.add(types.InlineKeyboardButton(text="Назад в админ-панель", callback_data='back_admin'))
            await message.answer('Успешно!', reply_markup=inlinekeyboard_back)
            crypto.append(f'{data["wait_add"]}')
            await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
