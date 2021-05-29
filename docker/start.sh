#!/bin/bash
#/usr/bin/mysqld_safe --skip-grant-tables &
/usr/bin/mysqld_safe &
sleep 5
mysql -u root -t < infrastructure/norhwind/northwind-nofks-setup.sql
mysql -u root -e "CREATE USER 'demo'@'localhost' IDENTIFIED BY 'demo'"
mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'demo'@'localhost'"
#/bin/bash
dic