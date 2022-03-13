from environs import Env

env = Env()
env.read_env()

PG_HOST = env('PG_HOST', 'localhost')
PG_PORT = int(env('PG_PORT', 5432))
PG_USER = env('PG_USER', 'postgres')
PG_PASSWD = env('PG_PASSWD', 'mysecretpassword')
PG_DATABASE = env('PG_DATABASE', 'postgres')
