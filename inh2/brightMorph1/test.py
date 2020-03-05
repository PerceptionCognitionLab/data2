import mysql.connector
import sys
import os
SCRIPT_DIR=os.environ.get('SCRIPT_DIR')
sys.path.append(SCRIPT_DIR)
from expLib import *

useDB=True
dbConf = exp
expName='morph1'
print(checkExp(expName,dbConf))
exit()

