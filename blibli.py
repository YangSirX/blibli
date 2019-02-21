import csv
import json
import time

import requests
'https://api.bilibili.com/x/web-interface/newlist?rid=33&pn=1&jsonp=jsonp&_=1550734576472'

class Bili(object):
	def __init__(self):
		self.retry = 0
		self.page = 0
		self.html = ''
		self.url = 'https://api.bilibili.com/x/web-interface/newlist?pn=1&ps=20&rid=33&jsonp=jsonp'
		self.headers = {
			'Cookie': '_uuid=47249C59-D669-A37D-C939-FCE9F4D317C773902infoc; buvid3=2214A598-A89D-4F2C-A739-29206B9DF4F948762infoc; LIVE_BUVID=AUTO5515468527871948; stardustvideo=1; CURRENT_FNVAL=16; rpdid=olmkpsmwlodospmxkqopw; fts=1547638274; im_local_unread_92189508=0; sid=88yfk1i3; im_notify_type_92189508=0; bp_t_offset_92189508=211900371990380314',
			'Host': 'api.bilibili.com',
			'Referer': 'https://www.bilibili.com/v/anime/serial/?spm_id_from=333.334.b_7072696d6172795f6d656e75.8',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
			'Connection': 'keep-alive'
		}
		self.save_header()

	def save_header(self):
		"""保存到csv中的表头"""
		headers = [['番剧名', '图片链接', '播放量', '弹幕量', '投稿时间']]
		with open('bili.csv', 'w', encoding='utf-8', newline='') as f:
			writer = csv.writer(f)
			writer.writerows(headers)

	def save_csv(self, data_list):
		"""将数据保存到csv中"""
		with open('bili.csv', 'a', encoding='utf-8', newline='') as f:
			writer = csv.writer(f)
			writer.writerows(data_list)

	def get_html(self, url):
		"""获取网页源码"""
		try:
			self.retry += 1
			response = requests.get(url, headers=self.headers)
			self.html = response.text
		# print(self.html)
		except Exception as e:
			if self.retry > 3:
				print(f'请求失败，正在尝试第{self.retry}次重新请求')
				time.sleep(3)
				return
			self.get_html(self.url)
		else:
			self.retry = 0

	def get_data(self):
		"""获取数据"""
		data_list = []
		result = json.loads(self.html)
		datas = result["data"]["archives"]
		for d in datas:
			data = []
			data.append(d["title"])
			data.append(d["pic"])
			data.append(d["stat"]["view"])
			data.append(d["stat"]["danmaku"])
			# 创建时间
			time_local = time.localtime(d["ctime"])
			ctime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
			data.append(ctime)
			data_list.append(data)
		self.save_csv(data_list)

	def run(self):
		for x in range(1, 11):
			time.sleep(2)
			print(f'正在爬取第{x}页数据，请稍后')
			# url = f'https://api.bilibili.com/x/web-interface/newlist?pn={x}&ps=20&_=1546868687676&rid=33&type=0&jsonp=jsonp'
			url = f'https://api.bilibili.com/x/web-interface/newlist?pn={x}&ps=20&rid=33&jsonp=jsonp'
			self.get_html(url)
			self.get_data()


if __name__ == '__main__':
	bili = Bili()
	bili.run()


