#!/usr/bin/python3

import sys, os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__),'app'))

#TODO: find better way to set env variables
os.environ['DATABASE_URL']= "sqlite:////home/jdv/projects/website/SmartHome_PortoWeb/app/Database/database.db"

from homedash import app as application
