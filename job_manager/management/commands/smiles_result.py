from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
import json, requests
from django.db import transaction
from job_user.models import JobResult, Job
from urllib import parse


class Command(BaseCommand):
    help = 'waiting 상태의 작업들을 runnung 상태로 바꿔주며, 각각에 연결된 모듈을 돌려 결과를 저장하는 로직입니다.'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                waiting_jobs = Job.objects.filter(job_status='waiting')
                for job in waiting_jobs:
                    job.job_status = "running"
                    job.save()

                    urls = None
                    if job.module_api.module_api_cd == 'CD001':
                        urls = "http://10.39.149.110:8081/predict_deep_hit?content=" + parse.quote(job.smiles)
                    elif job.module_api.module_api_cd == 'CD002':
                        urls = "http://192.168.1.209:9093/bbb_permeability?smiles=" + parse.quote(job.smiles)
                    elif job.module_api.module_api_cd == 'CD003':
                        urls = "http://10.39.149.110:8082/predict_cyp?content=" + parse.quote(job.smiles)
                    elif job.module_api.module_api_cd == 'CD004':
                        urls = "http://10.39.149.110:8082/predict_herg?content=" + parse.quote(job.smiles)
                    elif job.module_api.module_api_cd == 'CD005':
                        urls = "http://10.39.149.110:8085/predict_ms?content=" + parse.quote(job.smiles)
                    elif job.module_api.module_api_cd == 'CD006':
                        urls = "http://10.39.149.110:8083/predict_chemtrans?content=" + parse.quote(job.smiles)
                    elif job.module_api.module_api_cd == 'CD007':
                        urls = "http://192.168.1.209:9093/predict_dili?content=" + parse.quote(job.smiles)
                    elif job.module_api.module_api_cd == 'CD008':
                        urls = "http://192.168.1.209:8521/predict_ar?content=" + parse.quote(job.smiles)
                    req = requests.get(urls)

                    soup = BeautifulSoup(req.text, 'html.parser')
                    jsonObject = json.loads(str(soup))

                    job_result = JobResult.objects.get(job_id=job.id)
                    job_result.result_json = jsonObject
                    job_result.save()
        except:
            return "API 호출 실패"