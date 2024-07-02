from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from . import heat_gain as hg
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import JSONParser
import io
import json


@login_required(login_url="/login")
@csrf_exempt
def HeatCalculation(request):
    if request.method == 'POST':
        if request.user.calc_access:
            rights_list = [ 'walls', 'windows', 'roof', 'occupants', 'equipments'] 
            access = request.user.calc_access
            allowed_sources = []

            for right in rights_list:
                if access.__getattribute__(right):
                    allowed_sources.append(right)

            if not len(allowed_sources):
                response = {
                    'success': False,
                    'message' : 'You are not allowed to access calculator'
                }
                return HttpResponse(json.dumps(response), content_type='application/json')

            else:
                stream = io.BytesIO(request.body)               
                data = JSONParser().parse(stream)
                # heat_load = hg.TotalHeatLoad(data)
                heat_load = hg.PermissionedTotalHeatLoad(data, allowed_sources)

                response = heat_load.get_result()
                return HttpResponse(json.dumps(response), content_type='application/json')