"""
Centralised FSM states for the JIP bot.
"""
from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    waiting_for_language = State()
    waiting_for_name = State()
    waiting_for_user_type = State()
    waiting_for_privacy = State()
    waiting_for_phone = State()
    waiting_for_location = State()
    waiting_for_store_confirmation = State()


class LanguageStates(StatesGroup):
    choosing = State()
