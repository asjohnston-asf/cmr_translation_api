import urllib
import urllib2
import xml.etree.cElementTree as ET


def build_cmr_parms(asf_parms):
    cmr_parms = {}
    cmr_parms['options[attribute][or]'] = 'true'
    cmr_parms['attribute[]'] = []

    cmr_parms['provider'] = 'ASF'

    cmr_parms['page_size'] = asf_parms.get('maxResults', 2000)

    if 'platform' in asf_parms:
        cmr_parms['platform'] = asf_parms['platform'].split(',')

    if 'processingLevel' in asf_parms:
        for level in asf_parms['processingLevel'].split(','):
            cmr_parms['attribute[]'].append('string,PROCESSING_TYPE,' + level)

    if 'granule_list' in asf_parms:
       cmr_parms['readable_granule_name'] = asf_parms['granule_list'].split(',')

    if 'start' in asf_parms or 'end' in asf_parms:
        cmr_parms['temporal'] = asf_parms.get('start', '') + ',' + asf_parms.get('end', '')

    if 'polygon' in asf_parms:
        cmr_parms['polygon'] = asf_parms['polygon']

    print str(cmr_parms)
    return cmr_parms


def send_cmr_request(parms):
    url = 'https://cmr.earthdata.nasa.gov/search/granules.echo10'
    url_values = urllib.urlencode(parms, doseq=True)
    print str(url_values)
    req = urllib2.Request(url, url_values)
    response = urllib2.urlopen(req)
    xml_response = response.read()
    return xml_response


def attr(name):
    return "./AdditionalAttributes/AdditionalAttribute/[Name='" + name + "']/Values/Value"


def parse_xml_response(xml):
    root = ET.fromstring(xml)
    results = []
    for result in root.iter('result'):
        for granule in result.iter('Granule'):
            results.append({
                'granuleName': granule.findtext("./DataGranule/ProducerGranuleId"),
                'sceneId': granule.findtext("./DataGranule/ProducerGranuleId"),
                'sizeMB': granule.findtext("./DataGranule/SizeMBDataGranule"),
                'processingTime':  granule.findtext("./DataGranule/ProductionDateTime"),
                'startTime':  granule.findtext("./Temporal/RangeDateTime/BeginningDateTime"),
                'endTime':  granule.findtext("./Temporal/RangeDateTime/EndingDateTime"),
                'absoluteOrbit': granule.findtext("./OrbitCalculatedSpatialDomains/OrbitCalculatedSpatialDomain/OrbitNumber"),
                'platform': granule.findtext(attr('ASF_PLATFORM')),
                'md5': granule.findtext(attr('MD5SUM')),
                'beamMode': granule.findtext(attr('BEAM_MODE_TYPE')),
                'beamModeDescription': granule.findtext(attr('BEAM_MODE_DESC')),
                'bytes': granule.findtext(attr("BYTES")),
                'granuleType':  granule.findtext(attr('GRANULE_TYPE')),
                'acquisitionDate': granule.findtext(attr('ACQUISITION_DATE')),
                'flightDirection': granule.findtext(attr('ASCENDING_DESCENDING')),
                'thumbnailUrl': granule.findtext(attr('THUMBNAIL_URL')),
                'farEndLat':  granule.findtext(attr('FAR_END_LAT')),
                'farStartLat':  granule.findtext(attr('FAR_START_LAT')),
                'nearStartLat':  granule.findtext(attr('NEAR_START_LAT')),
                'nearEndLat':  granule.findtext(attr('NEAR_END_LAT')),
                'farEndLon':  granule.findtext(attr('FAR_END_LON')),
                'farStartLon':  granule.findtext(attr('FAR_START_LON')),
                'nearStartLon':  granule.findtext(attr('NEAR_START_LON')),
                'nearEndLon':  granule.findtext(attr('NEAR_END_LON')),
                'processingType':  granule.findtext(attr('PROCESSING_TYPE')),
                'finalFrame':  granule.findtext(attr('FRAME_NUMBER')),
                'centerLat':  granule.findtext(attr('CENTER_LAT')),
                'centerLon':  granule.findtext(attr('CENTER_LON')),
                'polarization':  granule.findtext(attr('POLARIZATION')),
                'pathNumber':  granule.findtext(attr('PATH_NUMBER')),
                'faradayRotation':  granule.findtext(attr('FARADAY_ROTATION')),
                'ascendingDecending':  granule.findtext(attr('ASCENDING_DESCENDING')),
                'fileName': granule.findtext("./OnlineAccessURLs/OnlineAccessURL/URL").split('/')[-1],
                'downloadUrl': granule.findtext("./OnlineAccessURLs/OnlineAccessURL/URL"),
                'browseUrl': granule.findtext("./AssociatedBrowseImageUrls/ProviderBrowseUrl/URL")
            })
    return results

