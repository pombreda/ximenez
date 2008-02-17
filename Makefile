##
## Makefile (for developers)
##

egg:
	python2.4 setup.py bdist_egg --dist-dir .
	python2.5 setup.py bdist_egg --dist-dir .
	rm -rf build/ src/ximenez.egg-info/

register:
	python2.4 setup.py register

upload:
	python2.4 setup.py bdist_egg --dist-dir . upload
	python2.5 setup.py bdist_egg --dist-dir . upload

clean:
	rm -f *.egg