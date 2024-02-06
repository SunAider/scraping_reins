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
# Create your views here.

def scraping(userId, password, trackName, stationFrom, stationTo, distance, distanceType, priceMax, areaMin, level, built_year, built_month, etc_multi):	
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
	delay = 20 #seconds
	style_condition = 'grid-row-start: 1; grid-column: 14 / span 11;'
	style_condition2 = 'grid-row: 1 / span 2; grid-column-start: 1;'
	result = []
	# login
	try:
		WebDriverWait(driver, delay).until(lambda s: s.find_element(By.ID, "__BVID__13")).is_displayed()  
	except TimeoutException as ex:
		print("Error")
		driver.close()
		driver.quit()
		return "Error"
	driver.find_element(By.ID, '__BVID__13').send_keys(id)
	driver.find_element(By.ID, '__BVID__16').send_keys(passwd)
	driver.find_element(By.XPATH, './/*[@class="p-checkbox-input custom-control custom-checkbox b-custom-control-lg"]').click()
	driver.find_element(By.XPATH, './/*[@class="btn p-button p-3 large btn-primary btn-block px-0"]').click()

	# 2nd page
	try:
		WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '賃貸 物件検索')]"))).click()
	except TimeoutException:
		print("loginError")
		driver.close()
		driver.quit()
		return "loginError"
	# 3rd page
	WebDriverWait(driver, delay).until(lambda s: s.find_element(By.ID, "__BVID__140")).is_displayed()  
	select = Select(driver.find_element(By.ID, '__BVID__140'))
	select.select_by_index(2)
	select = Select(driver.find_element(By.ID, '__BVID__149'))
	select.select_by_index(3)
	driver.find_element(By.ID, '__BVID__292').send_keys(trackName)
	driver.find_element(By.ID, '__BVID__296').send_keys(stationFrom)
	driver.find_element(By.ID, '__BVID__298').send_keys(stationTo) 
	driver.find_element(By.ID, '__BVID__301').send_keys(distance)
	select = Select(driver.find_element(By.ID, '__BVID__303'))
	if (distanceType == '1'):
		select.select_by_index(1)
	else:
		select.select_by_index(2)
	driver.find_element(By.ID, '__BVID__374').send_keys(priceMax)
	driver.find_element(By.ID, '__BVID__402').send_keys(areaMin)
	print("------------level-------------", level)
	driver.find_element(By.ID, '__BVID__438').send_keys(level)
	print("---------- end --------------", (built_year))
	if (built_year != ''):
		selectYear = Select(driver.find_element(By.ID, '__BVID__468'))
		selectYear.select_by_index(2027 - int(built_year))
	if (built_month != ''):
		selectMonth = Select(driver.find_element(By.ID, '__BVID__470'))
		selectMonth.select_by_index(int(built_month))
	print("--------multi element------", etc_multi)
	if (len(etc_multi) > 0):
		try:
			print("multiElement ready")
			multiElement = WebDriverWait(driver, delay).until(EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(text(), '入力ガイド')]")))
			if len(multiElement) >= 10:
				print("length: ", len(multiElement))
				try:
					driver.execute_script("arguments[0].scrollIntoView(true);", multiElement[9])
					# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					# multiElement = WebDriverWait(driver, delay).until(EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(text(), '入力ガイド')]")))
					multiElement[9].click()
				except Exception as ex:
					print(ex.__str__)
					print("test0")
				print("test1")
				if (len(etc_multi) == 1):
					if (etc_multi[0] == '1'):
						print("detected", 1)
						WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'ペット相談')]"))).click()
					else:
						print("detected", 2)
						WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), '事務所使用可')]"))).click()
				elif (len(etc_multi) == 2):
					print("detected 1 2")
					WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'ペット相談')]"))).click()
					WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), '事務所使用可')]"))).click()
				try:
					WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '決定')]"))).click()
				except Exception as ex:
					confirmElement = WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(text(), '検索結果が500件を超えています')]")))
					if (confirmElement):
						print("500 over Error")
						driver.close()
						driver.quit()
						return "500 Over Error"
			else:
				print("Not enough elements found")
			print("multiElement end")
		except NoSuchElementException as ex:
			driver.close()
			driver.quit()
			return "500Error"		
	print("test1.4")
	try:
		print("Test1.5")
		WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '検索')]"))).click()
		WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '賃貸マンション')]"))).click()
	except NoSuchElementException as ex:
		driver.close()
		driver.quit()
		print("test1.6")
		return "Error"
	print("test2")
	# getting result
	try:
		i = 0
		while(True):       
			i = i + 1 
			locator = (By.CSS_SELECTOR, f'div.p-table-body-item[style="{style_condition}"]')
			WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
			html = driver.page_source.encode('utf-8')
			soup = BeautifulSoup(html, "html.parser")        
			# print("soup", soup)
			address_group = soup.find_all("div", class_='p-table-body-item', style="grid-row-start: 1; grid-column: 14 / span 11;")
			for address_div in address_group:
				result.append(address_div.text)
				print(result)
			nextButton = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Go to next page"]')
			nextButton.click()
			expected_text = str(i*50 + 1)
			WebDriverWait(driver, delay).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, f'div.p-table-body-item[style="{style_condition2}"]'), expected_text))
		
	except NoSuchElementException as e:
		print("noElement")
		# return "Error"
	resultString = ','.join(result)	
	driver.close()
	driver.quit()
	return resultString

#FBV
def contactPage(request):
	form = ContactForm()
	return render(request, "contact.html", {"contactForm": form})

def postContact(request):
	if request.method == "POST" and request.is_ajax():
		form = ContactForm(request.POST)
		print(form["userId"].value())
		userId = form["userId"].value()
		password = form["password"].value()
		trackName = form["trackName"].value()
		stationFrom = form["stationFrom"].value()
		stationTo = form["stationTo"].value()
		distance = form["distance"].value()
		distanceType = form["distanceType"].value()
		priceMax = form["priceMax"].value()
		areaMin = form["areaMin"].value()
		level = form["level"].value()
		built_year = form["built_year"].value()
		built_month = form["built_month"].value()
		etc_multi = form["etc_multi"].value()

		res = scraping(userId, password, trackName, stationFrom, stationTo, distance, distanceType, priceMax, areaMin, level, built_year, built_month, etc_multi)
		# form.save()
		return JsonResponse({"success": res}, status=200)
	return JsonResponse({"success":False}, status=400)

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