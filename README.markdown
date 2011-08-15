Conqueue
======
Conqueue is a queue manager library built on the top of redis. You can create jobs in queues, and process later with worker
scripts asynchronously.

Installation
-------------

```
git clone git://github.com/emre/conqueue.git
sudo python setup.py install
```
In order to use conqueue, you need to instal redis-py library (sudo pip install redis), and a working redis-server instance.

Conqueue works with Configuration objects. There are some options you can choose for conqueue's workflow.

A simple worker script that listens 'feeds' queue.

``` python
from conqueue.conqueue import Conqueue
from conqueue.lib.config import BaseConfig

class Configuration(BaseConfig):
   REDIS_SERVER_INFO = {
      'host'     : 'localhost',
      'port'     : 6379,
      'db'       : 0,
   }

   USE_MULTI_PROCESSING = True
   POOLSIZE_PER_WORKER  = 5

def parse_feed(data):
    import time
    # make something with the feed
    time.sleep(2)
    print data

# listens two queues: ['feeds', 'messages']
worker = Conqueue(Configuration).worker()
worker.register_task('feeds', parse_feed)

worker.listen_tasks()

```

Client script that puts jobs to the worker
``` python
from conqueue.conqueue import Conqueue

client  = Conqueue(Configuration).client()
client.add_task('messages', 'how you doing?')
```

Configuration Options
-------------
### USE_MULTI_PROCESSING = True/False - Default Value: True
If set True, conqueue forks worker function based on cpu count by default.

### POOLSIZE_PER_WORKER = Integer - Default Value: None
If you don't set this explicitly, conqueue forks workers based on CPU count. (which is recommended.)

### PREFIX = 'conqueue' - Default Value: Conqueue
Prefix for the redis keys

### RETRY_BEHAVIOUR      = (True, 100)
if worker functions raised any exception, conqueue catches it, and requeue if you want. First argument is for enabling/disabling.
second argument is for retry count.

Task Priority
-------------
There is no support for this. But you can do it manually by creating more instances for your workers. If you use register_task more than one
in one worker, first registered queue will have high priority.

Basic Admin Script
-------------
there is a simple and stupid script for queue monitoring in the /tools directory. A frontend with more meaningful information
will be added in the future.

```
emre@amy:~/github_projects/conqueue/tools$ python conqueue-admin.py
conqueue:feeds 15
conqueue:feeds:failed 1
conqueue:messages 5
```

Todo
------------
* Management/Monitoring Frontend
* _Optional_ gevent based pool instead of multiprocessing library.
* Redis sharding in the back. (with consistent hashing: <http://emreyilmaz.me/implementing-consistent-hashing-into-your-redis>)

Notes
------------
Remember that, conqueue is not tested well. It is a weekend hackathon project, and still in early development.