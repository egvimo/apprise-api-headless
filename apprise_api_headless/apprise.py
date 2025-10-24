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
    # Ensure config_key does not escape config_dir via path traversal
    for ext in ["yml", "yaml"]:
        candidate_path = os.path.join(config_dir, f"{config_key}.{ext}")
        norm_candidate_path = os.path.normpath(os.path.abspath(candidate_path))
        norm_config_dir = os.path.normpath(os.path.abspath(config_dir))
        if not norm_candidate_path.startswith(norm_config_dir + os.sep):
            continue
        if os.path.isfile(norm_candidate_path):
            config_path = norm_candidate_path
            break

    if config_path is None:
        return None

    config.add(config_path)
    apobj.add(config)

    return apobj
