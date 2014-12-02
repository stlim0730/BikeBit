import simplejson as json
from simplejson import loads
import math
import time
from datetime import datetime
from random import randint
import re

# START CONSTANTS
PI = math.pi
urlRegex = re.compile(
  r'^https?://'  # http:// or https://
  r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
  r'localhost|'  # localhost...
  r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
  r'(?::\d+)?'  # optional port
  r'(?:/?|[/?]\S+)$', re.IGNORECASE)
# END CONSTANTS

# START UTILITY FUNCTIONS
def randomInt(inclusiveMin, exlusiveMax):
  return randint(inclusiveMin, exlusiveMax-1)

def readJsonFile(filename):
  return json.load(open(filename))

def readTextFile(filename):
  return open(filename, "r") 

def printJsonObj(obj, fname="", i=2):
  if obj is None:
    print "JSON object is None"
    return 1
  filename = fname
  outputString = json.dumps(obj, sort_keys=True, indent=i*" ")
  if filename is "":  # standard output
    print(outputString)
    return 0
  else: # output file
    if not filename.endswith(".json"):
      filename = filename + ".json"
    f = open(filename, "w")
    f.write(outputString)
    f.close()
    return 0

def outputString(content, filename=""):
  if filename=="":
    print(content)
  else:
    f = open(filename, "w")
    f.write(content)
    f.close()

def search(listOfDict, val):
  for dictionary in listOfDict:
    # for key in dictionary:
    if dictionary["username"]==val:
      return dictionary
  return None

def binarySearch(theList, value, low, high):
  if high < low:
    return None # indicates the value isn't in theList
  mid = int(math.floor((low + high)/2))
  if theList[mid] > value:
    return binarySearch(theList, value, low, mid-1)
  elif theList[mid] < value:
    return binarySearch(theList, value, mid+1, high)
  else:
    return mid

def listHas(theList, target):
  val = binarySearch(theList, target, 0, len(theList)-1)
  if val is None:
    return False
  else:
    return True

def isURL(url):
  if urlRegex.match(url) is None:
    return False
  else:
    return True

def getTimeString():
  return time.strftime("%H:%M:%S")

def bbLog(s):
  print "#BikeBit [" + getTimeString() + "] - " + s
# END UTILITY FUNCTIONS
