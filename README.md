finder-py
=======

It is a tool for 'LAN file Share', support [win, mac, linux]

### Use help

~~~bash
~ finder
usage: finder [-h] [-i IP] [-p PORT] [-d DIR] [-q] [-u] [--start]
              [--pid_file PID_FILE] [--log_file LOG_FILE] [--stop]

LAN file sharing 1.2.2

optional arguments:
  -h, --help            show this help message and exit
  -i IP, --ip IP        Local IP
  -p PORT, --port PORT  Local port
  -d DIR, --dir DIR     Shared directory path
  -q, --qr              Show QRCode
  -u, --upload          Support upload
  --start               daemon start
  --pid_file PID_FILE   pid_file
  --log_file LOG_FILE   log_file
  --stop                daemon stop

make it easy
~~~

### Install

~~~bash
~ sudo pip install finder-py
~~~

or 

~~~bash
~ sudo pip install finder-py -i https://pypi.tuna.tsinghua.edu.cn/simple/
~~~

Install the latest version with Github

~~~bash
~ sudo pip install git+https://github.com/hyxf/finder-java.git@master
~~~

---------

### Uninstall

~~~bash
~ sudo pip uninstall finder-py
~~~

### Upgrade

~~~bash
~ sudo pip install --upgrade finder-py
~~~

or

~~~bash
~ sudo pip install -U finder-py
~~~

--------------------

### build source

local install [for mac]

~~~bash
~ chmod +x install.sh
~ ./install.sh
~~~


----------------------

### License


    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
