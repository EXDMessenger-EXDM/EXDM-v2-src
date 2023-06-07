# Конфигурация EXDM

# OpenAI
# Для эндпоинтов /api/ai
# Получи ключ на https://platform.openai.com/account/api-keys
OPENAI_KEY = ""
OPENAI_IMAGE_SIZE = "256x256" # 256x256 = 0.0018$, 512x512 = 0.0020$ или 1024x1024 = 0.0022$

# Проверять сообщение на содержимое, которое подходит не для всех (напр. угрозы, насилие, и так далее)
# На основе технологий от OpenAI
CHECK_MESSAGE = True

# Пользователи (Users)

# Регистрация
# MIN_USER_ID лучше оставляйте на 2
MIN_USER_ID = 2
MAX_USER_ID = (2 ** 63 - 1) # НЕ МЕНЯТЬ, ЛИМИТЫ SQLITE3

# Стандартая биография о пользователе
DEFAULT_BIO = ""

# MAX_USERNAME_LENGTH - Максимальная длина ника, лучше ставте около 30
MAX_USERNAME_LENGTH = 30

# Настройки генераций дискриминиатора (#0001)
# НИКОГДА НЕ СТАВТЕ БОЛЬШЕ 9, И НЕ СТАВТЕ ВЕЗДЕ 0
# Вы же не хотите что-то типо Example#00015? (+Это сломает клиент)
MIN_DISCRIMINATOR = 2
MAX_DISCRIMINATOR = 9

# Генерация токена при генераций
# Формат токена: {Хеш USER_ID в SHA256}.{Случайная строка длиной в 30 символов}.{Случайная строка в 200 символов захешированная в SHA256}
# Формат токена: {Хеш USER_ID в SHA256}.{REGISTER_RANDOM_STR_LEN}.{REGISTER_RANDOM_STR_LEN_SHA256}
# Пример токена: 9d252e92e3332e5b8e9733aa1c778901509f453969c3e90ff35b9cbe2a2e9086.0eA67u7yR1ijMIDTO05y.f69d5111b80bf4060168aca185b33b6058c1556e4b488408fff5234f7bf693f7

REGISTER_RANDOM_STR_LEN = 30
REGISTER_RANDOM_STR_LEN_SHA256 = 200