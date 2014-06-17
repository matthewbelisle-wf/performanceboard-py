performanceboard-py
===================

Python plugin for [PerformanceBoard](https://github.com/mgbelisle/performanceboard)

Installation
-------

```
$ pip install git+ssh://git@github.com/mgbelisle/performanceboard-py.git#egg=performanceboard
```

Simple Usage
------------

Create a board if you don't have your own.

* Go to http://performanceboard-public.appspot.com/
* Click `+ New Board`

The API for the board will appear on the right side of the navbar.  Export this global config to
start posting things to PerformanceBoard.

```
$ export PERFORMANCEBOARD_API=http://performanceboard-public.appspot.com/api/ahlzfnBlcmZvcm1hbmNlYm9hcmQtcHVibGljchILEgVCb2FyZBiAgICAmc6UCgw
```

```py
import performanceboard

with performanceboard.Metric('jelly_donut'):
    print('eating jelly donut')
```

Testing
-------

```
$ nosetests performanceboard/tests
```
