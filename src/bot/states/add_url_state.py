from aiogram.fsm.state import StatesGroup, State


class AddUrlState(StatesGroup):
    url = State()
