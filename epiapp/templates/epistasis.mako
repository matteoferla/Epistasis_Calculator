<%inherit file="layout.mako"/>
<!---Intro-->
<%!
    import json

%>
<div class="card p-2">
    <h3 class="card-header bg-dark">


        <a class="card-link text-light" data-toggle="collapse" href="#intro"><i class="far fa-angle-down"></i>&#xA0;&#xA0;&#xA0;Introduction</a>


    </h3>
    <div class="card-body" id="intro">
        <p>Combining different mutations into the same variant often does not result in an additive effect, instead the mutations can antagonise or synergise, a phenomenon called epistasis.</p>
        <p>This tool calculates the epistatic effect different mutations can have on a protein structure.</p>
        <p>For example, if a mutant has 3 mutations, there are different combinations possible: Three single mutants and three double mutants. The creation of these 6 mutants as well as the parent protein and triple mutant make a total of 8 mutants. This would result in a complete dataset (full deconvolution of a triple mutant). Alternatively, it is not necessary to deconvolute all mutations from a multi-mutational variant, since this would be very time consuming. Instead, it is possible to include different subsets of mutations in double, triple, quadruple or nth mutants.</p>
        <p>In either case, this site accepts two ways of inputting the data. The default is by generating and filling out a table online, the second is by generating and filling out an Excel spreadsheet and uploading it. The data can be in various replicates. Cases with a single replicated are accepted. Leave a replicate blank if missing.</p>
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
                <div class="custom-control custom-switch">
                  <input type="checkbox" class="custom-control-input" id="zeroWT">
                  <label class="custom-control-label" for="zeroWT"> centre Wild Type
                    <i class="far fa-question-circle" style="cursor: pointer;" data-toggle="modal" data-target="#zeroWTModal"></i></label>
                </div>
                ## <input type="radio" name="your_study" value="S"> Selectivity &#xA0;
                ## <input type="radio" name="your_study" value="C" checked> Conversion
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
                    <button type="button" class="btn btn-danger"
                            id="clear_table"
                            data-toggle="tooltip" title="Remove the filled table"
                    ><i class="far fa-trash-alt"></i> Clear</button>
                    <button type="button" class="btn btn-secondary"
                            id="random_table"
                            data-toggle="tooltip" title="Fill the table with random numbers. This is actually meaningless and serves the purpose of allowing users to try data that is not the demo"
                    ><i class="far fa-dice"></i> Random</button>
                    <button type="button" class="btn btn-primary" id="demo_table"
                            data-toggle="modal" data-target="#dataTableModal"
                            data-toggle="tooltip" title="Use empirical data"
                            ><i class="far fa-hand-holding-magic"></i> Demos</button>

                    <button type="button" class="btn btn-success" id="submit_table"><i class="far fa-calculator"></i> Submit</button>
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
                ## <input type="radio" name="your_study2" value="S">Selectivity &#xA0;
                ## <input type="radio" name="your_study2" value="C" checked>Conversion
                <div class="custom-control custom-switch">
                  <input type="checkbox" class="custom-control-input" id="zeroWT2">
                  <label class="custom-control-label" for="zeroWT"> centre Wild Type
                    <i class="far fa-question-circle" style="cursor: pointer;" data-toggle="modal" data-target="#zeroWTModal"></i></label>
                </div>
            </div>
            <div class="col-xl-7 col-xl-12 col-lg-12">
                <div class="form-group">
                    <label for="file_upload">Upload Excel spreadsheet</label>
                    <input type="file" id="file_upload" class="form-control-file"
                       accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel">
                  </div>


            </div>
            <div class="col-xl-6 offset-md-2">
                <br>
                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-danger"
                            id="clear"
                            data-toggle="tooltip" title="Remove the filled table"
                    ><i class="far fa-trash-alt"></i>  Clear</button>
                    <!-- <button type="button" class="btn btn-primary" id="demo">Demo</button> -->
                    <button type="button" class="btn btn-success" id="submit"><i class="far fa-calculator"></i>  Submit</button>
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
              %for demo, data in demo_data.items():
                  <button type="button" class="list-group-item list-group-item-action"
                          data-values="${json.dumps(data).replace('NaN', 'null')}"
                          data-citation=""
                          data-mutants=""
                          data-name="${demo}"
                  >${demo.replace('_', ' ')}
                      <br/><small class="text-muted">${data["brief"]}
    </small></button>
              %endfor
</div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

    <div class="modal fade" tabindex="-1" id="zeroWTModal">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Data centering</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">


          <p>For certain types of dataset it is important to make sure that the data is shifted to making the wild type average is zero.</p>
          <p>
        Note that there are different equations for quantifying epistatic effects (see below). For certain types of dataset it is important to make sure that the data is shifted to making the wild type average is zero. For selectivity (in kJ/mol or kcal/mol) this is not required, however, it is for any values given in percentage (e.g., conversion).
          </p><p>

        This tool also allows to determine epistatic effects for these parameters, as reported for cytochrome P450 in the related paper:
         </p><p>
          <ul>
          <li> Selectivity in kJ/mol or kcal/mol</li>
          <li>Conversion of substrate to product (%)</li>
          <li>Product formation rate (PFR) in µmol products / µmol enzyme x 1 / min</li>
          <li>NADPH consumption rate (NCR) in µmol NADPH / µmol enzyme x 1 / min</li>
          <li>Coupling efficiency (CE) in percentage (%)</li>
          <li>Total turnover number (TTN) in µmol products / µmol enzyme</li>
          <li>Total turnover frequency (TTF) in µmol products / µmol enzyme x 1 / min</li>
      </ul>
          <p>Other studies used different equations for the following parameters:</p>
          <ul>
              <li>Weinreich 2006: MIC concentrations of antibiotics in µg/mL</li>
              <li>Shakhnovich 2016: Turnover in kcat-1; Binding in Km; Catalytic efficiency in kcat/Km</li>
              <li>Dalby 2018: Tagg in °C; Tm in °C</li>
          </ul>
        <p>For some of the cases above, there are also demos/examples.
        </p>
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
        $(document).ready(function () {
            <%include file="format_func.js"/>
            <%include file="powersetplot.js"/>
            <%include file="epistasis.js"/>
        });
    </script>
</%block>