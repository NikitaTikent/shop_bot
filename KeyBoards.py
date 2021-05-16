from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from MemberBase import PublicDirector


def next_list(amount_page):
    KeyboardBuyProduceNext = InlineKeyboardMarkup(row_width=2)
    produces = PublicDirector.DownloadProduces()[amount_page::-1]
    z = 1
    for produce in produces:
        KeyboardBuyProduceNext.add(InlineKeyboardButton(str(produce[1]), callback_data=str(produce[1])))
        z += 1
        if z == 10:
            break
    if amount_page >= len(PublicDirector.DownloadProduces())-1:
        KeyboardBuyProduceNext.add(InlineKeyboardButton('->', callback_data='next'))
    elif amount_page < 9:
        KeyboardBuyProduceNext.add(InlineKeyboardButton('<-', callback_data='back'))
    else:
        KeyboardBuyProduceNext.row(InlineKeyboardButton('<-', callback_data='back'),
                                   InlineKeyboardButton('->', callback_data='next'))
    return KeyboardBuyProduceNext
