# The Invisible Unicorn!

It is an API towards a dynamic nginx+lua+redis based proxy that
invisibly proxies your requests from the big bad internetz to
any host/port of your choosing.


# To install from source:

$ sudo python ./setup.py install

# To build a .deb package:

$ sudo apt-get -y install python-stdeb
$ python setup.py --command-packages=stdeb.command bdist_deb

# In either case, a script will be added to your path called dyamic-proxy-api

