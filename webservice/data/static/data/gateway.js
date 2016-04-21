function loadMeasurements(type){
    targetId = "#measurements-type-" + type;

    url = base_url + "?type=" + type + "&start=" + start.format("YYYY-MM-DD") + "&end=" + end.format("YYYY-MM-DD");
    console.log(url);

    $.getJSON(url, function(data) {
        items = [];
        items.push("<th>Date</th>");
        $.each(data.measurements.sensors, function(index, value){
            items.push("<th>Sensor " + value + "</th>");
        });

        $(targetId + " table thead").empty();
        $(targetId + " table thead").append(items);

        $(targetId + " table tbody").empty();
        $.each(data.measurements.values, function(index, value){
            row = [];
            row.push("<td>" + value.date + "</td>");

            $.each(value.data, function(index, value){
                if(value != null){
                    row.push("<td>" + value + "</td>");
                }
                else{
                    row.push("<td></td>");
                }
            });

            $(targetId + " table tbody").append(
                "<tr>" + row + "</tr>"
            );
        });
    });
}

function loadPrevMeasurements(type){
    start = start.subtract(20, 'days');
    end = end.subtract(20, 'days');
    loadMeasurements(type);
}

function loadNextMeasurements(type){
    start = start.add(20, 'days');
    end = end.add(20, 'days');
    loadMeasurements(type);
}

$('#measurementDataTabs a[data-toggle="tab"]').on('shown.bs.tab', function(e){
    console.log(e.target.dataset.measurementType); // newly activated tab
    loadMeasurements(e.target.dataset.measurementType);
});

loadMeasurements(1); // Load first tab. Quick Hack.
$("#measurementDataTabs a:first").tab('show');