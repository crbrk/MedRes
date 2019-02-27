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
from bokeh.models import ColumnDataSource, Panel, LabelSet
from bokeh.models import DatetimeTickFormatter
from bokeh.models import HoverTool, PanTool, ResetTool, TapTool
from bokeh.models.widgets import CheckboxGroup, Tabs
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import DateRangeSlider
from bokeh.models.widgets import DatePicker
import pandas as pd
import numpy as np


# class MainView(View):
#     templ = 'index.html'
#
#     def get(self, request):
#         all_files = File.objects.all()
#         return render(request, self.templ, {"all_files": all_files})


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

class ClinicUpdate(View):
    temp = 'operations.html'
    form_class = ClinicForm

    def get(self, request, clinic_id):
        object = Clinic.objects.get(pk=clinic_id)
        form = self.form_class(initial={'name': object.name,
                                        'street': object.street,
                                        'street_number': object.street_number,
                                        'city': object.city,
                                        'postal': object.postal,
                                        'phone': object.phone})
        return render(request, self.temp, {'form': form})

    def post(self, request, clinic_id):
        object = Clinic.objects.get(pk=clinic_id)
        form = self.form_class(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect('c_ops')
        return redirect('c_ops')

class ClinicDelete(View):
    temp = 'operations.html'
    form_class = ClinicForm

    def get(self, request, clinic_id):
        object = Clinic.objects.get(pk=clinic_id)
        form = self.form_class(initial={'name': object.name,
                                        'street': object.street,
                                        'street_number': object.street_number,
                                        'city': object.city,
                                        'postal': object.postal,
                                        'phone': object.phone})
        return render(request, self.temp, {'form': form})

    def post(self, request, clinic_id):
        object = Clinic.objects.get(pk=clinic_id)
        object.delete()
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
        return redirect('s_ops')

class SpecialistUpdate(View):
    temp = 'operations.html'
    form_class = SpecialistForm

    def get(self, request, specialist_id):
        object = Specialist.objects.get(pk=specialist_id)
        form = self.form_class(initial={'name': object.name,
                                        'surname': object.surname,
                                        'specialisation': object.specialisation})
        return render(request, self.temp, {'form': form})

    def post(self, request, specialist_id):
        object = Specialist.objects.get(pk=specialist_id)
        form = self.form_class(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect('s_ops')
        return redirect('s_ops')

class SpecialistDelete(View):
    temp = 'operations.html'
    form_class = SpecialistForm

    def get(self, request, specialist_id):
        object = Specialist.objects.get(pk = specialist_id)
        form = self.form_class(initial={'name': object.name,
                                        'surname': object.surname,
                                        'specialisation': object.specialisation})
        return render(request, self.temp, {'form': form})

    def post(self, request, specialist_id):
        object = Specialist.objects.get(pk=specialist_id)
        object.delete()
        return redirect('c_ops')

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


class ExaminationUpdate(View):
    temp = 'operations.html'
    form_class = ExaminationForm

    def get(self, request, examination_id):
        object = Examination.objects.get(pk=examination_id)
        form = self.form_class(initial={'name': object.name,
                                        'date': object.date,
                                        'signer': object.signer_id,
                                        'clinic': object.clinic_id})
        return render(request, self.temp, {'form': form})

    def post(self, request, examination_id):
        object = Examination.objects.get(pk=examination_id)
        form = self.form_class(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect('e_ops')
        return redirect('e_ops')


class ExaminationDelete(View):
    temp = 'operations.html'
    form_class = ExaminationForm

    def get(self, request, examination_id):
        object = Examination.objects.get(pk = examination_id)
        form = self.form_class(initial={'name': object.name,
                                        'date': object.date,
                                        'signer': object.signer_id,
                                        'clinic': object.clinic_id})
        return render(request, self.temp, {'form': form})

    def post(self, request, examination_id):
        object = Examination.objects.get(pk=examination_id)
        object.delete()
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


class FileUpdate(View):
    temp = 'operations.html'
    form_class = FileForm

    def get(self, request, file_id):
        object = File.objects.get(pk=file_id)
        form = self.form_class(initial={'file': object.file,
                                        'examination': object.examination_id})
        return render(request, self.temp, {'form': form})

    def post(self, request, file_id):
        object = File.objects.get(pk=file_id)
        form = self.form_class(request.POST, request.FILES, instance=object)

        if form.is_valid():
            form.save()
            return redirect('f_ops')
        return redirect('f_ops')

class FileDelete(View):
    temp = 'operations.html'
    form_class = FileForm

    def get(self, request, file_id):
        object = File.objects.get(pk = file_id)
        form = self.form_class(initial={'file': object.file,
                                        'examination': object.examination_id,
                                        })
        return render(request, self.temp, {'form': form})

    def post(self, request, file_id):
        object = File.objects.get(pk=file_id)
        object.delete()
        return redirect('f_ops')



def make_plot(source):
    source = source
    start = source.data['examination__date'].min() - pd.Timedelta(days=5)
    stop = source.data['examination__date'].max() + pd.Timedelta(days=5)


    TOOLTIPS = """
        <div>
            <div>
                <embed
                    src='/media/@file' alt="@file" height="300" width="170"
                ></embed>
            </div>
            <div>
                <p>
                <span style="font-size: 10px; font-weight: bold;">@examination__name</span>
                <p>
                <span style="font-size: 10px; font-weight: bold;">@examination__date{%d-%B-%Y}</span>
                <p>
                <span style="font-size: 10px; font-weight: bold;">@examination__signer__surname</span>
                <span style="font-size: 10px; font-weight: bold;">@examination__signer__specialisation</span>
            </div>
        </div>
        """

    # hover_tool1 = HoverTool(mode='vline',
    #                        tooltips=[('Data', '@examination__date{%Y-%m-%d}'),
    #                                  ('Nazwa badania', '@examination__name'),
    #                                  ('Lekarz', '(@examination__signer__surname, '
    #                                             '@examination__signer__name)'),
    #                                  ('Specjalizacja', '@examination__signer__specialisation'),
    #                                  ('set-index', '$index')
    #                                  ],
    #                        formatters={
    #                            'examination__date': 'datetime'}
    #                        )
    hover_tool = HoverTool(
                           tooltips=TOOLTIPS,
                           formatters={
                               'examination__date': 'datetime'}
                           )
    tap_callback = CustomJS(code="""
    console.log(cb_data);
    var indices_of_selected_examinations = cb_data.source.selected.indices;

    var operations_div = document.getElementById('operations');
        
    var get_created_div = document.getElementById('canvas')
    if (get_created_div) {
        get_created_div.remove()
    }
    
    var new_div = document.createElement("div")
    new_div.setAttribute('id', 'canvas')
    operations_div.appendChild(new_div);
    
    for (let c=0; c < indices_of_selected_examinations.length; c++) {
        
        var single_index = indices_of_selected_examinations[c];
        var single_file = cb_data.source.data['file'][single_index];
        
        
        var new_emb = document.createElement('embed');
        
        new_div.appendChild(new_emb);
        
        new_emb.src = /media/ + single_file;
        new_emb.alt = /media/ + single_file;
        new_emb.width = "25%";
        new_emb.height = "500px";
        };

    """)

    reset_callback = CustomJS(code="""
    var catch_canvas = document.getElementById('canvas');
    if (catch_canvas) {
    catch_canvas.remove()
    }
    """)

    tap_tool = TapTool(names=['g2'],
                       behavior='select',
                       callback=tap_callback)

    reset_tool = ResetTool()


    hover_tool.renderers = []
    tap_tool.renderers = []

    tools = [hover_tool, 'wheel_zoom', tap_tool, PanTool(), reset_tool]

    p = figure(title="Mrecords",
               plot_width=1000,
               plot_height=480,
               x_axis_type='datetime',
               y_range=(-11, 11),
               # x_range=list(self.var_for_x_range),
               tools=tools,
               active_scroll='wheel_zoom',
               )

    p.js_on_event('reset', reset_callback)
    p.xaxis[0].formatter = DatetimeTickFormatter(months='%B %Y')

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


    main_time_line = p.line(x=(start, stop), y=(0, 0), color='#57b9f2', line_width=20, line_dash="1 1")
    g3 = p.segment(source=source, x0='examination__date', y0='zeroes',
                   x1='examination__date', y1='level',
                   color="#f2db57", line_width=3, hover_color='red')
    g1 = p.square(source=source, x='examination__date', y=0, size=10, color='black', name='g1', hover_color='navy')

    g2 = p.circle(source=source, x='examination__date', y='level', color='#c157f2', name='g2', size=15, hover_color='red')
    tap_tool.renderers.append(g2)
    hover_tool.renderers.append(g2)
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
        print(query2)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_colwidth', -1)

        df = pd.DataFrame.from_records(query2)

        df['examination__date'] = pd.to_datetime(df['examination__date'])
        df['examination__date'] = df['examination__date']
        df['zeroes'] = 0
        df.reset_index(level=0, inplace=True)
        levels = np.array([-9, 9, -7, 7, -5, 5, -3, 3])
        level = levels[df['index'] % 8]
        df['level'] = level
        #df = df.drop_duplicates("examination_id", keep='first')
        df.set_index('examination__date', inplace=True)


        source1 = df.groupby("examination__signer__specialisation", as_index=False)
        source = ColumnDataSource(df)
        psource = ColumnDataSource(df)

        min_date = df.index.get_level_values('examination__date').min() - pd.Timedelta(days=1)
        max_date = df.index.get_level_values('examination__date').max() + pd.Timedelta(days=1)

        var_for_uniques = list(df['examination__signer__specialisation'].unique())
        var_for_uniques.sort()

        checkboxes = CheckboxGroup(labels=var_for_uniques,
                                   active=[i for i in range(len(var_for_uniques))],
                                   sizing_mode="scale_both")

        slider = DateRangeSlider(start=min_date,
                                 end=max_date,
                                 value=(min_date, max_date),
                                 step=10700,
                                 title="Zakres czasu",
                                 sizing_mode="scale_both")

        datepicker_s = DatePicker(min_date=min_date,
                                max_date=max_date,
                                value=min_date,
                                title='Badania od:')

        datepicker_e = DatePicker(min_date=min_date,
                                  max_date=max_date,
                                  value=max_date,
                                  title='Badania do:')



        callback = CustomJS(args=dict
        (source=source,
         psource=psource,
         ds=datepicker_s,
         de=datepicker_e,
         slider=slider,
         checkboxes=checkboxes),
         code="""
         console.log(source);
         var source = source.data
         var partsource = psource.data

         var smin = new Date(ds.value)
         console.log(smin);
         var smax = new Date(de.value)
         console.log(smax);
         smax.setHours(smax.getHours() + 10)
         console.log(smax);
         var checkboxes = checkboxes
         var l_checkboxes = checkboxes.labels;
         var a_checkboxes = checkboxes.active
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
            if (source['examination__date'][b] <= smax && (source['examination__date'][b] >= smin)) { 
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
         
         partsource['examination__date'] = new Float64Array(float);
         console.log(cb_obj);
         console.log(cb_obj.values);
         console.log(psource.data);
         psource.change.emit();
            """)


        checkboxes.js_on_change('active', callback)
        datepicker_s.js_on_change('value', callback)
        datepicker_e.js_on_change('value', callback)

        plot = make_plot(psource)

        controls = widgetbox(checkboxes, datepicker_s, datepicker_e)
        layout = row(plot, controls)
        tab = Panel(child=layout, title='records')
        tabs = Tabs(tabs=[tab])
        curdoc().add_root(tabs)
        script, div = components(tabs)
        return render(request, self.templ, locals())
