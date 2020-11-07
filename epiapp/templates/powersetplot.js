//<%text>
// Makes the power set plots


class Powersetplot {
    static epiColors = { //allow changing before construction.
                        '+ Sign epistasis': 'springgreen',
                        '- Sign epistasis': 'salmon',
                        //'= Sign epistasis': 'lightgray',
                        '+ Reciprocal sign epistasis': 'teal',
                        '- Reciprocal sign epistasis': 'pink',
                        //'=  Reciprocal sign epistasis': 'lightgray',
                        '+ Magnitude epistasis': 'forestgreen',
                        '- Magnitude epistasis': 'firebrick',
                        'Additive': 'violet'
                        //'=  Magnitude epistasis': 'lightgray'
                    };

    constructor(mode, data) {
        // alldata = {theoretical: [], empirical: []}
        this.mode = mode;
        this.mutationNumber = data.mutationNumber;
        // data is an array of arrays like: ['-', '-', '-', '37.787106', '1.1198141476138903']
        this.empiricalData = data.empiricalData;
        this.theoreticalData = data.theoreticalData;
        // for data = theo theo data + tier 0 and 1 emp
        this.data = this.mode === 'emp' ? this.empiricalData : this.theoreticalData.concat(this.empiricalData.filter(row => row.tier < 2));

        this.places = this.mode === 'emp' ? this.getBinomial() : this.getFatBinomial(); // e.g 1 on top tier , 2, 3, 1 bottom...
        this.layout = this.makeLayout(); // layout.scale is dependent on this.data.
        this.epiColors = Powersetplot.epiColors;
        // start canvas
        this.tooltip = d3.select("body")
                         .append("div")
                         .attr("class", "tooltip")
                         .style("opacity", 0)
                         .style("min-width", "100px"); //detach not needed.
        this.svg = d3.select("body")
                     .append("svg:svg").attr("width", "100%")
                     .attr("height", (this.mutationNumber + 1) * this.layout.y_step + 50)
                     .attr("id", this.mode + "-svg")
                     .remove(); //detach
        this.arrowGroup = this.svg.insert("g", ":first-child").attr("id", this.mode+"arrows");
        this.makeDiamond();
        this.makeLegend();
        this.makeArrows();

    }

    appendTo(divElement) { // "#" + mode + "-graph-plot"
        d3.select(divElement).append(() => this.svg.node());
        this.correctSVG(divElement);
        return this;
    }

    static parseData(data) {
        //data is a table... which is not great.
        //['-', '-', '-', '37.787106', '1.1198141476138903']
        // ['+', '+', '+', [2, 7], 68.412413, 4.42236566744663, 86.41156399999998, 6.8995876213317775, -17.999150999999983,'- Magnitude epistasis']
        const mutationNumber = data.empirical.data[0].length - 2;
        const empiricalData = data.empirical.data.map(row => ({
                                                            id: row.slice(0,-2).join(""),
                                                            tier: row.slice(0,-2).filter(sign => sign === '+').length,
                                                            sign: row.slice(0,-2),
                                                            avg: parseFloat(row.slice(-2, -1)),
                                                            sd: parseFloat(row.slice(-1)[0])
                                                            })
                                                    );
        const theoreticalData = data.theoretical.data.map(row => ({
                                                            id: row.slice(0,-7).join(""),
                                                            tier: row.slice(0,-7).filter(sign => sign === '+').length,
                                                            sign: row.slice(0,-7),
                                                            rawOrigins: row.slice(-7, -6)[0],
                                                            emp_avg: parseFloat(row.slice(-6, -5)),
                                                            emp_sd: parseFloat(row.slice(-5, -4)),
                                                            avg: parseFloat(row.slice(-4, -3)),
                                                            sd: parseFloat(row.slice(-3, -2)),
                                                            diff_avg: parseFloat(row.slice(-2, -1)),
                                                            epistasis: row.slice(-1)[0]
                                                            })
                                                    );
        //origin is as Paul wrote it, 1 = wt, 2 =  first mut etc.
        theoreticalData.forEach(row => {
                                    row.origins = row.rawOrigins.map(weirdIdx => empiricalData[weirdIdx - 1].id)
                                });
        return {
            mutationNumber: mutationNumber,
            empiricalData: empiricalData,
            theoreticalData: theoreticalData,
        };


    }

    getBinomial() {
        //arrange the super set into a diamond
        //quicker than a combinatorial..
        return [[1],
                [1, 1],
                [1, 2, 1],
                [1, 3, 3, 1],
                [1, 4, 6, 4, 1],
                [1, 5, 10, 10, 5, 1],
                [1, 6, 15, 20, 15, 6, 1],
                [1, 7, 21, 35, 35, 21, 7, 1],
                [1, 8, 28, 56, 70, 56, 28, 8, 1]
            ][this.mutationNumber];
    }

    getFatBinomial() {
        // this is not a superset, its a bigger thing
        let places = Array(this.mutationNumber + 1).fill(0);
        this.data.forEach(row => places[row.tier]++);
        return places
    }

    makeLayout () {
        // where does everything go
        // layout
        let x_step = 50;
        return {
            mutationNumber: this.mutationNumber,
            x_step: x_step,
            y_step: 50,
            x_mid: Math.max(...this.places) / 2 * x_step,
            // the following two are changed as datapoints are added..
            x_offset: Array(this.mutationNumber + 1).fill(0).map((v, index) => -(this.places[index] - 1) / 2 * x_step),
            x_index: Array(this.mutationNumber + 1).fill(0),
            y_offset: 50,
            mode: this.mode,
            scale: (x_step / 4) / Math.max(...this.data.map(row => row.avg))
        };

    };

    getDatapoint(sign) {
        // sign = '+-+-'
        // if th breaks here, itt means the datapoint does not exists.=
        return this.datapoints.filter(datapoint => datapoint.id === sign)[0];
    }

    makeArrows() {
        if (this.mode === "theo") {
            this.datapoints.filter(datapoint => datapoint.origins !== undefined)
                           .forEach(datapoint => {
                                                    datapoint.origins
                                                            .map(sign => this.getDatapoint(sign))
                                                            .forEach(od => this.addArrow(datapoint, od))
                        });
        }
    }

    addArrow(beginDp, endDp) {
        this.arrowGroup.append("line")
                        .attr("x1", beginDp.x)
                        .attr("y1", beginDp.y)
                        .attr("x2", endDp.x)
                        .attr("y2", endDp.y)
                        .attr("stroke", "lightgray")
                        .attr("stroke-width", 1)
                        .data([{x1: beginDp.x, y1: beginDp.y,
                                x2: endDp.x, y2: endDp.y,
                                terminus1: beginDp.node,
                                terminus2: endDp.node
                        }]);
                //.attr("node","node-"+ni.toString());
                //.style("border", "gray");
    }

    makeDiamond() {
        this.datapoints = this.data.map((item, i) => this.calcDatapoint(item, i));
        this.datapoints.forEach(datapoint => this.addDatapoint(datapoint));
    }

    calcDatapoint(item, i) {
        // called by makeDiamond()
        // ++---- is tier 2, as in "a combo of two plusses".
        let datapoint = {
            x: this.layout.x_mid + this.layout.x_offset[item.tier] + this.layout.x_index[item.tier] * this.layout.x_step,
            y: this.layout.y_offset + (this.layout.mutationNumber - item.tier) * this.layout.y_step,
            v: this.layout.scale * parseFloat(item.avg),
            v_sd: this.layout.scale * (item.avg + item.sd),
            v_e: item.emp_avg ? this.layout.scale * parseFloat(item.emp_avg) : undefined,
            // theo is coloured and with sdev
            //tier 0 (wt) and tier 1 (singletons) are real... so no colours.
            color: this.epiColors[item.epistasis] || "gray",
            color_sd: "lightGray",
            id: item.id, //may differ in future
            text: item.id,
            //add the 2,3,4 annotation if theo
            info: (item.origins ? item.origins + '; Value: ' : 'Value: ') + this.roundToSD(item.avg, item.sd),
            node: i + this.mutationNumber + 2,
            origins: item.origins,
            isLegend: false
        };
        this.layout.x_index[item.tier]++;
        return datapoint;
    }

    addDatapoint(datapoint) {
        // datapoint is a dict with x y value color text and info
        // tooltip is the physical tooltip that gets filled with datapoint.info.
        // plot
        const group = this.svg.append("g");
        const plotThis = this;
        let data = [{x: 0, y: 0, node: datapoint.node, sign: datapoint.id}];
        group.data(data)
            .style("cursor", "grab");
        //Legend.
        if (datapoint.isLegend) {
            group.append("text")
                .attr("x", datapoint.x + 20)
                .attr("y", datapoint.y + 6)
                .attr("text-anchor", "left")
                .style("fill", "black")
                .text(datapoint.text); //.attr("dy", ".35em")
        } else {
            group.append("text")
                .attr("x", datapoint.x)
                .attr("y", datapoint.y + 20)
                .attr("text-anchor", "middle")
                .style("fill", "black")
                .text(datapoint.text); //.attr("dy", ".35em")
        }
        //Stdev circle
        group.append("circle")
            .attr("cx", datapoint.x)
            .attr("cy", datapoint.y)
            .attr("r", datapoint.v_sd > 0 ? datapoint.v_sd : 0.001)
            .style("fill", datapoint.color_sd);
        group.append("circle")
            .attr("cx", datapoint.x)
            .attr("cy", datapoint.y)
            .attr("r", datapoint.v > 0 ? datapoint.v : 0.001)
            .style("fill", datapoint.color);
        if (this.mode === 'theo') {
            group.append("circle")
                .attr("cx", datapoint.x)
                .attr("cy", datapoint.y)
                .attr("r", datapoint.v_e > 0 ? datapoint.v_e : 0.001)
                .style("stroke", "black")
                .style("stroke-width", "1")
                .style("fill", "none")
        }
        //store.
        datapoint.element = group;
        // drag
        group.on("mouseover", (d) => {
            this.tooltip.transition()
                .duration(200)
                .style("opacity", .9);
            this.tooltip.html(datapoint.info)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY - 28) + "px");
        })
            .on("mouseout", (d) =>  {
                this.tooltip.transition()
                    .duration(500)
                    .style("opacity", 0);
            });
        group.call(d3.drag()
            .on('drag', function (d) { //change of this!!
                d.x += d3.event.dx;
                d.y += d3.event.dy;
                const target = d3.select(this);
                target.attr('transform', 'translate(' + d.x + ',' + d.y + ')');
                const node = target.data()[0].node; // +--+
                plotThis.arrowGroup.selectAll('line').each(function(d2) {
                    const line = d3.select(this);
                    const data = line.data()[0];
                    if (data.terminus1 === node) {
                        line.attr('x1', data.x1+d.x);
                        line.attr('y1', data.y1+d.y);
                    }
                    if (data.terminus2 === node) {
                        line.attr('x2', data.x2+d.x);
                        line.attr('y2', data.y2+d.y);}
                })
                    //.each(function(d) {d3.select(this).attr("x1", 200)})
                // plotThis.arrowGroup.selectAll('line')
                //     .filter(function(d) { return d.data.uniqueID === myDatum.data.uniqueID; });
                // data[0].beginArrows.map(arrow => {arrow.x1 += d3.event.dx; arrow.y1 += d3.event.dy;});
                // data[0].endArrows.map(arrow => {arrow.x2 += d3.event.dx; arrow.y2 += d3.event.dy;});
                // plotThis.arrowGroup.selectAll("*").remove();
                // plotThis.makeArrows();
            })
            .on("start", function () {
                d3.select(this).style("cursor", "grabbing")
            })
            .on("end", function () {
                d3.select(this).style("cursor", "pointer")
            })
        );
    }

    makeLegend() {
        if (this.mode === 'theo') {
            this.makeTheoLegend();
            }
        else {
            this.makeEmpLegend();
            }
        }

    makeTheoLegend() {
        //x_offset: -(places[mutationNumber]-1)/2*x_step)
        const widesttier = Math.round(this.mutationNumber / 2 + 0.5);
        let x = this.layout.x_mid +
                this.layout.x_offset[widesttier] +
                (this.layout.x_index[widesttier] + 1.5) * this.layout.x_step; //far right
        /// theoretical values
        this.addDatapoint({
                                    x: x,
                                    y: this.layout.y_offset + this.mutationNumber * this.layout.y_step, //bottom
                                    v: 4,
                                    v_sd: 0,
                                    v_e: 0,
                                    color: "gray",
                                    color_sd: "lightGray",
                                    text: 'Theoretical',
                                    info: 'Theoretical',
                                    isLegend: true
                                });
        /// theoretical SD
        this.addDatapoint({
                            x: x,
                            y: this.layout.y_offset + (this.layout.mutationNumber - 1) * this.layout.y_step, //bottom
                            v: 2,
                            v_sd: 4,
                            v_e: 0,
                            color: "white",
                            color_sd: "lightGray",
                            text: 'Theoretical SD',
                            info: 'theoretical SD',
                            isLegend: true
                        });
        /// emp
        this.addDatapoint({
                            x: x,
                            y: this.layout.y_offset + (this.layout.mutationNumber - 2) * this.layout.y_step, //bottom
                            v: 0,
                            v_sd: 0,
                            v_e: 4,
                            color: "none",
                            color_sd: "none",
                            text: 'Empirical',
                            info: 'Empirical',
                            isLegend: true
                        });

        //legend right
        // x has now shifted for new column
        x = this.layout.x_mid + this.layout.x_offset[widesttier] + (this.layout.x_index[widesttier] + 4) * this.layout.x_step;
        //uber far right
        Object.keys(this.epiColors).forEach((key, index) =>
                                                    this.addDatapoint({
                                                        x: x,
                                                        y: this.layout.y_offset + (this.layout.mutationNumber - index / 2) * this.layout.y_step, //bottom
                                                        v: 4,
                                                        v_sd: 0,
                                                        v_e: 0,
                                                        color: this.epiColors[key],
                                                        color_sd: "none",
                                                        text: key,
                                                        info: key,
                                                        isLegend: true
                                                    })
                                            );
    }

    makeEmpLegend() {
        //x_offset: -(places[mutationNumber]-1)/2*x_step)
        const widesttier = Math.round(this.mutationNumber / 2 + 0.5);
        let x = this.layout.x_mid +
                this.layout.x_offset[widesttier] +
                (this.layout.x_index[widesttier] + 1.5) * this.layout.x_step; //far right
        /// theoretical values
        this.addDatapoint({
                            x: x,
                            y: this.layout.y_offset + (this.mutationNumber - 0) * this.layout.y_step, //bottom
                            v: 4,
                            v_sd: 0,
                            v_e: 0,
                            color: "gray",
                            color_sd: "lightGray",
                            text: 'Empirical',
                            info: 'Empirical',
                            isLegend: true
                        });
        /// theoretical SD
        this.addDatapoint({
                            x: x,
                            y: this.layout.y_offset + (this.layout.mutationNumber - 1) * this.layout.y_step, //bottom
                            v: 2,
                            v_sd: 4,
                            v_e: 0,
                            color: "white",
                            color_sd: "lightGray",
                            text: 'Empirical SD',
                            info: 'Empirical SD',
                            isLegend: true
                        });
    }

    roundToSD(mean, sd) {
        // TODO this is buggy.
        if (!! sd) {
            let d = Math.pow(10, Math.log10(sd));
            if (d > 1) {
                let rd = Math.round(d);
                return '{0}±{1}'.format(Math.round(mean / rd) * rd, Math.round(sd / rd) * rd);
            } else {
                let rd = Math.round(1/d);
                return '{0}±{1}'.format(Math.round(mean * rd) / rd, Math.round(sd * rd) / rd);
            }
        } else {
            return '{0}±nan'.format(Math.round(mean * 10) / 10);
        }

        }

    correctSVG(divElement) {
        //viewBox="0 0 1000 1500"
        let size = [0,0, 0, 0];
        d3.selectAll(`${divElement} circle`).each(function(d) {
            const target = d3.select(this);
            size = [
                Math.min(size[0], target.attr('cx')),
                Math.min(size[1], target.attr('cy')),
                Math.max(size[2], target.attr('cx')),
                Math.max(size[3], target.attr('cy'))
            ];
        });
        d3.selectAll(`${divElement} svg`).attr('viewBox', `${size[0]-20} ${size[1]-20} ${size[2]+20} ${size[3]+250}`)

    }

}


//</%text>