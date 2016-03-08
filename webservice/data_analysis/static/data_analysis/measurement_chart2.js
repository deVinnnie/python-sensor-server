registerKeyboardHandler = function(callback) {
    var callback = callback;
    d3.select(window).on("keydown", callback);
};

var url = '/rest/companies/2/installations/4/gateways/8/sensors/16/measurements.json';
d3.json(url, function(error, incoming_data) {
    //if (error) return console.warn(error);
    if (error) throw error;

    var data = incoming_data.measurements;

    var formatDate = d3.time.format("%Y-%m-%dT%H:%M:%S");

    for (var i = 0; i < data.length; i++) {
        data[i].timestamp = formatDate.parse(data[i].timestamp);
    }

    data.sort(function(a, b) {
        return a.timestamp - b.timestamp;
    });

    drawGraph(data);

});

function drawGraph(data) {
    console.log(data);

    SimpleGraph = function(elemid, options) {
        var self = this;
        this.chart = document.getElementById(elemid);
        this.cx = this.chart.clientWidth;
        this.cy = this.chart.clientHeight;
        this.options = options || {};
        this.options.xmax = options.xmax || 30;
        this.options.xmin = options.xmin || 0;
        this.options.ymax = options.ymax || 10;
        this.options.ymin = options.ymin || 0;

        this.padding = {
            "top": this.options.title ? 40 : 20,
            "right": 30,
            "bottom": this.options.xlabel ? 80 : 10,
            "left": this.options.ylabel ? 70 : 45
        };

        this.size = {
            "width": this.cx - this.padding.left - this.padding.right,
            "height": this.cy - this.padding.top - this.padding.bottom
        };

        // x-scale
        this.x = d3.time.scale()
            /*.domain(d3.extent(data, function(d) {
                return d.timestamp;
            }))*/
            .domain([data[0].timestamp, data[data.length - 1].timestamp])
            .range([0, this.size.width])
            .nice();

        // drag x-axis logic
        this.downx = Math.NaN;

        // y-scale (inverted domain)
        this.y = d3.scale.linear()
            .domain(d3.extent(data, function(d) {
                return d.value;
            }))
            .range([this.size.height, 0])
            .nice();

        // drag y-axis logic
        this.downy = Math.NaN;

        this.dragged = this.selected = null;

        this.line = d3.svg.line()
            .x(function(d) {
                return self.x(d.timestamp);
            })
            .y(function(d) {
                return self.y(d.value);
            });

        /*var xrange = (this.options.xmax - this.options.xmin),
            yrange2 = (this.options.ymax - this.options.ymin) / 2,
            yrange4 = yrange2 / 2,
            datacount = this.size.width / 30;

        this.points = d3.range(datacount).map(function(i) {
            return {
                x: i * xrange / datacount,
                y: this.options.ymin + yrange4 + Math.random() * yrange2
            };
        }, self);*/

        this.vis = d3.select(this.chart).append("svg")
            .attr("width", this.cx)
            .attr("height", this.cy)
            .append("g")
            .attr("transform", "translate(" + this.padding.left + "," + this.padding.top + ")");

        this.focus = this.vis.append("g")
            .attr("class", "focus")
            .style("display", "none");

        this.focus.append("circle")
            .attr("r", 4.5);

        this.focus.append("text")
            .attr("x", 9)
            .attr("dy", ".35em");

        this.plot = this.vis.append("rect")
            .attr("width", this.size.width)
            .attr("height", this.size.height)
            .style("fill", "#EEEEEE")
            .attr("pointer-events", "all")
            .on("mousedown.drag", self.plot_drag())
            .on("touchstart.drag", self.plot_drag())
            .on("mouseover", function() { self.focus.style("display", null); })
            .on("mouseout", function() { self.focus.style("display", "none"); })
            .on("mousemove", self.mymousemove());
        this.plot.call(d3.behavior.zoom().x(this.x).y(this.y).on("zoom", this.redraw()));

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

        this.bisectDate = d3.bisector(function(d) { return d.timestamp; }).left;

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
            .on("touchmove.drag", self.mousemove())
            .on("mouseup.drag", self.mouseup())
            .on("touchend.drag", self.mouseup());

        this.redraw()();
    };

    //
    // SimpleGraph methods
    //

    SimpleGraph.prototype.plot_drag = function() {
        var self = this;
        return function() {
            registerKeyboardHandler(self.keydown());
            d3.select('body').style("cursor", "move");
        }
    };

    SimpleGraph.prototype.update = function() {
        var self = this;
        //var lines = this.vis.select("path").attr("d", this.line(this.points));
        var lines = this.vis.select("path").attr("d", this.line);
    };

    SimpleGraph.prototype.datapoint_drag = function() {
        var self = this;
        return function(d) {
            registerKeyboardHandler(self.keydown());
            document.onselectstart = function() {
                return false;
            };
            self.selected = self.dragged = d;
            self.update();

        }
    };

    SimpleGraph.prototype.mousemove = function() {
        var self = this;
        return function() {
            var p = d3.mouse(self.vis[0][0]),
                t = d3.event.changedTouches;

            if (self.dragged) {
                self.dragged.y = self.y.invert(Math.max(0, Math.min(self.size.height, p[1])));
                self.update();
            };
        }
    };

    SimpleGraph.prototype.mymousemove = function() {
        var self = this;
        return function() {
            var p = d3.mouse(self.vis[0][0]);
            var x0 = self.x.invert(p[0]),
                i = self.bisectDate(data, x0, 1),
                d0 = data[i - 1],
                d1 = data[i],
                d = x0 - d0.timestamp > d1.timestamp - x0 ? d1 : d0;
        self.focus.attr("transform", "translate(" + self.x(d.timestamp) + "," + self.y(d.value) + ")");
        self.focus.select("text").text(d.value);
        }
    }

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

    SimpleGraph.prototype.keydown = function() {
        var self = this;
        return function() {
            if (!self.selected) return;
            switch (d3.event.keyCode) {
                case 8: // backspace
                case 46:
                    { // delete
                        var i = self.points.indexOf(self.selected);
                        self.points.splice(i, 1);
                        self.selected = self.points.length ? self.points[i > 0 ? i - 1 : 0] : null;
                        self.update();
                        break;
                    }
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
                .text(fx)
                //.style("cursor", "ew-resize")
                .on("mouseover", function(d) {
                    d3.select(this).style("font-weight", "bold");
                })
                .on("mouseout", function(d) {
                    d3.select(this).style("font-weight", "normal");
                })
                .on("mousedown.drag", self.xaxis_drag())
                .on("touchstart.drag", self.xaxis_drag());

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
                //.style("cursor", "ns-resize")
                .on("mouseover", function(d) {
                    d3.select(this).style("font-weight", "bold");
                })
                .on("mouseout", function(d) {
                    d3.select(this).style("font-weight", "normal");
                })
                .on("mousedown.drag", self.yaxis_drag())
                .on("touchstart.drag", self.yaxis_drag());

            gy.exit().remove();
            self.plot.call(d3.behavior.zoom().x(self.x).y(self.y).on("zoom", self.redraw()));
            self.update();
        }
    };

    SimpleGraph.prototype.xaxis_drag = function() {
        var self = this;
        return function(d) {
            document.onselectstart = function() {
                return false;
            };
            var p = d3.mouse(self.vis[0][0]);
            self.downx = self.x.invert(p[0]);
        }
    };

    SimpleGraph.prototype.yaxis_drag = function(d) {
        var self = this;
        return function(d) {
            document.onselectstart = function() {
                return false;
            };
            var p = d3.mouse(self.vis[0][0]);
            self.downy = self.y.invert(p[1]);
        }
    };

    var len = data.length;
    graph = new SimpleGraph("chart1", {
        "xmax": data[len-1].timestamp, "xmin": data[0].timestamp,
        "ymax": data[len-1].value, "ymin": data[0].value,
        "title": "Capacity measurements",
        "xlabel": "Time",
        "ylabel": "Value"
    });
}