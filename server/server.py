# AUTHOR: SEONGTAEK LIM (seongtaek.lim0730@gmail.com)

from __future__ import division
import sys
import os
import uuid
import tornado
from tornado import web
from tornado import wsgi
from tornado import gen
from tornado import template
from myUtility import *

# START CONSTANTS
SECOND = 1000
MINUTE = 60
HOUR = 60
M = 100
KM = 1000
FOOT = 12
MILE = 5280
DATA_LABEL = "BikeBit Record"

SERVER_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.join(SERVER_PATH, os.pardir)
DEFAULT_SERVER_CONF = os.path.join(SERVER_PATH, "conf/bikeBitServerConf.json")
# END CONSTANTS

# START CONFIGURATION
serverConfFile = DEFAULT_SERVER_CONF
if(len(sys.argv)>2):
  serverConfFile = sys.argv[1]
serverConf = readJsonFile(serverConfFile)

serverPort = serverConf["serverOptions"]["port"]
clientPath = os.path.join(ROOT_PATH, serverConf["serverOptions"]["clientPath"])
uploadPath = os.path.join(SERVER_PATH, serverConf["serverOptions"]["uploadPath"])
imagePath = clientPath + "/img"
samplePath = clientPath + "/sample"
# END CONFIGURATION

# START HANDLERS
class indexPageHandler(tornado.web.RequestHandler):
  @gen.coroutine
  def get(self):
    self.render("index.html")
    bbLog("called indexPageHandler")

class indexPageBookmarkHandler(tornado.web.RequestHandler):
  @gen.coroutine
  def get(self, bookmark):
    self.render("index.html" + bookmark)
    bbLog("called indexPageBookmarkHandler")

class uploadHandler(tornado.web.RequestHandler):
  def post(self):
    diameter = float(self.get_argument("diameterArg"))
    unit = self.get_argument("unitArg")
    fileObj = self.request.files["fileArg"][0]
    fileName = fileObj["filename"]
    extension = os.path.splitext(fileName)[1]
    tempFileName = str(uuid.uuid4()) + extension
    uploadFileHandler = open(tempFileName, "w")
    uploadFileHandler.write(fileObj["body"])
    uploadFileHandler.close()
    readHandler = readTextFile(tempFileName)
    results = self.process(readHandler, diameter, unit)
    readHandler.close()
    # self.write(tornado.escape.json_encode(results))
    # self.finish(tempFileName + " is uploaded!! Check %s folder" %uploadPath)
    self.render("viz.html", data=tornado.escape.json_encode(results))
    bbLog("called uploadHandler")

  def process(self, fileHandler, diameter, unit):
    # START TARGET DATA FORMAT
    # data: {
    #   xs: {
    #     'data1': 'x1',
    #     'data2': 'x2',
    #   },
    #   columns: [
    #     ['x1', 10, 30, 45, 50, 70, 100],
    #     ['x2', 30, 50, 75, 100, 120],
    #     ['data1', 30, 200, 100, 400, 150, 250],
    #     ['data2', 20, 180, 240, 100, 190]
    #   ]
    # }
    # END TARGET DATA FORMAT
    results = { "data": { "xs":{}, "columns":[]} } # RESULTS TO RETURN
    lineCnt = 0 # LINE COUNT OF INPUT FILE
    tempList = [] # TEMPORARY LIST
    triggerLists = [] # GROUPED DATA POINT
    instVLists = [] # LIST OF INSTANTANEOUS V
    # START INPUT RAW DATA
    line = fileHandler.readline()
    while line!="":
      num = int(line)
      if lineCnt == 0:
        # FIRST DATA
        tempList.append(num)
      elif num >= tempList[lineCnt-1]:
        # KEEP GOING
        tempList.append(num)
      elif num < tempList[lineCnt-1]:
        # NEW LIST
        triggerLists.append(tempList)
        tempList = [num]
        lineCnt = 0
      else:
        print "Unexpected condition"
      lineCnt += 1
      line = fileHandler.readline()
    triggerLists.append(tempList) # THE FINAL LIST
    # END INPUT RAW DATA
    # START FORMATTING DATA
    triggerCnt = 0 # COUNT OF DATA POINT
    triggerListCnt = 0 # COUNT OF GROUP OF DATA POINT
    deltaD = PI * diameter # DISTANCE TRAVELED PER ROTATION
    maxInstV = 0
    instVCnt = 0
    instVSum = 0
    for triggers in triggerLists:
      # FOR EACH TRIGGER DATA GROUP
      instVs = []
      instVs.append(0)
      for i in range(1, len(triggers)):
        deltaT = (triggers[i] - triggers[i-1]) / SECOND # DELTA T PER ROTATION IN SECONDS
        instV = 0
        if unit=="cm":
          instV = (((deltaD / M) / KM) * MINUTE * HOUR) / deltaT # INSTANTANEOUS VELOCITY PER ROTATION (km/h)
        else:
          instV = (((deltaD / FOOT) / MILE) * MINUTE * HOUR) / deltaT # INSTANTANEOUS VELOCITY PER ROTATION (mph)
        instVs.append(instV)
        triggerCnt += 1
      instVCnt += len(instVs)
      instVSum += sum(instVs)
      instVLists.append(instVs)
      maxInstV = max(maxInstV, max(instVs))
      triggerListCnt += 1
      xName = "x" + str(triggerListCnt)
      yName = DATA_LABEL + str(triggerListCnt)
      triggers.insert(0, xName)
      instVs.insert(0, yName)
      results["data"]["xs"][yName] = xName
      results["data"]["columns"].append(triggers)
      results["data"]["columns"].append(instVs)
    results["maxInstV"] = maxInstV
    results["avgInstV"] = instVSum / instVCnt
    if unit == "cm":
      results["unitV"] = "km/h"
      results["unitD"] = "km"
      results["totalD"] = ((triggerCnt * diameter * PI) / M) / KM
    else:
      results["unitV"] = "mph"
      results["unitD"] = "miles"
      results["totalD"] = ((triggerCnt * diameter * PI) / FOOT) / MILE
    # END FORMATTING DATA
    return results

# class bikeBitPageHandler(tornado.web.RequestHandler):
#   @gen.coroutine
#   def get(self):
#     mode = self.get_query_argument("mode")
#     self.render("bikeBit.html", mode=mode)
#     bbLog("called bikeBitPageHandler")
# END HANDLERS

# START INITIALIZATION
serverApp = tornado.wsgi.WSGIApplication(
  [
    (r"/", indexPageHandler),
    (r"/index(.*)", indexPageBookmarkHandler),
    (r"/img/(.*)", tornado.web.StaticFileHandler, {"path": imagePath}),
    (r"/sample/(.*)", tornado.web.StaticFileHandler, {"path": samplePath}),
    (r"/upload", uploadHandler)
    # (r"/bikeBit", bikeBitPageHandler),
  ],
  static_path=clientPath,
  template_path=clientPath,
  debug=True
)
# END INITIALIZATION

# START
bbLog("BikeBit server has started")
serverApp.listen(serverPort)
bbLog("The server is listening on port " + str(serverPort))
tornado.ioloop.IOLoop.instance().start()
# END
