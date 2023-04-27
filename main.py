# -*- coding: utf-8 -*-
import time

from loguru import logger
import httpx

from config import *
from campus_net import CampusNet
from sso import SSO


def test_connection() -> bool:
    try:
        return (
            httpx.get("http://connect.rom.miui.com/generate_204", timeout=5).status_code
            == 204
        )
    except Exception as e:
        return False


connected = False
while True:
    if not DEBUG and test_connection():
        if not connected:
            logger.info("You have connected to the Internet")
            connected = True
        time.sleep(CHECK_INTERVAL)
        continue
    connected = False

    logger.info(f"Start login in {START_DELAY}s...")
    time.sleep(START_DELAY)

    logger.info(
        f"Username: {SSO_USERNAME}, Password: {SSO_PASSWORD}, Service: {CAMPUSNET_SERVICE}"
    )

    client = httpx.Client(
        headers={
            "User-Agent": USER_AGENT,
        },
        verify=False,
        follow_redirects=True,
    )
    campus_net = CampusNet(client)
    sso = SSO(client)

    try:
        portal_url = campus_net.get_portal_url()
        logger.info("Portal url: {}", portal_url)
    except Exception as e:
        logger.exception("Failed to get portal url")
        continue

    try:
        sso.login(SSO_USERNAME, SSO_PASSWORD, portal_url)
        logger.info("Login SSO success")
    except Exception as e:
        logger.exception("Failed to login SSO")
        continue

    try:
        services = campus_net.get_services(portal_url)
        logger.info(f"Get services: {', '.join(services.keys())}")
    except Exception as e:
        logger.exception("Failed to get services")
        continue

    if CAMPUSNET_SERVICE not in services:
        logger.error(f"{CAMPUSNET_SERVICE} is not an available service!")

    try:
        campus_net.login_service(portal_url, SSO_USERNAME, CAMPUSNET_SERVICE)
        logger.info("Login service success")
    except Exception as e:
        logger.exception("Failed to login services")
        continue
