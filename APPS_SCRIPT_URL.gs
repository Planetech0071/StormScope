function doPost(e) {
  var data = JSON.parse(e.postData.contents);
  var lat = data.lat;
  var lon = data.lon;
  var timestamp = new Date().toISOString();
  var props = PropertiesService.getScriptProperties();
  props.setProperty('lat', lat);
  props.setProperty('lon', lon);
  props.setProperty('timestamp', timestamp);
  return ContentService.createTextOutput("Location updated");
}

function doGet(e) {
  var props = PropertiesService.getScriptProperties();
  var result = {
    lat: props.getProperty('lat'),
    lon: props.getProperty('lon'),
    timestamp: props.getProperty('timestamp')
  };
  return ContentService.createTextOutput(JSON.stringify(result)).setMimeType(ContentService.MimeType.JSON);
}