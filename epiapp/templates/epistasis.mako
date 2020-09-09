<%inherit file="layout.mako"/>
<!---Intro-->
<div class="card p-2">
    <h3 class="card-header bg-dark">


        <a class="card-link text-light" data-toggle="collapse" href="#intro"><i class="far fa-angle-down"></i>&#xA0;&#xA0;&#xA0;Introduction</a>


    </h3>
    <div class="card-body" id="intro">
        <p>Calculate the epistatic effect different mutations have on a structure.</p>
        <p>This site accepts two ways of inputting the data. The default is by generating
            and filling out a table online, the second is by generating and filling
            out an Excel spreadsheet and uploading it.</p>
        <p>Cases with a single replicated are accepted. Leave a replicate blank if missing.</p>
    </div>
</div>
<br>
<!--Form-->
<div class="card p-2">
    <h3 class="card-header bg-dark">


        <a class="card-link text-light" data-toggle="collapse" href="#directly"><i class="far fa-angle-down"></i>&#xA0;&#xA0;&#xA0;Fill
            directly</a>


    </h3>
    <div class="card-body" id="directly">
        <div class="row">
            <div class="col-xl-4 col-xl-3 col-lg-12">
                <input type="radio" name="your_study" value="S"> Selectivity &#xA0;
                <input type="radio" name="your_study" value="C" checked> Conversion
            </div>
            <div class="col-xl-3 col-xl-3">
                <div class="input-group">
                    <div class="input-group-prepend"><span class="input-group-text" id="mutation_number2-addon">mutation N</span>
                    </div>
                    <input type="number" class="form-control" placeholder="N" aria-label="mutation_number"
                           aria-describedby="mutation_number2-addon" id="mutation_number2">
                </div>
            </div>
            <div class="col-xl-4 col-xl-5">
                <div class="input-group">
                    <div class="input-group-prepend"><span class="input-group-text" id="replicate_number2-addon">replicate N</span>
                    </div>
                    <input type="number" class="form-control" placeholder="N" aria-label="replicate_number2"
                           aria-describedby="replicate_number2-addon" id="replicate_number2">
                    <div class="input-group-append">
                        <button class="btn btn-success" type="button" id="make_table">Go</button>
                    </div>
                </div>
            </div>
        </div>
        <br>
        <div clas="row" id="mut_input_table">
            <div class="col-xl-7 col-xl-12 col-lg-12">
                <div class="alert alert-warning" role="alert">Set numbers first. The table will be dynamically
                    generated.
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-xl-6 offset-md-2">
                <br>
                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-secondary" id="clear_table">Clear</button>
                    <button type="button" class="btn btn-primary" id="demo_table"
                            data-toggle="modal" data-target="#dataTableModal"
                            >Demos</button>
                    <button type="button" class="btn btn-success" id="submit_table">Submit</button>
                </div>
            </div>
        </div>
    </div>
</div>
<br>
<div class="card p-2">
    <h3 class="card-header bg-dark">


        <a class="collapsed card-link text-light" data-toggle="collapse" href="#alt1"><i class="far fa-angle-down"></i>&#xA0;&#xA0;&#xA0;Alt
            (part 1): Create template</a>


    </h3>
    <div class="card-body collapse" id="alt1">
        <div class="row">
            <div class="col-xl-4">
                <div class="input-group">
                    <div class="input-group-prepend"><span class="input-group-text" id="mutation_number-addon">mutation number</span>
                    </div>
                    <input type="number" class="form-control" placeholder="N" aria-label="mutation_number"
                           aria-describedby="mutation_number-addon" id="mutation_number">
                </div>
            </div>
            <div class="col-xl-4">
                <div class="input-group">
                    <div class="input-group-prepend"><span class="input-group-text" id="replicate_number-addon">replicate number</span>
                    </div>
                    <input type="number" class="form-control" placeholder="N" aria-label="replicate_number"
                           aria-describedby="replicate_number-addon" id="replicate_number">
                </div>
            </div>
            <div class="col-xl-4"><a class="btn btn-primary" id="create" href="/create_epistasis"
                                     download="epistasis_template.xlsx">Create</a>
            </div>
        </div>
    </div>
</div>
<br>
<div class="card p-2">
    <h3 class="card-header bg-dark">


        <a class="collapsed card-link text-light" data-toggle="collapse" href="#alt2"><i class="far fa-angle-down"></i>&#xA0;&#xA0;&#xA0;Alt
            (part 2): Upload filled</a>


    </h3>
    <div class="card-body collapse" id="alt2">
        <div class="row">
            <div class="col-xl-5 col-xl-12 col-lg-12">
                <input type="radio" name="your_study2" value="S">Selectivity &#xA0;
                <input type="radio" name="your_study2" value="C" checked>Conversion
            </div>
            <div class="col-xl-7 col-xl-12 col-lg-12">
                <input type="file" id="file_upload"
                       accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel">
            </div>
            <div class="col-xl-6 offset-md-2">
                <br>
                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-secondary" id="clear">Clear</button>
                    <button type="button" class="btn btn-primary" id="demo">Demo</button>
                    <button type="button" class="btn btn-success" id="submit">Submit</button>
                </div>
            </div>
        </div>
    </div>
</div>
<br>
<!--Results-->
<div class="card p-2">
    <h3 class="card-header bg-dark">


        <a class="collapsed card-link text-light" data-toggle="collapse" href="#res"><i class="far fa-angle-down"></i>&#xA0;&#xA0;&#xA0;Result</a>


    </h3>
    <div class="card-body collapse" id="res">
        <div id="results"></div>
        <br>
        <div id="heatmap"></div>
    </div>
</div>

## =====================================================================================================================

<%block name="modal">
    <div class="modal fade" tabindex="-1" id="dataTableModal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Demo data</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <p>All examples are from empirical data.</p>
          <div class="list-group" id="demoData">
              %for demo in demo_data:
                  <button type="button" class="list-group-item list-group-item-action"
                          data-values="${demo_data[demo]}"
                          data-citation=""
                          data-mutants=""
                          data-name="${demo}"
                  >${demo.replace('_', ' ')}</button>
              %endfor
</div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
</%block>

## =====================================================================================================================

<%block name="code">
    <script>
        <%include file="epistasis.js"/>
    </script>
</%block>