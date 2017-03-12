#!/bin/bash
rsync -aPc --no-p --no-g --chmod=o=r,ug=rw,D+X --no-o --perms --delete src/ $1:/home/pi/garage