import requests
import os
import time
import tkinter as tk
from snownlp import SnowNLP
import chardet
import re
import json
import xlwt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
# 结巴分析
import jieba.analyse
# 词云
from wordcloud import WordCloud
# 读取图片
from matplotlib.image import imread
# 获取图片像素值
from wordcloud import ImageColorGenerator
# 忽略警告信息
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

warnings.filterwarnings('ignore')

# 解决画图时出现的中文乱码问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 请求头
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
}


def get_search(keyword,max_page,out_file):

    #循环遍历每一页
    for page in range(1,max_page+1):
        url = 'https://api.bilibili.com/x/web-interface/wbi/search/type'
        #请求头部信息
        headers = {'Accept':'application/json, text/plain, */*',
                   'Accept-Encoding':'gzip, deflate, br',
                   'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                   'Cookie':"i-wanna-go-back=-1; buvid_fp_plain=undefined; blackside_state=0; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO5316570218767173; fingerprint3=b0e52d915ce07bd389376c6de48c660b; b_ut=5; DedeUserID=1316489550; DedeUserID__ckMd5=64517466436da821; buvid4=5CD7E787-FAC6-E95E-7BA2-F0C82592887130716-022061619-WEPh3cauru8b1JCxP5mEm3KHPtq6%2BCAeZ%2FhZwuYUcM%2BfVO2um8i%2B1g%3D%3D; rpdid=|(u)~m~J~|uY0J'uYY))k|R)~; hit-new-style-dyn=0; hit-dyn-v2=1; is-2022-channel=1; _ga=GA1.1.707183765.1675571602; _ga_JTP03JY54M=GS1.1.1675571601.1.1.1675573082.0.0.0; CURRENT_QUALITY=80; CURRENT_PID=76e2a150-cb8b-11ed-97a6-611ea7a615fa; FEED_LIVE_VERSION=V8; buvid3=BAF434BC-3670-0E22-D701-05631655CDB898847infoc; b_nut=1687233898; _uuid=BB57DDA6-1FC2-1FB9-3E69-B10210EE2103E2B88066infoc; header_theme_version=CLOSE; home_feed_column=5; CURRENT_FNVAL=4048; PVID=1; fingerprint=d9527af159731671543912e3ededee94; buvid_fp=d9527af159731671543912e3ededee94; SESSDATA=b24f5462%2C1703982027%2C0de7c%2A72dnbgwT0uJQigAfeNq0itQoyKFzNbaY2B7_QsekDtH4XCAmWIXU3JkePwZxhN9igCScPlUAAAMgA; bili_jct=1db3d9d61d3a3fd82b29599dcae1f780; innersign=0; b_lsid=C7FAAB108_18928DC682E; sid=5df1f29r; browser_resolution=1652-963; bp_video_offset_1316489550=815036655075328000",
                   'Origin':'https://search.bilibili.com',
                   'Referer':'https://www.bilibili.com/',
                   'Sec-Ch-Ua':'"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
                   'Sec-Ch-Ua-Mobile':'?0',
                   'Sec-Ch-Ua-Platform':'"Windows"',
                   'Sec-Fetch-Dest':'empty',
                   'Sec-Fetch-Mode':'cors',
                   'Sec-Fetch-Site':'same-site',
                   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',}
        #请求参数
        params = {
        "__refresh__": 'true',
        '_extra':'',
        'context':'',
        'page': page,
        'page_size': 1,
        'from_source':'',
        'from_spmid': '333.337',
        'platform': 'pc',
        'highlight': '1',
        'single_column': '0',
        'keyword': keyword,
        'qv_id': 'IOR0RRf4f9v7uPCtYKkpAMvR5yyK7YuK',
        'ad_resource': '5654',
        'category_id':'',
        'search_type': 'video',
        'dynamic_offset': '30',
        'preload':'true',
        'com2co':'true',
        }
        #发送GET请求
        r = requests.get(url=url,headers=headers,params=params)
        j_data = r.json()
        data_list = j_data['data']['result']
        bvid_list = []
        for data in data_list:
            bvid_list.append(data['bvid'])
        bvids = ','.join(bvid_list)
        return bvids


        #创建DataFrame并保存到CSV文件
        # df = pd.DataFrame(
        #     {'BV号':bvid_list,}
        # )
        # csv_header = ['BV号']
        # if os.path.exists(out_file):
        #     headers = None
        # else:
        #     headers = csv_header
        # df.to_csv(out_file,encoding='utf_8_sig',mode='a+',index=False,header=headers)
# 数据存储函数
def write_to_excel(words, filename, sheet_name='sheet1'):
    '''
    将item存储到excel中。
    :param words: 保存item的list    [{},{}]格式
    :return:
    '''
    try:
        # 1、创建工作薄
        work_book = xlwt.Workbook(encoding='utf-8')
        # 2、创建sheet表单
        sheet = work_book.add_sheet(sheet_name)
        # 3、写表头
        # head = ['英文','中文']
        head = []
        for k in words[0].keys():
            head.append(k)

        for i in range(len(head)):
            sheet.write(0, i, head[i])
        # 4、添加内容
        # 行号
        i = 1
        for item in words:
            for j in range(len(head)):
                sheet.write(i, j, item[head[j]])
            # 写完一行，将行号+1
            i += 1
        # 保存
        work_book.save(filename)
        print('写入excel成功！')

    except Exception as e:
        print('写入excel失败！', e)


# 获取视频的cid
def get_cid(bvid):
    # API地址
    API = 'https://api.bilibili.com/x/player/pagelist'

    # 参数
    params = {
        'bvid': bvid,
        'jsonp': 'jsonp',
    }

    # 发起请求
    response = requests.get(url=API, headers=headers, params=params)

    # 网页源代码
    html = response.text

    # html文档转换为字典
    dict = json.loads(html)

    result = dict["data"][0]["cid"]

    return result


# 爬取B站视频弹幕
def get_barrage(cid):
    # API地址
    API = 'https://api.bilibili.com/x/v1/dm/list.so'

    # 参数
    params = {
        'oid': cid,
    }

    # 发起请求
    response = requests.get(url=API, headers=headers, params=params)

    # 网页源代码编码
    response.encoding = chardet.detect(response.content)['encoding']

    # 网页源代码
    html = response.text

    # 正则表达式预编译
    pattern = re.compile(r'<d p="(.*?)">(.*?)</d>')

    # 正则表达式数据解析
    result = pattern.findall(html)

    # 存放数据容器
    words = []

    # 计数器
    count = 0

    for item in result:
        count += 1

        info = item[0].split(',')
        # 出现时间
        appear_time = info[0]
        # 类型
        type = info[1]
        # 字号
        font_size = info[2]
        # 字体颜色
        font_color = info[3]
        # 发送时间
        send_time = info[4]
        # 弹幕池
        pool = info[5]
        # 作者
        author_id = info[6]
        # 数据库记录
        database_id = info[7]
        # 弹幕内容
        content = item[1]

        words.append({
            'atime': appear_time,
            'type': type,
            'font_size': font_size,
            'font_color': font_color,
            'send_time': send_time,
            'pool': pool,
            'author_id': author_id,
            'database_id': database_id,
            'content': content,
        })

        print('第{}条数据解析完成'.format(count))

    # 保存数据
    write_to_excel(words=words, filename='danmu.xls', sheet_name='danmu')


# 1.弹幕内容分析 -- 词云图
def content_analysis(data):
    # 弹幕内容列表
    content_list = data['content'].tolist()

    # 列表数据转成字符串数据
    content = ''.join(content_list)

    # 去除空行及空白字符
    text = re.sub(r'[\n\s\t]', '', content)

    # 读取图片模板
    back_img = imread("back.jpg")

    # 生成图片的像素值
    img_colors = ImageColorGenerator(back_img)

    # 使用结巴分析提取标签

    tags = jieba.analyse.extract_tags(text, topK=600, withWeight=True, allowPOS=('n', 'vn', 'v'))

    # tags是数组形式，把数组转为词频字典
    cloud_data = {item[0]: item[1] for item in tags}

    word_cloud = WordCloud(
        # 字体，本电脑c盘下的黑体，这样才能显示中文
        font_path="c:\windows\Fonts\simhei.ttf",
        # 图片的背景颜色
        background_color="white",
        # 字体个数，不超过上面选取的个数
        max_words=500,
        # 字体大小
        max_font_size=35,
        # 图片像素宽
        width=2500,
        # 使用图片模板，上面读取图片的像素
        mask=back_img,
        # 图片像素高
        height=1080,
    ).generate_from_frequencies(cloud_data)  # 传入上面的词频结果

    # 替换默认的字体颜色
    sub_color = word_cloud.recolor(color_func=img_colors)

    # 创建一个图形实例，设置画布大小
    plt.figure(figsize=(25, 25))

    # 插值='双线性'
    plt.imshow(sub_color, interpolation='bilinear')

    # 不显示坐标尺寸
    plt.axis("off")

    # 保存图片
    word_cloud.to_file('E:\\pachong\\static\\images\\弹幕词云.png')

    # 展示图片
    #plt.show()


# 2.弹幕发送者分析 -- 水平条形图
def author_analysis(data):
    # 统计每个发送者的弹幕数，取前十名
    counts = data['author_id'].value_counts()[:10]

    # 发送者id列表
    y = counts.index.tolist()
    # 对应弹幕个数列表
    x = counts.values.tolist()

    # 创建图
    fig = plt.figure(figsize=(15, 8))

    # facecolor颜色
    # tick_label：y轴各条名称
    b = plt.barh(y=y, width=x, tick_label=y, facecolor='#CF9E9E')

    # 使y轴字体倾斜25度
    plt.yticks(rotation=25, fontsize=12)

    # x轴标签
    plt.xlabel('发送弹幕数', fontsize=15)

    # 设置图例
    plt.legend(['发送者'])

    # 设置标题
    plt.title('TOP10发送弹幕排名', fontsize=15, color='#613030')

    # 为横向水平的柱图右侧添加数据标签
    for rect in b:
        w = rect.get_width()
        plt.text(w, rect.get_y() + rect.get_height() / 2, '%d' % int(w), ha='left', va='center', fontsize=11)

    # 保存图片
    plt.savefig('E:\\pachong\\static\\images\\TOP10发送弹幕量排名.png')

    # 展示图片
    #plt.show()


# 3.弹幕颜色分析 -- 饼图
def color_analysis(data):
    # 统计每个类别的电影数，取前五名的类型
    counts = data['font_color'].value_counts()[: 5]

    # 弹幕颜色列表
    x = counts.index.tolist()

    # 对应个数列表
    y = counts.values.tolist()

    # 弹幕颜色占比列表
    percentage = list(map(lambda i: i / np.sum(y), y))

    # 创建图
    fig = plt.figure(figsize=(15, 6))

    # 指定分离饼图中的哪一块区域
    explode = [0.1, 0, 0, 0, 0]

    # 定义饼图区域颜色
    color = []
    # 将爬取到的十进制颜色码转换为十六进制颜色码
    for decimal_color in x:
        hexadecimal = hex(decimal_color)
        hexadecimal = '#' + hexadecimal[2:].upper()

        while len(hexadecimal) < 7:
            hexadecimal = hexadecimal[0] + '0' + hexadecimal[1:]

        color.append(hexadecimal)

    # %.2f%%:表示小数点后2位
    # shadow=True设置阴影特效
    plt.pie(percentage, labels=color, autopct='%.2f%%', colors=color, explode=explode, shadow=True,wedgeprops={'alpha': 0.5})

    # 设置标题
    plt.title('TOP5弹幕颜色占比', fontsize=15)

    # 设置图例
    plt.legend(color, fontsize=14)

    # 避免图片比例压缩为椭圆
    plt.axis('equal')

    # 保存图片
    plt.savefig('E:\\pachong\\static\\images\\TOP5弹幕颜色占比.png')

    # 展示图片
    #plt.show()


# 4.弹幕发送时间分析 -- 密度图
def atime_analysis(data):
    # 弹幕出现在视频中的时间列表
    atime = data['atime'].tolist()

    time = []

    # 把时间单位改为分
    for item in atime:
        time.append(int(item / 60))

    # 采用DataFrame的plot方法实现可视化，画出密度图
    df = pd.DataFrame(time)
    df.plot(kind='kde', label='弹幕密度', grid=True)

    # 设置标题
    plt.title('视频弹幕密度')

    # 设置x轴标签
    plt.xlabel('时间/分')

    # 设置y轴标签
    plt.ylabel('百分比')

    # 设置图例
    plt.legend(['弹幕密度'])

    # 限制x轴长度
    plt.xlim(0, )

    # 保存图片
    plt.savefig('E:\\pachong\\static\\images\\弹幕密度图.png')

    # 展示图片
    #plt.show()
def sentiment_analyse(data):
    content_list = data['content'].tolist()

    # 列表数据转成字符串数据
    #content = ''.join(content_list)

    # 去除空行及空白字符
    #text = re.sub(r'[\n\s\t]', '', content)
    '''情感分析'''
    score_list = []
    tag_list = []
    positive_count = 0
    negative_count = 0
    atime = data['atime'].tolist()

    time = []

    # 把时间单位改为分
    for item in atime:
        time.append(item / 60)
    for comment in content_list:
        tag = ''  # 情感标签
        sentiment_score = SnowNLP(comment).sentiments  # 使用SnowNLP进行情感分析，得到情感得分
        if sentiment_score < 0.3:
            tag = '消极'  # 情感得分小于0.3为消极评论
            negative_count += 1
        else:
            tag = '积极'  # 情感得分大于等于0.3为积极评论
            positive_count += 1
        score_list.append(sentiment_score)  # 将情感得分添加到列表中
        tag_list.append(tag)  # 将情感标签添加到列表中
    df = pd.DataFrame({'弹幕时间': time, '情感得分': score_list, '分析结果': tag_list})  # 创建DataFrame存储数据
    df.to_excel('情感分析结果.xlsx', index=None)  # 将DataFrame保存到Excel文件中，不包含索引
    df = df.sort_values(by='弹幕时间')  # 你的列名指的是你想要按照排序的列名
    #得分
    # 制作曲线图

    x = df.iloc[:, 0]  # 第一列数据作为x轴
    y = df.iloc[:, 1]  # 第二列数据作为y轴

    # 制作曲线图
    plt.scatter(x, y)
    plt.xlabel('时间/分钟')
    plt.ylabel('情感得分')
    plt.title('弹幕情感得分随时间变化图')
    plt.savefig('E:\\pachong\\static\\images\\弹幕情感得分随时间变化图.png')
    #plt.show()
    #饼状图
    labels = ['消极', '积极']
    sizes = [negative_count, positive_count]  # 这里填入消极和积极评论的数量
    colors = ['red', 'green']  # 消极评论用红色，积极评论用绿色表示
    explode = (0.1, 0)  # 突出显示消极评论部分

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # 确保绘制的饼图是圆形的

    plt.savefig('E:\\pachong\\static\\images\\情感分析饼状图.png')  # 保存饼状图为PNG文件
    #plt.show()  # 显示饼状图
    df['弹幕时间'] = df['弹幕时间'].astype(int)  # 将时间转换为整数进行分组
    average_scores = df.groupby('弹幕时间')['情感得分'].mean()
    plt.figure(figsize=(10, 6))
    plt.plot(average_scores, marker='o')
    plt.title('每分钟情感得分均值')
    plt.xlabel('分钟')
    plt.ylabel('情感得分均值')
    plt.grid(True)
    plt.savefig('E:\\pachong\\static\\images\\每分钟情感得分均值随时间变化曲线图.png')
from flask import Flask, render_template ,request
import os
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>B站弹幕分析系统</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <style>
        body {
            background-color: #f7f7f7;
            font-family: 'Arial', sans-serif;
        }
        .search-container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .search-container h1 {
            text-align: center;
            color: #333;
        }
        .search-box {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .search-input {
            flex-grow: 1;
            border: 1px solid #ddd;
            padding: 10px;
            margin-right: 5px;
            border-radius: 5px;
        }
        .search-button {
            border: none;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }
        .search-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="search-container">
        <h1>欢迎来到B站弹幕分析系统</h1>
        <form method="POST" action="/submit" class="search-box">
            <input type="text" name="param1" placeholder="输入视频名称" class="search-input">
            <input type="submit" value="搜索" class="search-button">
        </form>
    </div>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.0.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
</body>
</html>


    '''

@app.route('/submit', methods=['POST'])
def submit():
    keyword = request.form.get('param1')
    solve(keyword)
    print(keyword)
    #获取本机图片文件的路径
    image_folder = 'E:\\pachong\\static\\images'  # 修改为你的图片文件夹路径
    images = os.listdir(image_folder)

    # 将图片列表传递给HTML模板
    return render_template('index.html', images=images)

def solve(keyword):
    max_page = 1
    result_file = 'b站视频_{}_前{}页.csv'.format(keyword, max_page)
    bvid = get_search(keyword=keyword.encode('utf-8'),
                      max_page=max_page,
                      out_file=result_file)
    # 根据搜索结果加载图片界面
    # 1.数据爬取
    cid = get_cid(bvid)
    get_barrage(cid)
    data = pd.read_excel('danmu.xls', sheet_name='danmu')
    sentiment_analyse(data)
    atime_analysis(data)

    color_analysis(data)

    author_analysis(data)
    content_analysis(data)


if __name__ == '__main__':
  app.run()
