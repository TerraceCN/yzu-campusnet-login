# YZU CampusNet Login

扬州大学校园网登录器

## 简介

就是一个简单的登录校园网的脚本，可以用Docker挂着自动登录校园网。

截至2023/04/03开发完成时有效。

## 用法

首先设置环境变量或者添加`.env`文件，环境变量定义如下：

|变量名|描述|默认值|
|-|-|-|
|USER_AGENT|模拟访问所用的UA|见`config.py`|
|SSO_USERNAME|统一身份认证系统的用户名|-|
|SSO_PASSWORD|统一身份认证系统的密码|-|
|CAMPUSNET_SERVICE|校园网服务名|-|
|CHECK_INTERVAL|检测是否联网的时间间隔（秒）|60|
|DEBUG|调试模式（忽略是否已经连网）|False|

可用的校园网服务（依旧是截至开发完成时间）：

- 学校互联网服务
- 移动互联网服务
- 联通互联网服务
- 电信互联网服务
- 免费校内服务

### 命令行

```shell
pip install -r requirements.txt
python main.py
```

运行时出错的话会卡死，以防止脚本不断尝试重连而产生意料之外的问题，请检查日志排除错误后再试。

操作成功后脚本并不会自动退出，而是会每隔60秒检测一下是否联网，断网会重连。


### Docker

先构建镜像

```shell
docker build -t yzu_campusnet_login .
```

然后开启容器

```shell
docker run \
    -d \
    --name yzu_campusnet_login \
    -e SSO_USERNAME=<你的统一身份认证用户名> \
    -e SSO_PASSWORD=<你的统一身份认证密码> \
    -e CAMPUSNET_SERVICE=<校园网服务名> \
    --restart always \
    yzu_campusnet_login
```

或使用`.env`文件保存环境变量

```shell
docker run \
    -d \
    --name yzu_campusnet_login \
    -v ./.env:/app/.env \
    --restart always \
    yzu_campusnet_login
```

## 免责说明

YZU Campus Login（以下简称“本脚本”）为便于作者个人生活的脚本，本脚本所用的方法均为对正常登录过的模拟，不得用于任何商业用途。

本脚本之著作权归脚本作者所有。用户可以自由选择是否使用本脚本。如果用户下载、安装、使用本脚本，即表明用户信任该脚本作者，脚本作者对因使用项目而造成的损失不承担任何责任。
