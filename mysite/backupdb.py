import logging
import os

BASE_DIR = os.path.dirname(__file__)

cmdStr = (r'cd /home/www/AccountOnline/Mytest '
          '&& rm -rf db db2'
          '&& dd if=db.txt |openssl des3 -d -k "8yhn(IJN&U*"|tar zxf - '
          '&& mv db db2 '
          '&& [ "x$(diff db2/production.sqlite3 ../src/mysite/production.sqlite3)" != "x" ] '
          '&& rm -rf /home/www/AccountOnline/Mytest/db '
          '&& mkdir -p /home/www/AccountOnline/Mytest/db '
          '&& cp /home/www/AccountOnline/src/mysite/production.sqlite3 /home/www/AccountOnline/Mytest/db/ '
          '&& cd /home/www/AccountOnline/Mytest '
          '&& rm -rf db.txt '
          '&& tar -zcvf - db|openssl des3 -salt -k "8yhn(IJN&U*" | dd of=db.txt '
          '&& cp db.txt db.txt_`date +%Y-%m-%d[%H:%M:%S]`'
          '&& rm -rf db db2'
          '&& git add .'
          '&& git commit -a -m "routinely update"'
          '&& git push')

os.system(cmdStr)