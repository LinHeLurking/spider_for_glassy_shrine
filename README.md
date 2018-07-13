# spider_for_glassy_shrine
a spider that can crawl glassy shrine automatically

configure.py will install dependencies.
cause on windows deivces installation of twisted via pip3 always fails,so in this script twisted is installed via easy_install

run llss_start.py after install the dependencies and it will ask you for a date to stop.
any posts before the date you input will not be crawled.
resultes are stored in the same folder.
the folder nemed abstract stores the abstract in txt tiles with date and title as their names.
image folder stores the images.

# 中文说明
一个可以自动爬取琉璃神社的爬虫程序

使用说明：

第一次运行之前通过python运行configure.py将自动安装相关依赖
由于在Windows机器上通过pip3安装twisted总是失败所以通过easy_install安装

运行llss_start.py即开始主程序，会提示输入一个停止日期，表示早于输
入日期的内容将不会被抓取。有关日期判断有一个已知的小问题，详见
known_bugs.txt

爬取的结果将会保存在本地文件夹内，abstract文件夹将保存抓取的文本内容，
并自动识别其中的磁力链接，补全前缀后保存在对应文本的最前部分，image文
件夹中将保存抓取得到的预览图，可以自己去看看画风喜不喜欢(w
