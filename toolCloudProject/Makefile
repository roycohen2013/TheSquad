ready: clean update
	python3 newSlate.py
push:
	git push origin master
pull:
	git pull origin master
clean:
	rm -rf *.pyc
test: ready
	python3 manage.py runserver
update: pull push
run:
	python3 manage.py runserver

