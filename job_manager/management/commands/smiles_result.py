from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
import json, requests
from job_user.models import JobResult, Job
from urllib import parse


class Command(BaseCommand):
    help = 'waiting 상태의 작업들을 runnung 상태로 바꿔주며, 각각에 연결된 모듈을 돌려 결과를 저장하는 로직입니다.'

    def handle(self, *args, **kwargs):
        # waiting 선별
        job_results = JobResult.objects.select_related('job').filter(job__job_status='waiting')
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
                # urls = "http://10.39.149.110:8081/predict_deep_hit?content=" + parse.quote(content)
                #  urls = "http://192.168.1.209:8081/predict_deep_hit?content=" + parse.quote(content)
                urls = "http://192.168.1.209:9093/deep_hit/?smiles=" + parse.quote(content)
            elif running_job.module_api.module_api_cd == 'CD002':
                # urls = "http://10.39.149.110:8084/predict_bbbp?content=" + parse.quote(content)
                # urls = "http://192.168.1.209:9093/predict_bbbp?content=" + parse.quote(content)
                urls = "http://192.168.1.209:9093/bbb_permeability/?smiles=" + parse.quote(content)
            elif running_job.module_api.module_api_cd == 'CD003':
                # urls = "http://10.39.149.110:8082/predict_cyp?content=" + parse.quote(content)
                urls = "http://192.168.1.209:8082/predict_cyp?content=" + parse.quote(content)
            elif running_job.module_api.module_api_cd == 'CD004':
                # urls = "http://10.39.149.110:8082/predict_herg?content=" + parse.quote(content)
                urls = "http://192.168.1.209:8082/predict_herg?content=" + parse.quote(content)
            elif running_job.module_api.module_api_cd == 'CD005':
                # urls = "http://10.39.149.110:8085/predict_ms?content=" + parse.quote(content)
                urls = "http://192.168.1.209:8085/predict_ms?content=" + parse.quote(content)
            elif running_job.module_api.module_api_cd == 'CD006':
                # urls = "http://10.39.149.110:8083/predict_chemtrans?content=" + parse.quote(content)
                urls = "http://192.168.1.209:8083/predict_chemtrans?content=" + parse.quote(content)
            elif running_job.module_api.module_api_cd == 'CD007':
                # urls = "http://10.39.149.110:9093/predict_dili?content=" + parse.quote(content)
                urls = "http://192.168.1.209:9093/predict_dili?content=" + parse.quote(content)
            elif running_job.module_api.module_api_cd == 'CD008':
                # urls = "http://10.39.149.110:8521/predict_ar?content=" + parse.quote(content)
                urls = "http://192.168.1.209:8521/predict_ar?content=" + parse.quote(content)
            print(urls)
            req = requests.get(urls)
            ## GET HTML SOURCE
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            jsonObject = json.loads(str(soup))

            job_result.result_json = jsonObject
            job_result.save()