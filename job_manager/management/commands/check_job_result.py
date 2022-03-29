from django.core.management.base import BaseCommand
from job_user.models import JobResult, Job


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        job_results = JobResult.objects.all()
        for job_result in job_results:
            if isinstance(job_result.result_json, dict):
                if job_result.result_json['time'] != 'no_data' and job_result.result_json['time'] != 'exception':
                    job = Job.objects.get(pk=job_result.job_id)
                    job.job_status = 'complete'
                    job.save()
                elif job_result.result_json['time'] == 'exception':
                    job = Job.objects.get(pk=job_result.job_id)
                    job.job_status = 'fail'
                    job.save()
            elif isinstance(job_result.result_json, int):
                if job_result.result_json == 0 or job_result.result_json == 1:
                    job = Job.objects.get(pk=job_result.job_id)
                    job.job_status = 'complete'
                    job.save()