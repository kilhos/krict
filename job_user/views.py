import datetime, io, json, threading, csv, requests, os
from _ast import expr
from time import sleep
import pandas as pd
# import pymysql
# smiles input result
import numpy as np
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# job pagination
from django.core.paginator import Paginator
# django ORM or Import
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from rdkit.Chem import AllChem
from rdkit.Chem.rdDepictor import Compute2DCoords, GenerateDepictionMatching2DStructure
from reportlab.pdfbase.ttfonts import TTFont
# report Import
from reportlab.pdfgen import canvas
from django.db.models import Q
from sympy import primenu
from sympy.printing.codeprinter import requires

from accounts.models import User
from .calculate_property import prediction
from .generate_molecule_image import fn_generate_mocule_image
from .models import *
from job_user.include_views import fn_chemtrans_report
from django.contrib.auth import update_session_auth_hash
from wsgiref.util import FileWrapper
from rdkit import Chem
import matplotlib.pyplot as plt
from accounts.forms import PasswordChangeForm
from urllib import parse


# from background_task import background


def main_page(request):
    return render(request, '../templates/job_user/index.html')


def siteMap(request):
    return render(request, 'job_user/siteMap.html')


def contactUs(request):
    return render(request, 'job_user/../job_manager/templates/job_manager/contactUs.html')


def privacyPolicy(request):
    return render(request, 'job_user/privacyPolicy.html')


def job_status_running_change_to_completed(request):
    status_running_list = list(Job.objects.all().filter(job_status='running').values('id'))
    for i, temp in enumerate(status_running_list):
        temp.values()
        print(temp.values())

    job = Job()

    return redirect('job_user:job_list')


class JobListView(LoginRequiredMixin, ListView):
    template_name = 'job_user/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        job_list = Job.objects.filter(Q(user=self.request.user)).order_by('-create_date')
        if self.request.GET.get('search_text'):
            if self.request.GET.get('search_select') == 'job_name':
                job_list = Job.objects.filter(Q(user=self.request.user) & Q(job_name__icontains=self.request.GET.get('search_text', ''))).order_by('-create_date')
            elif self.request.GET.get('search_select') == 'module':
                job_list = Job.objects.filter(Q(user=self.request.user) & Q(module_api__module__module_name__icontains=self.request.GET.get('search_text', ''))).order_by('-create_date')
            elif self.request.GET.get('search_select') == 'smiles':
                job_list = Job.objects.filter(Q(user=self.request.user) & Q(smiles__icontains=self.request.GET.get('search_text', ''))).order_by('-create_date')
        return job_list

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context


job_list = JobListView.as_view()


class JobDetailView(LoginRequiredMixin, DetailView):
    template_name = "job_user/job_detail.html"
    context_object_name = 'job'
    model = Job


job_detail_page = JobDetailView.as_view()


@login_required
def job_register_page(request):
    if request.POST.get('module_api_pk') is not None:
        print(request.POST['module_api_name'])
        print(request.POST['module_api_pk'])
        print(request.POST['module_name'])
        choose_module_id = Module.objects.get(id=request.POST['module_api_pk']).id
        choose_module_api_id = ModuleApi.objects.get(module_api_name=request.POST['module_api_name']).id
        # choose_module_api_name = ModuleApi.objects.get(module_api_name=request.POST['module_api_name']).module_api_name
        print(choose_module_id)
        print(choose_module_api_id)
        module_api_list = ModuleApi.objects.all()
        module_list = Module.objects.all()
        context = {'module_api_list': module_api_list,
                   'module': module_list, 'qs_len': len(module_list), 'module_pk': choose_module_id,
                   'module_api_pk': choose_module_api_id
                   }
        return render(request, 'job_user/job_register.html', context)
    module_api_list = ModuleApi.objects.all()
    module_list = Module.objects.all()
    context = {'module_api_list': module_api_list,
               'module': module_list, 'qs_len': len(module_list)}
    return render(request, 'job_user/job_register.html', context)


@login_required
def job_register(request):
    if request.method == 'POST':
        module = Module.objects.all()
    return render(request, 'job_user/job_register.html', {'module': module})


@login_required
def module_list(request):
    page = request.GET.get('page', 1)
    module_list = Module.objects.order_by('-create_date').all()
    paginator = Paginator(module_list, 10)

    page_obj = paginator.get_page(page)
    return render(request, 'job_user/module_list.html', {'modules': page_obj})


def module_user_search(request):
    page = request.GET.get('page', 1)
    module_list = Module.objects.order_by('create_date').all()
    paginator = Paginator(module_list, 10)

    page_obj = paginator.get_page(page)
    return render(request, 'job_user/module_list.html', {'modules': page_obj})


@login_required
def smiles_input(request):
    return render(request, 'job_user/smiles_input.html')


@login_required
def job_result_page(request, pk):
    result_detail = JobResult.objects.get(job_id=pk)
    job = Job.objects.get(pk=pk)
    smiles = job.smiles
    smiles_detail = prediction(smiles)

    img_path = 'smiles/userpk' + str(job.user_id) + '/jobpk' + str(job.pk) + '.png'

    return render(request, 'job_user/result_detail.html',
                  {'result_detail': result_detail, "smiles_detail": smiles_detail, "img_path": img_path})


class ResultListView(LoginRequiredMixin, ListView):
    template_name = "job_user/job_result.html"
    context_object_name = "result"
    paginate_by = 10

    def get_queryset(self):
        job_Result_list = JobResult.objects.filter(job__user=self.request.user, job__job_status='complete').order_by('-create_date')
        if self.request.GET.get('search_text'):
            if self.request.GET.get('search_select') == 'job_name':
                job_Result_list = JobResult.objects.filter(Q(job__user=self.request.user, job__job_status='complete') & Q(
                    job__job_name__icontains=self.request.GET.get('search_text'))).order_by('-create_date')
            elif self.request.GET.get('search_select') == 'module':
                job_Result_list = JobResult.objects.filter(Q(job__user=self.request.user, job__job_status='complete') & Q(
                    job__module_api__module__module_name__icontains=self.request.GET.get('search_text'))).order_by('-create_date')
            elif self.request.GET.get('search_select') == 'writer':
                job_Result_list = JobResult.objects.filter(Q(job__user=self.request.user, job__job_status='complete') & Q(
                    job__user__name__icontains=self.request.GET.get('search_text'))).order_by('-create_date')
        return job_Result_list

    def get_context_data(self, **kwargs):
        context = super(ResultListView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context


job_result_page_list = ResultListView.as_view()


@login_required()
def profile(request):
    return render(request, 'accounts/profile.html')


@csrf_exempt
@login_required()
def profile_delete(request):
    if request.method == "POST":
        id = request.POST['id']
        user = User.objects.get(pk=id)
        user.state = 'del'
        user.save()
        return redirect('accounts:logout')


@login_required()
def profile_modify(request):
    if request.method == "POST":
        id = request.POST['id']
        username = request.POST['username']
        #password = request.POST['password']
        name = request.POST['name']

        phone_number = request.POST['phoneNumber']
        mobile_phone_number = request.POST['mobilePhoneNumber']
        email = request.POST['email']
        institution = request.POST['institution']
        department = request.POST['department']
        user = User.objects.get(pk=id)
        user.username = username
        #user.password = password
        user.name = name
        user.mobile_phone = mobile_phone_number
        user.company_phone = phone_number
        user.email = email
        user.institution = institution
        user.department = department
        #User.set_password(user, password)
        user.save()
        update_session_auth_hash(request, user)
        return redirect('accounts:profile')
    return render(request, 'job_user/profile_modify.html', )


@login_required()
def user_password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        pk = request.POST['pk']
        target_user = User.objects.get(pk=pk)
        if form.is_valid():
            target_user.password = request.POST['password1']
            target_user.set_password(request.POST['password1'])
            target_user.save()
            return redirect("accounts:profile")
    else:
        form = PasswordChangeForm

    return render(request, 'job_user/user_password_change.html', { 'form': form, })


@login_required
def job_register_page_api(request):
    module_id = request.GET.get('module_id')

    data = ModuleApi.objects.filter(module=module_id)

    data = list(data.values())

    return JsonResponse(data, safe=False)


@login_required
def job_detail_page_api(request, pk):
    module_id = request.GET.get('module_id')

    data = ModuleApi.objects.filter(module=module_id)

    data = list(data.values())

    return JsonResponse(data, safe=False)


#  크론텝
def smiles_result():
    print("run!!!==============================================================================")
    # waiting 선별
    job_results = JobResult.objects.select_related('job').filter(job__job_status='waiting')
    print(job_results)
    # waiting 상태 job start
    for index, job_result in enumerate(job_results):
        # status running
        running_job = Job.objects.get(pk=job_result.job_id)
        running_job.job_status = "running"
        running_job.save()
        # api running
        content = running_job.smiles
        print(running_job.smiles)
        urls = ""
        if running_job.module_api.module_api_cd == 'CD001':
            urls = "http://10.39.149.110:8081/predict_deep_hit?content=" + parse.quote(content)
        elif running_job.module_api.module_api_cd == 'CD002':
            urls = "http://10.39.149.110:8084/predict_bbbp?content=" + parse.quote(content)
        elif running_job.module_api.module_api_cd == 'CD003':
            urls = "http://10.39.149.110:8082/predict_cyp?content=" + parse.quote(content)
        elif running_job.module_api.module_api_cd == 'CD004':
            urls = "http://10.39.149.110:8082/predict_herg?content=" + parse.quote(content)
        elif running_job.module_api.module_api_cd == 'CD005':
            urls = "http://10.39.149.110:8085/predict_ms?content=" + parse.quote(content)
        elif running_job.module_api.module_api_cd == 'CD006':
            urls = "http://10.39.149.110:8083/predict_chemtrans?content=" + parse.quote(content)
        print(urls)
        req = requests.get(urls)
        ## GET HTML SOURCE
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        jsonObject = json.loads(str(soup))

        job_result.result_json = jsonObject
        job_result.save()


def job_thread_run():
    t = threading.Thread(target=smiles_result)
    t.start()


def check_job_result():

    job_results = JobResult.objects.all()

    for job_result in job_results:
        if job_result.result_json['time'] != 'no_data' and job_result.result_json['time'] != 'exception':
            job = Job.objects.get(pk=job_result.job_id)
            job.job_status = 'complete'
            job.save()
        elif job_result.result_json['time'] == 'exception':
            job = Job.objects.get(pk=job_result.job_id)
            job.job_status = 'fail'
            job.save()
        """
        time_data = job_result.result_json['time']
        if time_data == 'exception':
            job.job_status = 'fail'
            job.save()
        elif time_data != 'no_data':
            job = Job.objects.get(pk=job_result.job_id)
            job_result = JobResult.objects.get(job_id=job.pk)
            if job_result.job.module_api.module_api_cd == 'CD001':
                if 'graph' in job_result.result_json \
                        and job_result.result_json['graph'] == False \
                        and job.job_status != 'fail':
                    job.job_status = 'fail'
                    job.save()

            elif job_result.job.module_api.module_api_cd == 'CD002' \
                    and job_result.result_json['BBBP'] == False \
                    and job.job_status != 'fail':
                job.job_status = 'fail'
                job.save()

            elif job_result.job.module_api.module_api_cd == 'CD003' \
                    and (job_result.result_json['CYP1A2'] == False
                         or job_result.result_json['CYP2C19'] == False
                         or job_result.result_json['CYP2C9'] == False
                         or job_result.result_json['CYP2D6'] == False
                         or job_result.result_json['CYP3A4'] == False) \
                    and job.job_status != 'fail':
                job.job_status = 'fail'
                job.save()

            elif job_result.job.module_api.module_api_cd == 'CD004' \
                    and job_result.result_json['hERG_inhibition'] == False \
                    and job.job_status != 'fail':
                job.job_status = 'fail'
                job.save()

            elif job_result.job.module_api.module_api_cd == 'CD005' \
                    and job_result.result_json['Human'] == False \
                    and job.job_status != 'fail':
                job.job_status = 'fail'
                job.save()
        else:
            print('API가 안 돌아간 것?')
        """


@login_required
def job_insert(request):
    job = Job.objects.create(job_name=request.POST['job_name'],
                             job_explanation=request.POST['job_explanation'],
                             smiles=request.POST['smiles'],
                             job_status='waiting',
                             module_api=ModuleApi.objects.get(pk=request.POST['moduleApi']),
                             user=User.objects.get(pk=request.POST['user']))

    ## 좀더 효율적인 방법 찾기 리펙토링 필수
    # exec(open('C:\\euclid_krict\\euclid_krict\\media\\job_user\\module_api\\' + ModuleApi.objects.get(
    #   pk=request.POST['moduleApi']), encoding='UTF8').read())
    fn_generate_mocule_image(job.pk)
    jobRes = JobResult()
    jobRes.job = job
    jobRes.result_json = {'time': 'no_data'}
    jobRes.save()
    print(job.pk)

    return HttpResponse(json.dumps({"pk": job.pk}, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def job_detail_page_modify(request, pk):
    page_res = request.session['page_res']
    page_typeOfString = str(page_res)

    if request.method == 'POST':
        job = Job.objects.get(pk=pk)

        job.job_name = request.POST['job_name']
        job.job_explanation = request.POST['job_explanation']
        job.smiles = request.POST['smiles']
        job.job_start_dt = request.POST['job_start_dt']
        job.module_api = ModuleApi.objects.get(pk=request.POST['moduleApi'])
        job.user = User.objects.get(pk=request.POST['user'])
        job.save()

    return HttpResponseRedirect('/job_list/?page=' + page_typeOfString)


@login_required
def job_detail_page_delete(request, pk):
    Job(pk).delete()
    return render(request, 'job_user/job_list.html')


@login_required
def job_result_report(request, pk):
    job_res_list = JobResult.objects.get(pk=pk)
    job_list = job_res_list.job
    if job_list.module_api.module_api_cd == 'CD006':
        return fn_chemtrans_report(pk)
    else:
        return fn_result_report(pk)


def fn_result_report(pk):
    job_res_list = JobResult.objects.get(pk=pk)
    job_list = job_res_list.job
    user_list = job_list.user
    module_list = job_list.module_api.module
    module_api_list = job_list.module_api

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."

    # font 추가. 필요시 사용
    canvas.pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    canvas.pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    canvas.pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    canvas.pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
    p = canvas.Canvas(buffer)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    pdf_name = job_list.job_name
    if pdf_name == '':
        pdf_name = 'no_name'

    p.setLineWidth(.1)
    p.setFont('Helvetica', 22)
    p.drawString(30, 750, pdf_name)

    p.setFont('Helvetica-Bold', 12)
    p.drawString(440, 759, 'Writer : ' + user_list.name)
    p.drawString(440, 739, 'Report Date : ' + str(datetime.datetime.now().strftime('%Y-%m-%d')))
    p.line(425, 729, 600, 729)

    p.setFont('Helvetica', 22)
    p.drawString(100, 620, 'Job Description')

    p.setFont('Helvetica', 12)
    p.drawString(100, 590, 'Module used : ' + module_list.module_name)
    p.drawString(100, 570, 'Usage module API : ' + str(module_api_list.module_api_name))
    p.drawString(100, 550, 'Job Explanation : ' + job_list.job_explanation)

    p.setFont('Helvetica', 22)
    p.drawString(100, 480, 'Job Data')

    p.setFont('Helvetica', 12)
    p.drawString(100, 450, 'Job Smiles : ' + job_list.smiles)

    img_path = settings.BASE_DIR + '/static/smiles/userpk' + str(job_list.user_id) + '/jobpk' + str(
        job_list.pk) + '.png'
    mask = [0, 0, 0, 0, 0, 0]
    p.drawImage(img_path, x=400, y=350, width=100, height=100, mask=mask)
    smiles_detail = prediction(job_list.smiles)
    p.drawString(100, 430, 'Molecular weight : ' + str(smiles_detail['weight']))
    p.drawString(100, 410, 'LogP : ' + str(smiles_detail['logp']))
    p.drawString(100, 390, 'H-Bond Acceptor : ' + str(smiles_detail['numH']))
    p.drawString(100, 370, 'H-Bond Dornor : ' + str(smiles_detail['numHD']))
    p.drawString(100, 350, 'Rotatable Bond : ' + str(smiles_detail['numR']))
    p.drawString(100, 330, 'QED (drug likeness) : ' + str(round(smiles_detail['qed'], 3)))

    p.setFont('Helvetica', 22)
    p.drawString(100, 250, 'Job Result')
    p.setFont('Helvetica', 12)
    if job_list.module_api.module_api_cd == 'CD001':
        probability = ''
        result = '';
        gr = str(job_res_list.result_json['graph'])
        de = str(job_res_list.result_json['descriptor'])
        fi = str(job_res_list.result_json['fingerprint'])

        if gr == 'nan' and de == 'nan' and fi == 'nan':
            probability = 'nan'
            result = 'hERG-nonblocker'
        elif gr == 'nan' and de =='nan' and fi != 'nan':
            probability = fi
            if float(fi[:4]) > 0.5:
                result = 'hERG-blocker'
            else:
                result = 'hERG-nonblocker'
        elif gr == 'nan' and de != 'nan' and fi == 'nan':
            probability = de
            if float(de[:4]) > 0.5:
                result = 'hERG-blocker'
            else:
                result = 'hERG-nonblocker'
        elif gr != 'nan' and de == 'nan' and fi == 'nan':
            probability = gr
            if float(gr[:4]) > 0.5:
                result = 'hERG-blocker'
            else:
                result = 'hERG-nonblocker'
        elif gr != 'nan' and de != 'nan' and fi == 'nan' and float(gr[:4]) >= float(de[:4]):
            probability = gr
            if float(gr[:4]) > 0.5:
                result = 'hERG-blocker'
            else:
                result = 'hERG-nonblocker'
        elif gr != 'nan' and de != 'nan' and fi == 'nan' and float(de[:4]) >= float(gr[:4]):
            probability = de
            if float(de[:4]) > 0.5:
                result = 'hERG-blocker'
            else:
                result = 'hERG-nonblocker'
        elif gr == 'nan' and de != 'nan' and fi != 'nan' and float(de[:4]) >= float(fi[:4]):
            probability = de
            if float(de[:4]) > 0.5:
                result = 'hERG-blocker'
            else:
                result = 'hERG-nonblocker'
        elif gr == 'nan' and de != 'nan' and fi != 'nan' and float(fi[:4]) >= float(de[:4]):
            probability = fi
            if float(fi[:4]) > 0.5:
                result = 'hERG-blocker'
            else:
                result = 'hERG-nonblocker'
        elif gr != 'nan' and de == 'nan' and fi != 'nan' and float(gr[:4]) >= float(fi[:4]):
            probability = gr
            if float(gr[:4]) > 0.5:
                result = 'hERG-blocker'
            else:
                result = 'hERG-nonblocker'
        elif gr != 'nan' and de == 'nan' and fi != 'nan' and float(fi[:4]) >= float(gr[:4]):
            probability = fi
            if float(fi[:4]) > 0.5:
                result = 'hERG-blocker'
            else:
                result = 'hERG-nonblocker'
        # 모두다 nan 이 아닌경우
        elif gr != 'nan' and de != 'nan' and fi != 'nan' and float(gr[:4]) >= float(de[:4]) and float(gr[:4]) >= float(fi[:4]):
            probability = gr
            if float(gr[:4]) > 0.5:
                result = 'hERG-blocker'
            else:
                result = 'hERG-nonblocker'
        elif gr != 'nan' and de != 'nan' and fi != 'nan' and float(de[:4]) >= float(gr[:4]) and float(de[:4]) >= float(fi[:4]):
            probability = de
            if float(de[:4]) > 0.5:
                result = 'hERG-blocker'
            else:
                result = 'hERG-nonblocker'
        elif gr != 'nan' and de != 'nan' and fi != 'nan' and float(fi[:4]) >= float(gr[:4]) and float(fi[:4]) >= float(de[:4]):
            probability = fi
            if float(fi[:4]) > 0.5:
                result = 'hERG-blocker'
            else:
                result = 'hERG-nonblocker'

        #p.drawString(100, 220, 'Probability : ' + probability)
        p.drawString(100, 220, 'Result : ' + result)
        p.drawString(100, 200, 'Elapsed time : ' + str(round(float(job_res_list.result_json['time']), 1)))
    elif job_list.module_api.module_api_cd == 'CD002':
        if float(str(job_res_list.result_json['BBBP'])[:4]) > 0.5:
            result = 'Permeable'
        else:
            result = 'Non-permeable'
        p.drawString(100, 220, 'BBBP : ' + result)
        p.drawString(100, 200, 'Elapsed time : ' + str(round(float(job_res_list.result_json['time']), 1)))
    elif job_list.module_api.module_api_cd == 'CD003':
        if float(str(job_res_list.result_json['CYP1A2'])[:4]) > 0.5:
            res1 = 'inhibitor'
        else:
            res1 = 'non-inhibitor'
        if float(str(job_res_list.result_json['CYP2C19'])[:4]) > 0.5:
            res2 = 'inhibitor'
        else:
            res2 = 'non-inhibitor'
        if float(str(job_res_list.result_json['CYP2C9'])[:4]) > 0.5:
            res3 = 'inhibitor'
        else:
            res3 = 'non-inhibitor'
        if float(str(job_res_list.result_json['CYP2D6'])[:4]) > 0.5:
            res4 = 'inhibitor'
        else:
            res4 = 'non-inhibitor'
        if float(str(job_res_list.result_json['CYP3A4'])[:4]) > 0.5:
            res5 = 'inhibitor'
        else:
            res5 = 'non-inhibitor'
        p.drawString(100, 220, 'CYP1A2 : ' + res1)
        p.drawString(100, 200, 'CYP2C19 : ' + res2)
        p.drawString(100, 180, 'CYP2C9 : ' + res3)
        p.drawString(100, 160, 'CYP2D6 : ' + res4)
        p.drawString(100, 140, 'CYP3A4 : ' + res5)
        p.drawString(100, 120, 'Elapsed time : ' + str(round(float(job_res_list.result_json['time']), 1)))
    elif job_list.module_api.module_api_cd == 'CD004':
        if float(str(job_res_list.result_json['hERG_inhibition'])[:4]) > 0.5:
            result = 'hERG-blocker'
        else:
            result = 'hERG-nonblocker'
        p.drawString(100, 220, 'Result : ' + result)
        p.drawString(100, 200, 'Elapsed time : ' + str(round(float(job_res_list.result_json['time']), 1)))
    elif job_list.module_api.module_api_cd == 'CD005':
        p.drawString(100, 220, 'Human : ' + str(job_res_list.result_json['Human']))
        #p.drawString(100, 200, 'Mouse : ' + str(job_res_list.result_json['Mouse']))
        p.drawString(100, 180, 'Elapsed time : ' + str(round(float(job_res_list.result_json['time']), 1)))
        
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='' + pdf_name + '.pdf')


# def coll_proc(des_score, fig_score, graph_score, start_Date, job_id):
#    conn = pymysql.connect(host='192.168.1.22', user='root', password='1q2w3e4r', db='krict_db_server', charset='utf8')


def module_search(request):
    if request.method == 'GET':
        search_condition = request.GET['searchCondition']
        if search_condition == 'module_name':
            keyword = request.GET['keyword']
            module_name_search_list = Module.objects.filter(Q(module_name__icontains=keyword))
            page = request.GET.get('page', 1)
            paginator = Paginator(module_name_search_list, 10)
            page_obj = paginator.get_page(page)
            return render(request, 'job_user/module_list.html', {'modules': page_obj})
        if search_condition == 'module_category':
            keyword = request.GET['keyword']
            module_category_search_list = Module.objects.filter(Q(module_category__icontains=keyword))
            page = request.GET.get('page', 1)
            paginator = Paginator(module_category_search_list, 10)
            page_obj = paginator.get_page(page)
            return render(request, 'job_user/module_list.html', {'modules': page_obj})
        if search_condition == 'paper_link':
            keyword = request.GET['keyword']
            module_paper_link_search_list = Module.objects.filter(Q(paper_link__icontains=keyword))
            page = request.GET.get('page', 1)
            paginator = Paginator(module_paper_link_search_list, 10)
            page_obj = paginator.get_page(page)
            return render(request, 'job_user/module_list.html', {'modules': page_obj})
    return render(request, 'job_user/module_list.html')


def module_detail(request, pk):
    qs = Module.objects.get(pk=pk)
    module_api = ModuleApi.objects.all()
    return render(request, 'job_user/module_detail.html', {'module': qs, 'module_api': module_api, 'pk': pk,})


def chemtrans_result_make_csv_file(job_list, job_res_list, module_api_list, module_list, user_list):
    csv_report = pd.DataFrame(np.random.rand(1, 101),
                              columns=['CID1', 'CID2', 'CID3', 'CID4', 'CID5',
                                       'CID6', 'CID7', 'CID8', 'CID9', 'CID10',
                                       'CID11', 'CID12', 'CID13', 'CID14', 'CID15',
                                       'CID16', 'CID17', 'CID18', 'CID19', 'CID20',
                                       'CID21', 'CID22', 'CID23', 'CID24', 'CID25',
                                       'CID26', 'CID27', 'CID28', 'CID29', 'CID30',
                                       'CID31', 'CID32', 'CID33', 'CID34', 'CID35',
                                       'CID36', 'CID37', 'CID38', 'CID39', 'CID40',
                                       'CID41', 'CID42', 'CID43', 'CID44', 'CID45',
                                       'CID46', 'CID47', 'CID48', 'CID49', 'CID50',
                                       'CID51', 'CID52', 'CID53', 'CID54', 'CID55',
                                       'CID56', 'CID57', 'CID58', 'CID59', 'CID60',
                                       'CID61', 'CID62', 'CID63', 'CID64', 'CID65',
                                       'CID66', 'CID67', 'CID68', 'CID69', 'CID70',
                                       'CID71', 'CID72', 'CID73', 'CID74', 'CID75',
                                       'CID76', 'CID77', 'CID78', 'CID79', 'CID80',
                                       'CID81', 'CID82', 'CID83', 'CID84', 'CID85',
                                       'CID86', 'CID87', 'CID88', 'CID89', 'CID90',
                                       'CID91', 'CID92', 'CID93', 'CID94', 'CID95',
                                       'CID96', 'CID97', 'CID98', 'CID99', 'CID100',
                                       'time'
                                       ])
    csv_report.to_csv(job_list.job_name + '.csv', index=False, mode='w', encoding='utf-8')
    read_csv_report = pd.read_csv(job_list.job_name + '.csv')
    file_name = "" + job_list.job_name + ".csv"
    wrapper = FileWrapper(read_csv_report)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    writer = csv.writer(response)
    writer.writerow(
        ['Job name', 'Writer', 'Report date', 'Module name', 'Module api name', 'smiles', 'Job explanation',
         'CID1', 'CID2', 'CID3', 'CID4', 'CID5',
         'CID6', 'CID7', 'CID8', 'CID9', 'CID10',
         'CID11', 'CID12', 'CID13', 'CID14', 'CID15',
         'CID16', 'CID17', 'CID18', 'CID19', 'CID20',
         'CID21', 'CID22', 'CID23', 'CID24', 'CID25',
         'CID26', 'CID27', 'CID28', 'CID29', 'CID30',
         'CID31', 'CID32', 'CID33', 'CID34', 'CID35',
         'CID36', 'CID37', 'CID38', 'CID39', 'CID40',
         'CID41', 'CID42', 'CID43', 'CID44', 'CID45',
         'CID46', 'CID47', 'CID48', 'CID49', 'CID50',
         'CID51', 'CID52', 'CID53', 'CID54', 'CID55',
         'CID56', 'CID57', 'CID58', 'CID59', 'CID60',
         'CID61', 'CID62', 'CID63', 'CID64', 'CID65',
         'CID66', 'CID67', 'CID68', 'CID69', 'CID70',
         'CID71', 'CID72', 'CID73', 'CID74', 'CID75',
         'CID76', 'CID77', 'CID78', 'CID79', 'CID80',
         'CID81', 'CID82', 'CID83', 'CID84', 'CID85',
         'CID86', 'CID87', 'CID88', 'CID89', 'CID90',
         'CID91', 'CID92', 'CID93', 'CID94', 'CID95',
         'CID96', 'CID97', 'CID98', 'CID99', 'CID100',
         'Elapsed time'
         ])
    writer.writerow(
        [job_list.job_name, user_list.name, str(datetime.datetime.now().strftime('%Y-%m-%d')), module_list.module_name,
         module_api_list.module_api_name,
         job_list.smiles, job_list.job_explanation,
         job_res_list.result_json['CID1'] if 'CID1' in job_res_list.result_json else '',
         job_res_list.result_json['CID2'] if 'CID2' in job_res_list.result_json else '',
         job_res_list.result_json['CID3'] if 'CID3' in job_res_list.result_json else '',
         job_res_list.result_json['CID4'] if 'CID4' in job_res_list.result_json else '',
         job_res_list.result_json['CID5'] if 'CID5' in job_res_list.result_json else '',
         job_res_list.result_json['CID6'] if 'CID6' in job_res_list.result_json else '',
         job_res_list.result_json['CID7'] if 'CID7' in job_res_list.result_json else '',
         job_res_list.result_json['CID8'] if 'CID8' in job_res_list.result_json else '',
         job_res_list.result_json['CID9'] if 'CID9' in job_res_list.result_json else '',
         job_res_list.result_json['CID10'] if 'CID10' in job_res_list.result_json else '',
         job_res_list.result_json['CID11'] if 'CID11' in job_res_list.result_json else '',
         job_res_list.result_json['CID12'] if 'CID12' in job_res_list.result_json else '',
         job_res_list.result_json['CID13'] if 'CID13' in job_res_list.result_json else '',
         job_res_list.result_json['CID14'] if 'CID14' in job_res_list.result_json else '',
         job_res_list.result_json['CID15'] if 'CID15' in job_res_list.result_json else '',
         job_res_list.result_json['CID16'] if 'CID16' in job_res_list.result_json else '',
         job_res_list.result_json['CID17'] if 'CID17' in job_res_list.result_json else '',
         job_res_list.result_json['CID18'] if 'CID18' in job_res_list.result_json else '',
         job_res_list.result_json['CID19'] if 'CID19' in job_res_list.result_json else '',
         job_res_list.result_json['CID20'] if 'CID20' in job_res_list.result_json else '',
         job_res_list.result_json['CID21'] if 'CID21' in job_res_list.result_json else '',
         job_res_list.result_json['CID22'] if 'CID22' in job_res_list.result_json else '',
         job_res_list.result_json['CID23'] if 'CID23' in job_res_list.result_json else '',
         job_res_list.result_json['CID24'] if 'CID24' in job_res_list.result_json else '',
         job_res_list.result_json['CID25'] if 'CID25' in job_res_list.result_json else '',
         job_res_list.result_json['CID26'] if 'CID26' in job_res_list.result_json else '',
         job_res_list.result_json['CID27'] if 'CID27' in job_res_list.result_json else '',
         job_res_list.result_json['CID28'] if 'CID28' in job_res_list.result_json else '',
         job_res_list.result_json['CID29'] if 'CID29' in job_res_list.result_json else '',
         job_res_list.result_json['CID30'] if 'CID30' in job_res_list.result_json else '',
         job_res_list.result_json['CID31'] if 'CID31' in job_res_list.result_json else '',
         job_res_list.result_json['CID32'] if 'CID32' in job_res_list.result_json else '',
         job_res_list.result_json['CID33'] if 'CID33' in job_res_list.result_json else '',
         job_res_list.result_json['CID34'] if 'CID34' in job_res_list.result_json else '',
         job_res_list.result_json['CID35'] if 'CID35' in job_res_list.result_json else '',
         job_res_list.result_json['CID36'] if 'CID36' in job_res_list.result_json else '',
         job_res_list.result_json['CID37'] if 'CID37' in job_res_list.result_json else '',
         job_res_list.result_json['CID38'] if 'CID38' in job_res_list.result_json else '',
         job_res_list.result_json['CID39'] if 'CID39' in job_res_list.result_json else '',
         job_res_list.result_json['CID40'] if 'CID40' in job_res_list.result_json else '',
         job_res_list.result_json['CID41'] if 'CID41' in job_res_list.result_json else '',
         job_res_list.result_json['CID42'] if 'CID42' in job_res_list.result_json else '',
         job_res_list.result_json['CID43'] if 'CID43' in job_res_list.result_json else '',
         job_res_list.result_json['CID44'] if 'CID44' in job_res_list.result_json else '',
         job_res_list.result_json['CID45'] if 'CID45' in job_res_list.result_json else '',
         job_res_list.result_json['CID46'] if 'CID46' in job_res_list.result_json else '',
         job_res_list.result_json['CID47'] if 'CDI47' in job_res_list.result_json else '',
         job_res_list.result_json['CID48'] if 'CID48' in job_res_list.result_json else '',
         job_res_list.result_json['CID49'] if 'CID49' in job_res_list.result_json else '',
         job_res_list.result_json['CID50'] if 'CID50' in job_res_list.result_json else '',
         job_res_list.result_json['CID51'] if 'CID51' in job_res_list.result_json else '',
         job_res_list.result_json['CID52'] if 'CID52' in job_res_list.result_json else '',
         job_res_list.result_json['CID53'] if 'CID53' in job_res_list.result_json else '',
         job_res_list.result_json['CID54'] if 'CID54' in job_res_list.result_json else '',
         job_res_list.result_json['CID55'] if 'CID55' in job_res_list.result_json else '',
         job_res_list.result_json['CID56'] if 'CID56' in job_res_list.result_json else '',
         job_res_list.result_json['CID57'] if 'CID57' in job_res_list.result_json else '',
         job_res_list.result_json['CID58'] if 'CID58' in job_res_list.result_json else '',
         job_res_list.result_json['CID59'] if 'CID59' in job_res_list.result_json else '',
         job_res_list.result_json['CID60'] if 'CID60' in job_res_list.result_json else '',
         job_res_list.result_json['CID61'] if 'CID61' in job_res_list.result_json else '',
         job_res_list.result_json['CID62'] if 'CID62' in job_res_list.result_json else '',
         job_res_list.result_json['CID63'] if 'CID63' in job_res_list.result_json else '',
         job_res_list.result_json['CID64'] if 'CID64' in job_res_list.result_json else '',
         job_res_list.result_json['CID65'] if 'CID65' in job_res_list.result_json else '',
         job_res_list.result_json['CID66'] if 'CID66' in job_res_list.result_json else '',
         job_res_list.result_json['CID67'] if 'CID67' in job_res_list.result_json else '',
         job_res_list.result_json['CID68'] if 'CID68' in job_res_list.result_json else '',
         job_res_list.result_json['CID69'] if 'CID69' in job_res_list.result_json else '',
         job_res_list.result_json['CID70'] if 'CID70' in job_res_list.result_json else '',
         job_res_list.result_json['CID71'] if 'CID71' in job_res_list.result_json else '',
         job_res_list.result_json['CID72'] if 'CID72' in job_res_list.result_json else '',
         job_res_list.result_json['CID73'] if 'CID73' in job_res_list.result_json else '',
         job_res_list.result_json['CID74'] if 'CID74' in job_res_list.result_json else '',
         job_res_list.result_json['CID75'] if 'CID75' in job_res_list.result_json else '',
         job_res_list.result_json['CID76'] if 'CID76' in job_res_list.result_json else '',
         job_res_list.result_json['CID77'] if 'CID77' in job_res_list.result_json else '',
         job_res_list.result_json['CID78'] if 'CID78' in job_res_list.result_json else '',
         job_res_list.result_json['CID79'] if 'CID79' in job_res_list.result_json else '',
         job_res_list.result_json['CID80'] if 'CID80' in job_res_list.result_json else '',
         job_res_list.result_json['CID81'] if 'CID81' in job_res_list.result_json else '',
         job_res_list.result_json['CID82'] if 'CID82' in job_res_list.result_json else '',
         job_res_list.result_json['CID83'] if 'CID83' in job_res_list.result_json else '',
         job_res_list.result_json['CID84'] if 'CID84' in job_res_list.result_json else '',
         job_res_list.result_json['CID85'] if 'CID85' in job_res_list.result_json else '',
         job_res_list.result_json['CID86'] if 'CID86' in job_res_list.result_json else '',
         job_res_list.result_json['CID87'] if 'CID87' in job_res_list.result_json else '',
         job_res_list.result_json['CID88'] if 'CID88' in job_res_list.result_json else '',
         job_res_list.result_json['CID89'] if 'CID89' in job_res_list.result_json else '',
         job_res_list.result_json['CID90'] if 'CID90' in job_res_list.result_json else '',
         job_res_list.result_json['CID91'] if 'CID91' in job_res_list.result_json else '',
         job_res_list.result_json['CID92'] if 'CID92' in job_res_list.result_json else '',
         job_res_list.result_json['CID93'] if 'CID93' in job_res_list.result_json else '',
         job_res_list.result_json['CID94'] if 'CID94' in job_res_list.result_json else '',
         job_res_list.result_json['CID95'] if 'CID95' in job_res_list.result_json else '',
         job_res_list.result_json['CID96'] if 'CID96' in job_res_list.result_json else '',
         job_res_list.result_json['CID97'] if 'CID97' in job_res_list.result_json else '',
         job_res_list.result_json['CID98'] if 'CID98' in job_res_list.result_json else '',
         job_res_list.result_json['CID99'] if 'CID99' in job_res_list.result_json else '',
         job_res_list.result_json['CID100'] if 'CID100' in job_res_list.result_json else '',
         round(float(job_res_list.result_json['time']), 1)
         ])
    # response['Content-Length'] = os.path.getsize(read_csv_report)

    return response


def job_result_report_csv(request, pk):
    job_res_list = JobResult.objects.get(pk=pk)
    job_list = job_res_list.job
    user_list = job_list.user
    module_list = job_list.module_api.module
    module_api_list = job_list.module_api
    if module_api_list.module_api_cd == 'CD001':
        return deep_hit_result_make_csv_file(job_list, job_res_list, module_api_list, module_list, user_list)
    elif module_api_list.module_api_cd == 'CD002':
        return bbbp_result_make_csv_file(job_list, job_res_list, module_api_list, module_list, user_list)
    elif module_api_list.module_api_cd == 'CD003':
        return cyp_result_make_csv_file(job_list, job_res_list, module_api_list, module_list, user_list)
    elif module_api_list.module_api_cd == 'CD004':
        return herg_result_make_csv_file(job_list, job_res_list, module_api_list, module_list, user_list)
    elif module_api_list.module_api_cd == 'CD005':
        return ms_result_make_csv_file(job_list, job_res_list, module_api_list, module_list, user_list)
    elif module_api_list.module_api_cd == 'CD006':
        return chemtrans_result_make_csv_file(job_list, job_res_list, module_api_list, module_list, user_list)


def deep_hit_result_make_csv_file(job_list, job_res_list, module_api_list, module_list, user_list):
    csv_report = pd.DataFrame.from_records(
        [{'graph': job_res_list.result_json['graph'], 'descriptor': job_res_list.result_json['descriptor'],
          'fingerprint': job_res_list.result_json['fingerprint'],
          'lead_time': job_res_list.result_json['time'], 'smiles': job_list.smiles}])
    # if not os.path.exists('C:\\job_result\\' + job_list.job_name + '.csv'):
    csv_report.to_csv(job_list.job_name + '.csv', index=False, mode='w', encoding='utf-8')
    read_csv_report = pd.read_csv(job_list.job_name + '.csv')
    file_name = "" + job_list.job_name + ".csv"
    wrapper = FileWrapper(read_csv_report)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    writer = csv.writer(response)
    writer.writerow(
        ['Job name', 'Writer', 'Report date', 'Module name', 'Module api name', 'Smiles', 'Job explanation',
         'graph', 'descriptor', 'fingerprint', 'Elapsed time'
         ])
    writer.writerow(
        [job_list.job_name, user_list.name, str(datetime.datetime.now().strftime('%Y-%m-%d')), module_list.module_name,
         module_api_list.module_api_name,
         job_list.smiles, job_list.job_explanation,
         job_res_list.result_json['graph'], job_res_list.result_json['descriptor'],
         job_res_list.result_json['fingerprint'], round(float(job_res_list.result_json['time']), 1)
         ])
    # response['Content-Length'] = os.path.getsize(read_csv_report)
    return response


def bbbp_result_make_csv_file(job_list, job_res_list, module_api_list, module_list, user_list):
    csv_report = pd.DataFrame.from_records(
        [{'BBBP': job_res_list.result_json['BBBP'], 'Elapsed time': job_res_list.result_json['time'],
          'smiles': job_list.smiles}])
    # if not os.path.exists('C:\\job_result\\' + job_list.job_name + '.csv'):
    csv_report.to_csv(job_list.job_name + '.csv', index=False, mode='w', encoding='utf-8')
    read_csv_report = pd.read_csv(job_list.job_name + '.csv')
    file_name = "" + job_list.job_name + ".csv"
    wrapper = FileWrapper(read_csv_report)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    writer = csv.writer(response)
    writer.writerow(
        ['Job name', 'Writer', 'Report date', 'Module name', 'Module apiname', 'Smiles', 'Job explanation',
         'bbbp', 'Elapsed time'
         ])
    writer.writerow(
        [job_list.job_name, user_list.name, str(datetime.datetime.now().strftime('%Y-%m-%d')), module_list.module_name,
         module_api_list.module_api_name,
         job_list.smiles, job_list.job_explanation,
         job_res_list.result_json['BBBP'], round(float(job_res_list.result_json['time']), 1)
         ])
    # response['Content-Length'] = os.path.getsize(read_csv_report)
    return response


def cyp_result_make_csv_file(job_list, job_res_list, module_api_list, module_list, user_list):
    csv_report = pd.DataFrame.from_records(
        [{'CYP1A2': job_res_list.result_json['CYP1A2'],
          'CYP2C9': job_res_list.result_json['CYP2C9'],
          'CYP2D6': job_res_list.result_json['CYP2D6'],
          'CYP3A4': job_res_list.result_json['CYP3A4'],
          'CYP2C19': job_res_list.result_json['CYP2C19'],
          'time': job_res_list.result_json['time'],
          'smiles': job_list.smiles}])
    # if not os.path.exists('C:\\job_result\\' + job_list.job_name + '.csv'):
    csv_report.to_csv(job_list.job_name + '.csv', index=False, mode='w', encoding='utf-8')
    read_csv_report = pd.read_csv(job_list.job_name + '.csv')
    file_name = "" + job_list.job_name + ".csv"
    wrapper = FileWrapper(read_csv_report)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    writer = csv.writer(response)
    writer.writerow(
        ['Job name', 'Writer', 'Report date', 'Module name', 'Module api name', 'smiles', 'Job explanation',
         'CYP1A2', 'CYP2C9', 'CYP2D6', 'CYP3A4', 'CYP2C19', 'Elapsed time',
         ])
    writer.writerow(
        [job_list.job_name, user_list.name, str(datetime.datetime.now().strftime('%Y-%m-%d')), module_list.module_name,
         module_api_list.module_api_name,
         job_list.smiles, job_list.job_explanation,
         job_res_list.result_json['CYP1A2'], job_res_list.result_json['CYP2C9'], job_res_list.result_json['CYP2D6'],
         job_res_list.result_json['CYP3A4'], job_res_list.result_json['CYP2C19'],
         round(float(job_res_list.result_json['time']), 1)

         ])
    # response['Content-Length'] = os.path.getsize(read_csv_report)
    return response


def herg_result_make_csv_file(job_list, job_res_list, module_api_list, module_list, user_list):
    csv_report = pd.DataFrame.from_records(
        [{'hERG_inhibition': job_res_list.result_json['hERG_inhibition'],
          'time': job_res_list.result_json['time'],
          'smiles': job_list.smiles}])
    # if not os.path.exists('C:\\job_result\\' + job_list.job_name + '.csv'):
    csv_report.to_csv(job_list.job_name + '.csv', index=False, mode='w', encoding=
    'utf-8')
    read_csv_report = pd.read_csv(job_list.job_name + '.csv')
    file_name = "" + job_list.job_name + ".csv"
    wrapper = FileWrapper(read_csv_report)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    writer = csv.writer(response)
    writer.writerow(
        ['Job name', 'Writer', 'Report date', 'Module name', 'Module api name', 'Smiles', 'Job explanation',
         'herg_inhibition', 'Elapsed time'
         ])
    writer.writerow(
        [job_list.job_name, user_list.name, str(datetime.datetime.now().strftime('%Y-%m-%d')), module_list.module_name,
         module_api_list.module_api_name,
         job_list.smiles, job_list.job_explanation,
         job_res_list.result_json['hERG_inhibition'], round(float(job_res_list.result_json['time']), 1)
         ])
    # response['Content-Length'] = os.path.getsize(read_csv_report)
    return response


def ms_result_make_csv_file(job_list, job_res_list, module_api_list, module_list, user_list):
    csv_report = pd.DataFrame.from_records(
        [{'Human': job_res_list.result_json['Human'], #'Mouse': job_res_list.result_json['Mouse'],
          'Elapsed time': job_res_list.result_json['time'],
          'Smiles': job_list.smiles}])
    # if not os.path.exists('C:\\job_result\\' + job_list.job_name + '.csv'):
    csv_report.to_csv(job_list.job_name + '.csv', index=False, mode='w', encoding='utf-8')
    read_csv_report = pd.read_csv(job_list.job_name + '.csv')
    file_name = "" + job_list.job_name + ".csv"
    wrapper = FileWrapper(read_csv_report)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    writer = csv.writer(response)
    writer.writerow(
        ['Job_name', 'Writer', 'Report date', 'Module name', 'Module api name', 'Smiles', 'Job explanation',
         'human', 'Elapsed time'
         ])
    writer.writerow(
        [job_list.job_name, user_list.name, str(datetime.datetime.now().strftime('%Y-%m-%d')), module_list.module_name,
         module_api_list.module_api_name,
         job_list.smiles, job_list.job_explanation,
         job_res_list.result_json['Human'], #job_res_list.result_json['Mouse'],
         round(float(job_res_list.result_json['time']), 1)
         ])
    # response['Content-Length'] = os.path.getsize(read_csv_report)
    return response


@login_required()
@csrf_exempt
def job_delete(request):
    job = Job.objects.get(pk=request.POST['pk'])
    job.delete()
    return redirect("job_user:job_list")
