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
from bokeh.models.widgets import TextInput
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.events import Reset
from bokeh.models import ColumnDataSource, Panel, LabelSet, Label
from bokeh.models import DatetimeTickFormatter
from bokeh.models import HoverTool, PanTool, ResetTool, TapTool
from bokeh.models.widgets import CheckboxGroup, Tabs
from bokeh.layouts import widgetbox, row, column, WidgetBox, layout
from bokeh.models.widgets import DateRangeSlider
from bokeh.models.widgets import DatePicker

import pandas as pd
import numpy as np


class ClinicOps(View):
    templ = 'operations.html'
    form_class = ClinicForm

    def get(self, request):
        form = self.form_class
        data = Clinic.objects.filter(owner=request.user).order_by('name')
        return render(request, self.templ, {'form': form,
                                            'data': data})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
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
        data = Specialist.objects.filter(owner=request.user).order_by('surname')
        return render(request, self.templ, {'form': form,
                                            'data': data})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
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
        object = Specialist.objects.get(pk=specialist_id)
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
        form = self.form_class(user=request.user)
        data = Examination.objects.filter(owner=request.user).order_by("-date")
        return render(request, self.templ, {'form': form,
                                            'data': data})

    def post(self, request):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return redirect('e_ops')


class ExaminationUpdate(View):
    temp = 'operations.html'
    form_class = ExaminationForm

    def get(self, request, examination_id):
        object = Examination.objects.get(pk=examination_id)
        form = self.form_class(user=request.user, initial={'name': object.name,
                                                           'date': object.date,
                                                           'signer': object.signer_id,
                                                           'clinic': object.clinic_id})
        return render(request, self.temp, {'form': form})

    def post(self, request, examination_id):
        object = Examination.objects.get(pk=examination_id)
        form = self.form_class(user=request.user, data=request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect('e_ops')
        return redirect('e_ops')


class ExaminationDelete(View):
    temp = 'operations.html'
    form_class = ExaminationForm

    def get(self, request, examination_id):
        object = Examination.objects.get(pk=examination_id)
        form = self.form_class(user=request.user, initial={'name': object.name,
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
        form = self.form_class(user=request.user)
        data = File.objects.filter(owner=request.user).order_by('-examination__date')
        return render(request, self.templ, {'form': form,
                                            'data': data})

    def post(self, request):
        form = self.form_class(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return redirect('f_ops')


class FileUpdate(View):
    temp = 'operations.html'
    form_class = FileForm

    def get(self, request, file_id):
        object = File.objects.get(pk=file_id)
        form = self.form_class(user=request.user, initial={'file': object.file,
                                                           'examination': object.examination_id})
        return render(request, self.temp, {'form': form})

    def post(self, request, file_id):
        object = File.objects.get(pk=file_id)
        form = self.form_class(user=request.user, data=request.POST, files=request.FILES, instance=object)

        if form.is_valid():
            form.save()
            return redirect('f_ops')
        return redirect('f_ops')


class FileDelete(View):
    temp = 'operations.html'
    form_class = FileForm

    def get(self, request, file_id):
        object = File.objects.get(pk=file_id)
        form = self.form_class(user=request.user, initial={'file': object.file,
                                                           'examination': object.examination_id,
                                                           })
        return render(request, self.temp, {'form': form})

    def post(self, request, file_id):
        object = File.objects.get(pk=file_id)
        object.delete()
        return redirect('f_ops')


class BokehOps(View):
    templ = 'index2.html'

    def get(self, request):
        query2 = File.objects.all().filter(owner=request.user).values('file', 'owner',
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
        del df['owner']
        df.set_index('examination__date', inplace=True)
        source = ColumnDataSource(df)
        psource = ColumnDataSource(df)

        min_date = df.index.get_level_values('examination__date').min()
        max_date = df.index.get_level_values('examination__date').max()

        var_for_uniques = list(df['examination__signer__specialisation'].unique())
        var_for_uniques.sort()

        checkboxes = CheckboxGroup(labels=var_for_uniques,
                                   active=[i for i in range(len(var_for_uniques))],
                                   sizing_mode="scale_both")

        datepicker_s = DatePicker(min_date=min_date,
                                  max_date=max_date,
                                  value=min_date,
                                  title='Badania od:')

        datepicker_e = DatePicker(min_date=min_date,
                                  max_date=max_date,
                                  value=max_date,
                                  title='Badania do:')

        # -----------------------------------------------------
        start = psource.data['examination__date'].min() - pd.Timedelta(days=10)
        stop = psource.data['examination__date'].max() + pd.Timedelta(days=10)

        tooltips = """
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

        hover_tool = HoverTool(
            tooltips=tooltips,
            formatters={
                'examination__date': 'datetime'}
        )

        tap_callback = CustomJS(code="""
            console.log(cb_obj);
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

        tap_tool = TapTool(names=['g2'],
                           behavior='select',
                           callback=tap_callback)

        # reset_tool = ResetTool()
        hover_tool.renderers = []
        tap_tool.renderers = []

        tools = [hover_tool, 'wheel_zoom', tap_tool, PanTool(), ResetTool()]

        p = figure(title="Mrecords",
                   plot_width=1000,
                   plot_height=480,
                   x_axis_type='datetime',
                   y_range=(-11, 11),
                   tools=tools,
                   active_scroll='wheel_zoom',
                   )

        p.xaxis[0].formatter = DatetimeTickFormatter(months='%m.%Y', days='%d.%m.%Y')

        p.background_fill_color = "whitesmoke"
        p.background_fill_alpha = 0.5
        p.border_fill_color = "white"
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

        main_time_line = p.line(x=(start, stop), y=(0, 0), color='#57b9f2', line_width=20)
        g3 = p.segment(source=psource, x0='examination__date', y0='zeroes',
                       x1='examination__date', y1='level',
                       color="#f2db57", line_width=3, hover_color='red')
        g1 = p.square(source=psource, x='examination__date', y=0, size=10, color='black', name='g1', hover_color='navy')

        g2 = p.circle(source=psource, x='examination__date', y='level', color='#c157f2', name='g2', size=15,
                      hover_color='red')
        tap_tool.renderers.append(g2)
        hover_tool.renderers.append(g2)
        # labels = LabelSet(x='examination__date', y='level', text='examination__name', level='glyph',
        #                   x_offset=10, y_offset=-8, source=psource, render_mode='canvas')


        labs = []
        for c in range(len(psource.data['level'])): # len of any column will work
            lab = Label(x=psource.data['examination__date'][c],
                        y=psource.data['level'][c],
                        text=psource.data['examination__name'][c],
                        x_offset=10,
                        y_offset=-8,
                        level='glyph')
            labs.append(lab)

        for lab in labs:
            p.add_layout(lab)

        callback = CustomJS(args=dict
        (source=source,
         psource=psource,
         ds=datepicker_s,
         de=datepicker_e,
         checkboxes=checkboxes,
         labs=labs,),
                            code="""
                 var source = source.data
                 var partsource = psource.data
                 var smin = new Date(ds.value)
                 var smax = new Date(de.value)
                 var labs = labs;
                 var clone = clone;
                 var new_labs = []
                 console.log(labs);
                 smax.setHours(smax.getHours() + 10)
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
                                new_labs.push(labs[b]);
                            }
                        }
                    }
                 console.log(labs);
                 partsource['examination__date'] = new Float64Array(float);
                 console.log("IM MAIN CALLBACK AND IVE BEEN ACTIVE");
                 psource.change.emit();
                 for (c = 0; c < labs.length; c++) {
                    if (!new_labs.includes(labs[c]))   {
                        labs[c].visible = false;
                                                       }
                    else if (new_labs.includes(labs[c]))   {
                        labs[c].visible = true; 
                                                     }
                                                   } 
                    """)


        search_callback = CustomJS(args=dict(ps=psource, labs=labs), code="""
           var cb = console.log(cb_obj); 
           var v = cb_obj.value;
           var re = new RegExp(v);
           var a = function() {console.log("cb_obj.value is ->", v)};
           a();
           var en = ps.data['examination__name']
           console.log(en);
           // 
           var l = labs
           for (let x = 0; x < en.length; x++) {
                if (en[x].toLowerCase().match(re)) { 
                l[x].text_color = "blue";
                l[x].text_font_size = "25pt";
                l[x].text_font_style = "bold";
                console.log("how many found ->", x);
                                 };
                                               };
                                               
           if (v.length == 0) {
                for (let x = 0; x < en.length; x++) {
                l[x].text_color = "#444444";
                l[x].text_font_size = "12pt";
                l[x].text_font_style = "normal";
                                                    };
                              };
        """)

        text_input = TextInput(title="Wyszukiwanie po nazwie:",
                               placeholder="wpisz nazwę badania",
                               callback=search_callback)

        reset_callback = CustomJS(args=dict(p=p,
                                            source=source,
                                            psource=psource,
                                            checkboxes=checkboxes,
                                            datepicker_s=datepicker_s,
                                            datepicker_e=datepicker_e,
                                            text_input=text_input,
                                            labs=labs,
                                            min_date=min_date,
                                            max_date=max_date), code="""

                        var catch_canvas = document.getElementById('canvas');
                        if (catch_canvas) {
                        catch_canvas.remove();
                        }
                        console.log("RESET CALLBACK START");
                        console.log(cb_obj);
                        var min_date = min_date

                        var s_value = datepicker_s.value

                        console.log('min date');
                        console.log(datepicker_s.min_date);


                        var min_date_new = new Date(min_date);
                        var max_date_new = new Date(max_date);


                        console.log('min_date_new = new Date(min_date)');
                        console.log(min_date_new);

                        var date_string = min_date_new.toDateString();
                        var locale_string = min_date_new.toLocaleDateString("pl-PL");
                        console.log(locale_string);
                        console.log('date_string');
                        console.log(date_string);
                        
                        var l = labs;
                        var text_input = text_input;
                        var en = psource.data['examination__name']
                        text_input.value = null;
                        for (let x = 0; x < en.length; x++) {
                                l[x].text_color = "#444444";
                                                    };
                              
                        
                        var labels = checkboxes.labels
                        var labels_holder = []
                        for (let a = 0; a < labels.length; a++) {
                            labels_holder.push(a)
                        }
                        checkboxes.active = labels_holder;

                        console.log('datepicker value before');
                        console.log(datepicker_s.value);


                        console.log(datepicker_s);
                        datepicker_s.value = min_date;
                        datepicker_e.value = max_date;                

                        console.log('datepicker value after');
                        console.log(datepicker_s.value);

                        var get_c_i = document.querySelectorAll('input.bk-widget-form-input')
                        var get_c_i1 = document.querySelector('input.bk-widget-form-input')

                        console.log(get_c_i);

                        // get_c_i[0].value = min_date_new.toDateString();
                        // get_c_i[1].value = max_date_new.toDateString();


                        // psource.data = psource.data;
                        // psource.change.emit();
                        
                        datepicker_s.change.emit(min_date);

                        """)


        checkboxes.js_on_change('active', callback)
        datepicker_s.js_on_change('value', callback)
        datepicker_e.js_on_change('value', callback)
        p.js_on_event(Reset, reset_callback)

        # --------------------------------------------------------
        controls = WidgetBox(checkboxes, datepicker_s, datepicker_e, text_input)
        layout = row(p, controls)
        tab = Panel(child=layout, title='records')
        tabs = Tabs(tabs=[tab])
        curdoc().add_root(tabs)
        script, div = components(tabs)
        return render(request, self.templ, locals())
