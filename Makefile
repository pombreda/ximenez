##
## Makefile (for developers)
##
## FIXME: add rules to check in the CheeseShop.
##

egg:
	python2.4 setup.py bdist_egg --dist-dir .
	python2.5 setup.py bdist_egg --dist-dir .
	rm -rf build/ src/ximenez.egg-info/

clean:
	rm -f *.egg