/**
 * Load the measurement data for the given measurementType.
 * The range is based on the global variables start and end.
 * These variables should be defined as a moment instance (see momentjs library).
 *
 * The data is directly added to the corresponding table for the type.
 */
function loadMeasurements(type){
    targetId = "#measurements-type-" + type;
    url = table_base_url + "?type=" + type + "&start=" + start.format("YYYY-MM-DD") + "&end=" + end.format("YYYY-MM-DD");

    $.getJSON(url, function(data) {
        var header = $("<tr></tr>");
        header.append(
            $("<th></th>").text("Date")
        );

        $.each(data.measurements.sensors, function(index, tag){
            header.append(
                $("<th></th>").text(tag)
            );
        });

        $(targetId + " table thead").empty();
        $(targetId + " table thead").append(header);

        console.log(data.measurements.values);

        data.measurements.values.sort(
            function(a, b){
                l = moment(a.date, 'YYYY-MM-DD');
                r = moment(b.date, 'YYYY-MM-DD');
                return l.isBefore(r);
            }
        );

        console.log(data.measurements.values);

        $.each(data.measurements.values, function(index, value){
            row = [];
            row.push("<td>" + value.date + "</td>");

            $.each(value.data, function(index, value){
                if(value != null){
                    row.push("<td>" + value + "</td>");
                }
                else{
                    row.push("<td>-</td>");
                }
            });

            $(targetId + " table tbody").append(
                "<tr>" + row + "</tr>"
            );
        });
    });
}

/**
 * Load the measurement data for the previous 20 days.
 * The new data is added to the bottom of the table.
 * This is a convenience method to avoid using loadMeasurements() directly.
 */
function loadNextMeasurements(type){
    start = start.subtract(20, 'days');
    end = end.subtract(20, 'days');
    loadMeasurements(type, true);
}

$('#measurementDataTabs a[data-toggle="tab"]').on('shown.bs.tab', function(e){
    targetId = "#measurements-type-" + e.target.dataset.measurementType;
    $(targetId + " table tbody").empty();

    start = moment().subtract(20, 'days');
    end = moment();

    console.log(e.target.dataset.measurementType); // newly activated tab
    loadMeasurements(e.target.dataset.measurementType, true);
});

// Show first tab, the event listener is called so the data is loaded automatically.
// No need to call the load method here explicitly.
$("#measurementDataTabs a:first").tab('show');