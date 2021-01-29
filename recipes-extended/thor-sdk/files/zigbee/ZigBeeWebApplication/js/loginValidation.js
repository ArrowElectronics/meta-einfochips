$(document).keypress(function (e) {
    if (e.which == 13 || event.keyCode == 13) {
        openScaningDeviceWindow();
         }
    });
function openScaningDeviceWindow() {
    if( document.getElementById("username").value == "admin"
           && document.getElementById("password").value == "einfochips")
    {
         location.href='scanZigbeeDevices.html';
    }
    else
    {
            alert( "Login Validation Failed" );
    }

    }