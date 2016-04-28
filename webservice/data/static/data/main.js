$(document).ready(function(){
    $(".nav-pills a").click(function(){
        $(this).tab('show');
    });

    $('.nav-pills a').on('shown.bs.tab', function(event){
        var pillName = $(event.target).text(); // Sensor x
        var id = pillName.slice(-1); // x
    });

    $('.graphDataTabs a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
        console.log(e.target.dataset.measurementType); // newly activated tab
        //loadGraph(e.target.dataset.measurementType, e.target.dataset.measurementTypeName, e.target.dataset.sensor);
        loadGraph(e.target.dataset.sensor, e.target.dataset.measurementType);
    });

    $('.measurements table').stickyTableHeaders();
});


function initialize() {
    // The location of the 'gateway' corresponds to the
    // location of the first sensor.
    var mapProp = {
        center:new google.maps.LatLng(
            gateway_position.lat,
            gateway_position.long
        ),
        zoom:18,
        mapTypeId:google.maps.MapTypeId.ROADMAP
        };
        var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);

        var marker = new google.maps.Marker({
        position: gateway_position,
        map: map,
        title: 'Gateway Location'
    });
}

google.maps.event.addDomListener(window, 'load', initialize);