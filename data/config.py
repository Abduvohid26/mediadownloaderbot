from environs import Env
env = Env()
env.read_env()
BOT_TOKEN=env.str('BOT_TOKEN')
BOT_TOKEN="7784958688:AAEQyF-dqMCKRWraVFCDVlcfPQOnVo0uWwI"
# BOT_TOKEN="7113658898:AAG3yuPySdtSkSB9HAuliS3rzwIs7HZ_pUs"
ADMINS=env.list('ADMINS')