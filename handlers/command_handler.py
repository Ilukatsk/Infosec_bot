import sys
sys.path.append('..')
from database.db_control import adduser, removeuser, FindCompanies, FindProducts
from Levenshtein import distance
import random
from handlers.keyboards import main_keyboard, companies_list_keyboard
import logging
from stuff import send_text
from handlers.main_keyboard_handler import fl, holidays
import pytz
import datetime

from aiogram import Router, types, filters, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

greeting_1 = """Привет, я мудрый ИБобот и я готов делиться с тобой своей мудростью. С моей помощью вы можете узнавать о значимых праздниках и событиях в ИБ (но не мероприятиях), полезных советах, а также лучше узнать российский рынок ИБ. И пусть ваш путь в кибербезе будет позитивным и мудрым! Чтобы узнать о всех возможностях бота, введите /help"""
helping = """Ежедневно вы автоматически получаете один мудрый совет по ИБ. Если вы хотите узнать больше, - просто нажмите кнопку "Получить мудрый совет по ИБ". А если вы хотите узнать о том, есть ли сегодня какой-либо праздник или знаменательное событие по ИБ, то нажмите кнопку "Что сегодня за день?". Если у вас есть идеи по улучшению бота или уточнению праздников и советов, то нажмите кнопку "Дать обратную связь". Будьте мудры!\n\nСписок доступных команд:\n/start - начало работы ИБобота\n/stop - завершение работы ИБобота\n/help - получение этой подсказки\n/advice - получение совета дня (равнозначно нажатию кнопки “Получить мудрый совет по ИБ”)\n/day - получение сегодняшнего события по ИБ (равнозначно нажатию кнопки “Что сегодня за день?”)\n/company - поиск по российским ИБ-разработчикам (равнозначно нажатию кнопки “ИБ-вендора”)\n/sectype - поиск по типам средств защиты, выпускаемых российскими ИБ-разработчиками (равнозначно нажатию кнопки “Типы средств защиты”\n/typelist- при вводе этой команды вы получите список всех типов средств защиты, которые поддерживает мудрый ИБобот)"""
#helping = """Список доступных команд:\n/start - начало работы ИБобота\n/stop - завершение работы ИБобота\n/help - получение этой подсказки\n/advice - получение совета дня (равнозначно нажатию кнопки “Получить мудрый совет по ИБ”)\n/day - получение сегодняшнего события по ИБ (равнозначно нажатию кнопки “Что сегодня за день?”)\n/company - поиск по российским ИБ-разработчикам (равнозначно нажатию кнопки “ИБ-вендора”)\n/sectype - поиск по типам средств защиты, выпускаемых российскими ИБ-разработчиками (равнозначно нажатию кнопки “Типы средств защиты”\n/typelist- при вводе этой команды вы получите список всех типов средств защиты, которые поддерживает мудрый ИБобот)"""
goodbye = """Спасибо что пользовались умным ИБоботом. Больше вы не будете получать от него никаких сообщений пока вновь не подпишитесь на него. Надеюсь, вы получили от него пользу и результат"""
router = Router()
products_full = ['Antibot', 'BAS', 'Backup', 'Compliance', 'Configuration Management', 'DAG', 'DAM', 'DCAP', 'DDoS', 'DLP', 'DNS', 'DPI', 'Data Diod', 'Deception', 'Digital Risk Protection', 'E-mail', 'EDR', 'FW', 'Forensics', 'Fraud', 'IAM', 'IDS', 'IGA', 'IPT', 'IRP', 'Kubernetes', 'MDM', 'MSS', 'NAC', 'NTA', 'OSINT', 'PAM', 'PKI', 'Password', 'Risk Management', 'SD-WAN', 'SDLC', 'SGRC', 'SIEM', 'SOAR', 'SSO', 'Threat Intelligence', 'UEBA', 'URL Filtering', 'USB', 'UTM', 'VDI', 'VPN', 'Vulnerability Management', 'WAF', 'XDR', 'ZTNA', 'АСУ ТП', 'Антивирус', 'Биометрия', 'Виртуализация', 'Защита от копирования', 'Защита от фотоподделок', 'Защищенная печать', 'Защищенный ПК', 'Защищенный документооборот', 'Защищенный офис', 'Защищенный телефон', 'Киберполигон', 'ОС', 'Облако', 'ПЭМИН', 'Песочница', 'Повышение осведомленности', 'СЗИ от НСД', 'СКЗИ', 'СУБД', 'СХД', 'Токен', 'Удаленный доступ', 'Чип', 'ЭЦП', 'Электронный замок']
users = {}

class ChooseCompany(StatesGroup):
    awaiting_input = State()

class ChooseProduct(StatesGroup):
    awaiting_input = State()

#------------------
command_logger = logging.getLogger(__name__)
command_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s :: %(asctime)s :: %(levelname)s :: %(message)s')
file_handler = logging.FileHandler('./logs/command_handler.log')
file_handler.setFormatter(formatter)
command_logger.addHandler(file_handler)
#------------

@router.message(filters.Command('start'))
async def start(message: types.Message):
    try:
        user_id = message.from_user.id
        adduser(str(user_id), './database/data.db', 'bot_users')
        keyboard = main_keyboard()
        await message.answer(greeting_1, reply_markup=keyboard)
        #await message.answer(greeting_2, reply_markup=keyboard)
        command_logger.info("Greeted the {} user".format(user_id))
    except:
        command_logger.exception("An error has occurred while trying to add the user {}".format(user_id))

@router.message(filters.Command('help'))
async def help(message: types.Message):
    try:
        await message.answer(helping)
        command_logger.info("Sent the bot info to the {} user".format(message.from_user.id))
    except:
        command_logger.exception("An error has occurring whu trying to send bot info to the {} user".format(message.from_user.id))

@router.message(filters.Command('stop'))
async def stop(message: types.Message):
    try:
        user_id = message.from_user.id
        removeuser(str(user_id), './database/data.db', 'bot_users')
        await message.answer(goodbye, reply_markup=types.ReplyKeyboardRemove())
        command_logger.info("Removed user {} from the list of bot users".format(message.from_user.id))
    except:
        command_logger.exception("An error has occurred while trying to remove user {} from the database".format(user_id))

@router.message(filters.Command('advice'))
async def Tip(message: types.Message):
    try:
        await message.answer(random.choice(fl))
        command_logger.info("Gave the advice to the user {}".format(message.from_user.id))
    except:
        command_logger.exception("An error has occurred while trying to give the advice to the user {}".format(message.from_user.id))

@router.message(filters.Command('day'))
async def Day(message: types.Message):
    try:
        today_date = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%d-%m")
        await message.answer(text=("Ура, день не пройдет зря, так как сегодня празднуется " + holidays[today_date].split("-")[1].strip() if today_date in holidays else "Сегодня никаких значимых ИБ-праздников нет 🤷"))
        command_logger.info("Gave info about the holidays happening today to the user {}".format(message.from_user.id))
    except:
        command_logger.exception("An error has occurred while trying to give the holiday info to the user {}".format(message.from_user.id))


@router.message(filters.Command('company'))
async def ProductsByCompany(message: types.Message, state: FSMContext):
    try:
        await message.answer("Введите полное или частичное название интересующей вас российской компании и вы получите список выпускаемых ею типов средств защиты и ссылку на ее сайт")
        await state.set_state(ChooseCompany.awaiting_input)
    except:
        command_logger.exception("An error has occurred while trying to give the advice to the user {}".format(message.from_user.id))
    
     
@router.message(filters.Command('sectype'))
async def CompaniesByProduct(message: types.Message, state: FSMContext):
    try:
        await message.answer("Введите аббревиатуру или название интересующего вас средства защиты и вы получите список отечественных компаний, которые его выпускают")
        await state.set_state(ChooseProduct.awaiting_input)
    except:
        command_logger.exception("An error has occurred while trying to give the advice to the user {}".format(message.from_user.id))
    

    
@router.message(filters.Command('typelist'))
async def tag_list(message: types.Message, state: FSMContext):
    users[message.from_user.id] = 0
    await message.answer("Список категорий продуктов:\n___________\n" + "".join(list(products_full[i] + "\n" for i in range(10 * users[message.from_user.id], min(10 * (users[message.from_user.id] + 1), len(products_full))))), reply_markup=companies_list_keyboard(users[message.from_user.id]))

@router.callback_query(F.data.startswith("page_"))
async def page_change(callback: types.CallbackQuery):
    if callback.data == "page_up":
        users[callback.from_user.id] += 1
    elif callback.data == "page_down":
        users[callback.from_user.id] -= 1
    await callback.message.edit_text("Список категорий продуктов:\n___________\n" + "".join(list(products_full[i] + "\n" for i in range(10 * users[callback.from_user.id], min(10 * (users[callback.from_user.id] + 1), len(products_full))))), reply_markup=companies_list_keyboard(users[callback.from_user.id]))

@router.message(filters.Command('easteregg'))
async def easteregg(message: types.Message, state: FSMContext):
    await message.answer("Браво! Тебя не устраивают правила и ты ищешь что-то выходящие за разрешенные границы. Может быть тебе стоит попробовать себя в роли пентестера или багхантера?")



    