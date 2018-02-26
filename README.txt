add this file to avoid FileNotFoundError: [Errno 2] No such file or directory: 'D:\\coding\\pgzero\\README.txt' when create a locally-editable install use pip3.
pip3 install --editable .

maybe the default version of pgzero installed by pip is lower so when debug pgzero code,will not find pgzrun moduel.