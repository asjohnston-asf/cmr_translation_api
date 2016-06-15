from django.http import JsonResponse, HttpResponse
from django.template import loader, Context
from cmr import build_cmr_parms, send_cmr_request, parse_xml_response
import json
import csv


def granule(request):
    cmr_parms = build_cmr_parms(request.GET)
    xml_response = send_cmr_request(cmr_parms)
    results = parse_xml_response(xml_response)

    output = request.GET.get('output', '').upper()

    if output == 'CSV':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="results.csv"'
        t = loader.get_template('search/csv.template')
        c = Context({'data': results})
        response.write(t.render(c))
        return response
    elif output == 'METALINK':
        response = HttpResponse(content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename="results.metalink"'
        t = loader.get_template('search/metalink.template')
        c = Context({'data': results})
        response.write(t.render(c))
        return response
    elif output == 'XML':
       return HttpResponse(xml_response, content_type='text/xml')
    return JsonResponse(results, safe=False)

