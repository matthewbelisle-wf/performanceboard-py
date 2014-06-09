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

```
$ curl -X POST http://performanceboard-public.appspot.com/api/
http://performanceboard-public.appspot.com/api/ahlzfnBlcmZvcm1hbmNlYm9hcmQtcHVibGljchILEgVCb2FyZBiAgICA-JaVCQw
```

Export this global config to start posting things to PerformanceBoard.

```
$ export PERFORMANCEBOARD_URL=http://performanceboard-public.appspot.com/api/ahlzfnBlcmZvcm1hbmNlYm9hcmQtcHVibGljchILEgVCb2FyZBiAgICA-JaVCQw
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
