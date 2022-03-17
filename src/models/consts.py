from xml.dom import minidom
import os

file = minidom.parse(os.path.abspath('connection.xml')) #minidom.parse('/Users/NikolaKolarov/Desktop/WBD python/WBD/src/connection.xml')

__hosts = file.getElementsByTagName('host')
__users = file.getElementsByTagName('user') 
__passwords = file.getElementsByTagName('pass')
__databases = file.getElementsByTagName('database')

# print(os.path.abspath('connection.xml'))
# Info
HOST = str(__hosts[0].firstChild.data) #'127.0.0.1'
DATABASE =  str(__databases[0].firstChild.data)#'WBD'
USER =  str(__users[0].firstChild.data) #'root'
PASSWORD = str(__passwords[0].firstChild.data) #'Nikolakolarov03!'