//window.demoData is filled in epistasis.mako
//<%text>

// state of where the blobs start at
window.originalPositions = {emp: [], theo: []};

$('#mail').attr('href', 'alref.oettam:otliam'.split("").reverse().join("") + String.fromCharCode(2 * 2 * 2 * 2 * 2 * 2) + 'moc.liamg'.split("").reverse().join(""));
$('#intro').collapse('show');
$('#directly').collapse('show');
$('#alt1').collapse('hide');
$('#alt2').collapse('hide');
$('#res').collapse('hide');

function update_mut_names_div() {
    var mutation_number = $('#mutation_number2').val();
    var replicate_number = $('#replicate_number2').val();
    var header = '<tr><th>Mutant</th>';
    for (let i = 1; i <= mutation_number; i++) { // HEADER row first half
        header += `<th><input placeholder="M${i}" data-toggle="tooltip" data-placement="top" title="Mutation number ${i}. Feel free to rename it something meaningful like D10N" id="M${i}"></th>`;
    }
    for (let i = 1; i <= replicate_number; i++) { // HEADER row second half
        header += `<th data-toggle="tooltip" data-placement="top" title="Replicate number ${i}">R${i}</th>`;
    }
    var body = '';
    var ordered_power_set = Array(Math.pow(2, mutation_number)).fill(' ').map((v, i) => (i).toString(2).padStart(mutation_number, '0').split("")).reverse().sort(function (a, b) {
        return a.reduce(function (accumulator, currentValue) {
            return accumulator + parseInt(currentValue)
        }, 0) - b.reduce(function (accumulator, currentValue) {
            return accumulator + parseInt(currentValue)
        }, 0)
    });
    for (let i = 0; i < Math.pow(2, mutation_number); i++) { // tbody rows...
        body += `<tr name='mutant' data-combo=${ordered_power_set[i].join('')}><td><button class="btn btn-outline-danger deletor"><i class="far fa-times"></i></button></td>`;
        for (var j = 0; j < mutation_number; j++) {
            //body += `<td>${(i).toString(2).padStart(mutation_number,'0').split("").map((v,i)=>v == "1" ? "+" : "-")[j]}</td>`;
            body += `<td>${ordered_power_set[i].map((v, i) => v == "1" ? "+" : "-")[j]}</td>`;
        }
        for (let j = 0; j < replicate_number; j++) {
            body += `<td><input placeholder="NaN" type="number" data-toggle="tooltip" data-placement="top" title="Empirical value" id="M${i}R${j}"></td>`;
        }
        body += '</tr>';
    }

    var txt = `<table class='table table-striped'><thead>${header}</thead><tbody>${body}</tbody></table>`;
    $("#mut_input_table").html(txt);
    $('.deletor').click(event => {
        const row = $(event.target).parents('tr');
        row.hide();
        row.find('input').val('');
    });
}

$("#make_table").click(function () {
    update_mut_names_div()
});

function update_create_url() {
    $('#create').attr("href", "/create?replicate_number=" + $("#replicate_number").val() + "&mutation_number=" + $("#mutation_number").val());
}

$('#create').hover(function () {
    update_create_url()
});
$('#replicate_number').change(function () {
    update_create_url()
});
$('#mutation_number').change(function () {
    update_create_url()
});
$('#clear').click(function () {
    alert("This does nothing")
});
$('#demo').click(function () {
    alert("This does nothing")
});

$('#random_table').click(function () {
    $('[name="mutant"] input').each(function (a, b) {
        $(this).val(Math.random())
    });
});

function makeGraphs(rawData) {
    const parsedData = Powersetplot.parseData(rawData);
    //console.log(JSON.stringify(parsedData));
    const theo = new Powersetplot("theo", parsedData);
    const emp = new Powersetplot("emp", parsedData);
    theo.appendTo("#theo-graph-plot");
    emp.appendTo("#emp-graph-plot");
    $('#theo-down').click(function () {
        saveSvgAsPng(document.getElementById("theo-svg"), "theoretical.png")
    });
    $('#emp-down').click(function () {
        saveSvgAsPng(document.getElementById("emp-svg"), "empirical.png")
    });
    $('#theo-reset').click(function () {
        //not sure why the Powersetplot
        $("#theo-graph-plot svg").detach();
        const theo = new Powersetplot("theo", parsedData);
        theo.appendTo("#theo-graph-plot");
    });
    $('#emp-reset').click(function () {
        $("#emp-graph-plot svg").detach();
        const emp = new Powersetplot("emp", parsedData);
        emp.appendTo("#emp-graph-plot");
    });
}


$('#submit').click(function () {
    // THIS IS THE FILE UPLOAD ROUTE
    $("#results").html('RUNNING!');
    var data = new FormData();
    data.append("file", document.getElementById('file_upload').files[0]);
    // data.append("your_study", $('input[name=your_study2]:checked').val());
    data.append("your_study", document.getElementById("zeroWT").checked ? 'C' : 'S');
    try {
        $.ajax({
            url: "/api",
            type: "POST",
            data: data,
            processData: false,
            cache: false,
            contentType: false,
            success: function (result) {
                //reply = JSON.parse(result.message);
                reply = result;
                $("#results").html(reply['html']);
                //window.sessionStorage.setItem('data', reply['raw']);
                makeGraphs(reply.raw);
                $('#res').collapse('show');
                $('#intro').collapse('hide');
                $('#directly').collapse('hide');
                $('#alt1').collapse('hide');
                $('#alt2').collapse('hide');
            },
            error: function (xhr, s) {
                $("#results").html(s);
            }
        });
    } catch (err) {
        $("#results").html(err);
    }
});




$('#submit_table').click(function () {
    // THIS IS TTHE TABLE UPLOAD ROUTE
    $("#results").html('RUNNING!');
    var mutation_number = parseFloat($("#mutation_number2").val());
    var replicate_number = parseFloat($("#replicate_number2").val());
    var mutation_names = new Array(mutation_number).fill('xxx');
    for (let i = 0; i < mutation_number; i++) {
        if ($("#M" + (i + 1).toString()).val()) {
            mutation_names[i] = $("#M" + (i + 1).toString()).val();
        } else {
            mutation_names[i] = "#M" + (i + 1).toString();
        }
    }
    var mpower = Math.pow(2, mutation_number);
    //var foundment_values = Array.apply(null, Array(mpower)).map((v, i) => (i).toString(2).padStart(mutation_number, '0').split("").map((v, i) => v == "1" ? "+" : "-"));
    //var foundment_values = Array.apply(null, Array(mpower)).map((v, i) => (i).toString(2).padStart(mutation_number, '0').split("").map((v, i) => parseFloat(v)));
    var foundment_values = jQuery.makeArray($('[name=mutant]').map(function (v, i) {
        return $(this).data('combo').toString()
    })).map(function (v, i) {
        return v.split("").map((v, i) => parseFloat(v))
    });
    var replicate_matrix = Array(mpower);
    for (var i = 0; i < mpower; i++) {
        replicate_matrix[i] = Array.apply(null, Array(replicate_number)).map((v, j) => parseFloat($("#M" + i.toString() + "R" + j.toString()).val()));
    }
    var data_array = Array.apply(null, Array(mpower)).map((v, i) => foundment_values[i].concat(replicate_matrix[i]));
    //data_array=None,replicate_matrix=None

    // your_study: $('input[name=your_study]:checked').val(),

    var data = {
        mutation_number: mutation_number,
        replicate_number: replicate_number,
        your_study: document.getElementById("zeroWT").checked ? 'C' : 'S',
        median: document.getElementById("median").checked,
        mutation_names: mutation_names,
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
            success: function (reply) {
                //reply = JSON.parse(result.message);
                $("#results").html(reply['html']);
                //window.sessionStorage.setItem('data', reply);
                if (reply.raw !== undefined) {
                    makeGraphs(reply.raw);
                }
                $('#res').collapse('show');
                $('#intro').collapse('hide');
                $('#directly').collapse('hide');
                $('#alt1').collapse('hide');
                $('#alt2').collapse('hide');
            },
            error: function (xhr, s) {
                $("#results").html(s);
            }
        });
    } catch (err) {
        $("#results").html(err);
    }
});

//JSON.stringify($('#demoData').children().first().data('values'))
// "{"file":"AcevedoRocha_p450_selectivity.xlsx","zero":false,"replicates":3,"mutants":3,"data":{"---":[null,null,null],"--+":[null,null,null],"-+-":[null,null,null],"+--":[null,null,null],"++-":[null,null,null],"+-+":[null,null,null],"-++":[null,null,null],"+++":[null,null,null]}}"

$('#demoData button').click(event => {
    const button = $(event.target);
    //const data = JSON.parse(button.data('values'));
    const data = button.data('values');
    // determine rows!
    if (data === undefined) return 0; //Data is not loaded yet?
    const firstK = Object.keys(data.data)[0];
    $('#mutation_number2').val(data.mutants);
    $('#replicate_number2').val(data.replicates);
    update_mut_names_div();
    data.mutation_names.forEach((v, i) => $('#M' + (i + 1)).val(v));
    document.getElementById("zeroWT").checked = data.zero;
    $('#dataTableModal').modal('hide');
    // fill values!
    Object.keys(data.data).forEach(k => {
        const signed = k.replace(/\-/g, '0').replace(/\+/g, '1');
        const row = $(`[data-combo="${signed}"]`);
        row.find('input').each((i, el) => $(el).val(data.data[k][i]));
    });
});
//</%text>