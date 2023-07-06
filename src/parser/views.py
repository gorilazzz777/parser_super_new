import threading

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from services_api.api.s3_client import S3Client


# Create your views here.

class ReportsView(View):
    def get(self, request):
        report_type = request.GET.get('type', 'im')
        reports = [{'key': report['Key'], 'date': report['LastModified'],
                    'month': report['Key'].split('/')[-1].split('.')[0]} for report in
                   S3Client().list_objects(f'reports_{report_type}')['Contents']
                   if report['Key'] != 'reports/']
        reports = sorted(reports, key=lambda d: d['date'])
        params = {
            'reports': reports,
            'report_name': 'Парсинг ' + (
                'Интернет магазинов' if report_type == 'im' else 'ПиП ФЛ' if report_type == 'pip' else 'пунктов выдачи')
        }
        return render(request, 'parser/reports.html', params)

    def post(self, request):
        from parser.reports.im_report import ImReport
        from parser.reports.pip_report import PipReport

        if request.GET.get('type') == 'pip':
            t = threading.Thread(target=PipReport().create_report)
        else:
            t = threading.Thread(target=ImReport().create_report)
        t.start()
        return HttpResponseRedirect(request.path)