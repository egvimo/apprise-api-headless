import os
from functools import lru_cache
from typing import Optional

from apprise import Apprise, AppriseConfig


@lru_cache
def get_apprise_instance(config_dir: str, config_key: str) -> Optional[Apprise]:
    apobj = Apprise()
    config = AppriseConfig()

    if not os.path.isdir(config_dir):
        return None

    config_path = None
    for ext in ["yml", "yaml"]:
        candidate_path = os.path.join(config_dir, f"{config_key}.{ext}")
        if os.path.isfile(candidate_path):
            config_path = candidate_path
            break

    if config_path is None:
        return None

    config.add(config_path)
    apobj.add(config)

    return apobj
