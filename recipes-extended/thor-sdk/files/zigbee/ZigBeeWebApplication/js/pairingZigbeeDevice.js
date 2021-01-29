var zigbeeDeviceTypeByID ={
  ONOFFLight:"0x0100",
  DimmableLight:"0x0101",
  ColorDimmableLight:"0x0102",
  ONOFFLightSwitch:"0x0103"
}

async function createPairingDevicesList(){
  localStorage.removeItem("dataName");
   var led;
    var retrievedData = localStorage.getItem("storageName");
    var data= JSON.parse(retrievedData);


    for (var i = 0; i < data.length ; i++) {

        var table = document.getElementById("paringTable");
        var dataList =table.insertRow(i+1);

               if(data[i][2]=="0x0100"){

                 led = "<td id =deviceType_" +i+ " >LED-ON      <img src='Image/blubon.jpeg' height='40' align= center ></img></td></tr>"
               }
               else{
                 led = "<td id =deviceType_" +i+">LED-OFF     <img src='Image/bluboff.jpeg' height='40' align= center ></img></td></tr>"
               }
              dataList.innerHTML ="<tr><td id =deviceName_" +i+">"    + data[i][0] + "</td><td id =euid64_ID"+i+">"+ data[i][1] +"</td>" + led;

       postPairingDevicesDataOnServer(data);
       myVar = setInterval(serverDataUpdate, 1000);


}
}
function postPairingDevicesDataOnServer(pairData){
var pairingDevicesList = [];

  for (var rowIndex = 0; rowIndex < pairData.length; rowIndex++)
  {

     var deviceName = pairData[rowIndex][0];
     var eui64 = pairData[rowIndex][1];
     var deviceType = pairData[rowIndex][2];
     var nodeId = pairData[rowIndex][3];

     item = {}
     item ["deviceName"] = deviceName;
     item ["eui64"] = eui64;
     item ["deviceType"]=deviceType;
     item ["nodeId"] = nodeId;

     pairingDevicesList.push(item);
  }

  $.ajax({
      type: "POST",
      //url: "http://localhost/cgi-bin/sendData.php",
      url: 'https://localhost/cgi-bin/zigbee/sendData.php',
      dataType: "text",
      data: { json: JSON.stringify(pairingDevicesList) },
      success: function () {
          console.log("success");
      },
      error: function(response) {
      alert(response.status);
      console.log("error");
    }
  });

}

function serverDataUpdate(){
  var items = [];
  $.ajax({
    type: "GET",
     //url: "http://localhost/cgi-bin/serverEvent.php",
    url: "https://localhost/cgi-bin/zigbee/serverEvent.php",
    crossDomain: true,
    cache: true,
    dataType :"JSON",
    success: function(data, textStatus, jqXHR) {

        var obj =data;
        items.push(obj);
        for (var i =0 ; i< items.length ;i++){

          if (($("#euid64_ID"+i).text()) === items[i].deviceEndpoint.eui64)
          {

          if(items[i].commandData === "0x0100"){
            $("#deviceType_"+i).html('LED-ON  <img src="Image/blubon.jpeg" height="40" align= "center" >');

          }
          else if(items[i].commandData === "0x0000")
          {

           $("#deviceType_"+i).html('LED-OFF  <img src="Image/bluboff.jpeg" height="40" align= "center" >');

          }
	  else{
            console.log("Invalid Device Type");
         }
        }
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
        console.log(textStatus);
        console.log(jqXHR);
    }
});

}
