import getpass
import logging
import os

from ma_pytemp.utils.config import ConfigModel


class User:
    def __init__(self, config: ConfigModel, root_dir: str, logger: logging.Logger):

        self.logger = logger
        self.config: ConfigModel = config
        self.root_dir: str = root_dir

        self.user_id: str = self._get_userid()

    def _get_userid(self) -> str:
        user_id = f"{os.environ.get('USERDOMAIN')}\\{getpass.getuser()}".split("\\")[-1]

        if self.logger:
            self.logger.info("SYS  | User: %s", user_id)

        return str(user_id)
