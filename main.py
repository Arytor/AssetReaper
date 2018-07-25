#!/usr/bin/env python2.7
# encoding: utf-8

# Asset Reaper
# Originally made by Adrian, fixed by Sparkles


try:
	import json, time, os, re, StringIO
	from PIL import Image
	from urllib import urlencode
	import requests, base58
	from BeautifulSoup import BeautifulSoup
except:
	print('ERROR:: missing module(s)')
	exit()


settings = json.loads(open('./settings/settings', 'r').read())
accounts = open('./settings 1/accounts', 'r').read().splitlines()
sessions = []
accountIndex = 0

class rbx():
	
	def __init__(self):
		self.session = requests.Session()
	
	def set_details(self, username, password):
		"sets cookie of session object"
		try:
			request = self.session.post('https://www.roblox.com/newlogin', data = {
			 'username': username,
			 'password': password
			})
			if ('.ROBLOSECURITY' in self.session.cookies.keys()):
				return True		
		except:
			pass
		return False
	
	def update(self, assetId, name, description, price):
		try:
			updateUrl = 'https://www.roblox.com/my/item.aspx?id={}'.format(assetId)
			request = self.session.get(updateUrl)
			if (request.status_code == 200):
				soup = BeautifulSoup(request.content)
				data = {
				 '__EVENTTARGET': 'ctl00$cphRoblox$SubmitButtonTop',
				 '__EVENTARGUMENT': '',
				 '__VIEWSTATE': soup.find('input', attrs={'name': '__VIEWSTATE'}).get('value'),
				 '__VIEWSTATEGENERATOR': soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'}).get('value'),
				 '__EVENTVALIDATION': soup.find('input', attrs={'name': '__EVENTVALIDATION'}).get('value'),
				 'ctl00$cphRoblox$NameTextBox': name,
				 'ctl00$cphRoblox$DescriptionTextBox': description,
				 'ctl00$cphRoblox$SellThisItemCheckBox': 'on',
				 'ctl00$cphRoblox$SellForRobux': 'on',
				 'ctl00$cphRoblox$RobuxPrice': price,
				 'ctl00$cphRoblox$EnableCommentsCheckBox': 'on',
				 'GenreButtons2': '1',
				 'ctl00$cphRoblox$actualGenreSelection': '1'
				}
				request2 = self.session.post(updateUrl, data=data)
				if (request2.status_code == 200):
					return True
		except:
			pass
		return False

	def upload(self, name, assetType, datafile, groupId = 0):
		try:
			uploadUrl = 'https://www.roblox.com/build/upload'
			request = self.session.get(uploadUrl)
			soup = BeautifulSoup(request.content)
			rvt = soup.find('input', attrs={'name': '__RequestVerificationToken'})
			if (rvt):
				rvt = rvt.get('value')
				uploadRequest = self.session.post(uploadUrl, data = {
				 '__RequestVerificationToken': rvt,
				 'assetTypeId': assetType,
				 'groupId': settings['groupId'],
				 'onVerificationPage': False,
				 'isOggUploadEnabled': True,
				 'isTgaUploadEnabled': True,
				 'name': name
				}, files = {'file': ('image.png', datafile, 'image/png')})
				if ('uploadedId' in uploadRequest.url):
					aid = re.search('uploadedId=(\d+)', uploadRequest.url)
					if (aid):
						return aid.group(1)
				elif ('later' in uploadRequest.url):
					print '-- UPLOAD BALANCING --'
					time.sleep(60)
				else:
					print 'ERROR:: unknown, {}'.format(uploadRequest.url)
					
		except:
			pass

class catalog():
	"""catalog api"""
	def __init__(self):
		pass
	
	@classmethod
	def search(self, CatalogContext = 1, PageNumber = 1, Subcategory = '', Category = '', SortType = '', AggregationFrequency = '', Keyword = ''):
		"""simple catalog search"""
		queryString = {}
		for key, value in locals().items():
			if (key != 'self' and key != 'queryString' and value != ''):
				queryString[key] = value
		queryString = urlencode(queryString)
		searchUrl = 'https://search.roblox.com/catalog/json?{}'.format(queryString)
		try:
			request = requests.get(searchUrl.format(queryString))
			if (request.status_code == 200):
				return request.json()
		except:
			pass
		return {}
	
	@classmethod
	def getData(self, assetId):
		"""gets data for asset"""
		assetUrl = 'https://assetgame.roblox.com/asset/?id={}'
		try:
			request = requests.get(assetUrl.format(assetId))
			if (request.status_code == 200):
				soup = BeautifulSoup(request.content)
				return soup
		except:
			pass

def save_asset(asset):
	"""saves the asset as a file"""
	nameString = '{0}_!_{1}'.format(asset['Name'].encode('utf-8').strip(), asset['AssetTypeID'])
	filename = base58.b58encode(nameString)+'.png'
	try:
		xmlData = catalog.getData(asset['AssetId'])
		if (xmlData):
			dataUrl = xmlData.content.url.text
			dataRequest = requests.get(dataUrl)
			if (dataRequest.status_code == 200):
				data = StringIO.StringIO(dataRequest.content)
				filepath = './files/{}'.format(filename)
				img = Image.open(data)
				img.save(filepath)
				return True
	except:
		pass
	return False

def start_upload():
	"""uploads assets"""
	global accountIndex
	global uploadCount
	for account in accounts:
		username, password = account.split(':')
		session = rbx()
		if (session.set_details(username, password) == True):
			sessions.append(session)
		else:
			print 'Invalid account: {}'.format(username)

	for filename in os.listdir('./files'):
		name, typeId = base58.b58decode(filename.replace('.png', '')).split('_!_')
		session = sessions[accountIndex]
		name = '{0}{1}'.format(settings['namePrefix'], name)
		uploadAttempt = session.upload(name, typeId, open('./files/{}'.format(filename), 'rb'), settings['groupId'])
		if ((accountIndex+1) >= len(sessions)):
			accountIndex = 0
		else:
			accountIndex += 1
		if (uploadAttempt):
			if (session.update(uploadAttempt, name, settings['description'], settings['price']) == True):
				print 'Uploaded - {0}'.format(uploadAttempt)

def start_download(at, sb, af, kw, s, e):
	"""downloads assets"""
	for pageNumber in range(int(s), int(e)):
		results = catalog.search(PageNumber = pageNumber, Subcategory = at, Category = 3, Keyword = kw, AggregationFrequency = af, SortType = sb)
		for a in results:
			saveAttempt = save_asset(a)
			print 'Downloaded - {0} - {1} - "{2}"'.format(a['AssetId'], saveAttempt, a['Name'].encode('utf-8').strip()[:15])

def ui_main():
	def title():
		print ('\n' * 100)
		print 'Asset Reaper @ thetrex.net\n & patches by Sparkle'
	def ui_download():
		print '> download > settings > asset type'
		print '12 - shirts'
		print '13 - t-shirts'
		print '14 - pants'
		assettype = raw_input('$ ')
		title()
		print '> download > settings > sort-by'
		print '0 - relevance'
		print '1 - most favorited'
		print '2 - bestselling'
		print '3 - recently updated'
		print '4 - price low to high'
		print '5 - price high to low'
		sortby = raw_input('$ ')
		title()
		print '> download > settings > aggregation frequency'
		print '0 - past day'
		print '1 - past week'
		print '2 - past month'
		print '3 - all time'
		aggregationfrequency = raw_input('$ ')
		title()
		print '> download > settings > keyword'
		keyword = raw_input('$ ')
		title()
		print '> download > settings > start page'
		start = raw_input('$ ')
		title()
		print '> download > settings > end page'
		end = raw_input('$ ')
		title()
		start_download(assettype, sortby, aggregationfrequency, keyword, start, end)
	def ui_upload():
		print '> upload'
		start_upload()
	title()
	print '> select mode'
	print '1 - download'
	print '2 - upload'
	user_input = raw_input('$ ').lower()
	if (user_input == '1'):
		title()
		ui_download()
	elif (user_input == '2'):
		title()
		ui_upload()
ui_main()
