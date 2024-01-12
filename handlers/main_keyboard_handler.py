import sys
import logging
import random
import datetime
import pytz
from Levenshtein import distance
from handlers.keyboards import main_keyboard, single_button_keyboard
sys.path.append('..')
from database.db_control import getusers, FindProducts, FindCompanies
from aiogram import Router, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.methods.send_message import SendMessage
from aiogram.fsm.context import FSMContext
router = Router()
feedback_receive_id = #ДОБАВЬТЕ АЙДИ

#------------------
main_keyboard_logger = logging.getLogger(__name__)
main_keyboard_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('./logs/main_keyboard_handler.log')
formatter = logging.Formatter('%(name)s :: %(asctime)s :: %(levelname)s :: %(message)s')
file_handler.setFormatter(formatter)
main_keyboard_logger.addHandler(file_handler)
#------------

try:
    with open(file="facts.txt") as file:
        fl = file.read().split("||")
        main_keyboard_logger.info("Successfully opened facts.txt")
except:
    main_keyboard_logger.critical("Couldn't open facts.txt")

try:
    with open("holidays.txt") as file:
        holidays = {line.split("||")[0] : line.split("||")[1] for line in file}
        main_keyboard_logger.info("Successfully opened holidays.txt")
except:
    main_keyboard_logger.critical("Couldn't open facts.txt")

companies = ['мкосистемы', 'groupib', 'profiscope', 'advsoft', 'altell', 'альтель', 'алтел', 'antibot', 'антибот', 'aquarius', 'аквариус', 'avsoft', 'авсофт', 'awillix', 'авиликс', 'bearpass', 'бирпас', 'bitcop', 'биткоп', 'bizone', 'бизон', 'businessecosystem', 'businessguardian', 'carbonsoft', 'cezurity', 'цезурити', 'clevercontrol', 'cloudadvisor', 'codescoring', 'crosstechsolutionsgroup', 'кросстех', 'кростех', 'crosstechnologies', 'кросс', 'ctrlhack', 'cvatechnologies', 'cyberpeak', 'сайберпик', 'cybertonica', 'сайбертоника', 'кибертоника', 'ddosguard', 'digitaldesign', 'диджитал', 'дизайн', 'drweb', 'доктор', 'веб', 'elcomsoft', 'элкомсофт', 'eplat4m', 'everytag', 'эвритег', 'falcongaze', 'фальконгейз', 'фалконгейз', 'facct', 'групайби', 'факт', 'группайби', 'грибы', 'ideco', 'айдеко', 'incsecurity', 'indeedid', 'индид', 'innostage', 'инностейдж', 'inoventica', 'иновентика', 'isbcgroupesmart', 'killbot', 'килбот', 'kraftway', 'крафтвей', 'luntry', 'лантри', 'makves', 'маквес', 'microolap', 'nanoantivirus', 'neobit', 'необит', 'networkprofi', 'ngenix', 'ngrsoftlab', 'энджиар', 'софтлаб', 'omion', 'ozforensics', 'оз', 'форенсикс', 'оз', 'форензикс', 'passleak', 'passwork', 'пассворк', 'peakсофт', 'пиксофт', 'pentestit', 'пентестит', 'perimetrix', 'периметрикс', 'phishman', 'фишман', 'positivetechnologies', 'позитив', 'пт', 'pt', 'позитивные', 'технологии', 'позитив', 'технолоджиз', 'qapp', 'qrate', 'кьюрейт', 'qratorlabs', 'куратор', 'rvision', 'эрвижн', 'rusiem', 'русием', 'safetech', 'сейфтех', 'сейфтек', 'securitm', 'securitytechnologyresearchsetere', 'securityvision', 'секьюрити', 'вижн', 'servicepipe', 'skydns', 'скайднс', 'solidlab', 'солидлаб', 'spacebit', 'спейсбит', 'stingray', 'stormwall', 'штормвол', 'surfsecure', 'swordfishsecurityappsechub', 'свордфиш', 'usergate', 'уг', 'юзергейт', 'ug', 'volgablob', 'xello', 'zapretservice', 'zecurion', 'зекурион', 'ареалконсалтингинтернетконтрольсервер', 'аванпост', 'адмсистемы', 'айтибастион', 'айтиновация', 'айтипровайд', 'актив', 'аладдин', 'алтэкссофт', 'амикон', 'амтгрупп', 'анкад', 'антифишинг', 'арудитсекьюрити', 'асплабс', 'атлас', 'атомбезопасность', 'б152', 'базальтспо', 'бастион', 'бифит', 'валидата', 'вебантифрод', 'webcontrol', 'вебконтрол', 'вебмониторэкс', 'wallarm', 'вычислительныерешения', 'газинформсервис', 'гис', 'гардатехнологии', 'гефесттехнолоджиз', 'ивк', 'инжиниринговыетехнологии', 'инконтрол', 'институтсетевыхтехнологий', 'инфовотч', 'infowatch', 'инфозонт', 'инфолэнд', 'инфомаксимум', 'инфопро', 'инфотактика', 'инфотекс', 'инфотексинтернеттраст', 'итэкспертиза', 'ицбаррикады', 'катюшапринт', 'киберполигон', 'киберпротект', 'кодбезопасности', 'конфидент', 'концернавтоматика', 'криптоком', 'криптопро', 'cryptopro', 'криптософт', 'криптоэкс', 'криптэкс', 'лаборатория50', 'лабораториякасперского', 'каспер', 'kaspersky', 'лк', 'дятлы', 'лабораторияппш', 'лисси', 'миландр', 'мсофт', 'мультифактор', 'нетамс', 'ниимасштаб', 'ниисокб', 'ниицентрпрограммсистем', 'новыеоблачныетехнологиимойофис', 'новыетехнологиибезопасности', 'норситранс', 'нотасервис', 'нпккриптонит', 'нпортк', 'нппгамма', 'нппитб', 'нпцксб', 'нтцатлас', 'нуматех', 'одинайдиэм', 'окбсапр', 'оксидженсофтвер', 'ореолсекьюрити', 'орлан', 'открытаямобильнаяплатформа', 'пангеорадар', 'пвс', 'перспективныймониторинг', 'пниэи', 'праймтек', 'протекшентехнолоджи', 'рдпру', 'редсофт', 'рнт', 'роса', 'ростелекомсолар', 'солар', 'рукссолюшенс', 'рупост', 'русбитех', 'астра', 'рцзифорт', 'стеррасиэспи', 'sterra', 'sterra', 'саврус', 'сайберлимфа', 'cyberlympha', 'сафиб', 'свемел', 'серчинформ', 'searchinform', 'сискрипто', 'системыпрактическойбезопасности', 'системыуправленияидентификацией', 'скдата', 'смартсофт', 'smartsoft', 'совинтегра', 'стахановец', 'стопфиш', 'stopphish', 'тионикс', 'тсс', 'tss', 'фаззилоджиклабс', 'фактортс', 'фрактел', 'фродекс', 'frodex', 'ханикорн', 'honeycorn', 'хэлф', 'цаир', 'цби', 'центрспециальнойсистемотехники', 'цифровыетехнологии', 'црт', 'цссбезопасность', 'шарксдатацентр', 'элвис', 'элтекс', 'eltex', 'эшелон']
alt_names = {'оксидженсофтвер': 'мкосистемы', 'groupib': 'facct','вебконтрол': 'webcontrol', 'альтель': 'altell', 'алтел': 'altell', 'антибот': 'antibot', 'аквариус': 'aquarius', 'авсофт': 'avsoft', 'авиликс': 'awillix', 'бирпас': 'bearpass', 'биткоп': 'bitcop', 'бизон': 'bizone', 'цезурити': 'cezurity', 'кросстех': 'crosstechsolutionsgroup', 'кростех': 'crosstechsolutionsgroup', 'кросс': 'crosstechnologies', 'сайберпик': 'cyberpeak', 'сайбертоника': 'cybertonica', 'кибертоника': 'cybertonica', 'диджитал': 'digitaldesign', 'дизайн': 'digitaldesign', 'доктор': 'drweb', 'веб': 'drweb', 'элкомсофт': 'elcomsoft', 'эвритег': 'everytag', 'фальконгейз': 'falcongaze', 'фалконгейз': 'falcongaze', 'групайби': 'facct', 'факт': 'facct', 'группайби': 'facct', 'грибы': 'facct', 'айдеко': 'ideco', 'индид': 'indeedid', 'инностейдж': 'innostage', 'иновентика': 'inoventica', 'килбот': 'killbot', 'крафтвей': 'kraftway', 'лантри': 'luntry', 'маквес': 'makves', 'необит': 'neobit', 'энджиар': 'ngrsoftlab', 'софтлаб': 'ngrsoftlab', 'оз': 'ozforensics', 'форенсикс': 'ozforensics', 'форензикс': 'ozforensics', 'пассворк': 'passwork', 'пиксофт': 'peakсофт', 'пентестит': 'pentestit', 'периметрикс': 'perimetrix', 'фишман': 'phishman', 'позитив': 'positivetechnologies', 'пт': 'positivetechnologies', 'pt': 'positivetechnologies', 'позитивные': 'positivetechnologies', 'технологии': 'positivetechnologies', 'технолоджиз': 'positivetechnologies', 'кьюрейт': 'qrate', 'куратор': 'qratorlabs', 'эрвижн': 'rvision', 'русием': 'rusiem', 'сейфтех': 'safetech', 'сейфтек': 'safetech', 'секьюрити': 'securityvision', 'вижн': 'securityvision', 'скайднс': 'skydns', 'солидлаб': 'solidlab', 'спейсбит': 'spacebit', 'штормвол': 'stormwall', 'свордфиш': 'swordfishsecurityappsechub', 'уг': 'usergate', 'юзергейт': 'usergate', 'ug': 'usergate', 'зекурион': 'zecurion', 'wallarm': 'вебмониторэкс', 'гис': 'газинформсервис', 'infowatch': 'инфовотч', 'cryptopro': 'криптопро', 'каспер': 'лабораториякасперского', 'kaspersky': 'лабораториякасперского', 'лк': 'лабораториякасперского', 'дятлы': 'лабораториякасперского', 'солар': 'ростелекомсолар', 'астра': 'русбитех', 'sterra': 'стеррасиэспи', 'cyberlympha': 'сайберлимфа', 'searchinform': 'серчинформ', 'smartsoft': 'смартсофт', 'stopphish': 'стопфиш', 'tss': 'тсс', 'frodex': 'фродекс', 'honeycorn': 'ханикорн', 'eltex': 'элтекс'}
helping = """Ежедневно вы автоматически получаете один мудрый совет по ИБ. Если вы хотите узнать больше, - просто нажмите кнопку "Получить мудрый совет по ИБ". А если вы хотите узнать о том, есть ли сегодня какой-либо праздник или знаменательное событие по ИБ, то нажмите кнопку "Что сегодня за день?". Если у вас есть идеи по улучшению бота или уточнению праздников и советов, то нажмите кнопку "Дать обратную связь". Будьте мудры!\n\nСписок доступных команд:\n/start - начало работы ИБобота\n/stop - завершение работы ИБобота\n/help - получение этой подсказки\n/advice - получение совета дня (равнозначно нажатию кнопки “Получить мудрый совет по ИБ”)\n/day - получение сегодняшнего события по ИБ (равнозначно нажатию кнопки “Что сегодня за день?”)\n/company - поиск по российским ИБ-разработчикам (равнозначно нажатию кнопки “ИБ-вендора”)\n/sectype - поиск по типам средств защиты, выпускаемых российскими ИБ-разработчиками (равнозначно нажатию кнопки “Типы средств защиты”\n/typelist- при вводе этой команды вы получите список всех типов средств защиты, которые поддерживает мудрый ИБобот)"""
products_full = ['DDoS', 'Digital Risk Protection', 'ZTNA', 'Antibot', 'Защита от фотоподделок', 'Risk Management', 'SIEM', 'VPN', 'DCAP', 'IGA', 'Deception', 'Vulnerability Management', 'DLP', 'СЗИ от НСД', 'WAF', 'IPT', 'USB', 'IDS', 'Облако', 'UEBA', 'СКЗИ', 'SSO', 'Биометрия', 'OSINT', 'BAS', 'DPI', 'E-mail', 'Threat Intelligence', 'EDR', 'PAM', 'UTM', 'Виртуализация', 'DAM', 'IAM', 'Песочница', 'NAC', 'MDM', 'Повышение осведомленности', 'FW', 'MSS', 'Fraud', 'АСУ ТП', 'Kubernetes', 'IRP', 'Антивирус', 'SD-WAN', 'ОС', 'PKI', 'Защита от копирования', 'SOAR', 'Киберполигон', 'XDR', 'ПЭМИН', 'Защищенный телефон', 'Чип', 'DAG', 'Data Diod', 'СУБД', 'Удаленный доступ', 'SDLC', 'Compliance', 'DNS', 'Электронный замок', 'Токен', 'Backup', 'Forensics', 'URL Filtering', 'ЭЦП', 'VDI', 'NTA', 'SGRC', 'Password', 'Защищенный ПК', 'СХД', 'Защищенная печать', 'Configuration Management', 'Защищенный офис', 'Защищенный документооборот']
products = ['ddos', 'digitalriskprotection', 'ztna', 'antibot', 'защитаотфотоподделок', 'riskmanagement', 'siem', 'vpn', 'dcap', 'iga', 'deception', 'vulnerabilitymanagement', 'dlp', 'сзиотнсд', 'waf', 'ipt', 'usb', 'ids', 'облако', 'ueba', 'скзи', 'sso', 'биометрия', 'osint', 'bas', 'dpi', 'email', 'threatintelligence', 'edr', 'pam', 'utm', 'виртуализация', 'dam', 'iam', 'песочница', 'nac', 'mdm', 'повышениеосведомленности', 'fw', 'mss', 'fraud', 'асутп', 'kubernetes', 'irp', 'антивирус', 'sdwan', 'ос', 'pki', 'защитаоткопирования', 'soar', 'киберполигон', 'xdr', 'пэмин', 'защищенныйтелефон', 'чип', 'dag', 'datadiod', 'субд', 'удаленныйдоступ', 'sdlc', 'compliance', 'dns', 'электронныйзамок', 'токен', 'backup', 'forensics', 'urlfiltering', 'эцп', 'vdi', 'nta', 'sgrc', 'password', 'защищенныйпк', 'схд', 'защищеннаяпечать', 'configurationmanagement', 'защищенныйофис', 'защищенныйдокументооборот']

class ReceiveFeedback(StatesGroup):
    writing_feedback = State()

class ChooseCompany(StatesGroup):
    awaiting_input = State()

class ChooseProduct(StatesGroup):
    awaiting_input = State()

@router.message(F.text == "Получить мудрый совет по ИБ")
async def Tip(message: types.Message):
    try:
        await message.answer(random.choice(fl))
        main_keyboard_logger.info("Gave the advice to the user {}".format(message.from_user.id))
    except:
        main_keyboard_logger.exception("An error has occurred while trying to give the advice to the user {}".format(message.from_user.id))

@router.message(F.text == "Что сегодня за день?")
async def Day(message: types.Message):
    try:
        today_date = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%d-%m")
        await message.answer(text=("Ура, день не пройдет зря, так как сегодня празднуется " + holidays[today_date].split("-")[1].strip() if today_date in holidays else "Сегодня никаких значимых ИБ-праздников нет 🤷"))
        main_keyboard_logger.info("Gave info about the holidays happening today to the user {}".format(message.from_user.id))
    except:
        main_keyboard_logger.exception("An error has occurred while trying to give the holiday info to the user {}".format(message.from_user.id))
        

@router.message(F.text == "Дать обратную связь")
async def Feedback(message: types.Message, state: FSMContext):
    try:
        await message.answer('Одним сообщением напишите ваше предложение.', reply_markup=single_button_keyboard("Отмена"))#потенциально можно будет и несколько, но мне кажется, одного достаточно
        await state.set_state(ReceiveFeedback.writing_feedback)
    except:
        main_keyboard_logger.exception("An error has occurred while trying to recieve feedback from the user {}".format(message.from_user.id))

    
@router.message(ReceiveFeedback.writing_feedback)
async def Feedback2(message: types.Message, state: FSMContext):
    try:
        if (message.text != "Отмена"):
            await message.answer("Спасибо за ваш отзыв", reply_markup=main_keyboard())
            await SendMessage(chat_id=feedback_receive_id, text="Отзыв о работе бота от пользователя @{}:".format(message.from_user.username))
            await SendMessage(chat_id=feedback_receive_id, text=message.text)
            await state.clear()
            main_keyboard_logger.info("Received feedback from the user {}".format(message.from_user.id))
        else:
            await message.answer("Отмена сбора обратной связи.", reply_markup=main_keyboard())
            await state.clear()
            main_keyboard_logger.info("Cancelled feedback reception from the user {}".format(message.from_user.id))
            
    except:
        main_keyboard_logger.exception("An error has occurred while trying to process feedback from the user {}".format(message.from_user.id))



async def LeastDistance(input_name, data):
    maxd = 1000
    for name in data:
        dist = distance(input_name, name)
        if dist < maxd:
            name = alt_names[name] if name in alt_names else name
            maxd, closest = dist, [name]
        elif dist == maxd:
            name = alt_names[name] if name in alt_names else name
            if name not in closest: closest.append(name)
    if maxd <= 2:
        return closest
    return "none"

async def FormatName(text):
    out = ""
    for char in text:
        if char.isalnum():
            out += char.lower()
    return out


@router.message(F.text == "ИБ-вендора")
async def ProductsByCompany(message: types.Message, state: FSMContext):
    try:
        await message.answer("Введите полное или частичное название интересующей вас российской компании и вы получите список выпускаемых ею типов средств защиты и ссылку на ее сайт")
        await state.set_state(ChooseCompany.awaiting_input)
    except:
        main_keyboard_logger.exception("An error has occurred while trying to give the advice to the user {}".format(message.from_user.id))
    

@router.message(ChooseCompany.awaiting_input)
async def ProductsByCompany2(message: types.Message, state: FSMContext):
    try:
        await state.clear()
        if len(message.text) < 100:
            comp_name = await FormatName(message.text)
            candidates = []
            for company in companies:
                if comp_name in company:
                    tmp = alt_names[company] if company in alt_names else company
                    if ((tmp not in candidates) and (len(comp_name) > 3)) : candidates.append(tmp)
                if comp_name == company:
                    candidates = [alt_names[company] if company in alt_names else company]
                    break
            candidates.sort()
            if len(candidates) == 0:
                comp_names = await LeastDistance(comp_name, companies) if len(comp_name) > 3 else "none"
                if comp_names != "none":
                    if len(comp_names) == 1:
                        company = comp_names[0]
                        company_profile = FindProducts(company, './database/data.db', "comp_data")
                        txt = "Компания выпускает продукты:\n\n"
                        for i in range(3, len(company_profile[0])):
                            if company_profile[0][i] == 1: txt += products_full[i-3] + "\n"
                        await message.answer(company_profile[0][1])
                        await message.answer(txt)
                        await message.answer(company_profile[0][2])
                    else:
                        txt = "Вашей компании нет в списке, возможно вы имели ввиду одну из этих:\n"
                        for company in comp_names:
                            company_name = FindProducts(company, './database/data.db', "comp_data")[0][1]
                            txt += str(company_name) + "\n"
                        await message.answer(txt)
                else:
                    await message.answer('Такой компании нет в моей базе. Проверьте, что нет ошибок или попробуйте другое написание. Если вы уверены, что такая компания есть, то напишите об этом через "Обратную связь"')
            elif len(candidates) == 1:
                comp_name = candidates[0]
                company_profile = FindProducts(comp_name, './database/data.db', "comp_data")
                txt = "Компания выпускает продукты:\n\n"
                for i in range(3, len(company_profile[0])):
                    if company_profile[0][i] == 1: txt += products_full[i-3] + "\n"
                await message.answer(company_profile[0][1])
                await message.answer(txt)
                await message.answer(company_profile[0][2])
            else:
                txt = "Такой компании нет в списке, возможно вы имели ввиду одну из этих:\n"
                for company in candidates:
                    company_name = FindProducts(company, './database/data.db', "comp_data")[0][1]
                    txt += str(company_name) + "\n"
                await message.answer(txt)
        else:
            await message.answer('Такой компании нет в моей базе. Проверьте, что нет ошибок или попробуйте другое написание. Если вы уверены, что такая компания есть, то напишите об этом через "Обратную связь"')
    except:
        main_keyboard_logger.exception("An error has occurred while trying to process feedback from the user {}".format(message.from_user.id))
    
@router.message(F.text == "Типы средств защиты")
async def CompaniesByProduct(message: types.Message, state: FSMContext):
    try:
        await message.answer("Введите аббревиатуру или название интересующего вас средства защиты и вы получите список отечественных компаний, которые его выпускают")
        await state.set_state(ChooseProduct.awaiting_input)
    except:
        main_keyboard_logger.exception("An error has occurred while trying to give the advice to the user {}".format(message.from_user.id))
    
@router.message(ChooseProduct.awaiting_input)
async def CompaniesByProduct2(message: types.Message, state: FSMContext):
    await state.clear()
    product = await FormatName(message.text)
    if product in products:
        company_names = FindCompanies(product, './database/data.db', "comp_data")
        text = "Подобные продукты выпускают:\n"
        for name in company_names:
            text += str(name[0]) + "\n"
        await message.answer(text)
    else:
        await message.answer("Такого типа средства защиты нет в моей базе. Проверьте, что нет ошибок или попробуйте другое написание. Вы можете получить список поддерживаемых типов, введя /typelist")
    
@router.message()
async def default_behaviour(message: types.Message, state: FSMContext):
    await message.answer(helping)








