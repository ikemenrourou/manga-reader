from flask import Flask, render_template, request, send_from_directory, abort
import os
from urllib.parse import unquote
import webbrowser
import configparser
from waitress import serve  # 导入 waitress

app = Flask(__name__)


config = configparser.ConfigParser()

# 使用 open 函数，指定 utf-8 编码读取配置文件
with open('config.ini', 'r', encoding='utf-8') as f:
    config.read_file(f)

# 获取漫画文件夹路径，确保包含中文路径的正确处理
COMICS_FOLDER = config.get("settings", "comics_folder")

# 输出路径调试
print(f"Comics folder path: {COMICS_FOLDER}")

# 每页显示的漫画数量
COMICS_PER_PAGE = 72

# 获取封面的路由
@app.route("/cover/<path:comic_folder>")
def get_cover(comic_folder):
    # 对 URL 中的路径进行解码，处理特殊字符
    comic_folder = unquote(comic_folder)
    folder_path = os.path.join(COMICS_FOLDER, comic_folder)

    print(f"[DEBUG] Cover Folder Path: {folder_path}")  # 调试输出，检查路径是否正确

    if os.path.isdir(folder_path):
        images = os.listdir(folder_path)
        if images:
            # 确保返回的图片文件经过 URL 编码
            return send_from_directory(folder_path, images[0])

    # 如果找不到封面图片，返回默认封面
    return send_from_directory("static", "default_cover.jpg")


# 主页路由，支持搜索和分页功能
@app.route("/")
def index():
    query = request.args.get("query", "").strip().lower()  # 获取搜索关键字并转小写
    page = max(1, int(request.args.get("page", 1)))  # 获取当前页数，至少为1

    comics = []
    for folder in os.listdir(COMICS_FOLDER):
        folder_path = os.path.join(COMICS_FOLDER, folder)
        if os.path.isdir(folder_path):
            # 过滤文件夹名称，确保搜索关键字与文件夹名称匹配
            if query in folder.lower():
                images = os.listdir(folder_path)
                first_image = images[0] if images else None
                modification_time = os.path.getmtime(folder_path)

                comics.append(
                    {
                        "title": folder,
                        "cover_url": f"/cover/{folder}",  # 封面图片的路径
                        "modification_time": modification_time,
                    }
                )

    # 按修改时间降序排列
    comics = sorted(comics, key=lambda x: x["modification_time"], reverse=True)

    # 计算分页
    total_comics = len(comics)
    start = (page - 1) * COMICS_PER_PAGE
    end = start + COMICS_PER_PAGE
    has_next_page = end < total_comics

    # 获取当前页的漫画
    comics = comics[start:end]

    return render_template(
        "index.html", comics=comics, query=query, page=page, has_next_page=has_next_page
    )


# 阅读页面路由
@app.route("/read/<path:comic_name>")
def read_comic(comic_name):
    # 对 URL 中的 comic_name 进行解码，处理空格和特殊字符
    comic_name = unquote(comic_name)
    folder_path = os.path.join(COMICS_FOLDER, comic_name)

    # 检查路径是否存在
    if os.path.isdir(folder_path):
        images = sorted(os.listdir(folder_path))
        image_urls = [f"/image/{comic_name}/{image}" for image in images]
        return render_template("read.html", images=image_urls, title=comic_name)

    # 如果路径不存在，返回 404 错误
    return "Comic not found", 404


# 获取漫画图片的路由
@app.route("/image/<path:comic_name>/<filename>")
def get_image(comic_name, filename):
    # 对 URL 中的文件名和文件夹名进行解码，处理特殊字符
    comic_name = unquote(comic_name)
    filename = unquote(filename)
    folder_path = os.path.join(COMICS_FOLDER, comic_name)

    # 检查路径和文件是否存在
    if os.path.isdir(folder_path) and os.path.isfile(
        os.path.join(folder_path, filename)
    ):
        return send_from_directory(folder_path, filename)

    # 如果文件不存在，返回 404 错误
    abort(404, description="Image not found")


# 启动应用
if __name__ == "__main__":
    port = 5000
    url = f"http://127.0.0.1:{port}"
    webbrowser.open(url)
    serve(app, host='0.0.0.0', port=port, threads=8)
