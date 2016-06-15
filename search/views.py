from django.http import JsonResponse, HttpResponse
from cmr import build_cmr_parms, send_cmr_request, parse_xml_response
import json
import csv


def granule(request):
    cmr_parms = build_cmr_parms(request.GET)
    xml_response = send_cmr_request(cmr_parms)
    results = parse_xml_response(xml_response)
    if request.GET.get('output', '') == 'CSV':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        writer = csv.writer(response)
        for result in results:
            row = [result[key] for key in result]
            writer.writerow(row)
        return response
    elif request.GET.get('output', '') == 'XML':
        return HttpResponse(xml_response, content_type='text/xml')
    return JsonResponse(results, safe=False)

