  var zigbeeDeviceTypeByID ={
    ONOFFLight:"0x0100",
    DimmableLight:"0x0101",
    ColorDimmableLight:"0x0102",
    ONOFFLightSwitch:"0x0103"
  }
  var modal = document.getElementById('myModal');
  var span = document.getElementsByClassName("close")[0];

  var modal_2 = document.getElementById('myModal_2');
  var span_2 = document.getElementsByClassName("close_2")[0];
   function buttonDisabled()
  {
   document.getElementById("pairbutton").disabled = true;
   document.getElementById("deletebutton").disabled = true;
   //document.getElementById("helpbutton").disabled = false;
  }
    function scaningZigbeeDevices() {
    document.getElementById("tablerow").style.display = "none";
    document.getElementById("label").style.display = "none";

      if($('table').find('td').length == 0) {
          document.getElementById("loader").style.display = "block";
          document.getElementById("label").style.display = "block";
      }
      startScaningZigbeeDevices()
      myVar = setTimeout(hideLoaderPage, 50000);
 }

function hideLoaderPage() {
     document.getElementById("loader").style.display = "none";
     document.getElementById("label").style.display = "none";

     getListScanZigbeeDevicesFromServer();
}

function startScaningZigbeeDevices(){
    $.ajax({
      type: 'POST',
      dataType: "script",
        url: 'https://localhost/zigbee/scanZigbeeDevices.sh',
      success: function(data,textStatus, xhr) {
            console.log(xhr.status);
            console.log("Success");
        },
      error: function(xhr, textStatus) {
             alert(xhr.status,xhr.url);

            console.log(xhr.status);
            console.log("error");
        }
       });
}
 function getListScanZigbeeDevicesFromServer() {
  var indexI ,indexJ, indexk, dataNumlenght;

    $.ajax({
      url: 'https://localhost/zigbee/devicelog.php',


      dataType :"JSON",
      success : function(data)
      {
        dataNumlenght = data.length;
       for(indexI = 0; indexI < dataNumlenght; indexI++)
      {
        for(indexJ = indexI+1; indexJ < dataNumlenght; )
        {
            if(data[indexJ].deviceEndpoint.eui64 == data[indexI].deviceEndpoint.eui64)
            {
                for(indexk = indexJ; indexk < dataNumlenght; indexk++)
                {
                  data[indexk] = data[indexk+1];

                }
                dataNumlenght--;
                          }
            else
            {
              indexJ++;
            }
        }

    }

       if(data.length === 0){
        document.getElementById("tablerow").style.display = "block";
       }
       insertZigbeeDevicesDataInTable(JSON.stringify(data));
    },

      error: function(error) {
        document.getElementById("tablerow").style.display = "block";
         console.log("error");
      }

    })
}

  function insertZigbeeDevicesDataInTable(scanZigbeeDevicesDataList){
   data = JSON.parse(scanZigbeeDevicesDataList);
   // document.getElementById("loader").style.display = "none";
    document.getElementById("pairbutton").disabled = false;
    document.getElementById("deletebutton").disabled = false;
    document.getElementById("helpbutton").disabled = false;

    if($('table').find('td').length == 0) {

       for (var i = 0; i < data.length; i++) {
          if(data[i].deviceType != null){
          if(data[i].deviceType == zigbeeDeviceTypeByID.ONOFFLight){
            data[i].deviceType  ="ON-OFF Light";
          }
          else if(data[i].deviceType == zigbeeDeviceTypeByID.DimmableLight){
            data[i].deviceType  ="Dimmable Light";
          }
          else if(data[i].deviceType == zigbeeDeviceTypeByID.ColorDimmableLight){
            data[i].deviceType  ="Color Dimmable Light";
          }
          else if(data[i].deviceType == zigbeeDeviceTypeByID.ONOFFLightSwitch){
            data[i].deviceType  ="ON-OFF Light Switch";
          }
        else{
          data[i].deviceType = "Other devices"
        }
      }
        tr = $('<tr/>');

       chk="<th>"+"<input type='checkbox' id = checkBoxID"+i+" onclick = selectPairingRowByCheckBox("+i+")>"+"</th>";
       tr.append(chk);
       tr.append("<td id =deviceName_" +i+" contenteditable='true'>" + "ZIGBEE_"+i+ "</td>")
       tr.append("<td>" + data[i].deviceEndpoint.eui64 + "</td>");
       tr.append("<td  id =devicetype_" +i+">" + data[i].deviceType + "</td>");
       tr.append("<td>" + data[i].nodeId + "</td>");

       $('table').append(tr);
        }

      }
   document.getElementById("scanbutton").disabled = true;
  // stopScaningZigbeeDevices();

}
function selectPairingRowByCheckBox(index) {

          if($("#devicetype_"+ index).text() === "ON-OFF Light" || $("#devicetype_"+ index).text() ==="Dimmable Light")
          {
            $("#deviceName_"+ index).prop("contenteditable", false);
           var rows = [];


           if($("#checkBoxID"+ index).is(":checked")){

           $('input:checked').each(function () {

             var row = [];

          $(this).closest('tr').find('td:not(:first-child)').each(function () {
           row.push($(this).text());

          });
          rows.push(row);
        });

        }

        else if($("#checkBoxID"+ index).is(":not(:checked)")){
            $("#deviceName_"+ index).prop("contenteditable", true);
        }


     localStorage.setItem("storageName",JSON.stringify(rows))
    }
    else{

      modal.style.display = "block";
      $("#checkBoxID"+ index).prop("checked", false);
    }
}
function deleteRowFromScaningTable(){
  $('input:checked').each(function () {
    $(this).closest('tr').remove();
  });
}

function stopScaningZigbeeDevices(){

  $.ajax({
    type: 'POST',
    dataType: "script",
    url: 'https://localhost/zigbee/stopScanningZigbeeDevices.sh',

    success: function(data,textStatus, xhr) {
          console.log(xhr.status);
          console.log("Success");
      },
    error: function(xhr, textStatus) {
           alert(xhr.status,xhr.url);

          console.log(xhr.status);
          console.log("error");
      }
     });
}


   span.onclick = function() {
   modal.style.display = "none";
}

 span_2.onclick = function() {
    modal_2.style.display = "none";
 }

function helpInstruction(){
  modal_2.style.display = "block";
}
window.onclick = function(event) {
  if (event.target == modal_2) {
      modal_2.style.display = "none";
  }
}
//When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
