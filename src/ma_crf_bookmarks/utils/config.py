import os
from typing import Literal, Optional

import yaml
from pydantic import BaseModel, Field


class UIConfig(BaseModel):
    min_width: int = Field(default=800, ge=600, description="Screen width in pixels")
    min_height: int = Field(default=400, ge=400, description="Screen height in pixels")
    hide_terminal: bool = Field(default=True, description="Hide Terminal")
    dev_mode: bool = Field(default=False, description="Set true for development")


class LoggerConfig(BaseModel):
    active: bool = Field(default=True, description="Active logging")
    level: Literal["WARN", "INFO", "ERROR"] = Field(
        default="WARN", description="Select logger level"
    )
    folder: str = Field(default="log", description="Folder to place the logs")


class UserSetting(BaseModel):
    folder: Optional[str] = Field(default=None, description="Path to user folder")


class BookMarkSetting(BaseModel):
    default_dir: str = Field(default=".", description="Default dir to search for aCRF")


class ConfigModel(BaseModel):
    userInterface: UIConfig = Field(default=UIConfig())
    userSetting: UserSetting = Field(default=UserSetting())
    logging: LoggerConfig = Field(default=LoggerConfig())
    bookmark: BookMarkSetting = Field(default=BookMarkSetting())


def load_config(path: str = "template-config.yml") -> tuple[ConfigModel, str]:
    """load configuration file. Use default paths or a default configuration

    Args:
        path (str, optional): path to config file

    Returns:
        tuple[ConfigModel, str]: configuration file and the config path used
    """
    default1 = "template-config.yml"

    # test if config file is available
    if os.path.exists(path):
        pass
    elif os.path.exists(default1):
        path = default1
    else:
        return ConfigModel(), "default config"

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return ConfigModel(**data), path
