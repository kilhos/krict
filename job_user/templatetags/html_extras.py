from django import template

register = template.Library()


@register.filter(name='get_job_status_btn_class')
def get_job_status_btn_class(job_status):
    if job_status == 'complete':
        return 'button-status completed'
    elif job_status == 'waiting':
        return 'button-status waiting'
    elif job_status == 'running':
        return 'button-status running'
    elif job_status == 'fail':
        return 'button-status fail'
    elif job_status == 'stop':
        return 'button-status stop'


@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg
