from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from .models import Clinic
from .models import Specialist
from .models import Examination
from .models import File

from .forms import ClinicForm
from .forms import SpecialistForm
from .forms import ExaminationForm
from .forms import FileForm

from bokeh.models import CustomJS
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Panel, LabelSet, CDSView
from bokeh.models import DatetimeTickFormatter
from bokeh.models import HoverTool, PanTool, ResetTool
from bokeh.models.widgets import CheckboxGroup, Tabs
from bokeh.layouts import column, row, WidgetBox
from bokeh.models.widgets import DateRangeSlider

import pandas as pd
import numpy as np


class MainView(View):
    templ = 'index.html'

    def get(self, request):
        all_files = File.objects.all()
        return render(request, self.templ, {"all_files": all_files})


class ClinicOps(View):
    templ = 'operations.html'
    form_class = ClinicForm

    def get(self, request):
        form = self.form_class
        data = Clinic.objects.all()
        return render(request, self.templ, {'form': form,
                                            'data': data})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('c_ops')


class SpecialistOps(View):
    templ = 'operations.html'
    form_class = SpecialistForm

    def get(self, request):
        form = self.form_class
        data = Specialist.objects.all()
        return render(request, self.templ, {'form': form,
                                            'data': data})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('s_ops')


class ExaminationOps(View):
    templ = 'operations.html'
    form_class = ExaminationForm

    def get(self, request):
        form = self.form_class()
        data = Examination.objects.all()
        return render(request, self.templ, {'form': form,
                                            'data': data})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('e_ops')


class FileOps(View):
    templ = 'operations.html'
    form_class = FileForm

    def get(self, request):
        form = self.form_class
        data = File.objects.all()
        return render(request, self.templ, {'form': form,
                                            'data': data})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('f_ops')


def make_plot(source):
    start = source.data['examination__date'].min()
    stop = source.data['examination__date'].max()

    # astart = source.data['examination__date_examination__signer__specialisation'][0][0]
    # astop = source.data['examination__date_examination__signer__specialisation'][-1][0]

    hover_tool = HoverTool(mode='vline',
                           tooltips=[('Data', '@examination__date{%Y-%m-%d}'),
                                     ('Nazwa badania', '@examination__name'),
                                     ('Lekarz', '(@examination__signer__surname, '
                                                '@examination__signer__name)'),
                                     ('Specjalizacja', '@examination__signer__specialisation'),
                                     ('set-index', '$index')
                                     ],
                           formatters={
                               'examination__date': 'datetime'}
                           )

    hover_tool.renderers = []
    tools = [hover_tool, 'wheel_zoom', PanTool(), ResetTool()]

    p = figure(title="Mrecords",
               plot_width=1200,
               plot_height=480,
               x_axis_type='datetime',
               y_range=(-11, 11),
               # x_range=list(self.var_for_x_range),
               tools=tools,
               active_scroll='wheel_zoom'
               )

    p.xaxis[0].formatter = DatetimeTickFormatter(days='%b %d')

    p.background_fill_color = "white"
    p.background_fill_alpha = 0.5
    p.border_fill_color = "whitesmoke"
    p.outline_line_width = 3
    p.outline_line_alpha = 0.3
    p.outline_line_color = "navy"
    p.xaxis.axis_label_standoff = 30
    p.yaxis.visible = False
    p.xaxis.major_tick_line_width = 4
    p.xaxis.major_tick_line_color = "firebrick"
    p.axis.major_tick_out = 20
    p.axis.minor_tick_out = 8

    p.ygrid.minor_grid_line_color = 'navy'
    p.ygrid.minor_grid_line_alpha = 0.05

    main_time_line = p.line(x=(start, stop), y=(0, 0), color='navy', line_width=20)

    g1 = p.square(source=source, x='examination__date', y=0, size=5, color='black', name='g1')
    hover_tool.renderers.append(g1)

    g2 = p.circle(source=source, x='examination__date', y='level', color='black', name='g2', size=15)
    g3 = p.segment(source=source, x0='examination__date', y0='zeroes',
                   x1='examination__date', y1='level',
                   color="#F4A582", line_width=2)
    labels = LabelSet(x='examination__date', y='level', text='examination__name', level='glyph',
                      x_offset=5, y_offset=5, source=source, render_mode='canvas')

    p.add_layout(labels)

    return p


class BokehOps(View):
    templ = 'index2.html'

    def get(self, request):
        query2 = File.objects.all().values('file',
                                           'examination_id',
                                           'examination__date',
                                           'examination__name',
                                           'examination__signer__name',
                                           'examination__signer__surname',
                                           'examination__signer__specialisation'). \
            order_by('examination__date')

        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_colwidth', -1)

        df = pd.DataFrame.from_records(query2)

        df['examination__date'] = pd.to_datetime(df['examination__date'])
        df['zeroes'] = 0
        df.reset_index(level=0, inplace=True)
        levels = np.array([-9, 9, -7, 7, -5, 5, -3, 3])
        level = levels[df['index'] % 8]
        df['level'] = level
        df = df.drop_duplicates("examination_id", keep='first')
        df.set_index('examination__date', inplace=True)
        df.drop_duplicates('examination_id', keep='first')
        # df['year'] = df.index.year
        # df['month'] = df.index.month
        # df['day'] = df.index.day

        matrix = df.values
        source1 = df.groupby("examination__signer__specialisation", as_index=False)
        source = ColumnDataSource(df)
        psource = ColumnDataSource(df)

        min_date = df.index.get_level_values('examination__date').min()
        max_date = df.index.get_level_values('examination__date').max()

        var_for_uniques = list(df['examination__signer__specialisation'].unique())
        checkboxes = CheckboxGroup(labels=var_for_uniques,
                                                 active=[i for i in range(len(var_for_uniques))])
        slider = DateRangeSlider(start=min_date,
                                 end=max_date,
                                 value=(min_date, max_date),
                                 step=1,
                                 title="Zakres czasu")

        callback = CustomJS(args=dict
        (source=source,
         psource=psource,
         slider=slider,
         checkboxes=checkboxes),
         code="""
         var source = source.data
         var partsource = psource.data
         var smin = slider.value[0];
         var smax = slider.value[1];
         var checkboxes = checkboxes
         var l_checkboxes = checkboxes.labels;
         console.log(l_checkboxes);
         var a_checkboxes = checkboxes.active
         console.log(a_checkboxes);
         var active_holder = []
         for (let a = 0; a < a_checkboxes.length; a++) {
            active_holder.push(l_checkboxes[a_checkboxes[a]]);
         }
         partsource['examination__name'] = [];
         partsource['examination__signer__name'] = [];
         partsource['examination__signer__surname'] = [];
         partsource['level'] = [];
         partsource['file'] = [];
         partsource['zeroes'] = [];
         partsource['index'] = [];
         partsource['examination_id'] = [];
         partsource['examination__signer__specialisation'] = [];
         var float = []

         for (let b = 0; b <= source['examination__name'].length; b++) {
            if (source['examination__date'][b] >= smin) {
                if (source['examination__date'][b] <= smax) {
                    if (active_holder.includes(source['examination__signer__specialisation'][b])) {
                        psource.data['examination__name'].push(source['examination__name'][b]);
                        psource.data['examination__signer__name'].push(source['examination__signer__name'][b]);
                        psource.data['examination__signer__surname'].push(source['examination__signer__surname'][b]);
                        psource.data['level'].push(source['level'][b]);
                        psource.data['file'].push(source['file'][b]);
                        psource.data['zeroes'].push(source['zeroes'][b]);
                        psource.data['index'].push(source['index'][b]);
                        psource.data['examination_id'].push(source['index'][b]);
                        psource.data['examination__signer__specialisation'].push(source['examination__signer__specialisation'][b]);
                        float.push(source['examination__date'][b]);
                    }
                }
            }
         }
         partsource['examination__date'] = new Float64Array(float);
         console.log(active_holder);
         console.log(cb_obj);
         console.log(psource.data);
         psource.change.emit();
            """)
        slider.js_on_change('value', callback)
        checkboxes.js_on_change('active', callback)
        plot = make_plot(psource)
        controls = WidgetBox(checkboxes, slider)
        layout = row(controls, plot)
        tab = Panel(child=layout, title='records')
        tabs = Tabs(tabs=[tab])
        curdoc().add_root(tabs)
        script, div = components(tabs)
        return render(request, self.templ, locals())
