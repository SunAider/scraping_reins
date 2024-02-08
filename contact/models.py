from django.db import models
from multiselectfield import MultiSelectField

# Create your models here.
class Contact(models.Model):
	userId = models.CharField(max_length=50, error_messages={'invalid' : 'aaaaa'})
	password = models.CharField(max_length = 50)
	trackName = models.CharField(max_length=50)
	stationFrom = models.CharField(max_length=50, blank=True)
	stationTo = models.CharField(max_length=50, blank=True)
	distance = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
	distanceType_Options = [
		(1, '分'),
        # (2, 'ｍ'),
	]
	distanceType = models.IntegerField(choices=distanceType_Options, default='1', blank=False)	
	priceMin = models.DecimalField(max_digits=10, decimal_places=1, blank=True)
	priceMax = models.DecimalField(max_digits=10, decimal_places=1, blank=True)
	roomMin = models.DecimalField(max_digits=2, decimal_places = 0, blank=True)
	areaMin = models.DecimalField(max_digits=10, decimal_places=1, blank=True)
	level = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
	built_year = models.DecimalField(max_digits=4, decimal_places = 0, blank=True)
	# etc = models.TextField(blank=True)
	etc_CHOICES =( 
		("0", ""),
		("1", "ペット相談"), 
		("2", "事務所使用可"),
		("3", "エレベーター"),
	) 
	etc_multi = MultiSelectField(choices = etc_CHOICES) 

	# name = models.CharField(max_length = 100, blank=True)
	# email = models.EmailField(blank=True)
	# message = models.TextField(blank=True)
	timestamp = models.DateTimeField(auto_now_add = True, blank=True)

	def __str__(self):
		return self.name