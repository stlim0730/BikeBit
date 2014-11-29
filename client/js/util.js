function request(path, data, dataType, async, successFunc, type) {
  var res;
  
  if(typeof async==="undefined") async = false;
  if(typeof dataType==="undefined") dataType = "json";
  if(typeof successFunc==="undefined") successFunc = function(_data) {res = _data;};
  if(typeof type==="undefined") type = "POST";

  $.ajax({
    url: path,
    type: type,
    dataType: dataType,
    data: data,
    async: async,
    success: successFunc
  });

  return res;
}

function randomFloat(inclusiveMin, exclusiveMax) { return Math.random() * (exclusiveMax - inclusiveMin) + inclusiveMin }

function randomInt(inclusiveMin, exclusiveMax) { return Math.floor(randomFloat(inclusiveMin, exclusiveMax)); }

function objectLength(obj) { var cnt = 0; for(key in obj) cnt++; return cnt; }

function toRadian(deg) { return deg * PI / 180; }

function getDegree(rad) { return rad * 180 / PI; }

function getDiagonalCenter(point1, point2) {
  var longAvg = (point2["longitude"] + point1["longitude"]) / 2;
  var latAvg = (point2["latitude"] + point1["latitude"]) / 2;
  return {longitude: longAvg, latitude: latAvg};
}

function getCenterFromBoundingBox(array) {
  var lons = [array[0], array[2]];
  var lats = [array[1], array[3]];

  return getDiagonalCenter(
    {longitude: lons[0], latitude: lats[0]},
    {longitude: lons[1], latitude: lats[1]}
  );
}

function getDistance(point1, point2) {
  var longitude1 = point1["longitude"];
  var longitude2 = point2["longitude"];
  var latitude1 = point1["latitude"];
  var latitude2 = point2["latitude"];

  var lat1Rad = getRadian(latitude1);
  var lat2Rad = getRadian(latitude2);
  var latitudeDiff = getRadian(latitude2-latitude1);
  var longitudeDiff = getRadian(longitude2-longitude1);

  var a = Math.sin(latitudeDiff/2) * Math.sin(latitudeDiff/2) +
          Math.cos(latitude1) * Math.cos(latitude2) *
          Math.sin(longitudeDiff/2) * Math.sin(longitudeDiff/2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

  var distance = EARTH_RADIUS * c;

  return distance;
}

function dom(jqueryObj) { return jqueryObj.get(0); }

function getTimeString() {
  var date = new Date();
  var h = date.getHours();
  var m = date.getMinutes();
  var s = date.getSeconds();

  if(h<10) h = "0" + h;
  if(m<10) m = "0" + m;
  if(s<10) s = "0" + s;

  return h + ":" + m + ":" + s;
}

function bbLog(s) {
  console.log("#BikerBit [" + getTimeString() + "] - " + s)
}

// function toCartesian(longitude, latitude, altitude, radius) {
//   var phi = (90 - latitude) * PI / 180;
//   var theta = (180 - longitude) * PI / 180;

//   var x = (radius + altitude) * Math.sin(phi) * Math.cos(theta);
//   var y = (radius + altitude) * Math.cos(phi);
//   var z = (radius + altitude) * Math.sin(phi) * Math.sin(theta);

//   return new THREE.Vector3(x, y, z);
// }
