from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		exclude = ["timestamp", ]
		
		labels = {'userId': "ユーザID", 'password': "パスワード", 'trackName' : "沿線１/沿線名", 'stationFrom' :  "駅名(From)", 'stationTo' : "駅名(To)",
			 "distance" : "駅から徒歩", "distanceType" : "以内", "priceMax" : "賃料(Max)", "areaMin" : "建物使用部分面積(Min)", "level" : "所在階", "built_year" : "築年月(年)", "built_month" : "築年月(月)", "etc_multi" : "設備・条件・住宅性能等" }
	
		widgets = {
			# 'message': forms.Textarea(attrs={'rows':4, 'cols':15}),
			'password': forms.PasswordInput(attrs={'rows':4, 'cols':15}),
			'etc_multi': forms.CheckboxSelectMultiple,
		}

	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({
		    'class': 'form-control'})
