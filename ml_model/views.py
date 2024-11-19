import json
import os
from re import S
from django.shortcuts import redirect, render,get_object_or_404
from django.core.paginator import Paginator

# Create your views here.

# views.py
from flask import request
import pandas as pd
import joblib
from django.http import HttpResponse, JsonResponse
from django.db.models import F
from datetime import datetime, timedelta

from ml_model.utils.data_import import *
from ml_model.utils.data_process import *



from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from ml_model.utils.data_import import *

import random
import string



from .forms import PredictedScheduleForm, ScheduleForm


from .forms import ItemForm
from django.core.mail import send_mail
from django.conf import settings
import plotly.express as px
import plotly.io as pio




# Load the model (assumes it's saved in the same directory)
model = joblib.load('ml_model/model.pkl')

# - Time(B>D)(CGP)
# - Vessel
# - Voyage
# - Wk/ ETB CGP


def home(request):
    return HttpResponse('Hello World')


# def predict(request):
#     week = request.GET.get('week')
#     vessel = request.GET.get('vessel')
#     voyage = request.GET.get('voyage')
#     time_cgp = request.GET.get('time_cgp')

#     # Log the received inputs
#     print(f"Received inputs: week={week}, vessel={vessel}, voyage={voyage}, time_cgp={time_cgp}")

#     # Convert inputs to the appropriate types
#     try:
#         week = float(week)
#         vessel = float(vessel)
#         voyage = float(voyage)
#         time_cgp = float(time_cgp)
#     except ValueError:
#         return JsonResponse({'error': 'Invalid input types'}, status=400)

#     # Create a DataFrame with feature names (as used in training)
#     input_data = pd.DataFrame({
#         'Wk/ ETB CGP': [week],
#         'Vessel': [vessel],
#         'Voyage': [voyage],
#         'Time(B>D)(CGP)': [time_cgp]
#     })

#     # Make predictions using the DataFrame
#     prediction = model.predict(input_data)
#     return JsonResponse({'prediction': prediction[0]})





@csrf_exempt
def predict_etb(request):
    if request.method == 'POST':
        # Get form inputs
        week = request.POST.get('week')
        vessel = request.POST.get('vessel')
        voyage = request.POST.get('voyage')
        etb_cgp = request.POST.get('etb_cgp')
        etd_cgp = request.POST.get('etd_cgp')

        # Convert inputs to appropriate types
        try:
            week = int(week)
            etb_cgp_date = datetime.strptime(etb_cgp, '%Y-%m-%d')
            etd_cgp_date = datetime.strptime(etd_cgp, '%Y-%m-%d')

            # Calculate the difference in days between ETD(CGP) and ETB(CGP)
            day_difference = (etd_cgp_date - etb_cgp_date).days
            print(f'etb_cgp_date : {etb_cgp_date}')
            print(f'etd_cgp_date : {etd_cgp_date}')
            print(f'day_difference : {day_difference}')
        except ValueError:
            return render(request, 'ml_model/predict_form.html', {'error': 'Invalid input types'})

        # Create a DataFrame for the model prediction
        input_data = pd.DataFrame({
            'Wk/ ETB CGP': [week],
            'Vessel': [vessel],
            'Voyage': [voyage],
            'Time(B>D)(CGP)': [day_difference]
        })

        # Make the prediction (this assumes the model is already loaded)
        model_output = model.predict(input_data)

        # Convert model output to an integer (days to add to ETD(CGP))
        predicted_days = int(model_output[0])
        print(f'Predicted days : {predicted_days}')

        # Add the predicted days to ETD(CGP) to calculate ETB(CMB)
        etb_cmb_date = etd_cgp_date + timedelta(days=predicted_days)
        print(f'Predicted date : {etb_cmb_date}')

        # Render the result
        return render(request, 'ml_model/predict_form.html', {
            'etb_cmb': etb_cmb_date.strftime('%Y-%m-%d'),
            'week': week,
            'vessel': vessel,
            'voyage': voyage,
            'etb_cgp': etb_cgp,
            'etd_cgp': etd_cgp,
        })

    # If no POST request, render the empty form
    return render(request, 'ml_model/predict_form.html')



# def cce_table(request):
#     #print the values sent from the form
#     if request.method == 'POST':
#         df = load_data()
#         df = remove_duplicate_vessels(df)
#         data_json = request.POST.get('vessel_names')
#         vessel_names = json.loads(data_json)
#         samples = generate_samples(df,vessel_names) 
#         print(f'vessel_names : {samples}')
#         return render(request, 'ml_model/cce_table.html', {'samples': samples})

        
        
    
#     return render(request, 'ml_model/cce_table.html')



@csrf_exempt
def cce_table(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        vessel_names = data.get('vessel_names', [])
        generate_samples(vessel_names)

        samples = list(Predicted_Schedule.objects.filter(vessel__in=vessel_names).values())
        
        # Return data as JSON for frontend to handle
        return JsonResponse({'samples': samples}, safe=False)
    
    # If GET request, just render the template without any data
    return render(request, 'ml_model/cce_table.html')





def search(request):


    # Generate a list of random words from a to z
    

    
    if request.method == 'POST':

        random_words = ['dune', 'matrix', 'inception', 'avatar', 'titanic', 'gladiator', 'godfather', 'rocky', 'jaws']
       
       

        query = json.loads(request.body)

        # Filter out empty queries or queries that consist only of spaces
        if not query.strip():
            return JsonResponse({'filtered_words': []})
        
        print(f'query:{query}')
            # Filter random words that start with the query
        filtered_words = [word for word in random_words if word.startswith(query)]
        print(filtered_words)
        return JsonResponse({'filtered_words': filtered_words})
        

    return render(request, 'ml_model/search.html')





def edit_record(request, pk):
    record = get_object_or_404(Predicted_Schedule, pk=pk)
    print(record)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        print('data :', data)
        form = PredictedScheduleForm(data, instance=record)
        if form.is_valid():
            form.save()
            print('working')
            return JsonResponse({'success': True})
        else:
            print('Form errors:', form.errors)
            return JsonResponse({'success': False, 'error': 'Invalid form data', 'errors': form.errors})
    
    print('not working')
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def delete_record(request, pk):
    record = get_object_or_404(Predicted_Schedule, pk=pk)
    if request.method == 'POST':
        record.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Delete failed'})

    

def item_list(request):
    items = Item.objects.all()
    return render(request, 'ml_model/item_list.html', {'items': items})

def update_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    print('Item :', item)
    if request.method == 'POST':
        print('POST :', request.POST)
        form = ItemForm(request.POST, instance=item)

        if form.is_valid():
            print('working')
            form.save()
            return JsonResponse({'success': True})
    print('not working')
    return JsonResponse({'success': False, 'error': 'Invalid form data'})

def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Delete failed'})




def line_chart_view(request):
    # Sample data
    data = {
        'x': ['A', 'B', 'C', 'D'],
        'y': [10, 15, 7, 20]
    }
    
    # Create a Plotly figure
    fig = px.line(x=data['x'], y=data['y'], title='Sample Line Chart', labels={'x':'Categories', 'y':'Values'})
    
    # Convert the figure to HTML
    graph_html = pio.to_html(fig, full_html=False)
    
    # Pass the graph HTML to the template
    return render(request, 'ml_model/line_chart.html', {'graph_html': graph_html})



def histogram_view(request):
    # Retrieve data from the Analytics model
    analytics_data = Analytics.objects.all().values()
    
    # Convert the QuerySet to a DataFrame
    df = pd.DataFrame(analytics_data)
    
    # Check if the DataFrame is not empty and has the required column
    if not df.empty and 'diff_cgp_cmb' in df.columns:
        # Create a count plot for the numeric column
        fig = px.histogram(df, x='diff_cgp_cmb', title='Count Plot', labels={'diff_cgp_cmb': 'Days Taken to Arrive at CMB from CGP', 'count': 'Days'})
        
        # Convert the figure to HTML
        graph_html = pio.to_html(fig, full_html=False)
        
        # Pass the graph HTML to the template
        return render(request, 'ml_model/histogram.html', {'graph_html': graph_html})
    else:
        return HttpResponse('No data available or column not found')


def pie_chart_view(request):
    # Retrieve data from the Analytics model
    analytics_data = Analytics.objects.all().values()
    
    # Convert the QuerySet to a DataFrame
    df = pd.DataFrame(analytics_data)
    
    # Check if the DataFrame is not empty and has the required column
    if not df.empty and 'diff_cgp_cmb' in df.columns:
        # Create a pie chart for the numeric column
        fig = px.pie(df, names='diff_cgp_cmb', title='Pie Chart of Days Taken to Arrive at CMB from CGP')
        
        # Convert the figure to HTML
        graph_html = pio.to_html(fig, full_html=False)
        
        # Pass the graph HTML to the template
        return render(request, 'ml_model/piechart.html', {'graph_html': graph_html})
    else:
        return HttpResponse('No data available or column not found')


# @csrf_exempt
# def combined_view(request):
#     if request.method == 'GET':
#         return chart_view(request)
#     elif request.method == 'POST':
#         return send_choice(request)
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method'})



def chart_view(request):
    # Data for the charts (replace with your actual data)
    unique_vessels = list(Schedule.objects.values_list('vessel', flat=True).distinct())
    analytics_data = Analytics.objects.all().values()
    df = pd.DataFrame(analytics_data)
    # Create a pie chart using Plotly
    if request.method == 'POST':
        data = json.loads(request.body)
        vessel = data.get('vessel')
        print(vessel)
        if vessel:
            samples = list(Analytics.objects.filter(vessel=vessel).values())
            df = pd.DataFrame(samples)
            print(df.head())
            if not df.empty and 'diff_cgp_cmb' in df.columns:
                # Create pie chart and histogram
                pie = px.pie(df, names='diff_cgp_cmb', title='Pie Chart of Days Taken to Arrive at CMB from CGP')
                hist = px.histogram(df, x='diff_cgp_cmb', title='Count Plot', labels={'diff_cgp_cmb': 'Days Taken to Arrive at CMB from CGP', 'Count': 'Days'})

                # Save the plots as images
                static_dir = os.path.join(settings.BASE_DIR, 'static', 'ml_model')
                pie_image_path = os.path.join(static_dir, 'pie_chart.png')
                hist_image_path = os.path.join(static_dir, 'hist_chart.png')

            # Ensure the directory exists
                os.makedirs(static_dir, exist_ok=True)
                pio.write_image(pie, pie_image_path)
                pio.write_image(hist, hist_image_path)

                context = {
                    'pie_chart': pie_image_path,
                    'hist_chart': hist_image_path,
                    'vessels': unique_vessels,
                    'selected_vessel': vessel
                }
                print('Im sending the context from the POST request')
                return JsonResponse(context)
            else:
                return HttpResponse('No data available or column not found')
    else:

        if not df.empty and 'diff_cgp_cmb' in df.columns:
            
            hist = px.histogram(df, x='diff_cgp_cmb', title='Count Plot', 
                        labels={'diff_cgp_cmb': 'Days Taken to Arrive at CMB from CGP', 'Count': 'Days'}
                        )
            pie = px.pie(df, names='diff_cgp_cmb', title='Pie Chart of Days Taken to Arrive at CMB from CGP')
            
            # Convert the figure to HTML
            hist_html = pio.to_html(hist, full_html=False)
            
            # Convert the figure to HTML
            pie_html = pio.to_html(pie, full_html=False)
        
            context = {
                'pie_chart': pie_html,
                'hist_chart': hist_html,
                'vessels': unique_vessels
            }
            print('Im sending the context from the GET request')
            return render(request, 'ml_model/analytics.html', context)

        else:
            return HttpResponse('No data available or column not found')



def card_list(request):

    cards = Schedule.objects.all()
    paginator = Paginator(cards, 12)  # Show 6 cards per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ml_model/page.html', {'page_obj': page_obj})


def page_view(request):
    services = Schedule.objects.values_list('service', flat=True).distinct()
    selected_services = request.GET.getlist('service')

    if selected_services:
        cards = Schedule.objects.filter(service__in=selected_services)
    else:
        cards = Schedule.objects.all()

    paginator = Paginator(cards, 6)  # Show 9 cards per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'services': services,
        'selected_services': selected_services,
    }
    return render(request, 'ml_model/page_filter.html', context)


@csrf_exempt
def add_vessels(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vessels = data.get('vessels', [])

        for vessel_data in vessels:
            name = vessel_data.get('name')
            service = vessel_data.get('service')
            if name and service:
                Vessel.objects.get_or_create(name=name, service=service)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def remove_vessel(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vessel_name = data.get('vessel_name')
        if vessel_name:
            try:

                vessel = Vessel.objects.get(name=vessel_name)
                if vessel.service == 'CCE':
                    del_cce_by_vessel_name(vessel)
                elif vessel.service == 'BES':
                    del_bes_by_vessel_name(vessel)
                else:
                    print('No service found')
                vessel.delete()
                return JsonResponse({'success': True})
            except Vessel.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Vessel not found'})





@csrf_exempt
def update_vessel_service(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vessel_name = data.get('name')
        new_service = data.get('service')
        previous_service = data.get('previous_service')

        if vessel_name and new_service and previous_service:
            try:
                vessel = Vessel.objects.get(name=vessel_name)
                vessel.service = new_service
                vessel.previous_service = previous_service
                vessel.save()
                if new_service  == 'CCE' and previous_service == 'BES':
                    first_query = (
                                    BES.objects
                                    .annotate(vessel_no_space=Lower(Replace(F('vessel'), Value(' '), Value(''))))
                                    .filter(vessel_no_space=vessel_name.replace(" ", "").lower(), voyage_complete=0)
                                    .first()
                                )
                    if first_query:
                        bes_to_cce(first_query)
                        del_bes(first_query)
                        generate_cce_partial(first_query)
                elif new_service  == 'BES' and previous_service == 'CCE':
                    first_query = (
                                    Schedule.objects
                                    .annotate(vessel_no_space=Lower(Replace(F('vessel'), Value(' '), Value(''))))
                                    .filter(vessel_no_space=vessel_name.replace(" ", "").lower(), voyage_complete=0)
                                    .first()
                                )
                    if first_query:
                        cce_to_bes(first_query)
                        del_cce(first_query)
                        generate_bes_partial(first_query)
                else:
                    print('No service change')

                   
                return JsonResponse({'success': True})
            except Vessel.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Vessel not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def show_cce_vessel(request):
    
    try:
        cce_vessels = Vessel.objects.filter(service='CCE').values_list('name', flat=True)
        return JsonResponse({'vessels': list(cce_vessels)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def show_bes_vessel(request):
    
    try:
        bes_vessels = Vessel.objects.filter(service='BES').values_list('name', flat=True)
        return JsonResponse({'vessels': list(bes_vessels)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def cce_rv(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        eta_to_etb_cgp = data.get('eta_to_etb_cgp', 1)
        etb_to_etd_cgp = data.get('etb_to_etd_cgp', 2)
        cgp_to_cmb = data.get('cgp_to_cmb', 5)
        eta_to_etb_cmb = data.get('eta_to_etb_cmb', 1)
        etb_to_etd_cmb = data.get('etb_to_etd_cmb', 2)
        cmb_to_cgp = data.get('cmb_to_cgp', 5)
        if eta_to_etb_cgp and etb_to_etd_cgp and cgp_to_cmb and eta_to_etb_cmb and etb_to_etd_cmb and cmb_to_cgp:
            CCE_RV.objects.all().delete()
            CCE_RV.objects.create(
                eta_to_etb_cgp=eta_to_etb_cgp,
                etb_to_etd_cgp=etb_to_etd_cgp,
                cgp_to_cmb=cgp_to_cmb,
                eta_to_etb_cmb=eta_to_etb_cmb,
                etb_to_etd_cmb=etb_to_etd_cmb,
                cmb_to_cgp=cmb_to_cgp
            )
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid data'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})    


@csrf_exempt
def bes_rv(request):
    if request.method == 'POST' :
        data = json.loads(request.body)
        eta_to_etb_cgp = data.get('eta_to_etb_cgp', 1)
        etb_to_etd_cgp = data.get('etb_to_etd_cgp', 2)
        cgp_to_sin = data.get('cgp_to_sin', 5)  
        eta_to_etb_sin = data.get('eta_to_etb_sin', 1)
        etb_to_etd_sin = data.get('etb_to_etd_sin', 2)
        sin_to_pkg = data.get('sin_to_pkg', 5)
        eta_to_etb_pkg = data.get('eta_to_etb_pkg', 1)
        etb_to_etd_pkg = data.get('etb_to_etd_pkg', 2)
        pkg_to_cgp = data.get('pkg_to_cgp', 5)
        if eta_to_etb_cgp and etb_to_etd_cgp and cgp_to_sin and eta_to_etb_sin and etb_to_etd_sin and sin_to_pkg and eta_to_etb_pkg and etb_to_etd_pkg and pkg_to_cgp:
            BES_RV.objects.all().delete()
            BES_RV.objects.create(
                eta_to_etb_cgp=eta_to_etb_cgp,
                etb_to_etd_cgp=etb_to_etd_cgp,
                cgp_to_sin=cgp_to_sin,
                eta_to_etb_sin=eta_to_etb_sin,
                etb_to_etd_sin=etb_to_etd_sin,
                sin_to_pkg=sin_to_pkg,
                eta_to_etb_pkg=eta_to_etb_pkg,
                etb_to_etd_pkg=etb_to_etd_pkg,
                pkg_to_cgp=pkg_to_cgp
            )
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid data'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def db_reset(request):

    Schedule.objects.all().delete()
    BES.objects.all().delete()
    cce_to_database()
    bes_to_database()
    return JsonResponse({'success': True})


@csrf_exempt
def generate_table_n_months(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        service = data.get('service')
        months = data.get('months')
        generate_schedule(service, months)
        return JsonResponse({'success': True})


@csrf_exempt
def set_voyage_complete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        model_name = data.get('model_name')
        month = data.get('month')
        year = data.get('year')
        set_voyage_complete_before(model_name, month, year)
        return JsonResponse({'success': True})


def show_schedule(request):
    schedules = list(Schedule.objects.all().order_by('eta_cgp').values())
    return JsonResponse({'schedules': schedules}, safe=False)


def show_bes(request):
    bes = list(BES.objects.all().order_by('eta_cgp').values())
    return JsonResponse({'bes': bes}, safe=False)
        


    





   










