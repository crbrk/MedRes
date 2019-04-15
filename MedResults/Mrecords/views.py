from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.formats import localize

from .models import Clinic
from .models import Specialist
from .models import Examination
from .models import File

from .forms import ClinicForm
from .forms import SpecialistForm
from .forms import ExaminationForm
from .forms import FileForm
from .forms import RegisterForm

from tabulate import tabulate
from bokeh.transform import jitter, factor_cmap

from bokeh.models import Arrow, VeeHead
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
from bokeh.layouts import widgetbox, row, column, WidgetBox
from bokeh.models.widgets import DatePicker


import pandas as pd
import numpy as np

LoginView.redirect_authenticated_user = True


class AddUser(View):
    temp = "registration/login.html"
    form_class = RegisterForm

    def get(self, request):
        form = self.form_class
        return render(request, self.temp, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_pw = form.cleaned_data.get('password')
            messages.success(request, 'REJESTRACJA UDANA. MOŻESZ SIĘ ZALOGOWAĆ')
            return redirect("login")
        else:
            messages.error(request, 'REJESTRACJA NIEUDANA.')
        return render(request, self.temp, locals())


class ClinicOps(LoginRequiredMixin, View):
    temp = 'operations.html'
    form_class = ClinicForm

    def get(self, request):
        form = self.form_class
        data = Clinic.objects.filter(owner=request.user).order_by('name')
        if data.count() == 0:
            messages.error(request, "LISTA PLACÓWEK JEST PUSTA")
        return render(request, self.temp, {'form': form, 'data': data})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(request, 'DODANO NOWĄ PLACÓWKĘ.')
            return redirect('c_ops')
        messages.error(request, 'NIE DODANO PLACÓWKI.')
        return render(request, self.temp, {'form': form})


class ClinicUpdate(LoginRequiredMixin, View):
    temp = 'operations.html'
    form_class = ClinicForm

    def get(self, request, clinic_id):
        try:
            requested_object = Clinic.objects.get(pk=clinic_id)
        except ObjectDoesNotExist:
            messages.error(request, "EDYCJA NIEUDANA - NIE ZNALEZIONO PLACÓWKI")
            return redirect('c_ops')
        form = self.form_class(initial={'name': requested_object.name,
                                        'street': requested_object.street,
                                        'street_number': requested_object.street_number,
                                        'city': requested_object.city,
                                        'postal': requested_object.postal})
        return render(request, self.temp, {'form': form})

    def post(self, request, clinic_id):
        try:
            requested_object = Clinic.objects.get(pk=clinic_id)
        except ObjectDoesNotExist:
            messages.error(request, "EDYCJA NIEUDANA - NIE ZNALEZIONO PLACÓWKI")
            return redirect('c_ops')
        form = self.form_class(request.POST, instance=requested_object)
        if form.is_valid():
            form.save()
            messages.success(request, 'EDYCJA UDANA.')
            return redirect('c_ops')
        messages.error(request, 'EDYCJA NIEUDANA.')
        return redirect("c_ops")


class ClinicDelete(LoginRequiredMixin, View):
    temp = 'operations.html'
    form_class = ClinicForm

    def get(self, request, clinic_id):
        try:
            requested_object = Clinic.objects.get(pk=clinic_id)
        except ObjectDoesNotExist:
            messages.error(request, "USUWANIE NIEUDANE - NIE ZNALEZIONO PLACÓWKI")
            return redirect('c_ops')
        form = self.form_class(initial={'name': requested_object.name,
                                        'street': requested_object.street,
                                        'street_number': requested_object.street_number,
                                        'city': requested_object.city,
                                        'postal': requested_object.postal})
        return render(request, self.temp, {'form': form})

    def post(self, request, clinic_id):
        try:
            requested_object = Clinic.objects.get(pk=clinic_id)
        except ObjectDoesNotExist:
            messages.error(request, "USUWANIE NIEUDANE - NIE ZNALEZIONO PLACÓWKI")
            return redirect("c_ops")
        requested_object.delete()
        messages.success(request, 'USUWANIE UDANE.')
        return redirect('c_ops')


class SpecialistOps(LoginRequiredMixin, View):
    temp = 'operations.html'
    form_class = SpecialistForm

    def get(self, request):
        form = self.form_class
        data = Specialist.objects.filter(owner=request.user).order_by('specialisation')
        if data.count() == 0:
            messages.error(request, "LISTA LEKARZY JEST PUSTA")
        return render(request, self.temp, {'form': form, 'data': data})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(request, "DODANO NOWEGO LEKARZA")
            return redirect('s_ops')
        messages.error(request, "NIE DODANO LEKARZA")
        return render(request, self.temp, {'form': form})


class SpecialistUpdate(LoginRequiredMixin, View):
    temp = 'operations.html'
    form_class = SpecialistForm

    def get(self, request, specialist_id):
        try:
            requested_object = Specialist.objects.get(pk=specialist_id)
        except ObjectDoesNotExist:
            messages.error(request, "EDYCJA NIEUDANA - NIE ZNALEZIONO LEKARZA")
            return redirect('s_ops')
        form = self.form_class(initial={'name': requested_object.name,
                                        'surname': requested_object.surname,
                                        'specialisation': requested_object.specialisation})
        return render(request, self.temp, {'form': form})

    def post(self, request, specialist_id):
        try:
            requested_object = Specialist.objects.get(pk=specialist_id)
        except ObjectDoesNotExist:
            messages.error(request, "EDYCJA NIEUDANA - NIE ZNALEZIONO LEKARZA")
            return redirect('s_ops')
        form = self.form_class(request.POST, instance=requested_object)
        if form.is_valid():
            form.save()
            messages.success(request, "EDYCJA UDANA")
            return redirect('s_ops')
        return redirect("s_ops")


class SpecialistDelete(LoginRequiredMixin, View):
    temp = 'operations.html'
    form_class = SpecialistForm

    def get(self, request, specialist_id):
        try:
            requested_object = Specialist.objects.get(pk=specialist_id)
        except ObjectDoesNotExist:
            messages.error(request, "USUWANIE NIEUDANE - NIE ZNALEZIONO LEKARZA")
            return redirect("s_ops")
        form = self.form_class(initial={'name': requested_object.name,
                                        'surname': requested_object.surname,
                                        'specialisation': requested_object.specialisation})
        return render(request, self.temp, {'form': form})

    def post(self, request, specialist_id):
        try:
            requested_object = Specialist.objects.get(pk=specialist_id)
        except ObjectDoesNotExist:
            messages.error(request, "USUWANIE NIEUDANE - NIE ZNALEZIONO LEKARZA")
            return redirect('s_ops')
        requested_object.delete()
        messages.success(request, "USUWANIE UDANE")
        return redirect('s_ops')


class ExaminationOps(LoginRequiredMixin, View):
    temp = 'operations.html'
    form_class = ExaminationForm

    def get(self, request):
        form = self.form_class(user=request.user)
        data = Examination.objects.filter(owner=request.user).order_by("-date")
        if data.count() == 0:
            messages.error(request, "LISTA BADAŃ JEST PUSTA")
        return render(request, self.temp, {'form': form, 'data': data})

    def post(self, request):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(request, "DODANO NOWE BADANIE")
            return redirect('e_ops')
        messages.error(request, "NIE DODANO BADANIA")
        return render(request, self.temp, {'form': form})


class ExaminationUpdate(LoginRequiredMixin, View):
    temp = 'operations.html'
    form_class = ExaminationForm

    def get(self, request, examination_id):
        try:
            requested_object = Examination.objects.get(pk=examination_id)
        except ObjectDoesNotExist:
            messages.error(request, "EDYCJA NIEUDANA - NIE ZNALEZIONO BADANIA")
            return redirect('e_ops')
        form = self.form_class(user=request.user, initial={'name': requested_object.name,
                                                           'date': requested_object.date,
                                                           'signer': requested_object.signer_id,
                                                           'clinic': requested_object.clinic_id})

        return render(request, self.temp, {'form': form})

    def post(self, request, examination_id):
        try:
            requested_object = Examination.objects.get(pk=examination_id)
        except ObjectDoesNotExist:
            messages.error(request, "EDYCJA NIEUDANA - NIE ZNALEZIONO BADANIA")
            return redirect('s_ops')
        form = self.form_class(user=request.user, data=request.POST, instance=requested_object)
        if form.is_valid():
            form.save()
            messages.success(request, "EDYCJA UDANA")
            return redirect('e_ops')
        messages.error(request, "EDYCJA NIEUDANA")
        return redirect('e_ops')


class ExaminationDelete(LoginRequiredMixin, View):
    temp = 'operations.html'
    form_class = ExaminationForm

    def get(self, request, examination_id):
        try:
            requested_object = Examination.objects.get(pk=examination_id)
        except ObjectDoesNotExist:
            messages.error(request, "USUWANIE NIUDANE - NIE ZNALEZIONO BADANIA")
            return redirect('e_ops')
        form = self.form_class(user=request.user, initial={'name': requested_object.name,
                                                           'date': requested_object.date,
                                                           'signer': requested_object.signer_id,
                                                           'clinic': requested_object.clinic_id})
        return render(request, self.temp, {'form': form})

    def post(self, request, examination_id):
        try:
            requested_object = Examination.objects.get(pk=examination_id)
        except ObjectDoesNotExist:
            messages.error(request, "USUWANIE NIEUDANE - NIE ZNALEZIONO BADANIA")
            return redirect('s_ops')
        requested_object.delete()
        messages.success(request, "USUWANIE UDANE.")
        return redirect('e_ops')


class FileOps(LoginRequiredMixin, View):
    temp = 'operations.html'
    form_class = FileForm

    def get(self, request):
        form = self.form_class(user=request.user)
        data = File.objects.filter(owner=request.user).order_by('-examination__date')
        if data.count() == 0:
            messages.error(request, "LISTA PLIKÓW JEST PUSTA")
        return render(request, self.temp, {'form': form, 'data': data})

    def post(self, request):
        form = self.form_class(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(request, "DODANO PLIK")
            return redirect('f_ops')
        elif ValueError:
            # will fire only on wrong file-type
            messages.error(request, "TYLKO PLIKI PDF !!!")
            return redirect("f_ops")
        messages.error(request, "NIE DODANO PLIKU")
        return render(request, self.temp, {'form': form})


class FileUpdate(LoginRequiredMixin, View):
    temp = 'operations.html'
    form_class = FileForm

    def get(self, request, file_id):
        try:
            requested_object = File.objects.get(pk=file_id)
        except ObjectDoesNotExist:
            messages.error(request, "EDYCJA NIEUDANA - NIE ZNALEZIONO PLIKU")
            return redirect('f_ops')
        form = self.form_class(user=request.user, initial={'file': requested_object.file,
                                                           'examination': requested_object.examination_id})
        return render(request, self.temp, {'form': form})

    def post(self, request, file_id):
        try:
            requested_object = File.objects.get(pk=file_id)
        except ObjectDoesNotExist:
            messages.error(request, "EDYCJA NIEUDANA - NIE ZNALEZIONO PLIKU")
            return redirect('f_ops')
        form = self.form_class(user=request.user, data=request.POST, files=request.FILES, instance=requested_object)

        if form.is_valid():
            form.save()
            messages.success(request, "EDYCJA UDANA")
            return redirect('f_ops')
        elif ValueError:
            # will fire only on wrong file type
            messages.error(request, 'TYLKO PLIKI PDF !!!')
            return redirect('f_ops')
        messages.error(request, "EDYCJA NIEUDANA")
        return redirect('f_ops')


class FileDelete(LoginRequiredMixin, View):
    temp = 'operations.html'
    form_class = FileForm

    def get(self, request, file_id):
        try:
            requested_object = File.objects.get(pk=file_id)
        except ObjectDoesNotExist:
            messages.error(request, "USUWANIE NIEUDANE - NIE ZNALEZIONO PLIKU")
            return redirect('f_ops')
        form = self.form_class(user=request.user, initial={'file': requested_object.file,
                                                           'examination': requested_object.examination_id,
                                                           })
        return render(request, self.temp, {'form': form})

    def post(self, request, file_id):
        try:
            requested_object = File.objects.get(pk=file_id)
        except ObjectDoesNotExist:
            messages.error(request, "USUWANIE NIEUDANE - NIE ZNALEZIONO PLIKU")
            return redirect('f_ops')
        requested_object.delete()
        messages.success(request, "USUWANIE UDANE")
        return redirect('f_ops')


class BokehOps(LoginRequiredMixin, View):
    temp = 'index2.html'

    def get(self, request):
        test_query_contents = File.objects.filter(owner=request.user).count()
        if test_query_contents == 0:
            messages.error(request, "DODAJ PLIKI DO BADAŃ - WYKRES JEST PUSTY")
            return redirect('f_ops')

        query = File.objects.all().filter(owner=request.user).values('file',
                                                                     'owner',
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

        df = pd.DataFrame.from_records(query)

        df['examination__date'] = pd.to_datetime(df['examination__date'])
        df['examination__date'] = df['examination__date']
        df['zeroes'] = 0
        df.reset_index(level=0, inplace=True)
        levels = np.array([-15, 15, -13, 13, -11, 11, -9, 9, -7, 7, -5, 5, -3, 3])
        print(levels)
        level = levels[df['index'] % 14]
        df['level'] = level
        # TODO if examination_name && examination__signer__spec && examination__date are same make level identical
        # TODO so the circle on the plot will be in exacly same spot
        del df['owner']
        df.set_index('examination__date', inplace=True)
        # print(tabulate(df, headers='keys', tablefmt='rst'))
        specialisations_column = df['examination__signer__specialisation']

        source = ColumnDataSource(df)
        psource = ColumnDataSource(df)

        min_date = df.index.get_level_values('examination__date').min()
        max_date = df.index.get_level_values('examination__date').max()

        var_for_uniques = list(specialisations_column.unique())
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

        start = psource.data['examination__date'].min() - pd.Timedelta(days=45)
        stop = psource.data['examination__date'].max() + pd.Timedelta(days=45)

        from MedResults.settings import S3_URL
        mr = S3_URL

        tooltips = """
                <div>
                    <div>
                        <p>
                        <span style="font-size: 12px; font-weight: bold;">@examination__name</span>
                        <p>
                        <span style="font-size: 12px; font-weight: bold;">@examination__date{%d.%m.%Y}</span>
                        <p>
                        <span style="font-size: 12px; font-weight: bold;">@examination__signer__surname</span>,
                        <span style="font-size: 12px; font-weight: bold;">@examination__signer__specialisation</span>
                    </div>
                </div>
                """

        hover_tool = HoverTool(
            tooltips=tooltips,
            formatters={
                'examination__date': 'datetime'}
        )

        tap_callback = CustomJS(args=dict(mr=S3_URL), code="""
            var indices_of_selected_examinations = cb_data.source.selected.indices;
            var operations_div = document.getElementById('operations');
            var get_created_div = document.getElementById('canvas')
            if (get_created_div) {
                get_created_div.remove()
                                 };
            var new_div = document.createElement("div")
            new_div.setAttribute('id', 'canvas')
            operations_div.appendChild(new_div);
            for (let c=0; c < indices_of_selected_examinations.length; c++) {
                var single_index = indices_of_selected_examinations[c];
                var single_file = cb_data.source.data['file'][single_index];
                var new_emb = document.createElement('embed');
                new_div.appendChild(new_emb);
                new_emb.src = mr + 'media/' + single_file;
                new_emb.alt = mr + 'media/' + single_file;
                new_emb.width = "33%";
                new_emb.height = "600px";
                                                                            }; """)

        tap_tool = TapTool(names=['g2'],
                           behavior='select',
                           callback=tap_callback)

        hover_tool.renderers = []
        tap_tool.renderers = []

        tools = [hover_tool, 'wheel_zoom', tap_tool, PanTool(), ResetTool(), 'zoom_in', 'zoom_out']

        p = figure(title="Mrecords",
                   plot_width=1000,
                   plot_height=480,
                   x_axis_type='datetime',
                   y_range=(-19, 19),
                   tools=tools,
                   active_scroll='wheel_zoom')

        p.xaxis[0].formatter = DatetimeTickFormatter(months='%m.%Y', days='%d.%m.%Y')

        p.background_fill_color = "whitesmoke"
        p.background_fill_alpha = 0.9
        p.border_fill_color = "white"
        p.outline_line_width = 5
        p.outline_line_alpha = 0.4
        p.outline_line_color = "green"
        p.xaxis.axis_label_standoff = 30
        p.yaxis.visible = False
        p.xaxis.major_tick_line_width = 4
        p.xaxis.major_tick_line_color = "firebrick"
        p.axis.major_tick_out = 20
        p.axis.minor_tick_out = 8
        p.ygrid.minor_grid_line_color = 'navy'
        p.ygrid.minor_grid_line_alpha = 0.05
        p.xaxis.axis_label_text_font_size = "40px"

        custom_pallete = ["#8A2BE2", "#8B2323", "#98F5FF", "#FF6103", "#00FFFF", "#458B74", "#636363", "#0000FF",
                          "#7FFF00", "#FF7F24", "#DC143C", "#CAFF70", "#9932CC", "#C1FFC1", "#97FFFF", "#00BFFF",
                          "#228B22", "#FFD700", "#8B7D6B", "#8470FF"]

        colors_for_circles = factor_cmap('examination__signer__specialisation',
                                         palette=custom_pallete,
                                         factors=specialisations_column.unique())

        main_time_line = p.line(x=(start, stop),
                                y=(0, 0),
                                color='#57b9f2',
                                line_alpha=0,
                                line_width=1,
                                line_cap='round',
                                line_dash="dashed")

        p.add_layout(Arrow(end=VeeHead(fill_color='#57b9f2'),
                           x_start=start,
                           y_start=0,
                           x_end=stop,
                           y_end=0,
                           line_width=6,
                           line_alpha=0.9,
                           line_color="#57b9f2",
                           line_dash="dotted",
                           ))

        g3 = p.segment(source=psource,
                       x0='examination__date',
                       y0='zeroes',
                       x1='examination__date',
                       y1='level',
                       color="#f2db57",
                       line_width=3,
                       hover_color='red',
                       line_dash="dashed",
                       line_cap='round')

        g1 = p.square(source=psource,
                      x='examination__date',
                      y=0,
                      size=10,
                      color='black',
                      name='g1',
                      hover_color='red',
                      fill_alpha=1)

        g2 = p.circle(source=psource,
                      x='examination__date',
                      y='level',
                      size=15,
                      color=colors_for_circles,
                      name='g2',
                      hover_color='red',
                      fill_alpha=0.6)

        tap_tool.renderers.append(g2)
        hover_tool.renderers.append(g2)

        labs = []

        def compute_text_align(value):
            return 'left' if value > 0 else 'right'

        def compute_x_offset(value):
            return 10 if value > 0 else -10

        for c in range(len(psource.data['level'])):  # len of any column will work; all are equal
            lab = Label(x=psource.data['examination__date'][c],
                        y=psource.data['level'][c],
                        text=psource.data['examination__name'][c],
                        x_offset=compute_x_offset(psource.data['level'][c]),
                        y_offset=-8,
                        level='glyph', angle=360, angle_units='deg', text_font_size='8pt',
                        text_align=compute_text_align(psource.data['level'][c]))
            labs.append(lab)

        for lab in labs:
            p.add_layout(lab)

        callback = CustomJS(args=dict(source=source,
                                      psource=psource,
                                      ds=datepicker_s,
                                      de=datepicker_e,
                                      checkboxes=checkboxes,
                                      labs=labs), code="""
         var source = source.data
         var partsource = psource.data
         var smin = new Date(ds.value)
         var smax = new Date(de.value)
         var labs = labs;
         var new_labs = [];
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
         partsource['examination__date'] = new Float64Array(float);
         psource.change.emit();
         for (c = 0; c < labs.length; c++) {
            if (!new_labs.includes(labs[c]))   {
                labs[c].visible = false;
                                               }
            else if (new_labs.includes(labs[c]))   {
                labs[c].visible = true; 
                                             }
                                           }
         if (cb_obj.title === "Wyszukiwanie po nazwie:") {
            var v = cb_obj.value;
            var re = new RegExp(v);
            var en = psource.data['examination__name']

                        //
            for (let x = 0; x < en.length; x++) {
                if (en[x].toLowerCase().match(re)) {
                    new_labs[x].text_color = 'blue';
                                                }  };
            if (v.length == 0) {
                for (let x = 0; x < en.length; x++) {
                    new_labs[x].text_color = "#444444";
                                                    }        
                               };                        }""")

        text_input = TextInput(title="Wyszukiwanie po nazwie:",
                               placeholder="wpisz nazwę badania",
                               callback=callback)

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

        // delete displayed docs after tap-tool usage:
        var catch_canvas = document.getElementById('canvas');
        if (catch_canvas) {
        catch_canvas.remove();
        }
        // 
        var min_date = min_date
        var s_value = datepicker_s.value

        var min_date_new = new Date(min_date);
        var max_date_new = new Date(max_date);

        var date_string = min_date_new.toDateString();
        var locale_string = min_date_new.toLocaleDateString("pl-PL");

        // reset labels after text_input search usage        
        var l = labs;
        var text_input = text_input;
        var en = psource.data['examination__name']
        text_input.value = null;
        for (let x = 0; x < en.length; x++) {
                l[x].text_color = "#444444";
                l[x].text_font_size = "8pt";
                l[x].text_font_style = "normal";
                                    };
        //

        // reset checkboxes to default of all selected
        var labels = checkboxes.labels
        var labels_holder = []
        for (let a = 0; a < labels.length; a++) {
            labels_holder.push(a)
        }
        checkboxes.active = labels_holder;
        //

        // control datepicker and its influence on partsource dates - is not 100% functional; fix/workaround required
        datepicker_s.value = min_date;
        datepicker_e.value = max_date;                
        //

        // other bits
        // var get_c_i = document.querySelectorAll('input.bk-widget-form-input')
        // var get_c_i1 = document.querySelector('input.bk-widget-form-input')


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

        controls = WidgetBox(checkboxes, datepicker_s, datepicker_e, text_input)
        layout = row(p, controls)
        tab = Panel(child=layout, title='records')
        tabs = Tabs(tabs=[tab])
        curdoc().add_root(tabs)
        script, div = components(tabs)
        return render(request, self.temp, locals())
