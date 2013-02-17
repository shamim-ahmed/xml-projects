#!/usr/bin/python

from httplib import HTTPConnection
import urllib
import cgi
from lxml import etree

print "Content-type:text/plain"
print

form = cgi.FieldStorage()

result = ""

if 'location' in form:
    loc = form['location'].value
    state = ""
    
    if 'state' in form:
        state = form['state'].value
        loc += " " + state
        
    loc += " AU" 
    params = urllib.urlencode({"address": loc, "sensor":"false"})
    conn = HTTPConnection("maps.googleapis.com")
    conn.request("GET", "/maps/api/geocode/xml?%s" % params)
    resp = conn.getresponse()
    
    if resp.status == 200:
        data = resp.read()
        xmltree = etree.fromstring(data)
        lat = xmltree.xpath("/GeocodeResponse/result/geometry/location/lat/text()")
        lng = xmltree.xpath("/GeocodeResponse/result/geometry/location/lng/text()")
        
        if len(lat) > 0 and len(lng) > 0:
            result = lat[0] + "|" + lng[0]
    
    resp.close()        
    conn.close()
    
print result
