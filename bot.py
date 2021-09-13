import logging
import json
import os, sys
import threading
from dotenv import dotenv_values
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)


def shutdown():
    global updater

    updater.stop()
    updater.is_idle = False

def stop():
    threading.Thread(target=shutdown).start()

def get_index(new_data, user):
    index = 0
    for item in new_data:
        if item["Username"] == user.username:
            return index
        index += 1
    return -1


def start(update: Update, _: CallbackContext) -> int:
    global new_data, chats_id

    content = []
    with open('info.json') as info:
        data = json.load(info)
        for item in data:
            content.append(item['Username'])

    user = update.message.from_user

    if user.username not in content:
        chats_id[user.username] = update.message.chat_id

        logger.info("User %s Started the bot", user.username)

        reply_keyboard = [['طراح شو مقدماتی'],
                        ['جنگ‌افزار سازی'],
                        ['مدل‌های جغرافیایی مقدماتی'],
                        ['لذت‌های باستان‌شناسی پیشرفته'],
                        ['دست‌آفریده‌های چرمی'],
                        ['برنامه نویسی خلاقانه'],
                        ['پاستیل با فیزیک - پایۀ هفتم'],
                        ['پاستیل با فیزیک - پایۀ هشتم'],
                        ['مدار منطقی 1'],
                        ['مدار منطقی 2'],
                        ['مدار منطقی 3'],
                        ['ترکیبیات'],
                        ['ماشین زمان - پایۀ هشتم'],
                        ['گراف'],
                        ['حلقه مطالعات ادبیات - پایۀ هشتم'],
                        ['حلقه مطالعات شیمی'],
                        ['فیزیک دوست‌داشتنی - پایۀ هفتم'],
                        ['فیزیک دوست‌داشتنی - پایۀ هشتم'],
                        ['صبحانه مزوزوئیک'],
                        ['سمینار‌های کامپیوتری'],
                        ['مدیر برتر'],
                        ['حلقه مطالعات فیزیک - پایۀ هشتم'],
                        ['حلقه مطالعات زیست‌شناسی'],
                        ['طراحی سایت'],
                        ['رمزگذاری با طعم ربات تلگرام'],
                        ['آرشیتکت'],
                        ['رویه‌های دو بعدی'],
                        ['شیمی کوانتوم'],
                        ['مشکات'],
                        ['ماشین زمان - پایۀ هفتم'],
                        ['حلقه مطالعات ریاضی - پایۀ هشتم'],
                        ['مباحثی در شیمی و زیست‌شناسی'],
                        ['فن بیان'],
                        ['آشپزی دلچسب و خوشمزه'],
                        ['نمایش رادیویی'],
                        ['عکاسی'],
                        ['حلقه مطالعات فیزیک - پایۀ هفتم'],
                        ['حلقه مطالعات ریاضی - پایۀ هفتم'],
                        ['نظریه اعداد']]

        update.message.reply_text('سلام! \n\n لطفاً نام کلاس تابستانه‌ی خود را انتخاب کنید.', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return CLASS

    else:
        update.message.reply_text('شما قبلاً پروژۀ خود را ثبت کرده‌اید!')
        return ConversationHandler.END


def Class(update: Update, _: CallbackContext) -> int:
    global new_data

    user = update.message.from_user

    logger.info("Class name of %s: %s", user.username, update.message.text)

    new_data.append({"Username": user.username,
                     "Classname": update.message.text,
                     "Projname": "",
                     "Description": "",
                     "ID": ""})

    update.message.reply_text('لطفاً نام پروژۀ خود را وارد کنید',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PROJ

def proj(update: Update, _: CallbackContext) -> int:
    global new_data

    user = update.message.from_user

    index = get_index(new_data, user)
    if index == -1:
        logger.info("User %s not found!", user.username)
        update.message.reply_text('لطفاً بات را از ابتدا به طور صحیح شروع کنید')
        return ConversationHandler.END
    else:
        new_data[index]["Projname"] = update.message.text

    logger.info("Project name of %s: %s", user.username, update.message.text)

    update.message.reply_text(
        'ممنون! حالا لطفاً توضیحاتی در زمینۀ پروژه‌تان بدهید. (حداقل 50 کلمه)'
    )

    return DESC

def description(update: Update, _: CallbackContext) -> int:
    global new_data, chats_id

    user = update.message.from_user
    user_abs = update.message.text

    word = user_abs.split()
    if len(word) >= 50:
        ### write user_abs to json
        index = get_index(new_data, user)
        if index == -1:
            logger.info("User %s not found!", user.username)
            update.message.reply_text('لطفاً بات را از ابتدا به طور صحیح شروع کنید')
            return ConversationHandler.END
        else:
            new_data[index]["Description"] = user_abs

        logger.info(
        "Description of %s has been saved!", user.username)

        update.message.reply_text(
        'توضیحات شما ثبت شد. لطفاً یک آی‌دی تلگرامی برای هماهنگی‌های بعدی ثبت کنید.' + '\n\n' + 'اگر می‌خواهید از همین حساب برای هماهنگی‌های بعدی استفاده کنید، عبارت - را ارسال کنید!' + '\n\n' + 'اگر آی‌دی ندارید، شماره‌ی تلفن خود در تلگرام را وارد کنید.')

        return ID

    else:
        logger.info("Description of %s does not meet requirements!", user.username)

        update.message.reply_text('چکيده نبايد کمتر از 50 کلمه باشد!!! دوباره سعی کنيد.')

def Id(update: Update, _: CallbackContext) -> int:
    global new_data, chats_id

    user = update.message.from_user
    user_id = update.message.text

    if user_id == '-':
        if user.username == None:
            logger.info("%s does not have ID", user.username)
            update.message.reply_text('شما آی‌دی تلگرامی ندارید، شمارۀ تلفن خود در تلگرام را وارد کنید.')
        else:
            index = get_index(new_data, user)
            if index == -1:
                logger.info("User %s not found!", user.username)
                update.message.reply_text('لطفاً بات را از ابتدا به طور صحیح شروع کنید')
                return ConversationHandler.END
            else:
                new_data[index]["ID"] = user.username

            logger.info("Data of %s has been saved!", user.username)

            update.message.reply_text('ممنون! اطلاعات شما ثبت شد. با آرزوی موفقیت برای شما و پروژه‌تان')

            with open('info.json') as info:
                data = json.load(info)

            data.append(new_data[index])
            new_data.pop(index)
            chats_id.pop(user.username)

            with open('info.json', "w") as file:
                file.write(json.dumps(data))

            return ConversationHandler.END

    elif user_id[0] == '@' or user_id[0] == '09':
        index = get_index(new_data, user)
        if index == -1:
            logger.info("User %s not found!", user.username)
            update.message.reply_text('لطفاً بات را از ابتدا به طور صحیح شروع کنید')
            return ConversationHandler.END
        else:
            new_data[index]["ID"] = user_id

        logger.info("Data of %s has been saved!", user.username)

        update.message.reply_text('ممنون! اطلاعات شما ثبت شد. با آرزوی موفقیت برای شما و پروژه‌تان')

        with open('info.json') as info:
            data = json.load(info)

        data.append(new_data[index])
        new_data.pop(index)
        chats_id.pop(user.username)

        with open('info.json', "w") as file:
            file.write(json.dumps(data))

        return ConversationHandler.END

    else:
        logger.info("ID of %s does not true!", user.username)
        update.message.reply_text('لطفاً یک آی‌دی یا شمارۀ معتبر ثبت کنید!')


def cancel(update: Update, _: CallbackContext) -> int:
    global new_data, API_TOKEN

    user = update.message.from_user

    logger.info("User %s canceled the conversation.", user.username)
    update.message.reply_text('خداحافظ! حتماً دوباره برگرد و چکیده‌ات رو ثبت کن.', reply_markup=ReplyKeyboardRemove())

    index = get_index(new_data, user)
    if index == -1:
        logger.info("User %s not found!", user.username)
        update.message.reply_text('لطفاً بات را از ابتدا به طور صحیح شروع کنید')
        return ConversationHandler.END
    else:
        new_data.pop(index)
        chats_id.pop(user.username)

    return ConversationHandler.END

def reset(update: Update, _: CallbackContext):
    global new_data, admins_ls, chats_id, updater, API_TOKEN

    user = update.message.from_user

    if user.username in admins_ls:
        for chat_id in chats_id.values():
            bot = Bot(token=API_TOKEN)
            try:
                bot.sendMessage(chat_id=chat_id, text='بات ریست شد!\nلطفاً مجدداً /start کنید.')
            except:
                logger.info("Someone blocked bot!")
        update.message.reply_text('بات با موفقیت ریست شد.')
        logger.info("Admin resets.")
        stop()

    else:
        update.message.reply_text('شما دسترسی انجام این کار را ندارید!')
        logger.info("Someone wanted to reset.")

def admin(update: Update, _: CallbackContext) -> int:
    global new_data, admins_ls

    user = update.message.from_user

    if user.username in admins_ls:
        with open('info.json') as info:
            data = json.load(info)

        username = []
        classname = []
        projname = []
        description = []
        ids = []
        for item in data:
            username.append(item['Username'])
            classname.append(item['Classname'])
            projname.append(item['Projname'])
            description.append(item['Description'])
            ids.append(item['ID'])

        if len(username) == 0:
            update.message.reply_text('اطلاعاتی نداریم! برو خیالت تخت.')
        else:
            for i in range(len(username)):
                update.message.reply_text('نام ثبت کننده: ' + str(username[i]) + '\n\n' + 'نام کلاس: ' + classname[i] + '\n\n' + 'نام پروژه: ' + projname[i] + '\n\n'+'توضیحات ثبت شده: ' + '\n' + description[i] + '\n\n' + 'آی‌دی ارتباطی: ' + ids[i])
        logger.info("Admin gets information.")

    else:
        update.message.reply_text('شما دسترسی انجام این کار را ندارید!')
        logger.info("Someone wanted to get information.")

def main() -> None:
    global new_data, API_TOKEN, updater

    if "info.json" not in os.listdir():
        with open("info.json", "w") as file:
            file.write(json.dumps([]))

    updater = Updater(API_TOKEN)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('reset', reset), CommandHandler('start', start), CommandHandler('admin35', admin)],
        states={
            CLASS: [
                CommandHandler('reset', reset),
                CommandHandler('cancel', cancel),
                MessageHandler(Filters.text, Class),
            ],
            PROJ: [
                CommandHandler('reset', reset),
                CommandHandler('cancel', cancel),
                MessageHandler(Filters.text, proj),
            ],
            DESC: [
                CommandHandler('reset', reset),
                CommandHandler('cancel', cancel),
                MessageHandler(Filters.text, description),
            ],
            ID: [
                CommandHandler('reset', reset),
                CommandHandler('cancel', cancel),
                MessageHandler(Filters.text, Id),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    environment_varables = dotenv_values(".env")

    # raise error for not existing .env file
    if "API_TOKEN" not in environment_varables.keys() or "ADMINS" not in environment_varables.keys():
        raise FileNotFoundError("You have to create a file and name it '.env'" \
                                    + " then pass in your API_TOKEN and ADMINS")

    API_TOKEN = environment_varables["API_TOKEN"]
    admins_ls = environment_varables["ADMINS"].split('-')

    new_data = []
    chats_id = {}
    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    CLASS, PROJ, DESC, ID = range(4)

    main()
    os.system("python3 {}".format(sys.argv[0]))