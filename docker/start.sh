#!/bin/bash
echo "Entering container..."
echo "Starting MySQL server..."
/usr/bin/mysqld_safe &
sleep 5
echo "Importing sample databases..."
mysql -u root -t < infrastructure/norhwind/northwind-nofks-setup.sql
mysql -u root -e "CREATE USER 'demo'@'localhost' IDENTIFIED BY 'demo'"
mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'demo'@'localhost'"
echo "Done!"
echo "Starting dIC..."
dic