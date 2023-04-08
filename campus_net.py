# -*- coding: utf-8 -*-
import re
from typing import Optional
from urllib.parse import quote

import httpx

from config import USER_AGENT


def get_host_query(portal_url: str):
    match_result = re.match(r"http://(.+?)/.*?\?(.+)", portal_url)
    if match_result is None:
        raise ValueError("Invalid portal url")
    return match_result.groups()


class CampusNet:
    def __init__(self, client: Optional[httpx.Client] = None) -> None:
        if client is None:
            self.client = httpx.Client(
                headers={"User-Agent": USER_AGENT},
                verify=False,
                follow_redirects=True,
            )
        else:
            self.client = client

    def get_portal_url(self):
        try:
            resp = self.client.get("http://123.123.123.123", timeout=5)
        except httpx.TimeoutException:
            raise Exception("Cannot get portal url: timeout")
        resp.raise_for_status()

        url = re.search(r"href='(.*?)'", resp.text)
        if url is None:
            raise Exception("Cannot get portal url: cannot find url")
        return url.group(1)

    def get_services(self, portal_url: str):
        host, query_string = get_host_query(portal_url)
        resp = self.client.post(
            f"http://{host}/eportal/InterFace.do?method=pageInfo",
            data={"queryString": query_string},
        )
        resp.raise_for_status()
        return resp.json()["service"]

    def login_service(self, portal_url: str, user_id: str, service: str):
        host, query_string = get_host_query(portal_url)
        resp = self.client.post(
            f"http://{host}/eportal/InterFace.do?method=loginOfCas",
            data={
                "userId": user_id,
                "flag": "casauthofservicecheck",
                "service": quote(service),
                "queryString": query_string,
                "operatorPwd": "",
                "operatorUserId": "",
                "passwordEncrypt": "false",
            },
        )
        resp.raise_for_status()

        data = resp.json()
        if data["result"] != "success":
            raise Exception(data["message"])
