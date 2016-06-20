import urllib
import urllib2
import xml.etree.cElementTree as ET
#TODO add logging


# translate legacy ASF platform values into CMR platform values
def translate_platform(plat):
   dict = {
             'SA': 'Sentinel-1A',
             'A3': 'ALOS',
             'E1': 'ERS-1',
             'E2': 'ERS-2',
             'J1': 'JERS-1',
             'R1': 'RADARSAT-1',
             'SP': 'SMAP',
             'UAVSAR': 'G-III',
             'UA': 'G-III',
             'AIRMOSS': 'G-III',
             'AI': 'G-III',
             'AIRSAR': 'DC-8',
             'AS': 'DC-8',
             'SEASAT': 'SEASAT 1',
             'SS': 'SEASAT 1'
          }
   return dict.get(plat, plat)


# translate legacy ASF search parameters into CMR search parameters
def build_cmr_parms(asf_parms):
    cmr_parms = {}
    cmr_parms['options[attribute][or]'] = 'true'
    cmr_parms['attribute[]'] = []

    cmr_parms['provider'] = 'ASF'

    cmr_parms['page_size'] = asf_parms.get('maxResults', 2000)

    if 'platform' in asf_parms:
        cmr_parms['platform'] = [translate_platform(plat) for plat in asf_parms['platform'].split(',')]

    if 'processingLevel' in asf_parms:
        for level in asf_parms['processingLevel'].split(','):
            cmr_parms['attribute[]'].append('string,PROCESSING_TYPE,' + level)

    if 'granule_list' in asf_parms:
       cmr_parms['readable_granule_name'] = asf_parms['granule_list'].split(',')

    if 'start' in asf_parms or 'end' in asf_parms:
        cmr_parms['temporal'] = asf_parms.get('start', '') + ',' + asf_parms.get('end', '')

    if 'polygon' in asf_parms:
        cmr_parms['polygon'] = asf_parms['polygon']

    return cmr_parms


# TODO handle HTTP errors returned by CMR search request
def send_cmr_request(parms):
    # TODO move CMR URL to configuration settings
    url = 'https://cmr.earthdata.nasa.gov/search/granules.echo10'
    url_values = urllib.urlencode(parms, doseq=True)
    req = urllib2.Request(url, url_values)
    response = urllib2.urlopen(req)
    xml_response = response.read()
    return xml_response


def attr(name):
    return "./AdditionalAttributes/AdditionalAttribute/[Name='" + name + "']/Values/Value"


def parse_cmr_xml_response(xml):
    root = ET.fromstring(xml)
    results = []
    for result in root.iter('result'):
        for granule in result.iter('Granule'):
            results.append({
                'granuleName': granule.findtext("./DataGranule/ProducerGranuleId"),
                'sizeMB': granule.findtext("./DataGranule/SizeMBDataGranule"),
                'processingDate':  granule.findtext("./DataGranule/ProductionDateTime"),
                'startTime':  granule.findtext("./Temporal/RangeDateTime/BeginningDateTime"),
                'stopTime':  granule.findtext("./Temporal/RangeDateTime/EndingDateTime"),
                'absoluteOrbit': granule.findtext("./OrbitCalculatedSpatialDomains/OrbitCalculatedSpatialDomain/OrbitNumber"),
                'platform': granule.findtext(attr('ASF_PLATFORM')),
                'md5': granule.findtext(attr('MD5SUM')),
                'beamMode': granule.findtext(attr('BEAM_MODE_TYPE')),
                'configurationName': granule.findtext(attr('BEAM_MODE_DESC')),
                'bytes': granule.findtext(attr("BYTES")),
                'granuleType':  granule.findtext(attr('GRANULE_TYPE')),
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
                'processingType':  granule.findtext(attr('PROCESSING_LEVEL')),
                'finalFrame':  granule.findtext(attr('CENTER_ESA_FRAME')),
                'centerLat':  granule.findtext(attr('CENTER_LAT')),
                'centerLon':  granule.findtext(attr('CENTER_LON')),
                'polarization':  granule.findtext(attr('POLARIZATION')),
                'faradayRotation':  granule.findtext(attr('FARADAY_ROTATION')),
                'stringFootprint': None,
                'doppler': granule.findtext(attr('DOPPLER')),
                'baselinePerp': granule.findtext(attr('INSAR_BASELINE')),
                'insarStackSize': granule.findtext(attr('INSAR_STACK_SIZE')),
                'processingDescription': granule.findtext(attr('PROCESSING_DESCRIPTION')),
                'product_file_id': None,
                'percentTroposphere': None,
                'frameNumber': granule.findtext(attr('FRAME_NUMBER')),
                'percentCoherence': None,
                'productName': None,
                'masterGranule': None,
                'percentUnwrapped': None,
                'beamSwath': None,
                'insarGrouping': granule.findtext(attr('INSAR_STACK_ID')),
                'offNadirAngle': granule.findtext(attr('OFF_NADIR_ANGLE')),
                'missionName': granule.findtext(attr('MISSION_NAME')),
                'relativeOrbit': granule.findtext(attr('PATH_NUMBER')),
                'flightLine': granule.findtext(attr('FLIGHT_LINE')),
                'processingTypeDisplay': granule.findtext(attr('PROCESSING_TYPE_DISPLAY')),
                'track': None,
                'beamModeType': granule.findtext(attr('BEAM_MODE_TYPE')),
                'processingLevel': granule.findtext(attr('PROCESSING_TYPE')),
                'lookDirection': granule.findtext(attr('LOOK_DIRECTION')),
                'varianceTroposphere': None,
                'slaveGranule': None,
                'sensor': None,
                'fileName': granule.findtext("./OnlineAccessURLs/OnlineAccessURL/URL").split('/')[-1],
                'downloadUrl': granule.findtext("./OnlineAccessURLs/OnlineAccessURL/URL"),
                'browse': granule.findtext("./AssociatedBrowseImageUrls/ProviderBrowseUrl/URL")
            })
    return results


def execute_cmr_search(query_parms):
    cmr_parms = build_cmr_parms(query_parms)
    xml_response = send_cmr_request(cmr_parms)
    results = parse_cmr_xml_response(xml_response)
    return results

