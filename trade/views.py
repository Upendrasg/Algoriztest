from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Stock
import trade.Trend as pnlalgo
import requests
import json
from django.shortcuts import redirect
from django.contrib import messages


def index(request):
    if request.POST:
        url = 'https://api.iextrading.com/1.0/stock/' + request.POST.get('ticker') + '/chart/1y'
        response = requests.get(url)
        try:
            result = json.loads(response.content.decode())
            prices = []
            for res in result:
                prices.append(res.get('close'))
            [positions, pnl] = pnlalgo.algo_result(request.POST.get('signal'), request.POST.get('trade'), prices)
            Stock.objects.create(name=request.POST.get('algo'), pnl=pnl, position=positions)
            messages.success(request, 'Form submission successful!')
        except:
            messages.success(request, 'Not a valid input!')
        return redirect('index')
    else:
        return render(request, 'index.html')


def table(request):
    algos = Stock.objects.all()
    outputs = []
    for algo in algos:
        pnl = json.loads(algo.pnl)
        avg = sum(pnl) / len(pnl)
        outputs.append({'name': algo.name, 'avg': avg, 'id': algo.id})
    template = loader.get_template('table.html')
    return HttpResponse(template.render({'algos': outputs}, request))


def chart(request, dataId):
    template = loader.get_template('chart.html')
    data = Stock.objects.get(id=dataId)
    return HttpResponse(template.render({'PNL': data.pnl, 'position': data.position}, request))
