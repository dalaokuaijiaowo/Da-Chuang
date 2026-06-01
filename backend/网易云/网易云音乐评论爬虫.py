# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 17:11:24 2019

@author: aotodata

微信公众号: 凹凸数读

微信公众号: 凹凸玩数据
"""
import requests
import jsonpath
import pandas as pd
import time
from fake_useragent import UserAgent
ua = UserAgent()
import random


headers = {'User-Agent':ua.random}


def get_json(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_text=response.json()
            return json_text
    except Exception:
        print('此页有问题！')
        return None


def get_song_name(song_id):
    """获取歌曲名称"""
    url = f'http://music.163.com/api/song/detail/?id={song_id}&ids=%5B{song_id}%5D'
    doc = get_json(url)
    if doc and 'songs' in doc and doc['songs']:
        return doc['songs'][0]['name']
    return str(song_id)  # 如果获取失败，返回ID作为名称
    

def stampToTime(stamp): #时间转换
    datatime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(str(stamp)[0:10])))
    datatime = datatime+'.'+str(stamp)[10:]
    return datatime


def get_comments(url,k):
    data = []
    doc = get_json(url)
    if doc is None:
        return data
    
    # 获取热评
    if 'hotComments' in doc and doc['hotComments']:
        for job in doc['hotComments']:
            dic = {}
            dic['content']=jsonpath.jsonpath(job,'$..content')[0].replace('\r', '')
            dic['time']= stampToTime(jsonpath.jsonpath(job,'$..time')[0])
            dic['userId']=jsonpath.jsonpath(job['user'],'$..userId')[0]  #用户ID
            dic['nickname']=jsonpath.jsonpath(job['user'],'$..nickname')[0]#用户名
            dic['likedCount']=jsonpath.jsonpath(job,'$..likedCount')[0] 
            dic['name']= k
            dic['is_hot'] = True  # 标记为热评
            data.append(dic)
    
    # 获取普通评论
    if 'comments' in doc and doc['comments']:
        for job in doc['comments']:
            dic = {}
            dic['content']=jsonpath.jsonpath(job,'$..content')[0].replace('\r', '')
            dic['time']= stampToTime(jsonpath.jsonpath(job,'$..time')[0])
            dic['userId']=jsonpath.jsonpath(job['user'],'$..userId')[0]  #用户ID
            dic['nickname']=jsonpath.jsonpath(job['user'],'$..nickname')[0]#用户名
            dic['likedCount']=jsonpath.jsonpath(job,'$..likedCount')[0] 
            dic['name']= k
            dic['is_hot'] = False  # 标记为普通评论
            data.append(dic)
    
    return data  


 #汇总
def main(song_id):
    final_result = pd.DataFrame()
    data_pinglun = []
    
    # 获取歌曲名称
    song_name = get_song_name(song_id)
    print(f'歌曲名称: {song_name}')
    print("爬取中，请耐心等待...")
    k = song_name  # 使用歌曲名称作为标识
    
    # 获取多页评论（最多5页，每页20条）
    for offset in range(0, 100, 20):
        urls = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + str(song_id) + '?limit=20&offset=' + str(offset)
        dic = get_comments(urls, k)
        data_pinglun.extend(dic)
        print(f'已获取第{offset//20 + 1}页评论，当前共{len(data_pinglun)}条评论')
        time.sleep(random.random())  # 礼貌爬虫
    
    # 统一命名规范：网易云_歌曲名称_id
    filename = f"网易云_{song_name}_{song_id}.csv"
    # 处理文件名中的特殊字符
    filename = filename.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
    
    # 创建result文件夹
    import os
    result_dir = os.path.join(os.path.dirname(__file__), '../result')
    os.makedirs(result_dir, exist_ok=True)
    
    file_path = os.path.join(result_dir, filename)
    final_result = pd.DataFrame(data_pinglun)
    
    # 统一列命名规范：用户名列改为"用户名"，评论内容列改为"评论内容"
    column_mapping = {
        'nickname': '用户名',
        'content': '评论内容',
        'time': 'time',
        'userId': 'userId',
        'likedCount': 'likedCount',
        'name': 'name',
        'is_hot': 'is_hot'
    }
    # 只重命名存在的列
    existing_columns = {k: v for k, v in column_mapping.items() if k in final_result.columns}
    final_result = final_result.rename(columns=existing_columns)
    
    final_result.to_csv(file_path, index_label="index_label", encoding='utf-8-sig')
    print(f'已成功采集歌曲"{song_name}"(ID:{song_id})的{len(data_pinglun)}条评论')
    print(f'评论数据已保存到: {file_path}\n')
    return final_result


if __name__ == "__main__":
    import sys
    # 从命令行获取参数
    if len(sys.argv) < 2:
        print("Usage: python 网易云音乐评论爬虫.py <song_id>")
        sys.exit(1)
    
    song_id = int(sys.argv[1])
    final_result = main(song_id)