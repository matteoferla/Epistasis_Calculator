from pyramid.view import view_config, view_defaults
from epistasis import Epistatic
from pyramid.response import FileResponse
import os, traceback, uuid, shutil, logging

log = logging.getLogger(__name__)

@view_defaults(route_name='api')
class Epistaticizer:

    def __init__(self, request):
        self.request = request
        self.data = request.json_body

    @view_config(renderer='json')
    def api(self):
        try:
            if 'file' not in self.request.POST:  # JSON
                data = self.epier_table()
            else:  # FormData
                data = self.epier_file()
            filename = os.path.join('epiapp', 'temp', '{0}.{1}'.format(uuid.uuid4(), 'xlsx'))
            data.save(filename)
            self.request.session['epistasis'] = filename
            suppinfo = ["Combinations", "Experimental average", "Experimental standard deviation", "Theoretical average",
                        "Theoretical standard deviation", "Exp.avg - Theor.avg", "Epistasis type"]
            raw = {'theoretical': {'data': data.all_of_it.tolist(), 'columns': data.mutations_list + suppinfo,
                                   'rows': data.comb_index},
                   'empirical': {'data': data.foundment_values.tolist(),
                                 'columns': data.mutations_list + ["Average", "Standard deviation"],
                                 'rows': data.mutant_list}}

            table = '<div class="table-responsive"><table class="table table-striped"><thead class="thead-dark">{thead}</thead><tbody>{tbody}</tbody></table></div>'
            td = '<td>{}</td>'
            th = '<th>{}</th>'
            tr = '<tr>{}</tr>'
            theo = table.format(thead=tr.format(''.join([th.format(x) for x in [''] + data.mutations_list + suppinfo])),
                                tbody=''.join([tr.format(th.format(data.comb_index[i] + ''.join(
                                    [td.format(x) if isinstance(x, str) or isinstance(x, tuple) else td.format(round(x, 1))
                                     for
                                     x in data.all_of_it[i]]))) for i in range(len(data.comb_index))]))
            emp = table.format(thead=tr.format(
                ''.join([th.format(x) for x in [''] + data.mutations_list + ["Average", "Standard deviation"]])),
                tbody=''.join([tr.format(th.format(data.mutant_list[i] + ''.join(
                    [td.format(x) if isinstance(x, str) or isinstance(x, tuple) else td.format(round(x, 1)) for x
                     in data.foundment_values[i]]))) for i in range(len(data.mutant_list))]))
            tabs = '<ul class="nav nav-tabs" id="myTab" role="tablist"><li class="nav-item"><a class="nav-link active" data-toggle="tab" href="#{set}-table" role="tab">Table</a></li><li class="nav-item"><a class="nav-link" data-toggle="tab" href="#{set}-graph" role="tab">Graph</a></li></ul><br/>'
            tabcont = '<div class="tab-content"><div class="tab-pane fade show active" id="{set}-table" role="tabpanel">{table}</div><div class="tab-pane fade" id="{set}-graph" role="tabpanel">{graph}</div></div>'
            graph = '<div id="{0}-graph-plot"><p>{1}</p><button type="button" class="btn btn-success" id="{0}-down"><i class="fa fa-download" style="margin-left:20px;"></i>Download</button></div>'
            html = '{down}<br/><h3>Theoretical</h3>{theonav}{theotab}<h3>Empirical</h3>{empnav}{emptab}'.format(
                down='<a class="btn btn-primary" href="/download_epistasis" download="epistasis_results.xlsx">Download</a>',
                theotab=tabcont.format(set='theo', table=theo, graph=graph.format('theo',
                                                                                  'Plot of the combinations of mutations. Note that the circles can be dragged, which is useful when the lines criss-cross under a circle.')),
                theonav=tabs.format(set='theo'),
                emptab=tabcont.format(set='emp', table=emp, graph=graph.format('emp',
                                                                               'Graph of the powerset of combinations mutants with circle width correlated to intensity.')),
                empnav=tabs.format(set='emp')
            )

            return {'html': html, 'raw': raw}
        except Exception as err:
            log.warning(str(err))
            log.debug(traceback.format_exc())
            return {'html': 'ERROR: ' + str(err)}

    def epier_table(self):
        return Epistatic(**self.data).calculate()


    def epier_file(self):
        new_filename = self.save_file()
        r = Epistatic.from_file(self.request.POST['your_study'], new_filename).calculate()
        if os.path.exists(new_filename):
            os.remove(new_filename)
        return r

    def save_file(self, field='file', extension='xlsx'):
        """
        Saves the file without doing anything to it.
        """

        filename = os.path.join('epiapp', 'temp', '{0}.{1}'.format(uuid.uuid4(), extension))
        with open(filename, 'wb') as output_file:
            if isinstance(self.request.params[field], str):  ###API user made a mess.
                log.warning(f'user uploaded a str not a file!')
                output_file.write(self.request.params[field].encode('utf-8'))
            else:
                self.request.params[field].file.seek(0)
                shutil.copyfileobj(self.request.params[field].file, output_file)
        return filename

    @view_config(route_name='download')
    def down(self):
        file = self.request.session['epistasis']
        response = FileResponse(
            file,
            request=self.request,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        return response


    @view_config(route_name='create')
    def create(self):
        file = os.path.join('extras_site', 'tmp', '{0}.{1}'.format(uuid.uuid4(), '.xlsx'))
        Epistatic.create_input_scheme(your_study='C', mutation_number=self.request.params['mutation_number'],
                                      replicate_number=self.request.params['replicate_number'], outfile=file)
        response = FileResponse(
            file,
            request=self.request,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        return response
