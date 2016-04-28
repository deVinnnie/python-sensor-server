SimpleGraph = function(elemid, data, options) {
    var self = this;
    this.chart = document.getElementById(elemid);
    this.cx = this.chart.clientWidth; // To be responsive
    this.cy = this.chart.clientHeight;
    //this.cx = 960;
    //this.cy = 500;
    this.options = options || {};
    this.options.xmax = options.xmax || 30;
    this.options.xmin = options.xmin || 0;
    this.options.ymax = options.ymax || 10;
    this.options.ymin = options.ymin || 0;

    d3.select(this.chart).selectAll("*").remove();

    this.padding = {
        "top": this.options.title ? 40 : 20,
        "right": 50,
        "bottom": this.options.xlabel ? 80 : 10,
        "left": this.options.ylabel ? 70 : 45
    };

    var margin = {
        top: 20,
        right: 50,
        bottom: 30,
        left: 50
    };

    this.size = {
        "width": this.cx - this.padding.left - this.padding.right,
        "height": this.cy - this.padding.top - this.padding.bottom
    };

    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    this.x = x = d3.time.scale()
                .range([0, this.size.width])
                .nice();
    this.y = y = d3.scale.linear()
                .range([this.size.height, 0])
                .nice();
    this.line = d3.svg.line()
                .x(function(d) {
                    return x(d.timestamp);
                })
                .y(function(d) {
                    return y(d.value);
                });

    this.x.domain([data[0].timestamp, data[data.length - 1].timestamp]);
    this.y.domain(d3.extent(data, function(d) {
        return d.value;
    }));

    this.vis = d3.select(this.chart)
        .classed("svg-container", true) //container class to make it responsive
        .append("svg")
//            .attr("width", this.cx)
//            .attr("height", this.cy)
        //responsive SVG needs these 2 attributes and no width and height attr
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0 " + this.cx + " " + this.cy)
        //class to make it responsive
        .classed("svg-content-responsive", true)
        .append("g")
        .attr("transform", "translate(" + this.padding.left + "," + this.padding.top + ")");


    this.plot = this.vis.append("rect")
        .attr("class", "overlay")
        .attr("width", this.size.width)
        .attr("height", this.size.height)
        .on("mousedown.drag", self.plot_drag())
        .on("mouseover", function() {
            self.focus.style("display", null);
        })
        .on("mouseout", function() {
            self.focus.style("display", "none");
        })
        .on("mousemove", mousemove);
    this.plot.call(d3.behavior.zoom().x(this.x).y(this.y).on("zoom", this.redraw()));

    this.focus = this.vis.append("g")
        .attr("class", "focus")
        .style("display", "none");

    this.focus.append("circle")
        .attr("r", 4.5);

    this.focus.append("text")
        .attr("x", 9)
        .attr("dy", ".35em");

    this.vis.append("svg")
        .attr("top", 0)
        .attr("left", 0)
        .attr("width", this.size.width)
        .attr("height", this.size.height)
        .attr("viewBox", "0 0 " + this.size.width + " " + this.size.height)
        .attr("class", "line")
        .append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", this.line);

    // add Chart Title
    if (this.options.title) {
        this.vis.append("text")
            .attr("class", "axis")
            .text(this.options.title)
            .attr("x", this.size.width / 2)
            .attr("dy", "-0.8em")
            .style("text-anchor", "middle");
    }

    // Add the x-axis label
    if (this.options.xlabel) {
        this.vis.append("text")
            .attr("class", "axis")
            .text(this.options.xlabel)
            .attr("x", this.size.width / 2)
            .attr("y", this.size.height)
            .attr("dy", "2.4em")
            .style("text-anchor", "middle");
    }

    // add y-axis label
    if (this.options.ylabel) {
        this.vis.append("g").append("text")
            .attr("class", "axis")
            .text(this.options.ylabel)
            .style("text-anchor", "middle")
            .attr("transform", "translate(" + -40 + " " + this.size.height / 2 + ") rotate(-90)");
    }

    d3.select(this.chart)
        .on("mousemove.drag", self.mousemove())
        .on("mouseup.drag", self.mouseup());

    this.redraw()();

    function mousemove() {
        var x0 = x.invert(d3.mouse(this)[0]),
            i = bisectDate(data, x0, 1),
            // http://stackoverflow.com/questions/26882631/d3-what-is-a-bisector
            d0 = data[i - 1],
            d1 = data[i],
            d = x0 - d0.date > d1.date - x0 ? d1 : d0;
        self.focus.attr("transform", "translate(" + x(d.timestamp) + "," + y(d.value) + ")");
        self.focus.select("text").text(formatUnit(d.value));
    }
};

/**
* SimpleGraph methods
*/

SimpleGraph.prototype.plot_drag = function() {
    var self = this;
    return function() {
        d3.select('body').style("cursor", "move");
    };

    //TODO load data.
};

SimpleGraph.prototype.mousemove = function() {
    var self = this;
    return function() {
        var p = d3.mouse(self.vis[0][0]);

        if (self.dragged) {
            self.dragged.y = self.y.invert(Math.max(0, Math.min(self.size.height, p[1])));
            self.update();
        };
    }
};

SimpleGraph.prototype.mouseup = function() {
    var self = this;
    return function() {
        document.onselectstart = function() {
            return true;
        };

        d3.select('body').style("cursor", "auto");

        if (!isNaN(self.downx)) {
            self.redraw()();
            self.downx = Math.NaN;
            d3.event.preventDefault();
            d3.event.stopPropagation();
        };
        if (!isNaN(self.downy)) {
            self.redraw()();
            self.downy = Math.NaN;
            d3.event.preventDefault();
            d3.event.stopPropagation();
        }
        if (self.dragged) {
            self.dragged = null
        }
    }
};

SimpleGraph.prototype.redraw = function() {
    var self = this;
    return function() {
        var tx = function(d) {
                return "translate(" + self.x(d) + ",0)";
            },
            ty = function(d) {
                return "translate(0," + self.y(d) + ")";
            },
            stroke = function(d) {
                return d ? "#ccc" : "#666";
            },
            fx = self.x.tickFormat(10),
            fy = self.y.tickFormat(10);

        // Regenerate x-ticks…
        var gx = self.vis.selectAll("g.x")
            .data(self.x.ticks(10), String)
            .attr("transform", tx);

        gx.select("text")
            .text(fx);

        var gxe = gx.enter().insert("g", "a")
            .attr("class", "x")
            .attr("transform", tx);

        gxe.append("line")
            .attr("stroke", stroke)
            .attr("y1", 0)
            .attr("y2", self.size.height);

        gxe.append("text")
            .attr("class", "axis")
            .attr("y", self.size.height)
            .attr("dy", "1em")
            .attr("text-anchor", "middle")
            .text(fx);

        gx.exit().remove();

        // Regenerate y-ticks…
        var gy = self.vis.selectAll("g.y")
            .data(self.y.ticks(10), String)
            .attr("transform", ty);

        gy.select("text")
            .text(fy);

        var gye = gy.enter().insert("g", "a")
            .attr("class", "y")
            .attr("transform", ty)
            .attr("background-fill", "#FFEEB6");

        gye.append("line")
            .attr("stroke", stroke)
            .attr("x1", 0)
            .attr("x2", self.size.width);

        gye.append("text")
            .attr("class", "axis")
            .attr("x", -3)
            .attr("dy", ".35em")
            .attr("text-anchor", "end")
            .text(fy)

        gy.exit().remove();
        self.plot.call(d3.behavior.zoom().x(self.x).y(self.y).on("zoom", self.redraw()));
        self.update();
    }
};

SimpleGraph.prototype.update = function() {
    var self = this;
    //var lines = this.vis.select("path").attr("d", this.line(this.points));
    var lines = this.vis.select("path").attr("d", this.line);
};
