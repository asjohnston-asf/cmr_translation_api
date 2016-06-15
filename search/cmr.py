import urllib
import urllib2
import xml.etree.cElementTree as ET


def build_cmr_parms(asf_parms):
    cmr_parms = {}
    cmr_parms['attribute[]'] = []

    cmr_parms['provider'] = 'ASF'

    cmr_parms['page_size'] = asf_parms.get('maxResults', 2000)

    if 'platform' in asf_parms:
        for plat in asf_parms['platform'].split(','):
            cmr_parms['attribute[]'].append('string,ASF_PLATFORM,' + plat)

    if 'granule_list' in asf_parms:
       cmr_parms['readable_granule_name'] = asf_parms['granule_list'].split(',')

    if 'start' in asf_parms or 'end' in asf_parms:
        cmr_parms['temporal'] = asf_parms.get('start', '') + ',' + asf_parms.get('end', '')

    if 'polygon' in asf_parms:
        cmr_parms['polygon'] = asf_parms['polygon']

    return cmr_parms


def send_cmr_request(parms):
    url = 'https://cmr.earthdata.nasa.gov/search/granules.echo10'
    url_values = urllib.urlencode(parms, doseq=True)
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
                'platform': granule.findtext(attr('ASF_PLATFORM')),
                'md5': granule.findtext(attr('MD5SUM')),
                'beamMode': granule.findtext(attr('BEAM_MODE_TYPE')),
                'beamModeDescription': granule.findtext(attr('BEAM_MODE_DESC')),
                'granuleName': granule.findtext("./DataGranule/ProducerGranuleId"),
                'sizeMB': granule.findtext("./DataGranule/SizeMBDataGranule"),
                'bytes': granule.findtext(attr("BYTES")),
                'fileName': granule.findtext("./OnlineAccessURLs/OnlineAccessURL/URL").split('/')[-1],
                'granuleType':  granule.findtext(attr('GRANULE_TYPE')),
                'sceneId': granule.findtext("./DataGranule/ProducerGranuleId"),
                'absoluteOrbit': granule.findtext("./OrbitCalculatedSpatialDomains/OrbitCalculatedSpatialDomain/OrbitNumber"),
                'sceneDate': granule.findtext(attr('ACQUISITION_DATE')),
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
                'startTime':  granule.findtext("./Temporal/RangeDateTime/BeginningDateTime"),
                'endTime':  granule.findtext("./Temporal/RangeDateTime/EndingDateTime"),
                'centerLat':  granule.findtext(attr('CENTER_LAT')),
                'centerLon':  granule.findtext(attr('CENTER_LON')),
                'polarization':  granule.findtext(attr('POLARIZATION')),
                'browseUrl': granule.findtext("./AssociatedBrowseImageUrls/ProviderBrowseUrl/URL"),
                'downloadUrl': granule.findtext("./OnlineAccessURLs/OnlineAccessURL/URL")
            })
    return results

