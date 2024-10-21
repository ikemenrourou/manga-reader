# 漫画/图片 web阅读器

- **这是使用AI写的一个非常简单的漫画阅读器 Web 应用程序，使用 Flask 构建。**
- 截止2天前，楼主没有看过1秒钟编程视频，代码编辑器用的还是记事本，纯靠gpt老师
- （AI主要用的是 4O 和 copilot，claude3.5，极少数 o1）

## 便携版

你可以从 [Releases 页面](https://github.com/ikemenrourou/manga-reader/releases) 下载最新的发行版。
下载rar文件，解压缩，修改config.ini文件填入泥的漫画路径，
运行exe。

## 截图

![首页截图](截图/test.jpg)

## 安装

. 安装依赖：
   ```
   pip install -r requirements.txt
   ```


## 使用方法

0. 修改config.ini文件，comics_folder = 填入存放漫画/图片文件的文件夹路径，例如 D:\Comics 或 P:\漫画（注意=后面有空格）

1. 运行应用程序：
   ```
   python app.py
   ```

2. 打开浏览器，访问 `http://localhost:5000`

3. 其他设备访问http://你的运行程序的局域网IP地址:5000（例如http://192.168.1.10:5000）

## 注意事项

- 确保 `config.ini` 中的漫画文件夹路径正确设置
- 漫画文件夹应包含子文件夹，每个子文件夹代表一部漫画，其中包含漫画图片
- 支持常见图片格式（如 JPG、PNG）



## 技术栈

- Python 3
- Flask
- Waitress (WSGI 服务器)
- HTML/CSS

欢迎提交 issue 不过楼主0编程经验大概率没有能力修TAT甚至bug越修越多！大概这个项目不会更新，见谅捏。
