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