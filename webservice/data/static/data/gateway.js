function loadMeasurements(type){
    targetId = "#measurements-type-" + type;
    //$(targetId).empty();

    url = base_url + "?type=" + type + "&start=2016-05-01&end=2016-05-03";
    console.log(url);

    $.getJSON(url, function(data) {
        items = [];
        items.push("<th>Date</th>");
        $.each(data.measurements.sensors, function(index, value){
            items.push("<th>Sensor " + value + "</th>" );
        });

        $(targetId + " table thead").append(items);

        $.each(data.measurements.values, function(index, value){
            row = [];
            row.push("<td>" + value.date + "</td>");

            $.each(value.data, function(index, value){
                row.push("<td>" + value + "</td>");
            });

            $(targetId + " table tbody").append(
                "<tr>" + row + "</tr>");
        });
    });

    /*sensors.forEach(function(s) {
        url = base_url + s + "/measurements.json?type=" + type + "&start=2016-03-04"

        $.getJSON(url, function(data) {
            sensor_id = 1;
            var items = [];
            $.each( data.measurements, function(index, value) {
                //console.log(value[1])
                items.push( "<li>" + value[1] + "</li>" );
            });

            $(targetId).append(
                        $("<div/>", { class : "col-md-5"}).append(
                                                                $("<h3/>", {
                                                                    text : "Sensor " + s
                                                                    }))
                                                          .append(
                                                                $("<ul/>").append(
                                                                        items.join("")
                                                                )
                                                          )
            );
        });
    });*/
}

$('#measurementDataTabs a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
    console.log(e.target.dataset.measurementType); // newly activated tab
    loadMeasurements(e.target.dataset.measurementType);
})

loadMeasurements(1); // Load first tab. Quick Hack.