#!/bin/bash
echo "Entering container..."
echo "Starting MySQL server..."
/usr/bin/mysqld_safe &
sleep 1
echo "Done!"
dic