import sys
import os
import tornado
from tornado import web
from tornado import gen
from tornado import template
from myUtility import *

# START CONSTANTS
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
imagePath = clientPath + "/img";
# END CONFIGURATION

# START HANDLERS
class indexPageHandler(tornado.web.RequestHandler):
  @gen.coroutine
  def get(self):
    self.render("index.html")
    bbLog("called indexPageHandler")

class bikerBitPageHandler(tornado.web.RequestHandler):
  @gen.coroutine
  def get(self):
    mode = self.get_query_argument("mode")
    self.render("bikerBit.html", mode=mode)
    bbLog("called bikerBitPageHandler")
# END HANDLERS

# START INITIALIZATION
serverApp = tornado.web.Application(
  [
    (r"/", indexPageHandler),
    (r"/img/(.*)", tornado.web.StaticFileHandler, {"path": imagePath}),
    (r"/bikerBit", bikerBitPageHandler)
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
