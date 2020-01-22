# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from monitor.settings import HBP_MY_USER_URL as USER_URL
from monitor.utils.hpc import HPC_SYSTEMS
from monitor.models import *

import requests
import json


def index(request):
    data = {"hpc": json.dumps(HPC_SYSTEMS)}
    return render(request, 'monitor/monitor.html', data)


def get_status(request):
    if request.method == 'GET':
        content = {'bsp-hpc-monitor-status': 1}
        return HttpResponse(json.dumps(content), content_type='application/json')


def get_user(request):
    headers = {
        'Authorization': request.META['HTTP_AUTHORIZATION'],
        'Content-Type': 'application/json'
    }
    r = requests.get(url=USER_URL, headers=headers)
    if r.status_code == 200:
        user = r.json()
        institution = ''
        email = ''
        if len(user['institutions']) >= 1:
            institutions = user['institutions']
            for i in institutions:
                if i['primary']:
                    institution = i['name']
        if len(user['emails']) >= 1:
            emails = user['emails']
            for e in emails:
                if e['primary']:
                    email = e['value']
        new_user = User(
            id=int(user['id']),
            username=user['username'],
            first_name=user['givenName'],
            last_name=user['familyName'],
            institution=institution,
            email=email
        )
        new_user.save()
        Visit(user=new_user).save()
    response = HttpResponse()
    response.status_code = r.status_code
    response.content = r.content
    return response


def get_hpc_info(request):
    url = ''
    headers = {
        'Authorization': request.META['HTTP_AUTHORIZATION'],
        'Content-Type': 'application/json'
    }
    if 'HTTP_X_UNICORE_USER_PREFERENCES' in request.META:
        headers['HTTP_X_UNICORE_USER_PREFERENCES'] = request.META['HTTP_X_UNICORE_USER_PREFERENCES']

    if request.path == '/pizdaint':
        url = 'https://brissago.cscs.ch:8080/DAINT-CSCS/rest/core'
    elif request.path == '/pizdaint/projects':
        url = 'https://brissago.cscs.ch:8080/DAINT-CSCS/rest/core/factories/default_target_system_factory'
    r = requests.get(url=url, headers=headers, verify=False)
    return HttpResponse(status=r.status_code, content=r.content)


def check_job_submission(request):
    hpc = None
    if request.path == '/pizdaint/check':
        hpc = HPC_SYSTEMS['1']
   
    job = hpc['job']['on_system']
    headers = {
            'Authorization': request.META['HTTP_AUTHORIZATION'],
            'Content-Type': 'application/json'
    }

    r = requests.post(url=hpc['submit_url'], headers=headers, data=job, verify=False)
    return HttpResponse(status=r.status_code, content=r.content)
