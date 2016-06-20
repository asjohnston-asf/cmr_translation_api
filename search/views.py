from django.http import JsonResponse, HttpResponse
from django.template import loader
from cmr import build_cmr_parms, send_cmr_request, parse_cmr_xml_response


def granule(request):
    cmr_parms = build_cmr_parms(request.GET)
    xml_response = send_cmr_request(cmr_parms)
    results = parse_cmr_xml_response(xml_response)

    output_format = request.GET.get('output', '').upper()

    if output_format == 'CSV':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="results.csv"'
        template = loader.get_template('search/csv.template')
        response.write(template.render({'results': results}))

    elif output_format == 'METALINK':
        response = HttpResponse(content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename="results.metalink"'
        template = loader.get_template('search/metalink.template')
        response.write(template.render({'results': results}))

    elif output_format == 'XML':
       response = HttpResponse(xml_response, content_type='text/xml')

    else:
        response = JsonResponse(results, safe=False)

    return response

