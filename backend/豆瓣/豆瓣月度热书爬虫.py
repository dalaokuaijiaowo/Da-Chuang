import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}

def get_book_list():
    url = 'https://book.douban.com/chart?subcat=all&icn=index-topchart-popular'
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        books = []
        
        all_links = soup.find_all('a', href=re.compile(r'/subject/\d+/?$'))
        print(f"找到 {len(all_links)} 个图书链接")
        
        seen_urls = set()
        for link in all_links:
            href = link.get('href')
            if href and href not in seen_urls:
                seen_urls.add(href)
                
                book_info = {
                    'book_url': href
                }
                
                if book_info['book_url'] not in [b['book_url'] for b in books]:
                    books.append(book_info)
        
        print(f"获取到 {len(books)} 个图书链接，正在获取详细信息...")
        
        for book in books:
            try:
                book_response = requests.get(book['book_url'], headers=headers, timeout=10)
                book_response.encoding = 'utf-8'
                book_soup = BeautifulSoup(book_response.text, 'html.parser')
                
                title_elem = book_soup.find('h1')
                if title_elem:
                    book['title'] = title_elem.get_text(strip=True)
                else:
                    book['title'] = '未知书名'
                
                pub_elem = book_soup.find('div', id='info')
                if pub_elem:
                    book['pub_info'] = pub_elem.get_text(strip=True)
                
                rating_elem = book_soup.find('strong', class_='ll rating_num ')
                if rating_elem:
                    book['rating'] = rating_elem.get_text(strip=True)
                
                people_elem = book_soup.find('span', property='v:votes')
                if people_elem:
                    book['rating_people'] = people_elem.get_text(strip=True)
                
                print(f"获取到图书: {book['title']}")
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"获取图书详情时出错: {e}")
                book['title'] = '获取失败'
        
        return books
        
    except Exception as e:
        print(f"获取图书列表时出错: {e}")
        return []

def get_book_comments(book_url, max_comments=20):
    comments = []
    comment_url = f"{book_url.rstrip('/')}/comments/"
    
    try:
        response = requests.get(comment_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        comment_items = soup.find_all('li', class_='comment-item')
        
        for item in comment_items[:max_comments]:
            try:
                comment_info = {}
                
                user_elem = item.find('span', class_='comment-info')
                if user_elem:
                    comment_info['user'] = user_elem.get_text(strip=True)
                
                rating_elem = item.find('span', class_='allstar')
                if rating_elem:
                    comment_info['rating'] = rating_elem.get('title')
                
                content_elem = item.find('span', class_='short')
                if content_elem:
                    comment_info['comment'] = content_elem.get_text(strip=True)
                
                time_elem = item.find('span', class_='comment-time')
                if time_elem:
                    comment_info['time'] = time_elem.get_text(strip=True)
                
                if comment_info.get('comment'):
                    comments.append(comment_info)
                    
            except Exception as e:
                continue
        
        time.sleep(random.uniform(1, 2))
        
    except Exception as e:
        print(f"获取评论时出错: {e}")
    
    return comments

def save_to_csv(data, book_id=None):
    import os
    # 创建result文件夹
    result_dir = os.path.join(os.path.dirname(__file__), '../result')
    os.makedirs(result_dir, exist_ok=True)
    
    # 统一命名规范：豆瓣读书_id（使用第一本书的书名作为标识）
    if data and len(data) > 0:
        first_book_name = data[0].get('书名', '未知书籍')
        # 处理文件名中的特殊字符
        safe_book_name = first_book_name.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
        filename = f'豆瓣读书_{safe_book_name}.csv'
    else:
        filename = '豆瓣读书_未知书籍.csv'
    
    file_path = os.path.join(result_dir, filename)
    
    # 统一列命名规范：用户名列改为"用户名"，评论内容列改为"评论内容"
    # 转换数据格式
    converted_data = []
    for item in data:
        converted_item = {
            '书名': item.get('书名', ''),
            '出版信息': item.get('出版信息', ''),
            '评价人数': item.get('评价人数', ''),
            '用户名': item.get('评论用户', ''),  # 统一列名
            '评论内容': item.get('评论内容', '')  # 统一列名
        }
        converted_data.append(converted_item)
    
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['书名', '出版信息', '评价人数', '用户名', '评论内容']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in converted_data:
            writer.writerow(item)
    
    print(f"数据已保存到 {file_path}")

def main(max_books=None):
    print("开始爬取豆瓣读书热门图书榜...")
    
    books = get_book_list()
    print(f"共找到 {len(books)} 本书")
    print("爬取中，请耐心等待...")
    
    if not books:
        print("未找到任何图书，请检查网络连接或网站结构是否发生变化")
        return
    
    # 如果指定了最大书籍数量，则截取前max_books本书
    if max_books:
        books = books[:max_books]
        print(f"根据用户指定，只爬取前 {max_books} 本书")
    
    all_data = []
    
    for idx, book in enumerate(books, 1):
        print(f"\n正在处理第 {idx}/{len(books)} 本书: {book.get('title', '未知')}")
        
        comments = get_book_comments(book['book_url'])
        print(f"  获取到 {len(comments)} 条评论")
        
        for comment in comments:
            data = {
                '书名': book.get('title', ''),
                '出版信息': book.get('pub_info', ''),
                '评价人数': book.get('rating_people', ''),
                '评论用户': comment.get('user', ''),
                '评论内容': comment.get('comment', ''),
            }
            all_data.append(data)
        
        time.sleep(random.uniform(1,2))
    
    if all_data:
        save_to_csv(all_data)
        print(f"\n爬取完成！共保存 {len(all_data)} 条数据")
    else:
        print("未获取到任何数据")

if __name__ == '__main__':
    import sys
    # 从命令行获取参数
    if len(sys.argv) > 1:
        try:
            max_books = int(sys.argv[1])
            main(max_books)
        except ValueError:
            print("Usage: python 豆瓣月度热书爬虫.py [max_books]")
            print("max_books 必须是一个整数")
            sys.exit(1)
    else:
        main()
