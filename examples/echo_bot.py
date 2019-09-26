import logging
from pyAitu import Bot, Dispatcher, executor
from pyAitu.types import Message, QuickButtonCommand, QuickButtonSelected,\
    InlineCommand, InlineCommandSelected, ReplyCommand

API_TOKEN = 'YOUR API TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


WELCOME_MENUS = [
    QuickButtonCommand("inline", 'welcome-menu-inline'),
    QuickButtonCommand("reply", 'welcome-menu-reply'),
    QuickButtonCommand("quick", 'welcome-menu-quick'),
]

INLINE_COMMAND_MENU = [
    InlineCommand("1", "inline-command-data-ASD-1"),
    InlineCommand("2", "inline-command-data-ASD-2"),
    InlineCommand("3", "inline-command-data-ASD-3"),
]

REPLY_COMMAND_MENU = [
    ReplyCommand("1"),
    ReplyCommand("2"),
    ReplyCommand("3"),
]

QUICK_BUTTON_COMMAND_MENU = [
    QuickButtonCommand("1", 'quick-button-data-ASD-1'),
    QuickButtonCommand("2", 'quick-button-data-ASD-2'),
    QuickButtonCommand("3", 'quick-button-data-ASD-3'),
]


@dp.message_handler(commands=['start', 'help'])
async def welcome(message: Message):
    await bot.send_message(message.chat.id, "Hello world")
    await bot.send_message(message.chat.id, "type keyboard")


@dp.message_handler(regexp='(^keyboard$)')
async def send_menu(message: Message):
    await bot.send_message(message.chat.id, "Select button", quick_button_commands=WELCOME_MENUS)


@dp.message_handler()
async def echo(message: Message):
    await bot.send_message(message.chat.id, message.text)


@dp.quick_button_handler(state="*", func=(lambda call: call.metadata.startswith('welcome-menu-')))
async def menu_handler(qb: QuickButtonSelected):
    text = 'You chose'
    if qb.metadata.endswith('inline'):
        text += ' inline buttons'
        await bot.send_message(qb.dialog.id, text, inline_commands=INLINE_COMMAND_MENU)
    if qb.metadata.endswith('reply'):
        text += ' reply buttons'
        await bot.send_message(qb.dialog.id, text, reply_keyboard=REPLY_COMMAND_MENU)
    if qb.metadata.endswith('quick'):
        text += ' quick buttons'
        await bot.send_message(qb.dialog.id, text, quick_button_commands=QUICK_BUTTON_COMMAND_MENU)


@dp.inline_command_handler(state="*", func=(lambda call: call.metadata.startswith('inline-command-data-')))
async def inline_menu_handler(ic: InlineCommandSelected):
    await bot.send_message(ic.dialog.id, "Got data from inline command: {}".format(ic.metadata))


if __name__ == '__main__':
    executor.start_polling(dp)