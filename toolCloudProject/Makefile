ready: clean pull
	python3 newSlate.py
push:
	git push origin master
pull:
	git pull origin master
clean:
	rm -rf *.pyc
test: ready
	python3 manage.py runserver

