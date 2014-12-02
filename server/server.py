# AUTHOR: SEONGTAEK LIM (seongtaek.lim0730@gmail.com)

import sys
import os
import uuid
import tornado
from tornado import web
from tornado import gen
from tornado import template
from myUtility import *

# START CONSTANTS
SECOND = 1000

SERVER_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.join(SERVER_PATH, os.pardir)
DEFAULT_SERVER_CONF = os.path.join(SERVER_PATH, "conf/bikerBitServerConf.json")
# END CONSTANTS

# START CONFIGURATION
serverConfFile = DEFAULT_SERVER_CONF
if(len(sys.argv)>2):
  serverConfFile = sys.argv[1]
serverConf = readJsonFile(serverConfFile)

serverPort = serverConf["serverOptions"]["port"]
clientPath = os.path.join(ROOT_PATH, serverConf["serverOptions"]["clientPath"])
uploadPath = os.path.join(SERVER_PATH, serverConf["serverOptions"]["uploadPath"])
imagePath = clientPath + "/img";
# END CONFIGURATION

# START HANDLERS
class indexPageHandler(tornado.web.RequestHandler):
  @gen.coroutine
  def get(self):
    self.render("index.html")
    bbLog("called indexPageHandler")

class uploadHandler(tornado.web.RequestHandler):
  def post(self):
    diameter = self.get_argument("diameterArg")
    unit = self.get_argument("unitArg")
    fileObj = self.request.files["fileArg"][0]
    fileName = fileObj["filename"]
    extension = os.path.splitext(fileName)[1]
    tempFileName = str(uuid.uuid4()) + extension
    uploadFileHandler = open(tempFileName, "w")
    uploadFileHandler.write(fileObj["body"])
    uploadFileHandler.close()
    readHandler = readTextFile(tempFileName)
    result = self.process(readHandler)
    readHandler.close()
    self.write("OK")
    # self.finish(tempFileName + " is uploaded!! Check %s folder" %uploadPath)
    # self.render("bikerBit.html")
    bbLog("called uploadHandler")

  def process(self, fileHandler):
    lineCnt = 0 # LINE COUNT OF INPUT FILE
    triggerCnt = 0 # COUNT OF DATA POINT
    tempList = [] # TEMPORARY LIST
    triggerLists = [] # GROUPED DATA POINT
    deltaTLists = [] # LIST OF DELTA T
    maxList = [] # MAXIMUM VALUES OF EACH TRIGGER
    # results = {"data": { "xs":{}, "columns":[] }}
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
        maxList.append(tempList[-1])
        tempList = [num]
        lineCnt = 0
      else:
        print "Unexpected condition"
      lineCnt += 1
      line = fileHandler.readline()
    triggerLists.append(tempList) # THE FINAL LIST
    maxList.append(tempList[-1]) # THE ITEM IN THE FINAL LIST
    for triggers in triggerLists:
      # FOR EACH TRIGGER DATA GROUP
      deltaTs = []
      deltaTs.append(0)
      for i in range(1, len(triggers)):
        deltaTs.append((triggers[i] - triggers[i-1]) / SECOND) # DELTA T PER ROTATION IN SECONDS
      deltaTLists.append(deltaTs)
      triggerCnt += 1
    return deltaTLists

# class bikerBitPageHandler(tornado.web.RequestHandler):
#   @gen.coroutine
#   def get(self):
#     mode = self.get_query_argument("mode")
#     self.render("bikerBit.html", mode=mode)
#     bbLog("called bikerBitPageHandler")
# END HANDLERS

# START INITIALIZATION
serverApp = tornado.web.Application(
  [
    (r"/", indexPageHandler),
    (r"/img/(.*)", tornado.web.StaticFileHandler, {"path": imagePath}),
    (r"/upload", uploadHandler)
    # (r"/bikerBit", bikerBitPageHandler),
  ],
  static_path=clientPath,
  template_path=clientPath,
  debug=True
)
# END INITIALIZATION

# START
bbLog("BikerBit server has started")
serverApp.listen(serverPort)
bbLog("The server is listening on port " + str(serverPort))
tornado.ioloop.IOLoop.instance().start()
# END
