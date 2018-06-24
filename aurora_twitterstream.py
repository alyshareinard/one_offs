import oauth2 as oauth
import urllib2 as urllib
import sys
import json

# See Assginment 6 instructions or README for how to get these credentials
access_token_key = "539211368-8ophAsphcSnn1t38rUODDdEk29upyC3CvC8unvEk"
access_token_secret = "euRSH9cNLMV9Ig9MVeAywY31gmnDBfuuG3QzBTbu1cg"

consumer_key = "5p3iiRRDOuPTTHYlTXfWgw"
consumer_secret = "rjU0AzOiOrNffqKen3xbVT92J5GAVX1x32iaNhiOp8"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
    url = "https://stream.twitter.com/1/statuses/sample.json"
    url = "https://stream.twitter.com/1/statuses/filter.json?track=aurora"
    parameters = []
    response = twitterreq(url, "GET", parameters)
    count=0
    for line in response:
        count+=1
        if count%1000 == 0:
            print "still working..."
        if line[0] == "[" or line[0]=="{":
            #            print "line"+ line+ "line"
            line_strip=json.loads(line)

      #      print line_strip
            if u'text' in line_strip.keys():

                if 'RT' not in line_strip[u'text']:
                    print " "
                    print "text:", line_strip[u'text']

              #              print line_strip
                    temp=line_strip[u'user']
              #              print "temp", temp
                    if line_strip[u'geo'] !=None:
                        geo=line_strip[u'geo']
                        print "geo location:", geo[u'coordinates']
                    elif u'location' in temp.keys() and temp[u'location']!="":
                        print "location:", temp[u'location']
                    else:
                        print "no location given"

#if line_strip[u'place'] != None:
#print "place", line_strip[u'place']

                            #                        print "geo location name", geo[u'name']
#        else:
#            print "line[0]", line[0]

#        except:
#            print "empty string"



if __name__ == '__main__':
  fetchsamples()
