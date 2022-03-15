import json, requests

from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import logout_then_login
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.core.paginator import Paginator
from accounts.decorators import admin_required
from accounts.models import *
from job_user.models import *
from .forms import UserModifyForm
from job_user import models


def left_css(request):
    return render(request, 'job_manager/left_css.html')


class MemberListView(LoginRequiredMixin, ListView):
    # def dispatch(self, request, *args, **kwargs):
    # if request.user.role != "sup":
    # return redirect("/")
    # return super().dispatch(request, *args, **kwargs)

    template_name = 'job_manager/member_manage.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        member_list = User.objects.order_by('-date_joined')
        if self.request.GET.get('searchMemberInput', ''):
            if self.request.GET.get('searchMemberSelect') == 'user_id':
                member_list = User.objects.filter(username__icontains=self.request.GET.get('searchMemberInput', '')).order_by('-date_joined')
            else:
                member_list = User.objects.filter(name__icontains=self.request.GET.get('searchMemberInput', '')).order_by('-date_joined')

        return member_list

    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)
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


member_manager = admin_required(MemberListView.as_view())


@admin_required
def member_modify(request, pk):
    target_user = User.objects.get(pk=pk)
    return render(request, "job_manager/member_modify.html", {
        "target_user": target_user, 
    })


@admin_required
def member_modify_save(request, pk):
    target_user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserModifyForm(request.POST, request.FILES, instance=target_user)
        if form.is_valid():
            target_user = form.save(commit=False)
            # target_user.set_password(request.POST['password'])
            target_user.save()
            # 본인 계정 수정시 로그아웃
            if target_user == request.user:
                return logout_then_login(request)
            return redirect("job_manager:member_modify", pk)
    else:
        form = UserModifyForm(instance=target_user)
    return render(request, "job_manager/member_modify_save.html", {
        "form": form, "user_pk" : pk,
    })


@admin_required
def module_manager(request):
    page = request.GET.get('page', 1)
    module_list = Module.objects.order_by('-create_date').all()
    paginator = Paginator(module_list, 10)

    page_obj = paginator.get_page(page)
    return render(request, 'job_manager/module_manage.html', {'modules': page_obj})


@admin_required
@csrf_exempt
def module_search(request):
    if request.method == "GET":
        search_condition = request.GET['searchCondition']
        if search_condition == 'module_name':
            keyword = request.GET['keyword']
            module_name_search_list = Module.objects.filter(Q(module_name__icontains=keyword))
            page = request.GET.get('page', 1)
            paginator = Paginator(module_name_search_list, 5)
            page_obj = paginator.get_page(page)
            return render(request, 'job_manager/module_manage.html', {'modules': page_obj})
        if search_condition == 'module_category':
            keyword = request.GET['keyword']
            module_category_search_list = Module.objects.filter(Q(module_category__icontains=keyword))
            page = request.GET.get('page', 1)
            paginator = Paginator(module_category_search_list, 5)
            page_obj = paginator.get_page(page)
            return render(request, 'job_manager/module_manage.html', {'modules': page_obj})
        if search_condition == 'paper_link':
            keyword = request.GET['keyword']
            module_paper_link_search_list = Module.objects.filter(Q(module_paper_link__icontains=keyword))
            page = request.GET.get('page', 1)
            paginator = Paginator(module_paper_link_search_list, 5)
            page_obj = paginator.get_page(page)
            return render(request, 'job_manager/module_manage.html', {'modules': page_obj})
    return render(request, 'job_manager/module_manage.html')


@admin_required
def module_detail(request, pk):
    level_list = Module.level_list
    category_list = Module.module_category_list
    type_list = Module.module_type_list
    qs = Module.objects.get(pk=pk)

    return render(request, 'job_manager/module_detail.html',
                  {'module': qs, 'level': level_list, 'category': category_list, 'type': type_list, 'pk': pk})


@admin_required
def module_detail_save(request, pk):
    level_list = Module.level_list
    category_list = Module.module_category_list
    type_list = Module.module_type_list
    qs = Module.objects.get(pk=pk)
    return render(request, 'job_manager/module_detail_save.html',
                  {'module': qs, 'level': level_list, 'category': category_list, 'type': type_list, 'pk': pk})


@admin_required
def set_api_module(module_name):
    print(module_name)


# f = open("c\\euclid_krict\\module_api\\" + module_name, 'w')
# print(f)

@admin_required
def module_register(request):
    level_list = Module.level_list
    category_list = Module.module_category_list
    type_list = Module.module_type_list
    if request.method == "POST":
        module = Module(module_name=request.POST['module_name'], module_explanation=request.POST['module_explanation']
                        , module_img=request.FILES['module_img'],
                        paper_link=request.POST['paper_link'], module_category=request.POST['module_category'],
                        module_level=request.POST['module_level'], module_type=request.POST['module_type'])

        module.save()
        # module_api = ModuleApi(module_id=module.id, module_api_name=request.FILES['module_api_name'])
        # module_api.save()
        return render(request, 'job_manager/module_manage.html')
    return render(request, 'job_manager/module_register.html',
                  {'level': level_list, 'category': category_list, 'type': type_list})


@admin_required
def module_modify(request, pk):
    level_list = Module.level_list
    category_list = Module.module_category_list
    type_list = Module.module_type_list
    qs = Module.objects.get(pk=pk)

    return render(request, 'job_manager/module_modify.html',
                  {'module': qs, 'level': level_list, 'category': category_list, 'type': type_list, 'pk': pk})


@admin_required
def do_module_modify(request):
    module_history_obj = Module.objects.get(pk=request.POST['id'])

    if request.method == "POST":
        module = Module.objects.get(pk=request.POST['id'])
        module.module_name = request.POST['module_name']
        module.module_explanation = request.POST['module_explanation']
        module.module_level = request.POST.get('module_level', 'lev3')
        module.module_category = request.POST.get('module_category', 'category1')
        module.module_type = request.POST.get('module_type', 'type1')
        module.paper_link = request.POST['paper_link']
        module.module_img = request.FILES.get('module_img', request.POST['originImageFileName'])
        module.save()
        return redirect("job_manager:module_detail", request.POST['id'])
    return redirect('/manager/module_detail/' + request.POST['id'])


@admin_required
def module_delete(request):
    if request.method == "POST":
        delete_no = request.POST['pk']
        module_api = ModuleApi.objects.get(pk=delete_no)
        module_api.delete()
        module = Module.objects.get(pk=delete_no)
        module.delete()
        return render(request, 'job_manager/module_manage.html')


class APIListView(LoginRequiredMixin, ListView):
    template_name = 'job_manager/module_api_manage.html'
    context_object_name = 'api_list'
    paginate_by = 10

    def get_queryset(self):
        api_list = ModuleApi.objects.all()
        return api_list

    def get_context_data(self, **kwargs):
        context = super(APIListView, self).get_context_data(**kwargs)
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


module_api_manage = admin_required(APIListView.as_view())


@admin_required
def module_api_modify(request, pk):
    target_api = ModuleApi.objects.get(pk=pk)
    return render(request, "job_manager/module_api_modify.html", {
        "target_api": target_api,
    })


@admin_required
def module_api_modify_save(request, pk):
    target_api = ModuleApi.objects.get(pk=pk)
    if request.method == 'POST':
        module = request.POST.get('module')
        api_name = request.POST.get('api_name')
        target_api.module_id = module
        target_api.module_api_name = api_name
        target_api.save()
        return redirect("job_manager:module_api_modify", pk)

    return render(request, "job_manager/module_api_modify_save.html", {
        "target_api": target_api,
    })


def test(request):
    if request.method == "GET":
        return render(request, "job_manager/test.html")
    if request.method == "POST":
        job = Job.objects.create(job_name='test',
                                 job_explanation='test',
                                 smiles=request.POST['smiles'],
                                 job_status='running',
                                 module_api=ModuleApi.objects.get(pk=6),
                                 user=User.objects.get(pk=request.POST['user']))
        jobRes = JobResult()
        jobRes.job = job
        content = job.smiles
        urls = "http://192.168.50.3:50051/predict_ms?content=" + content
        req = requests.get(urls)
        ## GET HTML SOURCE
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        jsonObject = json.loads(str(soup))
        jobRes.result_json = jsonObject
        print(jsonObject["time"])
        jobRes.save()

        return render(request, "job_manager/test.html", {'json': jsonObject})
