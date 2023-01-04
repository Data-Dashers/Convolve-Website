from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
from django.shortcuts import render
import os
import pandas as pd

def home(request):
  context = {
    "productIDs" : [id[5:-4] for id in os.listdir('./static/data/datasets/')]
  }

  return render(request, 'base.html', {"context":context})

@api_view(['POST'])
def get_preds(request):
    print(request.data)
    product_id = request.data.get('product_id')
    date = request.data.get('date')
    print(product_id, date)
    dataset = pd.read_csv("./static/data/predictions.csv")
    dataset["Dates"] = pd.to_datetime(dataset["Dates"], format="%d-%m-%Y")
    # print(dataset)
    date = pd.to_datetime(str(date), format="%Y-%m-%d")
    print(date)
    predictions = dataset[dataset["PLID"]==product_id]
    predictions = predictions[predictions["Dates"].between(left=predictions.Dates.min(), right=date)]
    
    predictions.sort_values("Dates", inplace=True)
    predictions.Dates = predictions.Dates.astype("str")
    data = {
        "dates":list(predictions.Dates.values),
        "preds":list(predictions.predictions_final.values)
    }
    return Response(data)

