## 记账

### 收入
| 日期       | 金额   | 名目         |
| :-------- | :----- | :---------- |
| 20170908  | 1000   | 订金         | 
| 20170921  | 2000   | 第2笔费用     | 

### 支出
| 日期       | 金额   | 名目         |
| :-------- | :----- | :---------- |
| 20170908  | 408.7  | 域名注册5年   | 

## 功能设计
- ![Design.jpeg](https://raw.githubusercontent.com/wu-wenxiang/Media-WebLink/master/qiniu/67aeafbf0acb4fddb44ed40ea0c564e3-Design.jpeg)
- ![Design2.jpeg](https://raw.githubusercontent.com/wu-wenxiang/Media-WebLink/master/qiniu/67aeafbf0acb4fddb44ed40ea0c564e3-Design2.jpeg)

## 网站
- [Demo](http://www.gaoyumedia.net)


## 开发
- 本地环境
	- Mac/Linux/Unix
		- 本地运行：`.\start.sh`
		- 本地测试：`.\run_test.sh`
	- Windows:
		- 本地运行：`.\start.bat`
		- 本地测试：`.\run_test.bat`
- 部署到生产环节
	- Config: copy `.fabricrc` to `fabricrc`, config it
	- Init: `fab -c fabricrc init_deploy_u1604`
	- Re-Deploy: `fab -c fabricrc deploy`
	- 升级数据库后，不知何故，有时候migrations目录中的0*文件删不干净，需要手动清理：
		- `rm -rf "${BASE_DIR}/mysite/account/migrations/0*"`
		- 然后在`./start.sh`就好了
- 超级管理员
	- `initdb.py`
	- `admin`, `56e1E@ab1234`
	- `op1`, `1E@ab1234`
	- `cx1`, `@aB1234`

## 坑
- i18n
	- settings文件中写zh-Hans，locale目录中文件夹名字必须是下划线，zh_Hans
	- 启动目录必须是Project根目录，supervior的配置文件亦然
	- ubuntu上要安装gettext: `sudo apt-get install gettext`，mac亦然: `brew install gettext`
	- Mac上面：`$ brew link gettext --force`
	
			Linking /usr/local/Cellar/gettext/0.19.8.1... 185 symlinks created
			If you need to have this software first in your PATH instead consider running:
			echo 'export PATH="/usr/local/opt/gettext/bin:$PATH"' >> ~/.bash_profile
- 参考
	- [ybdesire/WebLearn](https://github.com/ybdesire/WebLearn)
	- [本地化／国际化](http://www.cnblogs.com/oubo/archive/2012/04/05/2433690.html)
		- LocaleMiddleware 按照如下算法确定用户的语言:
			- 首先，在当前用户的 session 的中查找django_language键；
			- 如未找到，它会找寻一个cookie
			- 还找不到的话，它会在 HTTP 请求头部里查找Accept‐Language， 该头部是你的浏览器发送的，并且按优先顺序告诉服务器你的语言偏好。 Django会尝试头部中的每一个语种直到它发现一个可用的翻译。
			- 以上都失败了的话, 就使用全局的 LANGUAGE_CODE 设定值。
		- Django使用以下算法寻找翻译：
			- 首先，Django在该视图所在的应用程序文件夹中寻找 locale 目录。 若找到所选语言的翻译，则加载该翻译。
			- 第二步，Django在项目目录中寻找 locale 目录。 若找到翻译，则加载该翻译。
			- 最后，Django使用 django/conf/locale 目录中的基本翻译。

## Backlog
- restful API
- i18n，要可以切换中英文
- 404页面
    - 弄好看点的404，403，500，这个不重要，晚点弄好了
