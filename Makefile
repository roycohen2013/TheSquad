ready: clean
	git pull origin master
push:
	git push origin master
clean:
	rm -rf *.pyc

