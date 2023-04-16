from pathlib import Path
import pytomlpp

from conf.config import Config

config_name = "config.toml"

cfg = Config(**pytomlpp.loads(Path(config_name).read_text(encoding="utf-8")))
