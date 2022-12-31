from django.shortcuts import render


def root(request):
  context = {
    "productIDs" : ["id1", "id2", "id3", "id4", "id5", "id6"]
  }
  return render(request, 'templates/base.html', {"context":context})
