from environs import Env
env = Env()
env.read_env()
BOT_TOKEN=env.str('BOT_TOKEN')
# BOT_TOKEN="7113658898:AAGJmbRcFnoef7CRDIQRnnJ-yDGqd_s-9Cc"
ADMINS=env.list('ADMINS')
GET_TOKEN_URL=env.str("GET_TOKEN_URL")