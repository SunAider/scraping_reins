from django import forms
from .models import Contact
from django.utils.translation import gettext as _

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		exclude = ["timestamp", ]
		labels = {'propertyType1': "物件種別１",'propertyType2': "物件種別２",'userId': "ユーザID", 'password': "パスワード", 'trackName' : "沿線１/沿線名", 'stationFrom' :  "駅名(From)", 'stationTo' : "駅名(To)",
			 "distance" : "駅から徒歩(分以内):", "distanceType" : "以内", "priceMin" : "賃料(Min)万円", "priceMax" : "賃料(Max)万円", "areaMin" : "建物使用部分面積(Min)", "level" : "所在階", "built_year" : "築年(Min)西暦", "roomMin" : "間取部屋数(Min)", "etc_multi" : "設備・条件・住宅性能等" }
	
		widgets = {
			# 'message': forms.Textarea(attrs={'rows':4, 'cols':15}),
			'password': forms.PasswordInput(attrs={'rows':4, 'cols':15}),
			'etc_multi': forms.CheckboxSelectMultiple,
		}
		error_messages = {
			'userId' : {
				'invalid': _("Enter a ")
			}
			,
			'priceMax' : {
				'error' : _("sttttop!"),
			}
		}

	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		# self.fields['priceMax'].error_messages = {'invalid': 'stop!'}
		# self.fields['userId'].error_messages = {'required': 'ssssssssss!'}
		for field in self.fields:
			self.fields[field].widget.attrs.update({
		    'class': 'form-control'})
