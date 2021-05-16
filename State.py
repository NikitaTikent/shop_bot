from aiogram.dispatcher.filters.state import State, StatesGroup


class NewProduce(StatesGroup):
    name = State()
    description = State()
    coast = State()
    photo_url = State()
    start_parameter = State()
    payload = State()
