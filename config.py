# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv

load_dotenv()


def e(key, default=None, *, required=False):
    if required and key not in os.environ:
        raise ValueError(f"Environment variable {key} is required")
    return os.environ.get(key, default)


USER_AGENT = e(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
)

SSO_USERNAME = e("SSO_USERNAME", required=True)
SSO_PASSWORD = e("SSO_PASSWORD", required=True)

CAMPUSNET_SERVICE = e("CAMPUSNET_SERVICE", required=True)

CHECK_INTERVAL = int(e("CHECK_INTERVAL", "60"))
START_DELAY = int(e("START_DELAY", "10"))
DEBUG = e("DEBUG", "false").lower() in ("true", "1", "yes")
