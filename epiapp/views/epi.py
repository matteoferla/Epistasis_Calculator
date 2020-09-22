from pyramid.view import view_config, view_defaults
from epistasis import Epistatic
from pyramid.response import FileResponse
import os, traceback, uuid, shutil, logging, time
import pandas as pd
import re, json
from typing import List, Dict

log = logging.getLogger(__name__)

@view_defaults(route_name='api')
class Epistaticizer:
    temp_path = os.path.join('epiapp', 'temp')
    demo_data = {} # filled after declaration by `load_demo_data`

    def __init__(self, request):
        self.request = request
        self.data = request.json_body if request.body else {}
        self.tick = time.time()

    @view_config(route_name='home', renderer='../templates/epistasis.mako')
    def main(self):  # serving static basically.
        log.info('Serving main page')
        return {'demo_data': {k: json.dumps(v).replace('NaN', 'null') for k, v in self.demo_data.items()}}

    @view_config(renderer='json')
    def api(self):
        try:
            if 'file' not in self.request.POST:  # JSON
                data = self.via_table()
            else:  # FormData
                data = self.via_file()
            filename = os.path.join(self.temp_path, '{0}.{1}'.format(uuid.uuid4(), 'xlsx'))
            data.save(filename)
            self.request.session['epistasis'] = filename
            suppinfo = ["Combinations", "Experimental average", "Experimental standard error", "Theoretical average",
                        "Theoretical standard error", "Exp.avg - Theor.avg", "Epistasis type"]
            raw = {'theoretical': {'data': data.all_of_it.tolist(), 'columns': data.mutations_list + suppinfo,
                                   'rows': data.comb_index},
                   'empirical': {'data': data.foundment_values.tolist(),
                                 'columns': data.mutations_list + ["Average", "Standard error"],
                                 'rows': data.mutant_list}}
            raw = self.sanitize_nan(raw)
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
                ''.join([th.format(x) for x in [''] + data.mutations_list + ["Average", "Standard error"]])),
                tbody=''.join([tr.format(th.format(data.mutant_list[i] + ''.join(
                    [td.format(x) if isinstance(x, str) or isinstance(x, tuple) else td.format(round(x, 1)) for x
                     in data.foundment_values[i]]))) for i in range(len(data.mutant_list))]))
            tabs = '<ul class="nav nav-tabs" id="myTab" role="tablist"><li class="nav-item"><a class="nav-link active" data-toggle="tab" href="#{set}-table" role="tab">Table</a></li><li class="nav-item"><a class="nav-link" data-toggle="tab" href="#{set}-graph" role="tab">Graph</a></li></ul><br/>'
            tabcont = '<div class="tab-content"><div class="tab-pane fade show active" id="{set}-table" role="tabpanel">{table}</div><div class="tab-pane fade" id="{set}-graph" role="tabpanel">{graph}</div></div>'
            graph = '<div id="{0}-graph-plot"><p>{1}</p><button type="button" class="btn btn-success" id="{0}-down"><i class="fa fa-download" style="margin-left:20px;"></i>Download</button></div>'
            html = '{down}<br/><h3>Theoretical</h3>{theonav}{theotab}<h3>Empirical</h3>{empnav}{emptab}'.format(
                down='<a class="btn btn-primary" href="/download" download="epistasis_results.xlsx">Download</a>',
                theotab=tabcont.format(set='theo', table=theo, graph=graph.format('theo',
                                                                                  'Plot of the combinations of mutations. Note that the circles can be dragged, which is useful when the lines criss-cross under a circle.')),
                theonav=tabs.format(set='theo'),
                emptab=tabcont.format(set='emp', table=emp, graph=graph.format('emp',
                                                                               'Graph of the powerset of combinations mutants with circle width correlated to intensity.')),
                empnav=tabs.format(set='emp')
            )
            # timed
            tock = time.time()
            log.info(f'Calculation complete in {tock - self.tick:.3f} seconds')
            # done!
            return {'html': html, 'raw': raw}
        except Exception as err:
            log.warning(str(err))
            log.debug(traceback.format_exc())
            return {'html': 'ERROR: ' + str(err)}

    def sanitize_nan(self, obj):
        if isinstance(obj, dict):
            return {k: self.sanitize_nan(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.sanitize_nan(v) for v in obj]
        elif str(obj) == 'nan':
            return None
        else:
            return obj


    def via_table(self):
        return Epistatic(**self.data).calculate()

    def via_file(self):
        new_filename = self.save_file()
        r = Epistatic.from_file(self.request.POST['your_study'], new_filename).calculate()
        if os.path.exists(new_filename):
            os.remove(new_filename)
        return r

    def save_file(self, field='file', extension='xlsx'):
        """
        Saves the file without doing anything to it.
        """

        filename = os.path.join(self.temp_path, '{0}.{1}'.format(uuid.uuid4(), extension))
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
        log.info('Serving created filled sheet')
        return response


    @view_config(route_name='create')
    def create(self):
        file = os.path.join(self.temp_path, '{0}.{1}'.format(uuid.uuid4(), 'xlsx'))
        Epistatic.create_input_scheme(your_study='C', mutation_number=self.request.params['mutation_number'],
                                      replicate_number=self.request.params['replicate_number'], outfile=file)
        response = FileResponse(
            file,
            request=self.request,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        log.info('Serving created blank sheet')
        return response

    @view_config(route_name='demo')
    def demo(self):
        """
        This does nothing. The datasets are passed to the front end as they are small. No need to api it!
        Returns:

        """
        if 'dataset' not in self.data:
            return {'status': 'error', 'data': None}
        else:
            pass

    @classmethod
    def load_demo_data(cls) -> None:
        """
        Load the xlxs as a dict of dict of key +-+ (foundment) and value list of values.
        xlxs read from Demo folder.
        This method

        Returns: None

        """
        cls.demo_data = {}
        # os.getcwd() is not necessarily repo root...
        viewfolder = os.path.split(__file__)[0]
        epiappfolder = os.path.split(viewfolder)[0]
        reporoot = os.path.split(epiappfolder)[0]
        demofolder = os.path.join(reporoot, 'demo')
        for filename in os.listdir(demofolder):
            name, extension = os.path.splitext(filename)
            if extension == '.xlsx':
                try:
                    cls.demo_data[name] = cls.parse_demo(os.path.join(demofolder, filename))
                    log.info(f'Demo dataset {filename} loaded')
                except Exception as error:
                    log.error(f'Demo dataset {filename} failed to load. {error.__class__.__name__}: {error}')

    @classmethod
    def parse_demo(cls, filepath) -> Dict[str, List[float]]:
        """
        called by ``load_demo_data`` to do the actual reading
        Args:
            filepath:

        Returns:

        """
        df = pd.read_excel(filepath)
        dexes = list(df.transpose().to_dict().values())

        def extract_signname(dex):
            x = {int(re.match('M(\d+)', k).group(1)): v for k, v in dex.items() if re.match('M\d+', k)}
            return ''.join(
                [x[i] for i in range(1, max(x.keys()) + 1)])  # will rightfully crash if there is a missing value

        def extract_replicatenumber(dex):
            x = {int(re.match('Replicate n°(\d+)', k).group(1)): v for k, v in dex.items() if
                 re.match('Replicate n°\d+', k)}
            return [x[i] for i in range(1, max(x.keys()) + 1)]  # will rightfully crash if there is a missing value

        signnames = [extract_signname(dex) for dex in dexes]
        replicatenumbers = [extract_replicatenumber(dex) for dex in dexes]

        return dict(zip(signnames, replicatenumbers))

# ===== Load data!
Epistaticizer.load_demo_data()

