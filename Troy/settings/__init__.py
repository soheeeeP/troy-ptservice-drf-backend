from pathlib import Path

from environs import Env


BASE_DIR = Path(__file__).parent.parent.parent.absolute()
env = Env()
if BASE_DIR.joinpath(".env").is_file():
    Env.read_env(str(BASE_DIR.joinpath(".env")))

RUN_ENV = env("RUN_ENV", "dev")  # dev stage prod

# TODO: 나중에 동적으로 로딩하도록 수정
if RUN_ENV == "prod":
    from .production import *
else:
    from .development import *
