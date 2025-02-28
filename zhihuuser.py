from DrissionPage import Chromium
from bs4 import BeautifulSoup
import time
from collections import deque
import csv
import os
import random
class ZhihuRecursiveSpider:
    count=0
    def __init__(self, max_depth=3, max_followers=500000,csv_filename='D:\data\用户2.csv'):
        self.tab = Chromium().latest_tab
        self.tab.set.load_mode.none()
        self.visited = set()  # 已访问用户记录
        self.queue = deque()  # BFS队列
        self.max_depth = max_depth  # 最大递归深度
        self.max_followers = max_followers  # 每用户最大获取关注者数
        self.delay = random.randint(5,10)  # 请求间隔
        self.csv_filename = csv_filename
        self._init_csv()
        self.stored_ids = set()  # 存储已写入的回答ID
        self.datacount = 0  # 数据计数器

    def _init_csv(self):
        """初始化CSV文件，写入标题行"""
        if not os.path.isfile(self.csv_filename):
            with open(self.csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "admin_closed_comment", "answer_type", "avatar_url", "author_id", "author_gender", "name",
                    "is_advertiser", "author_type",
                    "author_url", "author_url_token", "can_comment", "collapse_reason",
                    "collapsed_by", "comment_count", "comment_permission", "content",
                    "content_need_truncated", "created_time", "force_login_when_click_read_more",
                    "id", "is_collapsed", "is_copyable", "is_labeled", "is_normal",
                    "question_created", "question_has_publishing_draft", "question_id",
                    "question_type", "question_title", "question_updated_time", "question_url",
                    "relationship_is_author", "relationship_is_authorized", "relationship_is_nothelp",
                    "relationship_is_thanked", "relationship_voting", "can_open_reward",
                    "is_rewardable", "reward_member_count", "reward_total_money", "updated_time",
                    "answer_url", "voteup_count"
                ])

    def get_answer(self, url_token):
        # 获取回答
        try:
            print(f"\n开始获取用户 {url_token} 的信息...")
            for i in range(1, 10000):  # 最多尝试10000页
                answer_url = 'https://www.zhihu.com/people/'+url_token+'/answers?page='+str(i)
                self.tab.get(answer_url)  # 访问回答网站
                self.tab.listen.start('api/v4/members/' + url_token + '/answers?')  # 指定监听目标并启动监听
                self.tab.scroll.to_bottom()  # 到最底端
                self.packet = self.tab.listen.wait()  # 等待数据包
                self.tab.stop_loading()  # 主动停止加载
                text = self.packet.response.body  # 数据包正文
                # print(text)
                # text = self._get_response_text()
                if not text: continue
                print(f'第{i}页........')
                # 存储回答内容
                for data in text['data']:
                    admin_closed_comment=data['admin_closed_comment']
                    answer_type=data['answer_type']
                    avatar_url = data['author']['avatar_url']
                    author_id=data['author']['id']
                    author_gender = data['author']['gender']
                    name=data['author']['name']
                    is_advertiser= data ['author']['is_advertiser']
                    author_type=data['author']['type']
                    author_url=data['author']['url']
                    author_url_token=data['author']['url_token']
                    can_comment=data['can_comment']['status']
                    collapse_reason=data['collapse_reason']
                    collapsed_by=data['collapsed_by']
                    comment_count=data['comment_count']
                    comment_permission=data['comment_permission']
                    content = self._parse_content(data.get('content', ''))
                    content_need_truncated=data['content_need_truncated']
                    created_time=data['created_time']
                    force_login_when_click_read_more=data['force_login_when_click_read_more']
                    id=data['id']
                    is_collapsed=data['is_collapsed']
                    is_copyable=data['is_copyable']
                    is_labeled=data['is_labeled']
                    is_normal=data['is_normal']
                    question_created=data['question']['created']
                    question_has_publishing_draft = data['question']['has_publishing_draft']
                    question_id = data['question']['id']
                    question_type = data['question']['question_type']
                    question_title = data['question']['title']
                    question_updated_time = data['question']['updated_time']
                    question_url = data['question']['url']
                    relationship_is_author = data['relationship']['is_author']
                    relationship_is_authorized = data['relationship']['is_authorized']
                    relationship_is_nothelp = data['relationship']['is_nothelp']
                    relationship_is_thanked = data['relationship']['is_thanked']
                    relationship_voting = data['relationship']['voting']
                    can_open_reward = data['reward_info']['can_open_reward']
                    is_rewardable = data['reward_info']['is_rewardable']
                    reward_member_count = data['reward_info']['reward_member_count']
                    reward_total_money = data['reward_info']['reward_total_money']
                    updated_time = data['updated_time']
                    answer_url=data['url']
                    voteup_count=data['voteup_count']

                    print(f"{content}")  # 示例输出
                    # 存储回答内容到CSV
                    with open(self.csv_filename, 'a', newline='', encoding='utf-8-sig') as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            admin_closed_comment, answer_type, avatar_url, author_id,author_gender,name,is_advertiser, author_type,
                            author_url, author_url_token, can_comment, collapse_reason,
                            collapsed_by, comment_count, comment_permission, content,
                            content_need_truncated, created_time, force_login_when_click_read_more,
                            id, is_collapsed, is_copyable, is_labeled, is_normal,
                            question_created, question_has_publishing_draft, question_id,
                            question_type, question_title, question_updated_time, question_url,
                            relationship_is_author, relationship_is_authorized, relationship_is_nothelp,
                            relationship_is_thanked, relationship_voting, can_open_reward,
                            is_rewardable, reward_member_count, reward_total_money, updated_time,
                            answer_url, voteup_count
                        ])

                if text['paging']['is_end']:
                    break
                time.sleep(self.delay)
        except Exception as e:
            print(f"获取回答异常：{e}")

    def get_followers(self, url_token):
        # 获取关注者
        try:
            print(f"\n开始获取用户 {url_token} 的关注者...")
            followers = []
            for page in range(1, 20):
                followers_url = 'https://www.zhihu.com/people/'+url_token+'/followers?page='+str(page)
                self.tab.get(followers_url)  # 访问回答网站
                self.tab.listen.start('api/v4/members/' + url_token + '/followers?')  # 指定监听目标并启动监听
                self.tab.scroll.to_bottom()  # 到最底端
                self.packet = self.tab.listen.wait()  # 等待数据包
                self.tab.stop_loading()  # 主动停止加载
                text = self.packet.response.body  # 数据包正文
                if not text: continue

                # 提取关注者token
                new_tokens = [data['url_token'] for data in text['data'] if 'url_token' in data]
                followers.extend(new_tokens)
                print(f"本页获取到{len(new_tokens)}个关注者")

                if text['paging']['is_end'] or len(followers) >= self.max_followers:
                    break
                time.sleep(self.delay)
            return followers[:self.max_followers]  # 返回限制数量的关注者
        except Exception as e:
            print(f"获取关注者异常：{e}")
            return []

    def _load_page(self, url, listen_str):
        """通用页面加载逻辑"""
        try:
            self.tab.get(url)
            self.tab.listen.start(listen_str)
            self.tab.scroll.to_bottom()
            self.tab.listen.wait()
            self.tab.stop_loading()
            return True
        except Exception as e:
            print(f"页面加载失败：{e}")
            return False

    def _parse_content(self, html):
        """解析回答内容"""
        soup = BeautifulSoup(html, 'lxml') if html else None
        return soup.get_text() if soup else ''

    def _get_response_text(self):
        """获取响应内容"""
        try:
            packet = self.tab.listen.wait()
            return packet.response.body
        except:
            return None

    def recursive_crawl(self, start_token):
        """递归爬取入口"""
        self.queue.append((start_token, 0))  # (token, 当前深度)
        self.visited.add(start_token)

        while self.queue:
            current_token, depth = self.queue.popleft()
            if depth > self.max_depth:
                continue

            # 获取当前用户数据
            self.get_answer(current_token)
            followers = self.get_followers(current_token)

            # 将关注者加入队列
            new_depth = depth + 1
            for follower in followers:
                if follower not in self.visited and new_depth <= self.max_depth:
                    self.visited.add(follower)
                    self.queue.append((follower, new_depth))
                    print(f"添加新用户到队列：{follower}（深度 {new_depth}）")

            time.sleep(self.delay)  # 控制整体节奏


if __name__ == '__main__':
    spider = ZhihuRecursiveSpider(
        max_depth=3,  # 控制爬取深度（0:仅自己，1:自己+直接关注者）
        max_followers=500000,  # 每个用户最多获取的关注者数量
        csv_filename = 'D:\data\用户2.csv' # 指定CSV文件名
    )

    # 示例初始用户
    start_token = "zhuruai"
    # 启动递归爬取
    spider.recursive_crawl(start_token)

