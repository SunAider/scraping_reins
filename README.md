# Django guide for implementing AJAX
This is the example project for implementing Forms with Django.



### Installation guide
- Clone repository

	`
	git clone https://github.com/agiledesign2/django-forms-examples.git
	`

- cd to repository.

- Create a virtualenv by following command
	- **For Linux/Mac**
	
		`
		virtualenv -p python3 .
		`

	- **For Windows**

		`
			virtualenv .
		`

- Activate virtualenv

	- **For Linux/Mac**
	
		`
			source bin/activate
		`

	- **For Windows**

		`
			.\Scripts\activate
		`

- Install required packages

	- **For Linux/Mac**
		
		`
			pip3 install -r requirements.txt
		`

	- **For Windows**

		`
			pip install -r requirements.txt
			pip install django-multiselectfield
			pip install selenium
			pip install bs4
			pip install webdriver_manager
		`

- cd to src and run the server
	
	- **For Linux/Mac**
		
		`
			python manage.py runserver
		`

	- **For Windows**

		`
			python manage.py runserver
		`
