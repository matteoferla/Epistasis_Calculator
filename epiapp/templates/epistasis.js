//<%text>

// Let's mod string python-style alla StackOverflow (.formatUnicorn)
String.prototype.format = String.prototype.format ||
    function() {
        "use strict";
        var str = this.toString();
        if (arguments.length) {
            var t = typeof arguments[0];
            var key;
            var args = ("string" === t || "number" === t) ?
                Array.prototype.slice.call(arguments) :
                arguments[0];

            for (key in args) {
                str = str.replace(new RegExp("\\{" + key + "\\}", "gi"), args[key]);
            }
        }

        return str;
    };


$(document).ready(function() {

    $('#mail').attr('href','alref.oettam:otliam'.split("").reverse().join("")+String.fromCharCode(2*2*2*2*2*2)+'moc.liamg'.split("").reverse().join(""));
    $('#intro').collapse('show');
    $('#directly').collapse('show');
    $('#alt1').collapse('hide');
    $('#alt2').collapse('hide');
    $('#res').collapse('hide');

    function update_mut_names_div() {
        var mutation_number = $('#mutation_number2').val();
        var replicate_number = $('#replicate_number2').val();
        var header = '<tr><th>Mutant</th>';
        for (var i = 1; i <= mutation_number; i++) { // HEADER row first half
            header += `<th><input placeholder="M${i}" data-toggle="tooltip" data-placement="top" title="Mutation number ${i}. Feel free to rename it something meaningful like D10N" id="M${i}"></th>`;
        }
        for (var i = 1; i <= replicate_number; i++) { // HEADER row second half
            header += `<th data-toggle="tooltip" data-placement="top" title="Replicate number ${i}">R${i}</th>`;
        }
        var body = '';
        var ordered_power_set=Array(Math.pow(2, mutation_number)).fill(' ').map((v,i)=>(i).toString(2).padStart(mutation_number,'0').split("")).reverse().sort(function(a, b){return a.reduce(function (accumulator, currentValue) {return accumulator + parseInt(currentValue)},0) - b.reduce(function (accumulator, currentValue) {return accumulator + parseInt(currentValue)},0)});
        for (var i = 0; i < Math.pow(2, mutation_number); i++) { // tbody rows...
            body += `<tr name='mutant' data-combo=${ordered_power_set[i].join('')}><td></td>`;
            for (var j = 0; j < mutation_number; j++) {
                //body += `<td>${(i).toString(2).padStart(mutation_number,'0').split("").map((v,i)=>v == "1" ? "+" : "-")[j]}</td>`;
                body += `<td>${ordered_power_set[i].map((v,i)=>v == "1" ? "+" : "-")[j]}</td>`;
            }
            for (var j = 0; j < replicate_number; j++) {
                body += `<td><input placeholder="xxx" type="number" data-toggle="tooltip" data-placement="top" title="Empirical value" id="M${i}R${j}"></td>`;
            }
            body += '</tr>';
        }

        var txt = `<table class='table table-striped'><thead>${header}</thead><tbody>${body}</tbody></table>`;
        $("#mut_input_table").html(txt);
    }

    $("#make_table").click(function() {
        update_mut_names_div()
    });

    function update_create_url() {
        $('#create').attr("href", "/create?replicate_number=" + $("#replicate_number").val() + "&mutation_number=" + $("#mutation_number").val());
    }
    $('#create').hover(function() {
        update_create_url()
    });
    $('#replicate_number').change(function() {
        update_create_url()
    });
    $('#mutation_number').change(function() {
        update_create_url()
    });
    $('#clear').click(function() {
        alert("This does nothing")
    });
    $('#demo').click(function() {
        alert("This does nothing")
    });

    function make_graphs(reply, mutation_number) {
        powersetplot("theo", reply['raw'],mutation_number);
        powersetplot("emp", reply['raw'],mutation_number);
        $('#theo-down').click(function () {saveSvgAsPng(document.getElementById("theo-svg"), "theoretical.png")});
        $('#emp-down').click(function () {saveSvgAsPng(document.getElementById("emp-svg"), "empirical.png")});
    }

    $('#submit').click(function() {
        $("#results").html('RUNNING!');
        var data = new FormData();
        data.append("file", document.getElementById('file_upload').files[0]);
        data.append("your_study", $('input[name=your_study2]:checked').val());
        try {
            $.ajax({
                url: "/api",
                type: "POST",
                data: data,
                processData: false,
                cache: false,
                contentType: false,
                success: function(result) {
                    //reply = JSON.parse(result.message);
                    reply = result;
                    $("#results").html(reply['html']);
                    //window.sessionStorage.setItem('data', reply['raw']);
                    make_graphs(reply,mutation_number);
                    $('#res').collapse('show');
                    $('#intro').collapse('hide');
                    $('#directly').collapse('hide');
                    $('#alt1').collapse('hide');
                    $('#alt2').collapse('hide');
                },
                error: function(xhr, s) {
                    $("#results").html(s);
                }
            });
        } catch (err) {
            $("#results").html(err);
        }
    });

    function add_datapoint(svg,tooltip,datapoint, layout,nodemap) {
    // datapoint is a dict with x y v(alue) color text and info
        var group=svg.append("g");
        var data=[{x: 0, y: 0, node: datapoint['node']}];
        group.data(data)
            .style("cursor", "grab");
        if (datapoint['isLegend'] != undefined) {
            group.append("text")
            .attr("x", datapoint["x"]+20)
            .attr("y", datapoint["y"]+6)
            .attr("text-anchor", "left")
            .style("fill", "black")
            .text(datapoint["text"]); //.attr("dy", ".35em")
        }
        else {
            group.append("text")
            .attr("x", datapoint["x"])
            .attr("y", datapoint["y"]+20)
            .attr("text-anchor", "middle")
            .style("fill", "black")
            .text(datapoint["text"]); //.attr("dy", ".35em")
        }

        group.append("circle")
            .attr("cx", datapoint["x"])
            .attr("cy", datapoint["y"])
            .attr("r", datapoint["v_sd"])
            .style("fill", datapoint["color_sd"])
        group.append("circle")
            .attr("cx", datapoint["x"])
            .attr("cy", datapoint["y"])
            .attr("r", datapoint["v"])
            .style("fill", datapoint["color"])
        if (layout["where"]=='theo') {
            group.append("circle")
                .attr("cx", datapoint["x"])
                .attr("cy", datapoint["y"])
                .attr("r", datapoint["v_e"])
                .style("stroke","black")
                .style("stroke-width","1")
                .style("fill","none")
        }
        group.on("mouseover", function(d) {
                tooltip.transition()
                    .duration(200)
                    .style("opacity", .9);
                tooltip.html(datapoint["info"])
                    .style("left", (d3.event.pageX) + "px")
                    .style("top", (d3.event.pageY - 28) + "px");
            })
            .on("mouseout", function(d) {
                tooltip.transition()
                    .duration(500)
                    .style("opacity", 0);
                });
        group.call(d3.drag()
            .on('drag', function (d) {
                    d.x += d3.event.dx;
                    d.y += d3.event.dy;
                    d3.select(this).attr('transform', 'translate(' + d.x + ',' + d.y + ')');
                    if (d.node != undefined) {
                        nodemap[d.node]['x']+= d3.event.dx;
                        nodemap[d.node]['y']+= d3.event.dy;
                        make_arrows(svg,nodemap)}
                })
            .on("start", function () {d3.select(this).style("cursor", "grabbing")})
            .on("end", function () {d3.select(this).style("cursor", "pointer")})
            );
    }

    function dragstarted(d) {
          d3.select(this).raise().classed("active", true);
        }

        function dragged(d) {
              //d3.select(this).select("text")
              //  .attr("x", d.x = d3.event.x)
              //  .attr("y", d.y = d3.event.y);
              d3.select(this).select("circle")
                .attr("cx", d.x = d3.event.x)
                .attr("cy", d.y = d3.event.y);
            }

        function dragended(d) {
          d3.select(this).classed("active", false);
        }


    function make_arrows(svg,nodemap) {
        if (! d3.select("#arrows").empty()) {d3.select("#arrows").remove()}
        var group=svg.insert("g",":first-child").attr("id","arrows");
        for (var ni =0; ni < nodemap.length; ni++) {
            var node=nodemap[ni];
            for (var oi = 0; oi < node['origin'].length; oi++) {
                var origin=node['origin'][oi];
                group.append("line")
                    .attr("x1", node['x'])
                    .attr("y1", node['y'])
                    .attr("x2", nodemap[origin]['x'])
                    .attr("y2", nodemap[origin]['y'])
                    .attr("stroke","lightgray")
                    .attr("stroke-width",1);
                    //.attr("node","node-"+ni.toString());
                    //.style("border", "gray");
            }
        }
    }

    function powersetplot(where, alldata,mutation_number) {
        var data=alldata['empirical'];
        var chosen_index=mutation_number;
        if (where == 'theo') {
            chosen_index=mutation_number+3;
            data=alldata['theoretical'];
        }
        //quicker than a combinatorial..
        var binomials = [
            [1],
            [1,1],
            [1,2,1],
            [1,3,3,1],
            [1,4,6,4,1],
            [1,5,10,10,5,1],
            [1,6,15,20,15,6,1],
            [1,7,21,35,35,21,7,1],
            [1,8,28,56,70,56,28,8,1]
          ];
        if (where == 'emp') {
            places=binomials[mutation_number];
        }
        else {
            places=Array(mutation_number+1).fill(0);
            for (var i=0; i<data['data'].length; i++) {
                var tier=data['data'][i].slice(0,mutation_number).join('').split("+").length - 1;
                places[tier]++;
            }
            //add-ins for the emp data...
            places[0]=1;
            places[1]=mutation_number;
        }
        var x_step=50;
        var layout={mutation_number: mutation_number,
                    x_step: x_step,
                    y_step: 50,
                    x_mid: Math.max(...places)/2*x_step,
                    x_offset: Array(mutation_number+1).fill(0).map((v,index) => -(places[index]-1)/2*x_step),
                    x_index: Array(mutation_number+1).fill(0),
                    y_offset:50,
                    chosen_index: chosen_index,
                    where: where
            };


        // start canvas
        var tooltip = d3.select("body").append("div").attr("class", "tooltip").style("opacity", 0).style("min-width", "100px");
        var svg = d3.select("#"+where+"-graph-plot").append("svg:svg").attr("width", "100%").attr("height",(mutation_number+1)*layout["y_step"]+50).attr("id",where+"-svg");

        // scale
        layout["scale"]=(x_step/4)/Math.max(...data['data'].map(x =>parseFloat(x[layout["chosen_index"]])));

        // data for arrows!
        var nodemap=new Array(Math.pow(2,mutation_number));

        // make datapoints weirdly (see below for normal).
        if (where=="theo") {
            places=binomials[mutation_number];
            var empdata=alldata['empirical'];
            for (var i=0; i<empdata['data'].length; i++) {
                var item=empdata['data'][i];
                var id=item.slice(0,mutation_number).join('');
                var tier=id.split("+").length - 1;
                if (tier < 2) {
                    var datapoint={x: layout["x_mid"]+layout["x_offset"][tier]+layout["x_index"][tier]*layout["x_step"],
                         y: layout["y_offset"]+(layout["mutation_number"]-tier)*layout["y_step"],
                         v: 0,
                         v_sd: 0,
                         v_e: layout["scale"]*parseFloat(item[mutation_number]),
                         color: "none",
                         color_sd: "none",
                         text:id,
                         info:'Value: '+roundToSD(parseFloat(item[mutation_number]),parseFloat(item[mutation_number+1])),
                         node: id.indexOf('+')+2
                  };
                  nodemap[id.indexOf('+')+2]={'x':datapoint['x'],'y':datapoint['y'],'origin':[1]}; //x, y, origin_id
                  add_datapoint(svg,tooltip,datapoint, layout,nodemap);
                  layout["x_index"][tier]++;
                }
            }
            nodemap[0]=nodemap[1]; //hack because of index from 1...
        }

        epiColors={'+ Sign epistasis':'springgreen',
                '- Sign epistasis':'salmon',
                '+ Reciprocal sign epistasis':'teal',
                '- Reciprocal sign epistasis':'pink',
                '+ Magnitude epistasis':'forestgreen',
                '- Magnitude epistasis':'firebrick'
                }

        // make normally
        for (var i=0; i<data['data'].length; i++) {
            var item=data['data'][i];
            var id=item.slice(0,mutation_number).join('');
            var tier=id.split("+").length - 1;
            var datapoint={x: layout["x_mid"]+layout["x_offset"][tier]+layout["x_index"][tier]*layout["x_step"],
                         y: layout["y_offset"]+(layout["mutation_number"]-tier)*layout["y_step"],
                         v: layout["scale"]*parseFloat(item[layout["chosen_index"]]),
                         v_sd: layout["scale"]*(parseFloat(item[layout["chosen_index"]])+parseFloat(item[layout["chosen_index"]+1])),
                         color: "gray",
                         color_sd: "lightGray",
                         text:id,
                         info:'Value: '+roundToSD(parseFloat(item[layout["chosen_index"]]),parseFloat(item[layout["chosen_index"]+1])),
                         node: i+mutation_number+2
                  };
            layout["x_index"][tier]++;
            if (where=="theo") {
                datapoint['info']=item[mutation_number]+' '+datapoint['info'];
                datapoint['v_e']=layout["scale"]*parseFloat(item[mutation_number+1]);
                if (tier >1) {
                datapoint['color']=epiColors[item[9]];
                nodemap[i+mutation_number+2]={'x':datapoint['x'],'y':datapoint['y'],'origin':item[mutation_number]}; //already an array of int... no need for .slice(1,-1).split(",").map((v,i) => parseInt(v))
                }
            }
            add_datapoint(svg,tooltip,datapoint, layout,nodemap);

        }

        // make legend
        //x_offset: -(places[mutation_number]-1)/2*x_step)
        widesttier=Math.round(mutation_number/2+0.5);
        x=layout["x_mid"]+layout["x_offset"][widesttier]+(layout["x_index"][widesttier]+1.5)*layout["x_step"]; //far right

        if (layout["where"] == "theo") {

            /// theoretical values
            var datapoint={x: x,
                             y: layout["y_offset"]+(layout["mutation_number"]-0)*layout["y_step"], //bottom
                             v: 4,
                             v_sd: 0,
                             v_e: 0,
                             color: "gray",
                             color_sd: "lightGray",
                             text:'Theoretical',
                             info:'Theoretical'
            };
            add_datapoint(svg,tooltip,datapoint, layout,nodemap);
                /// theoretical SD
            var datapoint={x: x,
                             y: layout["y_offset"]+(layout["mutation_number"]-1)*layout["y_step"], //bottom
                             v: 2,
                             v_sd: 4,
                             v_e: 0,
                             color: "white",
                             color_sd: "lightGray",
                             text:'Theoretical SD',
                             info:'theoretical SD'
            };
            add_datapoint(svg,tooltip,datapoint, layout,nodemap);


            /// emp
            var datapoint={x: x,
                             y: layout["y_offset"]+(layout["mutation_number"]-2)*layout["y_step"], //bottom
                             v: 0,
                             v_sd: 0,
                             v_e: 4,
                             color: "none",
                             color_sd: "none",
                             text:'Empirical',
                             info:'Empirical'
            };
            add_datapoint(svg,tooltip,datapoint, layout,nodemap);

            x=layout["x_mid"]+layout["x_offset"][widesttier]+(layout["x_index"][widesttier]+4)*layout["x_step"]; //uber far right

            Object.keys(epiColors).forEach(function(key,index) {
                var datapoint={x: x,
                                 y: layout["y_offset"]+(layout["mutation_number"]-index/2)*layout["y_step"], //bottom
                                 v: 4,
                                 v_sd: 0,
                                 v_e: 0,
                                 color: epiColors[key],
                                 color_sd: "none",
                                 text:key,
                                 info:key,
                                 isLegend: 1
                };
                add_datapoint(svg,tooltip,datapoint, layout,nodemap);
            });



        }
        else {
        /// theoretical values
        var datapoint={x: x,
                         y: layout["y_offset"]+(layout["mutation_number"]-0)*layout["y_step"], //bottom
                         v: 4,
                         v_sd: 0,
                         v_e: 0,
                         color: "gray",
                         color_sd: "lightGray",
                         text:'Empirical',
                         info:'Empirical'
        };
        add_datapoint(svg,tooltip,datapoint, layout,nodemap);
        /// theoretical SD
        var datapoint={x: x,
                         y: layout["y_offset"]+(layout["mutation_number"]-1)*layout["y_step"], //bottom
                         v: 2,
                         v_sd: 4,
                         v_e: 0,
                         color: "white",
                         color_sd: "lightGray",
                         text:'Empirical SD',
                         info:'Empirical SD'
        };
        add_datapoint(svg,tooltip,datapoint, layout,nodemap);
        }

    // make arrows
    if (where=="theo") {
        //console.log(nodemap);
        make_arrows(svg,nodemap);
    }
    }

    function roundToSD(mean,sd) {
        var d=Math.round(Math.pow(10,Math.log10(sd)));
        return '{0}±{1}'.format(Math.round(mean/d)*d, Math.round(sd/d)*d);
    }


    $('#submit_table').click(function() {
        $("#results").html('RUNNING!');
        var mutation_number = parseFloat($("#mutation_number2").val());
        var replicate_number = parseFloat($("#replicate_number2").val());
        var mutations_list = new Array(mutation_number).fill('xxx');
        for (var i = 0; i < mutation_number; i++) {
            if ($("#M" + (i + 1).toString()).val()) {
                mutations_list[i] = $("#M" + (i + 1).toString()).val();
            } else {
                mutations_list[i] = "#M" + (i + 1).toString();
            }
        }
        var mpower = Math.pow(2, mutation_number);
        //var foundment_values = Array.apply(null, Array(mpower)).map((v, i) => (i).toString(2).padStart(mutation_number, '0').split("").map((v, i) => v == "1" ? "+" : "-"));
        //var foundment_values = Array.apply(null, Array(mpower)).map((v, i) => (i).toString(2).padStart(mutation_number, '0').split("").map((v, i) => parseFloat(v)));
        var foundment_values = jQuery.makeArray($('[name=mutant]').map(function (v,i) {return $(this).data('combo').toString()})).map(function(v,i) {return v.split("").map((v, i) => parseFloat(v))});
        var replicate_matrix = Array(mpower);
        for (var i = 0; i < mpower; i++) {
            replicate_matrix[i] = Array.apply(null, Array(replicate_number)).map((v, j) => parseFloat($("#M" + i.toString() + "R" + j.toString()).val()));
        }
        var data_array = Array.apply(null, Array(mpower)).map((v, i) => foundment_values[i].concat(replicate_matrix[i]));
        //data_array=None,replicate_matrix=None

        var data = {
            mutation_number: mutation_number,
            replicate_number: replicate_number,
            your_study: $('input[name=your_study]:checked').val(),
            mutations_list: mutations_list,
            foundment_values: foundment_values,
            replicate_matrix: replicate_matrix,
            data_array: data_array
        };

        try {
            $.ajax({
                url: "/api",
                type: "POST",
                dataType: 'json',
                data: JSON.stringify(data),
                processData: false,
                cache: false,
                contentType: false,
                success: function(result) {
                    //reply = JSON.parse(result.message);
                    reply = result;
                    $("#results").html(reply['html']);
                    window.sessionStorage.setItem('data', reply);
                    make_graphs(reply,mutation_number);
                    $('#res').collapse('show');
                    $('#intro').collapse('hide');
                    $('#directly').collapse('hide');
                    $('#alt1').collapse('hide');
                    $('#alt2').collapse('hide');
                },
                error: function(xhr, s) {
                    $("#results").html(s);
                }
            });
        } catch (err) {
            $("#results").html(err);
        }
    });

    $('#demo_table').click(function() {
        $('#mutation_number2').val(3);
        $('#replicate_number2').val(3);
        update_mut_names_div();
        demo = [
            [40.408327, 37.176372, 35.776619],
            [43.913044,	47.390555,	42.959925],
            [34.551186,	34.033348,	30.844536],
            [37.383186,	35.019421,	42.932996],
            [31.102138,	28.735591,	29.401488],
            [29.78191,	24.641165,	25.13452],
            [79.956978,	84.28502,	74.090488],
            [76.937329,	69.938071,	58.361839]
        ];
        for (var m = 0; m < 8; m++) {
            for (var r = 0; r < 3; r++) {
                $(`#M${m}R${r}`).val(demo[m][r]);
            }
        }
    });




});
//</%text>