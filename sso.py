# -*- coding: utf-8 -*-
import re
from base64 import b64encode, b64decode
from typing import Optional

from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad
import httpx

from config import USER_AGENT

ERROR_MSG_CODE = {
    "1320009": "验证码有误，请确认后重新输入",
    "1320010": "手机号未绑定用户，请使用其他方式登录",
    "1320011": "用户未绑定过手机号，请使用其他方式登录",
    "1320012": "短信发送服务存在问题，请稍后再试",
    "1320013": "用户名有误，请确认后重新输入",
    "1320033": "手机验证码已过期，请重新获取",
    "1030028": "账号被锁定",
    "1030048": "秒内不能重复获取验证码",
    "9280078": "验证码有误，请确认后重新输入",
    "9280081": "验证码已过期，请重新获取验证码",
    "2040001": "短信发送失败",
    "2040002": "验证码有误，请确认后重新输入",
    "2040003": "验证码有误，请确认后重新输入",
    "2040004": "手机号码不符合规范",
    "1030027": "用户名或密码错误，请确认后重新输入",
    "1030031": "用户名或密码错误，请确认后重新输入",
    "1410041": "当前用户名已失效",
    "1410040": "当前用户名已失效",
    "1320007": "验证码有误，请确认后重新输入",
    "1320010": "手机号未绑定用户，请使用其他方式登录",
    "1320011": "用户未绑定过手机号，请使用其他方式登录",
    "1320012": "短信发送服务存在问题，请稍后再试",
    "1320013": "用户名有误，请确认后重新输入",
    "1030028": "账号被锁定",
    "2040004": "手机号码不符合规范",
    "1030027": "用户名或密码错误，请确认后重新输入",
    "1030031": "用户名或密码错误，请确认后重新输入",
    "1410041": "当前用户名已失效",
    "1410040": "当前用户名已失效",
    "1320007": "验证码有误，请确认后重新输入",
    "1320009": "验证码有误，请确认后重新输入",
    "1320012": "短信发送服务存在问题，请稍后再试",
    "1320013": "用户名有误，请确认后重新输入",
    "1320033": "手机验证码已过期，请重新获取",
    "1030048": "秒内不能重复获取验证码",
    "9280078": "验证码有误，请确认后重新输入",
    "9280081": "验证码已过期，请重新获取验证码",
    "2040001": "短信发送失败",
    "2040002": "验证码有误，请确认后重新输入",
    "2040003": "验证码有误，请确认后重新输入",
}

SSO_IP = "58.192.134.14"
SSO_HOST = "sso.yzu.edu.cn"


def encrypt(croypto, password):
    return b64encode(
        DES.new(b64decode(croypto), DES.MODE_ECB).encrypt(
            pad(password.encode("utf-8"), DES.block_size)
        )
    ).decode("utf-8")


def search_params(id: str, html_text: str) -> str:
    return re.search(rf'<p id="{id}">(.*?)</p>', html_text).group(1)


class SSO:
    def __init__(self, client: Optional[httpx.Client] = None) -> None:
        if client is None:
            self.client = httpx.Client(
                headers={"User-Agent": USER_AGENT},
                verify=False,
                follow_redirects=True,
            )
        else:
            self.client = client

    def get_login_params(self, service: Optional[str] = None):
        resp = self.client.get(
            f"https://{SSO_HOST}/login",
            params={"service": service},
            headers={"Host": SSO_HOST},
        )
        resp.raise_for_status()
        html = resp.text
        return {
            "execution": search_params("login-page-flowkey", html),
            "croypto": search_params("login-croypto", html),
        }

    def login(self, username: str, password: str, service: Optional[str] = None):
        params = self.get_login_params(service)
        resp = self.client.post(
            f"https://{SSO_HOST}/login",
            data={
                "username": username,
                "type": "UsernamePassword",
                "_eventId": "submit",
                "geolocation": "",
                "execution": params["execution"],
                "croypto": params["croypto"],
                "password": encrypt(params["croypto"], password),
            },
            headers={"Host": SSO_HOST},
        )

        if resp.status_code == 401:
            html = resp.text
            error_code = re.search(
                r'<div[^>]*?id="login-error-msg"[^>]*?>\s*<span>(.*?)</span>',
                html,
                re.DOTALL,
            )
            if error_code is None:
                raise Exception("Unknown error")
            if error_code.group(1) not in ERROR_MSG_CODE:
                error_code = error_code.group(1)
                raise Exception(f"Unknown error code: {error_code}")
            raise Exception(ERROR_MSG_CODE[error_code.group(1)])
        resp.raise_for_status()
