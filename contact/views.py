from django.shortcuts import render
from django.http import JsonResponse
from .forms import ContactForm
from django.views import View

from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from django.views.decorators.cache import cache_control
@cache_control(no_cache=True, must_revalidate=True)
# Create your views here.

def scraping(userId, password, propertyType1, trackName, stationFrom, stationTo, distance, distanceType, priceMin, priceMax, areaMin, level, built_year, roomMin, etc_multi):	
	# driver = webdriver.Chrome('./chromedriver')
	options = Options()
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	# driver = webdriver.Chrome('./chromedriver')
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

	driver.maximize_window()
	driver.set_window_size(1920, 1680)
	window_size = driver.get_window_rect()
	width = window_size['width']
	height = window_size['height']
	print(f"Window Width: {width}, Window Height: {height}")
	url = 'https://system.reins.jp/login/main/KG/GKG001200/'
	driver.get(url)
	# driver.execute_script("document.body.style.zoom='50%'")

	# user info
	id = userId
	passwd = password
	delay = 15 #seconds
	style_condition = 'grid-row-start: 1; grid-column: 14 / span 11;'
	style_condition2 = 'grid-row: 1 / span 2; grid-column-start: 1;'
	result = {'address':[], 'type':[], 'rent':[], 'manageFee':[],'serviceFee':[],'roomMin':[],'partArea':[],'mPrice':[],'averPrice':[],'name':[],'station':[],'trade':[],'phone':[], 'floorPlan':[]}
	propertyType1_id = ""
	propertyType2_id = ""
	trackName_id = ""
	stationFrom_id = ""
	stationTo_id = ""
	distance_id = ""
	distanceType_id = ""
	priceMin_id = ""
	priceMax_id = ""
	areaMin_id = ""
	roomMin_id = ""
	levelMax_id = ""
	builtYear_id = ""

	# login
	try:
		# WebDriverWait(driver, delay).until(lambda s: s.find_element(By.ID, "__BVID__13")).is_displayed()  
		WebDriverWait(driver, delay).until(
			EC.visibility_of_element_located((By.XPATH, "//span[@class='p-label-title' and contains(text(), 'ユーザID')]"))
		)
	except TimeoutException as ex:
		print("Error")
		driver.close()
		driver.quit()
		return {"error": "Error"}

	# get IDs of id and password input on login page
	html = driver.page_source.encode('utf-8')
	soup = BeautifulSoup(html, "html.parser")   
	id_pwd_elements = soup.find_all('input', class_='p-textbox-input form-control')
	idElement_id = id_pwd_elements[0].get('id')
	pwdElement_id = id_pwd_elements[1].get('id')
	print("idElement id: ", idElement_id)
	print("pwdElement_id: ", pwdElement_id)

	# input id and password on login page
	driver.find_element(By.ID, idElement_id).send_keys(id)
	driver.find_element(By.ID, pwdElement_id).send_keys(passwd)
	driver.find_element(By.XPATH, './/*[@class="p-checkbox-input custom-control custom-checkbox b-custom-control-lg"]').click()
	driver.find_element(By.XPATH, './/*[@class="btn p-button p-3 large btn-primary btn-block px-0"]').click()

	# 2nd page
	try:
		print("logged in")
		WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '賃貸 物件検索')]"))).click()

	except TimeoutException:
		print("loginError")
		driver.close()
		driver.quit()
		return {"error": "loginError"}

	# 3rd page
	time.sleep(5)
	# try:
	# 	WebDriverWait(driver, delay).until(EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(text(), '検索')]")))

	# except TimeoutException:
	# 	print("loginError")
	# 	driver.close()
	# 	driver.quit()
	# 	return {"error": "loginError"}
	
	# get IDs for input values on main filter page
	try: 
		html = driver.page_source.encode('utf-8')
		soup = BeautifulSoup(html, "html.parser")   

		propertyType1_elements = soup.find_all('span', class_='p-label-title', text='物件種別１')
		propertyType1_element = propertyType1_elements[0].find_parent('div').find_parent('div').find('select')
		propertyType1_id = propertyType1_element.get('id')
		print("propertyType")
		print("propertyType1_id", propertyType1_id)

		propertyType2_elements = soup.find_all('span', class_='p-label-title', text='物件種別２')
		propertyType2_element = propertyType2_elements[0].find_parent('div').find_parent('div').find('select')
		propertyType2_id = propertyType2_element.get('id')

		trackName_elements = soup.find_all('span', class_='p-label-title', text='沿線名')
		trackName_element = trackName_elements[0].find_parent('div').find_parent('div').find('input')
		trackName_id = trackName_element.get('id')
		
		stationFrom_elements = soup.find_all('span', class_='p-label-title', text='駅名')
		stationFromTo_elements = stationFrom_elements[0].find_parent('div').find_parent('div').find_all('input')
		stationFrom_id = stationFromTo_elements[0].get('id')
		stationTo_id = stationFromTo_elements[1].get('id')

		distance_elements = soup.find_all('span', class_='p-label-title', text='駅から徒歩')
		distance_element = distance_elements[0].find_parent('div').find_parent('div').find('input')
		distance_id = distance_element.get('id')
		distanceType_element = distance_elements[0].find_parent('div').find_parent('div').find('select')
		distanceType_id = distanceType_element.get('id')

		price_elements = soup.find_all('span', class_='p-label-title', text='賃料')
		priceMinMax_elements = price_elements[0].find_parent('div').find_parent('div').find_all('input')
		priceMin_id = priceMinMax_elements[0].get('id')
		priceMax_id = priceMinMax_elements[1].get('id')

		areaMin_elements = soup.find_all('span', class_='p-label-title', text='建物使用部分面積')
		areaMin_element = areaMin_elements[0].find_parent('div').find_parent('div').find('input')
		areaMin_id = areaMin_element.get('id')

		roomMin_elements = soup.find_all('span', class_='p-label-title', text='間取部屋数')
		roomMin_element = roomMin_elements[0].find_parent('div').find_parent('div').find('input')
		roomMin_id = roomMin_element.get('id')
		
		level_elements = soup.find_all('span', class_='p-label-title', text='所在階')
		levelMinMax_elements = level_elements[0].find_parent('div').find_parent('div').find_all('input')
		levelMax_id = levelMinMax_elements[1].get('id')

		builtYear_elements = soup.find_all('span', class_='p-label-title', text='築年月')
		builtYear_element = builtYear_elements[0].find_parent('div').find_parent('div').find('select')
		builtYear_id = builtYear_element.get('id')

		# for debug
		# with open("log.txt", "w") as file:
		# 	file.write(str(distance_element))
		print("ID : ", propertyType1_id, propertyType2_id, trackName_id, stationFrom_id, stationTo_id, distance_id, distanceType_id, priceMin_id, priceMax_id, areaMin_id, roomMin_id, levelMax_id, builtYear_id)
	
	except Exception as ex:
		print("error while getting IDs")
		print(ex.__str__)

	select = Select(driver.find_element(By.ID, propertyType1_id))
	select.select_by_index(int(propertyType1))
	# select = Select(driver.find_element(By.ID, propertyType2_id))
	# select.select_by_index(int(propertyType2))
	driver.find_element(By.ID, trackName_id).send_keys(trackName)
	driver.find_element(By.ID, stationFrom_id).send_keys(stationFrom)
	driver.find_element(By.ID, stationTo_id).send_keys(stationTo) 
	driver.find_element(By.ID, distance_id).send_keys(distance)	

	select = Select(driver.find_element(By.ID, distanceType_id))
	if (distanceType == '1'):
		select.select_by_index(1)
	else:
		select.select_by_index(2)

	driver.find_element(By.ID, priceMin_id).send_keys(priceMin)
	driver.find_element(By.ID, priceMax_id).send_keys(priceMax)
	driver.find_element(By.ID, areaMin_id).send_keys(areaMin)
	driver.find_element(By.ID, roomMin_id).send_keys(roomMin)
	print("------------level-------------", level)
	driver.find_element(By.ID, levelMax_id).send_keys(level)
	print("---------- end --------------", (built_year))
	if (built_year != ''):
		selectYear = Select(driver.find_element(By.ID, builtYear_id))
		selectYear.select_by_index(2027 - int(built_year))
	print("--------multi element------", etc_multi)

	if (len(etc_multi) > 0):
		try:
			print("multiElement ready")
			multiElement = WebDriverWait(driver, delay).until(EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(text(), '入力ガイド')]")))
			if len(multiElement) >= 10:
				print("length: ", len(multiElement))
				try:
					driver.execute_script("arguments[0].scrollIntoView(true);", multiElement[9])
					multiElement[9].click()
				except Exception as ex:
					print(ex.__str__)
					print("test0")
				print("test1")
				if (len(etc_multi) > 0):
					try:
						if '1' in etc_multi:
							print("******  1  ******")
							WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'ペット相談')]"))).click()
						if '2' in etc_multi:
							print("******** 2 *******")
							WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), '事務所使用可')]"))).click()
						if '3' in etc_multi:
							print("******  3  ******")
							WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'エレベータ')]"))).click()
					except TimeoutException as e:
						print("unable to click multi element")
				# 	if (etc_multi[0] == '1'):
				# 		print("detected", 1)
				# 		WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'ペット相談')]"))).click()
				# 	else:
				# 		print("detected", 2)
				# 		WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), '事務所使用可')]"))).click()
				# elif (len(etc_multi) == 2):
				# 	print("detected 1 2")
				# 	WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'ペット相談')]"))).click()
				# 	WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), '事務所使用可')]"))).click()
				try:
					WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '決定')]"))).click()
				except Exception as ex:
					confirmElement = WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(text(), '検索結果が500件を超えています')]")))
					if (confirmElement):
						print("500 over Error")
						driver.close()
						driver.quit()
						return {"error": "500OverError"}
			else:
				print("Not enough elements found")
			print("multiElement end")
		except NoSuchElementException as ex:
			driver.close()
			driver.quit()
			print("500OverError")
			return {"error": "500OverError"}		
	print("test1.4")

	propertyType_options = [
		"",
		"賃貸土地",
		"賃貸一戸建",
		"賃貸マンション",
		"賃貸外全(住宅以外建物全部)",
		"賃貸外一(住宅以外建物一部)"
	]
	propertyType1_str = propertyType_options[int(propertyType1)]
	# propertyType2_str = propertyType_options[int(propertyType2)]
	print("propertyType1_str", propertyType1_str)
	# print("propertyType2_str", propertyType2_str)
	try:
		print("Test1.5")
		WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '検索')]"))).click()
		WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '" + propertyType1_str + "')]"))).click()
	except Exception as ex:
		print("test1.6")
		try:
			print("test 1.65")
			confirmElement = WebDriverWait(driver, delay).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(text(), '検索結果が500件を超えています')]")))
			driver.close()
			driver.quit()
			if (confirmElement):
				print("500 over Error")
				return {"error": "500OverError"}
		except Exception as ex:
			print("noElementsss", str(ex))
			return {"error": "noElement"}
	print("test2")
	# getting result
	try:
		i = 0
		currentPropertyType = propertyType1_str
		while(True):       
			time.sleep(8)
			i = i + 1 
			locator = (By.CSS_SELECTOR, f'div.p-table-body-item[style="{style_condition}"]')
			try:
				WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
			except TimeoutException:
				print("Element not found within specified timeout")
				return {"error": "noElement"}
			except Exception as e :
				print("An error occured:", e)
				return {"error":  "Error"}
			html = driver.page_source.encode('utf-8')
			soup = BeautifulSoup(html, "html.parser")        
			divs_with_role_tabpanel = soup.find_all("div", {"role": "tabpanel", "style": ""})
			second_div = None
			second_div = divs_with_role_tabpanel[0]

			#  物件種目
			type_group = second_div.find_all("div", class_='p-table-body-item', style="grid-row-start: 1; grid-column: 5 / span 6;")  
			# 賃料
			rent_group = second_div.find_all("div", class_='p-table-body-item', style="grid-row-start: 2; grid-column: 5 / span 3;")
			# 管理費
			manageFee_group = second_div.find_all("div", class_='p-table-body-item', style="grid-row-start: 3; grid-column: 5 / span 3;")
			# 共益費
			serviceFee_group = second_div.find_all("div", class_='p-table-body-item', style="grid-row-start: 4; grid-column: 5 / span 3;")
			# 使用部分面積, 土地面積
			partArea_group = second_div.find_all("div", class_='p-table-body-item', style="grid-row-start: 1; grid-column: 11 / span 3;")
			# 間取
			floorPlan_group = second_div.find_all("div", class_='p-table-body-item', style="grid-row-start: 2; grid-column: 23 / span 2;")
			# 所在地
			address_group = second_div.find_all("div", class_='p-table-body-item', style="grid-row-start: 1; grid-column: 14 / span 11;")
			# 建物名
			if (currentPropertyType == '賃貸一戸建'):
				name_group = second_div.find_all("div", class_='p-table-body-item', style="grid-row-start: 2; grid-column: 14 / span 9;")
			else:
				name_group = second_div.find_all("div", class_='p-table-body-item', style="grid-row-start: 2; grid-column: 14 / span 5;")
			
			# 沿線駅
			station_group = second_div.find_all("div", class_='p-table-body-item', style="grid-row-start: 3; grid-column: 14 / span 5;")
			# 商号
			trade_group = second_div.find_all("span", class_='d-sm-none')
			# 電話番号
			phone_group = second_div.find_all('span', class_='')

			# 築年月
			# roomMin_group = second_div.find_all("div", class_='p-table-body-item', style="grid-row-start: 5; grid-column: 5 / span 9;")
			# ㎡単価
			# mPrice_group = second_div.find_all("div", class_='p-table-body-item', style="grid-row-start: 2; grid-column: 11 / span 3;")			
			# 坪単価
			# averPrice_group = second_div.find_all("div", class_='p-table-body-item', style="grid-row-start: 3; grid-column: 11 / span 3;")
			
			print("address len: ", len(address_group))
			print("trade len: ", len(trade_group))
			print("phone len: ", len(phone_group))

			for j in range(len(address_group)):
				result['address'].append(address_group[j].text.strip())
				result['type'].append(type_group[j].text.strip())
				result['rent'].append(rent_group[j].text.strip().replace(",", ""))
				result['manageFee'].append(manageFee_group[j].text.strip().replace(",", ""))
				result['serviceFee'].append(serviceFee_group[j].text.strip().replace(",", ""))
				result['partArea'].append(partArea_group[j].text.strip())
				if (currentPropertyType == '賃貸土地'):
					result['name'].append("") 
				else:
					result['name'].append(name_group[j].text)

				result['station'].append(station_group[j].text)
				result['trade'].append(trade_group[j].text)
				result['phone'].append(phone_group[j].text)
				if (currentPropertyType == '賃貸土地' or currentPropertyType == '賃貸外全(住宅以外建物全部)'):
					result['floorPlan'].append("")
				else:
					result['floorPlan'].append(floorPlan_group[j].text)
				# result['roomMin'].append(roomMin_group[j].text.strip())
				# result['mPrice'].append(mPrice_group[j].text.strip().replace(",", ""))
				# result['averPrice'].append(averPrice_group[j].text.strip().replace(",", ""))

			nextButton = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Go to next page"]')
			nextButton.click()
			expected_text = str(i*50 + 1)
			print(i,"clicked")

			# WebDriverWait(driver, delay).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, f'div.p-table-body-item[style="{style_condition2}"]'), expected_text))
	except NoSuchElementException as e:
		print("noElement")
	# resultString = ','.join(result)	
	driver.close()
	driver.quit()
	print("================result=================")
	print(result)
	return result

#FBV
def contactPage(request):
	form = ContactForm()
	return render(request, "contact.html", {"contactForm": form})

def postContact(request):
	if request.method == "POST":
		print("-------postContact--------")
		print(request.POST)
		form = ContactForm(request.POST)
		print(form["userId"].value())
		userId = form["userId"].value() 
		password = form["password"].value()
		propertyType1 = form["propertyType1"].value()
		# propertyType2 = form["propertyType2"].value()
		trackName = form["trackName"].value()
		stationFrom = form["stationFrom"].value()
		stationTo = form["stationTo"].value()
		distance = form["distance"].value()
		distanceType = '1'
		priceMin = form["priceMin"].value()
		priceMax = form["priceMax"].value()
		areaMin = form["areaMin"].value()
		level = form["level"].value()
		built_year = form["built_year"].value()
		roomMin = form["roomMin"].value()
		etc_multi = form["etc_multi"].value() 
		res = scraping(userId, password, propertyType1, trackName, stationFrom, stationTo, distance, distanceType, priceMin, priceMax, areaMin, level, built_year, roomMin, etc_multi)

		# print("protpertyType2", propertyType2)
		if "error" in res and (res['error'] == '500OverError' or res['error']  == 'loginError' or res['error']  == 'Error' or res['error']  == 'noElement'):
			return render(request, "contact.html", {'data' : res['error'], 'userId' : userId, 'password': password, 'propertyType1' : propertyType1, 'trackName' : trackName, 'stationFrom' : stationFrom, 'stationTo' : stationTo, 'distance' : distance, 'distanceType' : distanceType, 'priceMin' : priceMin, 'priceMax' : priceMax, 'areaMin' : areaMin, 'level' : level, 'built_year' : built_year, 'etc_multi' : etc_multi})
		else:
			return render(request, "map.html", {'map_data' : res, 'userId' : userId, 'password': password, 'propertyType1' : propertyType1, 'trackName' : trackName, 'stationFrom' : stationFrom, 'stationTo' : stationTo, 'distance' : distance, 'distanceType' : distanceType, 'priceMin' : priceMin, 'priceMax' : priceMax, 'areaMin' : areaMin, 'level' : level, 'built_year' : built_year, 'etc_multi' : etc_multi})

			# return JsonResponse({"success": res}, status=200)
	return JsonResponse({"success":False}, status=400)

def mapDisplay(request):
	print("=====map request ======")
	print(request)
	map_data = request.GET.get('data', '')
	return render(request, "map.html", {'map_data' : map_data})
#CBV
class ContactAjax(View):
	form_class = ContactForm
	template_name = "contact_cbv.html"

	def get(self, *args, **kwargs):
		form = self.form_class()
		return render(self.request, self.template_name, {"contactForm": form})

	def post(self, *args, **kwargs):
		if self.request.method == "POST" and self.request.is_ajax():
			form = self.form_class(self.request.POST)
			form.save()
			return JsonResponse({"success":"sdfasfdsafas"}, status=200)
		return JsonResponse({"success":False}, status=400)