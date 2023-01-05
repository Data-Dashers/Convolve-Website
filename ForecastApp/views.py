from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
from django.shortcuts import render
import os
import pandas as pd


def home(request):
    context = {"productIDs": [id[5:-4] for id in os.listdir("./static/data/datasets/")]}

    return render(request, "base.html", {"context": context})


@api_view(["POST"])
def get_preds(request):
    print(request.data)
    product_id = request.data.get("product_id")
    date = request.data.get("date")
    print(product_id, date)
    dataset = pd.read_csv("./static/data/predictions.csv")
    dataset["Dates"] = pd.to_datetime(dataset["Dates"], format="%d-%m-%Y")
    # print(dataset)
    old_dataset = pd.read_csv(f"./static/data/datasets/PLID_{product_id}.csv")
    print(old_dataset.columns)
    old_dataset["Booking_Date"] = pd.to_datetime(
        old_dataset["Booking_Date"], format="%d-%m-%Y"
    )

    date = pd.to_datetime(str(date), format="%Y-%m-%d")
    print(date)

    predictions = dataset[dataset["PLID"] == product_id]
    predictions = predictions[
        predictions["Dates"].between(left=predictions.Dates.min(), right=date)
    ]

    predictions.sort_values("Dates", inplace=True)
    old_dataset.sort_values("Booking_Date", inplace=True)

    print("Reached")

    predictions.Dates = predictions.Dates.astype("str")
    old_dataset.Booking_Date = old_dataset.Booking_Date.astype("str")
    old_preds = list(old_dataset.Booked_Qty.values)
    preds = [None for i in range(len(list(old_dataset.Booked_Qty.values)))] + list(
        predictions.predictions_final.values
    )
    preds[len(old_preds) - 1] = old_preds[len(old_preds) - 1]
    old_preds = [int(i) for i in old_preds]
    preds = [int(i) if i else i for i in preds]

    data = {
        "dates": list(old_dataset.Booking_Date.values) + list(predictions.Dates.values),
        "preds": preds,
        "old_preds": old_preds,
    }
    print(data["dates"])
    return Response(data)
