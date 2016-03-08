var url = '/rest/companies/2/installations/4/gateways/8/sensors/16/measurements.json';
d3.json(url, function(error, incoming_data) {
    //if (error) return console.warn(error);
    if (error) throw error;

    var data = incoming_data.measurements;
    console.log(data);

    var formatDate = d3.time.format("%Y-%m-%dT%H:%M:%S");

    for (var i = 0; i < data.length; i++) {
        data[i].timestamp = formatDate.parse(data[i].timestamp);
    }

    var margin = {
            top: 20,
            right: 20,
            bottom: 30,
            left: 50
        },
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.time.scale()
        .range([0, width])
        .nice();

    var y = d3.scale.linear()
        .range([height, 0])
        .nice();

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var line = d3.svg.line()
        .x(function(d) {
            return x(d.timestamp);
        })
        .y(function(d) {
            return y(d.value);
        });

    var svg = d3.select("#visualisation").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

    x.domain(d3.extent(data, function(d) {
        return d.timestamp;
    }));
    y.domain(d3.extent(data, function(d) {
        return d.value;
    }));

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Value");

    svg.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);
});