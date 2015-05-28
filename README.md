# ask-konyshev
yami

### Sphinx
- install sphinx
```sh
$ sudo apt-get install sphinxsearch
```
- edit sphinx.conf and put to /etc/sphinxsearch/ 
- run indexer
```sh
$ sudo indexer --all
```
- test
```sh
$ search <some query>
```



### Memcached
- install memcached
```sh
$ sudo apt-get install memcached
```
- start
```sh
$ sudo /etc/init.d/memcached start
```
- and install python memcache
```sh
$ sudo pip install python-memcached
