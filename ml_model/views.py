import json
from django.shortcuts import redirect, render,get_object_or_404

# Create your views here.

# views.py
import pandas as pd
import joblib
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta

from .utils.data_loader import *

from .utils.data_process import *

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from .models import Vessel ,Schedule
import random
import string

from .models import Predicted_Schedule

from .forms import PredictedScheduleForm, ScheduleForm

from .models import Item
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


def add_vessel(request):
    if request.method == 'POST':
        # Get data from the POST request
        name = request.POST.get('name')
        code = request.POST.get('code')

        # Create a new Vessel object and save it to the database
        new_vessel = Vessel(name=name, code=code)
        new_vessel.save()

        # Return a response or render a template after saving
        return render(request, 'ml_model/add_vessel.html', {'vessel': new_vessel})

    return render(request, 'ml_model/add_vessel.html')


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
    







