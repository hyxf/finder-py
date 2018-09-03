gutils-cli
=======

Python common tools, support [win, mac, linux]

### Use help

~~~bash
~ gutils
usage: gutils [-h] {resize,share} ...

Hey, gutils 1.1.7

optional arguments:
  -h, --help      show this help message and exit

Available commands:
  {resize,share}
    resize        images resize
    share         LAN file sharing

make it easy

~~~

### Install

~~~bash
~ sudo pip install gutils
~~~

If the following error is printed

~~~bash
Could not find a version that satisfies the requirement gutils (from versions: )

No matching distribution found for gutils
~~~

You can use 'zh' mirrors

> tsinghua: https://pypi.tuna.tsinghua.edu.cn/simple/
>
> douban  : https://pypi.douban.com/simple/

~~~bash
~ sudo pip install gutils -i https://pypi.douban.com/simple/
~~~

Install the latest version with Github

~~~bash
~ sudo pip install git+https://github.com/hyxf/gutils-cli.git@master
~~~

---------

### Uninstall

~~~bash
~ sudo pip uninstall gutils
~~~

### Upgrade

~~~bash
~ sudo pip install --upgrade gutils
~~~

or

~~~bash
~ sudo pip install -U gutils
~~~

--------------------

### build source

local install [for mac]

~~~bash
~ chmod +x install.sh
~ ./install.sh
~~~

pypi upload

~~~bash
~ chmod +x deploy.sh
~ ./deploy.sh
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
