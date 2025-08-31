function doPost(e) {
  var props = PropertiesService.getScriptProperties();
  props.setProperty('strike', e.postData.contents);
  return ContentService.createTextOutput("Strike info stored");
}

function doGet(e) {
  var props = PropertiesService.getScriptProperties();
  var strike = props.getProperty('strike');
  var result = strike ? strike : '{}';
  // if ?clear=1, clear it out lez go
  if (e.parameter.clear == '1') {
    props.deleteProperty('strike');
  }
  return ContentService.createTextOutput(result).setMimeType(ContentService.MimeType.JSON);
}