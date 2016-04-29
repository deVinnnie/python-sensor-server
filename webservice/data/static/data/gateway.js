function loadMeasurements(type){
    targetId = "#measurements-type-" + type;
    url = table_base_url + "?type=" + type + "&start=" + start.format("YYYY-MM-DD") + "&end=" + end.format("YYYY-MM-DD");

    $.getJSON(url, function(data) {
        /* var values = data.measurements.values;
        console.log(values);
        selection = d3.select(targetId + "tbody").selectAll("tr").data(values);
        selection.enter().append("tr").text(
            function(d){ return d; }
        );

        // create a row for each object in the data
        var rows = tbody.selectAll("tr")
            .data(values)
            .enter()
            .append("tr");

        // create a cell in each row for each column
        var cells = rows.selectAll("td")
            .data(function(row) {
                return values.map(function(column) {
                    return {column: column, value: row[column]};
                });
            })
            .enter()
            .append("td")
                .html(function(d) { return d.value; });
        */

        var header = $("<tr></tr>");
        var items = [];

        header.append(
            $("<th></th>").text("Date")
        );

        $.each(data.measurements.sensors, function(index, value){
            header.append(
                $("<th></th>").text("Sensor " + value )
            );

            items.push("<th>Sensor " + value + "</th>");
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

$("#measurementDataTabs a:first").tab('show');