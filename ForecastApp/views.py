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
    # print(request.data)
    product_id = request.data.get('product_id')
    date = request.data.get('date')
    # print(product_id, date)
    dataset = pd.read_csv("./static/data/predictions_1.csv")
    dataset["Dates"] = pd.to_datetime(dataset["Dates"], format="%d-%m-%Y")
    # print(dataset)
    old_dataset = pd.read_csv(f"./static/data/datasets/PLID_{product_id}.csv")
    # print(old_dataset.columns)
    old_dataset['Booking_Date'] = pd.to_datetime(old_dataset["Booking_Date"], format="%d-%m-%Y")

    train_data = pd.read_csv(f"./static/data/train_with_size.csv")
    train_data = train_data[train_data.PLID==product_id]

    date = pd.to_datetime(str(date), format="%Y-%m-%d")
    # print(date)

    predictions = dataset[dataset["PLID"]==product_id]
    predictions = predictions[predictions["Dates"].between(left=predictions.Dates.min(), right=date)]
    
    predictions.sort_values("Dates", inplace=True)
    old_dataset.sort_values("Booking_Date", inplace=True)



    # print("Reached")

    predictions.Dates = predictions.Dates.astype("str")
    old_dataset.Booking_Date = old_dataset.Booking_Date.astype("str")

    sizes = dict()

    for i in old_dataset.Booking_Date.values:
      # print(train_data[train_data.Booking_Date==i]["Size"].values[0])
      sizes[f"{i}"] = train_data[train_data.Booking_Date==i]["Size"].values[0]
    for i in predictions.Dates.values:
      sizes[f"{i}"] = predictions[predictions.Dates==i]["test_size"].values[0]
    data = {
        "dates":list(old_dataset.Booking_Date.values)+list(predictions.Dates.values),
        "preds":[0 for i in list(old_dataset.Booked_Qty.values)]+list(predictions.predictions_final.values),
        "old_preds":list(old_dataset.Booked_Qty.values),
        "sizes":sizes
        
    }
    return Response(data)

