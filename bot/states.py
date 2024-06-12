from aiogram.fsm.state import State, StatesGroup

class MainState(StatesGroup):
    MAIN = State()
    REVIEWS = State()
    ADMIN = State()
    NODATA = State()
    ERRORMAIN = State()

class ChoiseState(StatesGroup):
    CHOISE = State()


class PlatformState1(StatesGroup):
    MAIN = State()
    NOVALID = State()

class PlatformState2(StatesGroup):
    MAIN = State()
    NOVALID = State()

class AuthState2(StatesGroup):
    MAIN = State()
    LOGIN = State()
    PASS = State()
    NOVALIDLOGIN = State()
    NOVALIDPASSWORD = State()
    FINISH = State()

class AuthState1(StatesGroup):
    MAIN = State()
    LOGIN = State()
    PASS = State()
    NOVALIDLOGIN = State()
    NOVALIDPASSWORD = State()
    FINISH = State()