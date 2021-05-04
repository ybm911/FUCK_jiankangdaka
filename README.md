# FUCK_jiankangdaka
auto punch a card for 简道云
[文档说明](http://spacey.top/2020/07/12/%E8%87%AA%E5%8A%A8%E5%81%A5%E5%BA%B7%E6%89%93%E5%8D%A1%EF%BD%9CFUCK-jiankangdaka/)

使用前安装 PyYaml 库

` python3 -m pip install PyYaml`

目前一些信息需要自己填写在 `config.yaml` 中：

* 编号
* X-CSRF-Token
* Cookie
* 高德地图 API 的 key（可选，作用是获取位置和经纬度，高德给 eli0t 的 API 使用配额应该足够学校所有人打卡。调用量上限（次/日）300000、并发量上限（次/秒）200）

API 调用：

* 高德 API
* ipify API

#### 位置信息

位置信息是通过使用者 IP (ipify API)，结合高德 API 获取的，所以会有很大误差。而且当使用者开了代理，位置会直接变为代理服务器位置。

使用者可以通过参数 `-c` 使用自己在 `config.yaml` 中配制的的准确位置或者使用参数 `-i` 使用当前 `ip` 所在位置。

Demo:
由于当前日期已经提交，所以提交结果显示提交值重复
```shell
~$ python3 auto_punch_a_card.py -c
INFO:root: ** Get ready **
INFO:root: ** 详细位置获取经纬度开始 **
 当前经度（通过详细地址获取）：xxx.xxxxxx00000001
 当前纬度（通过详细地址获取）：xxx.xxxxxx000000001
200
200
200
200
200
200
200
 get if seccess 200
200
INFO:root: all ready to start !
 get number xxxxx
 get name xxx
 get name 2 xxx
 get sex x
 get telephone 189****6699
 get sdept 安xxxx
 get specialty 网络xxxxx
 get class 18xx
 get address 江西省xxxxxxxxxxxxxxxx
INFO:root: 信息全部获取完毕
INFO:root: ** Wait five seconds **
 push data {"code":4002,"msg":"提交值重复","meta":{"repeatFields":{"_widget_1581559576367":"18***********4"}}}
```

```shell
～$ python3 auto_punch_a_card.py -i
INFO:root: ** Get ready **
INFO:root: ** 位置通过 IP 获取开始 **
 当前 IP ：52.229.174.79
 当前城市（通过 IP 获取）：香港xxxxx
 当前省份（通过 IP 获取）：香港xxxxx
 当前经度（通过 IP 获取）：xxx.6340702
 当前纬度（通过 IP 获取）：xxx.01163526
200
200
200
200
200
200
200
 get if seccess 200
200
INFO:root: all ready to start !
 get number xxxxx
 get name xxx
 get name 2 xxx
 get sex x
 get telephone 189****6699
 get sdept 安xxxx
 get specialty 网络xxxxx
 get class 18xx
 get address 江西省xxxxxxxxxxxxxxxx
INFO:root: 信息全部获取完毕
INFO:root: ** Wait five seconds **
 push data {"code":4002,"msg":"提交值重复","meta":{"repeatFields":{"_widget_1581559576367":"18***********4"}}}
```
