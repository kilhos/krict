from django.core.management.base import BaseCommand
from job_user.models import JobResult, Job


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
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