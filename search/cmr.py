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

def parse_xml_response(xml):
    root = ET.fromstring(xml)
    results = []
    for result in root.iter('result'):
        for granule in result.iter('Granule'):
            results.append({
                'platform': granule.findtext("./AdditionalAttributes/AdditionalAttribute/[Name='ASF_PLATFORM']/Values/Value"),
                'granuleName': granule.findtext("./DataGranule/ProducerGranuleId"),
                'granuleType':  granule.findtext("./AdditionalAttributes/AdditionalAttribute/[Name='GRANULE_TYPE']/Values/Value"),
                'catSceneId': None,
                'sceneId': granule.findtext("./DataGranule/ProducerGranuleId"),
                'absoluteOrbit': granule.findtext("./OrbitCalculatedSpatialDomains/OrbitCalculatedSpatialDomain/OrbitNumber"),
                'track': None,
                'sceneDate': granule.findtext("./AdditionalAttributes/AdditionalAttribute/[Name='ACQUISITION_DATE']/Values/Value"),
                'flightDirection': granule.findtext("./AdditionalAttributes/AdditionalAttribute/[Name='ASCENDING_DESCENDING']/Values/Value"),
                'thumbnailUrl': granule.findtext("./AdditionalAttributes/AdditionalAttribute/[Name='THUMBNAIL_URL']/Values/Value"),
                'firstFrame': '',
                'finalFrame': '',
                'downloadUrl': granule.findtext("./OnlineAccessURLs/OnlineAccessURL/URL")
            })
    return results

