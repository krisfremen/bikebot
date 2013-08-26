#!/usr/bin/env python
# coding=utf-8
"""
"""
import re
import requests
import unicodedata
import time
import urllib
import urllib2
import parsedatetime.parsedatetime as pdt
import web
import sqlite3
import json
import pprint
import subprocess
import datetime
import random
import string
import bleach
import riak
from lxml import html
from BeautifulSoup import BeautifulSoup

bucket='bicycling'

def spank(phenny, input):
  if input.group(2):
    nick=input.group(2)
  else:
    nick=input.nick
  a=['',' with a spiked club', ' with a smile until it\'s gingerly red']
  return phenny.say("\001ACTION spanks " + nick + random.choice(a) + "\001")
spank.commands = ['spank']
spank.example = '.spank'

def amazon(phenny, input): 
    response = urllib2.urlopen('http://amzn.com/'+input.groups(2)[1],'lxml')
    html = response.read()
    soup = BeautifulSoup(html)
    ep=soup.find('span',{'id':'actualPriceValue'})
    return phenny.reply(bleach.clean(ep,tags=[], strip=True))
amazon.commands = ['ama']
amazon.example = '.ama'

def bible(phenny, input):
  return phenny.say('You can find the bicycle bible over at http://sheldonbrown.com/')
bible.commands = ['bible']
bible.example = '.bible'

#def karma(phenny, input):
#  inp = input.group(0).encode('ascii', 'ignore')
#  if inp[0] == '.':
#    return
#  for i in inp.split(' '):
#      if (i.endswith('++') or i.endswith('++;') or i.endswith('--') or i.endswith('--;')):
#          karm=i.split('++')[0]
#          if '--' in karm:
#              karm=i.split('--')[0]
#          if karm == '':
#              break
#          print('karm is ' + karm)
#          fetch=sqlquery('karma', karm,'karma')
#          if not fetch:
#              k=1
#          else:
#              if '--' in i:
#                  k=int(fetch[1])-1
#              else:
#                  k=int(fetch[1])+1
#          sqlrepsert('karma', karm, k ,'karma text primary key, karm text')
#          phenny.say(karm + ' has ' + str(k) +' karma')
#  return 
#karma.rule = r'.*(\+\+|\-\-).*'
#karma.priority = 'high'
#karma.thread = False

def skynet(phenny, input):
  return phenny.say('Skynet is now online!')
skynet.commands = ['skynet']
skynet.example = '.skynet'

def amgroma(phenny, input):
  return phenny.say('Your request has been submitted - Dr. Amgroma will be with you in just a moment.')
amgroma.commands = ['amgroma']
amgroma.example = '.amgroma'

def data(phenny, input):
  return phenny.say('Don\'t ask to ask, just ask')
data.commands = ['data']
data.example = '.data'

def forecast(phenny, input):
    if input.group(2):
        fetch=readdbattr(input.group(2).lower(),'location')
    else:
        fetch=readdbattr(input.nick.lower(),'location')
    if fetch:
        arg=fetch.split(".")[0]
        if arg.isdigit():
            arg=fetch.split(";")[0] #fetched something so use location from said nick
        else:
            arg=fetch.split(".")[0] #fetched something so use location from said nick
    else:
        arg=input.group(2) # look up arguments given (place)
    try:
        if not arg:
            return phenny.say("Location please?")
    except:
        pass
    fccoordsjs=json.loads(web.get("http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address="+arg))
    pprint.pprint(fccoordsjs)
    coords=fccoordsjs['results'][0]['geometry']['location']
    fciojs=web.get("https://api.forecast.io/forecast/"+ phenny.config.forecastapikey+"/"+str(coords['lat'])+','+str(coords['lng']))
    fcjs=json.loads(fciojs)
    pprint.pprint(fcjs)
    try:
        out='Currently : ' + fcjs['currently']['summary']
    except:
        try:
            out='Next few minutes : '+fcjs['minutely']['summary']
        except:
            out='Next Hour : ' + fcjs['hourly']['summary']
    return phenny.say(out)
forecast.commands = ['forecast']
forecast.example = '.forecast'

def weather(phenny, input):
  apikey=phenny.config.weatherundergroundapikey
  if input.group(2):
    fetch=readdbattr(input.group(2).lower(),'location')
    print fetch
    if fetch:
      arg=fetch.split(".")[0] #fetched something so use location from said nick
      if arg.isdigit():
        arg=fetch.split(";")[0] #fetched something so use location from said nick
      else:
        arg=fetch.split(".")[0] #fetched something so use location from said nick
    else:
      arg=input.group(2) # look up arguments given (place)
  else:
    fetch=readdbattr(input.nick.lower(),'location')
    print fetch
    if fetch:
      arg=fetch.split(".")[0] #fetched something so use location from said nick
      if arg.isdigit():
        arg=fetch.split(";")[0] #fetched something so use location from said nick
      else:
        arg=fetch.split(".")[0] #fetched something so use location from said nick
    else:
      arg=""
  if not arg:
    return phenny.reply("You either need to give me a place to look up or use .location set [place] for you to have a default location")
  wundero = web.get('http://api.wunderground.com/api/'+ apikey+'/conditions/q/' + arg.encode('utf-8') + '.json')
  wunderj=json.loads(wundero)
  pprint.pprint(wunderj)
  if not wunderj.get('current_observation'):
    return phenny.reply("You might want to be more specific with your query!")
  else:
    return phenny.reply(wunderj['current_observation']['observation_location']['city'] + ' is currently ' + wunderj['current_observation']['weather'] + ' \x02Temp:\x02 ' + wunderj['current_observation']['temperature_string'] + ' \x02Wind:\x02 ' + str(wunderj['current_observation']['wind_mph']) + 'MPH (' + str(wunderj['current_observation']['wind_kph']) + ' KPH / ' + str( "%.1f" % float(wunderj['current_observation']['wind_kph']*0.27777777)) + ' M/S)' + ' ' + wunderj['current_observation']['wind_dir'] + ' \x02Humidity:\x02 ' + wunderj['current_observation']['relative_humidity'] + ' at ' + wunderj['current_observation']['local_time_rfc822'] )
weather.commands = ['weather']
weather.example = '.weather'

def poke(phenny, input): 
  if input.group(2):
    return phenny.say(input.nick + " pokes " + input.group(2) + " oh so sensually")
  else:
    return phenny.say(input.nick + " pokes self oh so sensually")
poke.commands = ['poke']
poke.example = '.poke person'

def reddit(phenny, input): 
  if not input.group(2):
    return phenny.say("http://reddit.com/r/bicycling")
  orig = web.get('http://www.reddit.com/user/' + input.group(2) + '/about.json')
  j = json.loads(orig)
  return phenny.say(j['data']['name'] + ' has ' + str(j['data']['link_karma']) + ' link karma and ' + str(j['data']['comment_karma']) + ' comment karma')
reddit.commands = ['reddit']
reddit.example = '.reddit'

def nick(phenny, input): 
  if input.group(2):
    return phenny.say(input.group(2) +': Hello there, did you know you can change your nick by just typing "/nick nickhere" without the quotes?')
  else:
    return phenny.say('Hello there, did you know you can change your nick by just typing "/nick nickhere" without the quotes?')
nick.commands = ['nick']
nick.example = '.nick person'

def seltext(x):
  try:
    return {
      'martini': 'Shaken, not stirred. Just the way Bond likes it.',
      'rumandcoke': 'Captain Morgan or Bacardi Gold?',
      'whiskey': 'Shot of whiskey on the rocks coming up.',
      'rum':  'Where is the rum?! Why is the rum gone?!',
      'beer':  'Your beer is here!',
      'vodka': 'Here\'s your vodka sir!',
      'everclear': '151 proof or 190 proof',
      'coffee': 'Starbucks or aero?',
      'rbed': 'http://cyclingcuriosity.com/r/bicycling/doku.php/rbed',
      'fap': 'FaptainAwesome to the rescue!',
      'wig': 'Wiggie Wiggie Wedgie',
      'soap': 'Soap to the residue!',
    }[x]
  except KeyError:
    return ': tell krisfremen to implement this.. woops!'

def texts(phenny, input): 
  resp=seltext(input.group(1))
  if input.group(2):
    return phenny.say(input.group(2) +': ' + resp)
  else:
    return phenny.say(resp)
texts.commands = ['martini','rumandcoke','whiskey','rum','beer','vodka','coke','gin','tequila','brandy','everclear', 'coffee', 'rbed', 'fap','soap', 'wig']
texts.example = '.something [person]'

def velotext(x):
  try:
    return {
            'kris1': 'Don\'t eat/drink anything non-fat!',
            '101': 'Lighten The Fuck Up',
            '1': 'Obey The Rules.',
            '2': 'Lead by example.',
            '3': 'Guide the uninitiated.',
            '4': 'It\'s all about the bike.',
            '5': 'Harden The Fuck Up.',
            '6': 'Free your mind and your legs will follow.',
            '7': 'Tan lines should be cultivated and kept razor sharp.',
            '8': 'Saddles, bars, and tires shall be carefully matched.',
            '9': 'If you are out riding in bad weather, it means you are a badass.',
            '10': 'It never gets easier, you just go faster.',
            '11': 'Family does not come first. The bike does.',
            '12': 'The correct number of bikes to own is n+1.',
            '13': 'If you draw race number 13, turn it upside down.',
            '14': 'Shorts should be black.',
            '15': 'Black shorts should also be worn with leader\'s jerseys.',
            '16': 'Respect the jersey.',
            '17': 'Team kit is for members of the team.',
            '18': 'Know what to wear. Don\'t suffer kit confusion.',
            '19': 'Introduce Yourself.',
            '20': 'There are only three remedies for pain.',
            '21': 'Cold weather gear is for cold weather.',
            '22': 'Cycling caps are for cycling.',
            '23': 'Tuck only after reaching Escape Velocity.',
            '24': 'Speeds and distances shall be referred to and measured in clicks and meters',
            '25': 'The bikes on top of your car should be worth more than the car.',
            '26': 'Make your bike photogenic.',
            '27': 'Shorts and socks should be like Goldilocks.',
            '28': 'Socks can be any damn colour you like.',
            '29': 'No European Posterior Man-Satchels.',
            '30': 'No frame-mounted pumps.',
            '31': 'Spare tubes, multi-tools and repair kits should be stored in jersey',
            '32': 'Humps are for camels: no hydration packs.',
            '33': 'Shave your guns.',
            '34': 'Mountain bike shoes and pedals have their place.',
            '35': 'No visors on the road.',
            '36': 'Eyewear shall be cycling specific.',
            '37': 'The arms of the eyewear shall always be placed over the helmet',
            '38': 'Don\'t Play Leap Frog.',
            '39': 'Never ride without your eyewear.',
            '40': 'Tires are to be mounted with the label centered over the valve',
            '41': 'Quick-release levers are to be carefully positioned.',
            '42': 'A bike race shall never be preceded with a swim and/or followed by a run',
            '43': 'Don\'t be a jackass.',
            '44': 'Position matters.',
            '45': 'Slam your stem.',
            '46': 'Keep your bars level.',
            '47': 'Drink Tripels, don\'t ride triples.',
            '48': 'Saddles must be level and pushed back.',
            '49': 'Keep the rubber side down.',
            '50': 'Facial hair is to be carefully regulated.',
            '51': 'Livestrong wristbands are cockrings for your arms.',
            '52': 'Drink in Moderation.',
            '53': 'Keep your kit clean and new.',
            '54': 'No aerobars on road bikes.',
            '55': 'Earn your turns.',
            '56': 'Espresso or macchiato only.',
            '57': 'No stickers.',
            '58': 'Support your local bike shop.',
            '59': 'Hold your line.',
            '60': 'Ditch the washer-nut and valve-stem cap.',
            '61': 'Like your guns, saddles should be smooth and hard.',
            '62': 'You shall not ride with earphones.',
            '63': 'Point in the direction you\'re turning.',
            '64': 'Cornering confidence increases with time and experience.',
            '65': 'Maintain and respect your machine.',
            '66': 'No mirrors. http://cdn.memegenerator.net/instances/400x/35774736.jpg',
            '67': 'Do your time in the wind.',
            '68': 'Rides are to be measured by quality, not quantity.',
            '69': 'Cycling shoes and bicycles are made for riding.',
            '70': 'The purpose of competing is to win.',
            '71': 'Train Properly.',
            '72': 'Legs speak louder than words.',
            '73': 'Gear and brake cables should be cut to optimum length.',
            '74': 'V Meters or small computers only.',
            '75': 'Race numbers are for races.',
            '76': 'Helmets are to be hung from your stem.',
            '77': 'Respect the earth; don\'t litter.',
            '78': 'Remove unnecessary gear.',
            '79': 'Fight for your town lines.',
            '80': 'Always be Casually Deliberate.',
            '81': 'Don\'t talk it up.',
            '82': 'Close the gap.',
            '83': 'Be self-sufficient.',
            '84': 'Follow the Code.',
            '85': 'Descend like a Pro.',
            '86': 'Don\'t half-wheel.',
            '87': 'The Ride Starts on Time. No exceptions.',
            '88': 'Don\'t surge.',
            '89': 'Pronounce it Correctly.',
            '90': 'Never Get Out of the Big Ring.',
            '91': 'No Food On Training Rides Under Four Hours.',
    }[x]
  except KeyError:
    return 'Either krisfremen missed this one.. or there is no such rule!'

def velo(phenny, input):
  ircn=input.nick
  if input.group(2):
    if '>' in input.group(2):
      ircn=string.lstrip(string.split(input.group(2),'>')[1])
      rnum = string.strip(string.split(input.group(2),'>')[0])
      resp=': #' + rnum + ' ' + velotext(rnum)
    else:
      rnum = input.group(2)
      resp=': #' + rnum + ' '+ velotext(rnum)
  else:
    random.seed()
    rnum=str(random.randint(1,91))
    resp=': #' + rnum + ' ' +  velotext(rnum)
  return phenny.say(ircn + resp)
velo.commands = ['velo','rule']
velo.example = '.velo number'

def rotd(phenny, input):
  random.seed(time.strftime("%Y-%m-%d"))
  ran=random.randint(1,91)
  resp=velotext(str(ran))
  return phenny.say(input.nick + ': #' + str(ran) + ' ' + resp)
rotd.commands = ['rotd']
rotd.example = '.velo number'

def help(phenny, input): 
  return phenny.say('Take a look at http://cyclingcuriosity.com/r/bicycling')
help.commands = ['help']
help.example = '.help'

def fortune(phenny, input): 
  if not input.group(2):
    p = subprocess.Popen('fortune', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, error = p.communicate()
  else:
    p = subprocess.Popen(['fortune', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, error = p.communicate()
  return phenny.say(out.replace('\t',' '))
fortune.commands = ['fortune']
fortune.example = '.fortune'

def readdb(key):
    r=riak.RiakClient(port=8087, transport_class=riak.RiakPbcTransport)
    b=r.bucket(bucket)
 #   print 'readdb data'+ str(b.get(key).data)
    return b.get(key).get_data()

def readdbattr(key,attr):
    r=readdb(key)
    if r:
      try:
        return r[attr]
      except:
        return None
    return None

def updatedbattr(key, attr, data):                                                                                                                                                     
    old=readdb(key)
    if old:
        old[attr]=data
    else:
        old={attr:data}
    savedb(key,old)

def savedb(key, data):                                                                                                                                                       
    db=riak.RiakClient(port=8087, transport_class=riak.RiakPbcTransport)
    user_bucket=db.bucket(bucket)
    new_user=user_bucket.new(key, data)
    new_user.store()

def sqlquery(table, nick, key='person'):
  conn = sqlite3.connect('bicycling.db')
  cur = conn.cursor()
  cur.execute('SELECT * FROM ' + table + ' WHERE '+key+'=? LIMIT 1 COLLATE NOCASE', (nick,))
  return cur.fetchone()

def sqlrepsert(table, key, value, dblayout):
  conn = sqlite3.connect('bicycling.db')
  cur = conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS "+table+" (  " + dblayout +   ")")
  #cur.execute("CREATE TABLE IF NOT EXISTS location (person text primary key, location text)")
  sql="insert or replace into " + table + " values(?, ?)"
  cur.execute(sql, (key, value))
  conn.commit()

def photo(phenny, input): 
  n=input.nick
  r=" looks like "
  l=""
  if not input.group(2):
    fetch=readdbattr(n.lower(),'photo')
    if fetch:
      l=fetch
    else:
      r=": Give me a photo with .photo set [photohere]"
  else:
    t = unicodedata.normalize('NFKD', input.group(2)).encode('ascii', 'ignore').split(' ')
    if len(t) >= 1:
      if t[0] == 'set':
        if len(t) < 2:
          r='Where da ya live, duncey?'
        else:
          updatedbattr(n.lower(), 'photo',input.group(2)[4:])
          return phenny.say('Saving your photo!')
      else:
        n=t[0].lower()
        fetch=readdbattr(n,'photo')
        if fetch:
          l=fetch
        else:
          r=": Give me a photo with .photo set [photohere]"
  return phenny.say(n + r + l)
photo.commands = ['photo']
photo.example = '.photo set/person [photo]'

def nearby(phenny,input):
  location=readdbattr(input.nick, 'gpslocation')
  if location:
    location.replace(" ","%20")
  else:
    return phenny.say("You haven't set your location, please use .gpslocation set LAT,LONG")
  if gpslocation:
    presp=urllib2.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+location+"&name=%22" +input.group(2).replace(" ","%20")+ "%22&sensor=false&rankby=distance&key=CHANGETHISTHING").read()
    prespjs=json.loads(presp)
    print(presp)
    if prespjs['status'] == 'ZERO_RESULTS':
      return phenny.say("None found")
    else:
      return phenny.say(prespjs['results'][0]['name'] + ' ' + prespjs['results'][0]['vicinity'])
nearby.commands = ['nearby']

def gpslocation(phenny, input): 
  n=input.nick
  r=" is currently at "
  l=""
  if not input.group(2):
    fetch=readdbattr(n.lower(),'gpslocation')
    if fetch:
      l=fetch
    else:
      r=": Give me a location with .gpslocation set [locationhere]"
  else:
    t = unicodedata.normalize('NFKD', input.group(2)).encode('ascii', 'ignore').split(' ')
    if len(t) >= 1:
      if t[0] == 'set':
        if len(t) < 2:
          r='Where are ya, duncey?'
        else:
          updatedbattr(n.lower(), 'gpslocation',input.group(2)[4:])
          return phenny.say('Saving your weird location... Is your place bike friendly?' )
      else:
        n=t[0]
        fetch=readdbattr(n.lower(),'gpslocation')
        if fetch:
          l=fetch
        else:
          r=": Give me a location with .location set [locationhere]"
  return phenny.say(n + r + l)
gpslocation.commands = ['gpslocation']
gpslocation.example = '.gpslocation set/person [location]'




def location(phenny, input): 
  n=input.nick
  r=" lives in "
  l=""
  if not input.group(2):
    fetch=readdbattr(n.lower(),'location')
    if fetch:
      l=fetch
    else:
      r=": Give me a location with .location set [locationhere]"
  else:
    t = unicodedata.normalize('NFKD', input.group(2)).encode('ascii', 'ignore').split(' ')
    if len(t) >= 1:
      if t[0] == 'set':
        if len(t) < 2:
          r='Where da ya live, duncey?'
        else:
          updatedbattr(n.lower(), 'location',input.group(2)[4:])
          return phenny.say('Saving your weird location... Is your place bike friendly?' )
      else:
        n=t[0]
        fetch=readdbattr(n.lower(),'location')
        if fetch:
          l=fetch
        else:
          r=": Give me a location with .location set [locationhere]"
  return phenny.say(n + r + l)
location.commands = ['location']
location.example = '.location set/person [location]'

def about(phenny, input): 
  n=input.nick
  r="Interesting fact about "
  l=""
  if not input.group(2):
    fetch=readdbattr(n.lower(),'about')
    if fetch:
      l=n+': '+fetch
      n=""
    else:
      r=": Give me a story with .about set [abouthere]"
  else:
    t = unicodedata.normalize('NFKD', input.group(2)).encode('ascii', 'ignore').split(' ')
    if len(t) >= 1:
      if t[0] == 'set':
        if len(t) < 2:
          r='What\'s yer story, mate?'
        else:
          updatedbattr(n.lower(), 'about',input.group(2)[4:])
          return phenny.say('Saving your factoid!' )
      else:
        n=t[0]
        fetch=readdbattr(n.lower(),'about')
        if fetch:
          l=n+': '+fetch
          n=""
        else:
          r=": Give me a story with .about set [abouthere]"
  return phenny.say( n+ r+l)
about.commands = ['about']
about.example = '.about set/person [about]'

def strava2(phenny, input):
#    cookies=dict(_strava3_session="BAh7C0kiD3Nlc3Npb25faWQGOgZFRkkiJWI5OTNiMjFhMGQ3ZmE4ZWQ1ODEwZTczOWNiMWZmZjk3BjsAVEkiEGNsZWFyX2NsaWNrBjsARlRJIhBfY3NyZl90b2tlbgY7AEZJIjFBVWk5U0lrQ2laeWhvVWZ1T00vNWlJby9tb3JWY1g0azlxdzBDbnM4UERRPQY7AEZJIhRjYW1wYWlnbl9yZXN1bHQGOwBGSSI6MU1UMWhkR2hzWlhSbE96STljM1J5WVhaaFgyUnBjbVZqZEc5eWVUczBQVEk0TXpNME9RPT0GOwBGSSIHaWQGOwBGaQNFzQhJIhxyZWRpcmVjdF90b19hZnRlcl9sb2dpbgY7AEYiFS9hdGhsZXRlcy93aWxtZXI%3D--e5ec2c91ae2d4a13df88aae80add9d007be4e5c6")
#    cookies=dict(strava_remember_id="576837", strava_remember_code="1e24da821de4819b64", _strava3_session="BAh7CUkiD3Nlc3Npb25faWQGOgZFRkkiJTUxYTRkMDYyZDI1MzMxNzJiOGI2NTViODM5MTQ3YjJkBjsAVEkiEGNsZWFyX2NsaWNrBjsARlRJIhBfY3NyZl90b2tlbgY7AEZJIjFBbitxd0kzOHh1bEpjVHFKQjFDQmt1RTVKT0ZQRmp1L1FFQkgxNVdRaWdVPQY7AEZJIgdpZAY7AEZpA0XNCA%3D%3D--7fe09a964729a069a5bdc4d706ea57ec17436646")
    r=requests.get('http://krisfremen.com/tools/stravaproxy/athletes/krisfremen')
    tex=html.document_fromstring(r.text)
    print(r.url)
    urls=tex.xpath('//a/@href')
    for i in urls:
        if 'activities' in i:
            r=requests.get('http://krisfremen.com/tools/stravaproxy/'+i)
#            print(r.text)
            print(i)
            return
strava2.commands = ['strava2']
strava2.example = '.strava2 [username/id]'



def strava(phenny, input):
  return phenny.reply("Strava is no worky because of API updates. Until Strava releases their API to the public. No can do.")
  n=input.nick
  r=" lives in "
  l=""
  if not input.group(2):
    fetch=readdbattr(n.lower(),'strava')
    if fetch:
      l=fetch
    else:
      return
  else:
    t = unicodedata.normalize('NFKD', input.group(2)).encode('ascii', 'ignore').split(' ')
    if len(t) >= 1:
      if t[0] == 'set':
        if len(t) < 2:
          return 
        else:
          updatedbattr(n.lower(), 'strava',input.group(2)[4:])
          return phenny.say('Strava set up!')
      else:
        n=t[0]
        fetch=readdbattr(n.lower(),'strava')
        if fetch:
          l=fetch
        else:
          return
  saresp=urllib2.urlopen('http://www.strava.com/api/v1/rides/' + l).read()
  pprint.pprint(saresp)
  erract=False
  if 'error' in saresp:
      erract=True
  else:
      js2resp=json.loads(saresp)
  pprint.pprint(erract)
  sresp=web.get('http://www.strava.com/api/v1/rides?athleteName=' + l);
  pprint.pprint(sresp)
  if erract==True:
      if 'rides' in sresp:
          jsresp=json.loads(sresp)
          jsrespid=jsresp['rides'][0]
          pprint.pprint(jsrespid)
          s2resp=web.get('http://www.strava.com/api/v1/rides/' + str(jsresp['rides'][0]['id']))
          js2resp=json.loads(s2resp)
          pprint.pprint(js2resp)
      else:
          phenny.reply('something gone wrong tell krisfremen')
          return
  phenny.reply(js2resp['ride']['athlete']['username'] + ' rode ' + "%.2f" % float(js2resp['ride']['distance']/1000)  + ' km ('+ "%.2f" % float((js2resp['ride']['distance']/1000)*0.621371)  +' mi) in ' + str(datetime.timedelta(seconds=js2resp['ride']['elapsedTime'])) + ' (' +str(datetime.timedelta(seconds=js2resp['ride']['movingTime'])) + ' moving) averaging ' + "%.2f" % float(js2resp['ride']['averageSpeed']*3.6) + ' kph (' + "%.2f" % float((js2resp['ride']['averageSpeed']*3.6)*0.621371) + ' mph) climbing ' +  "%.2f" % float((js2resp['ride']['elevationGain'])) + 'm (' + "%.2f" % float((js2resp['ride']['elevationGain'])*3.2808399)  +   ' ft) on ' + time.strftime('%b %d, %Y',time.strptime(js2resp['ride']['startDate'],'%Y-%m-%dT%H:%M:%SZ')) + ' titled ' + js2resp['ride']['name'])
strava.commands = ['strava']
strava.example = '.strava [username/id]'

def bike(phenny, input): 
  n=input.nick
  r=" has "
  l=""
  if not input.group(2):
    fetch=readdbattr(n.lower(),'bike')
    if fetch:
      l=fetch
    else:
      r=": Give me a bike with .bike set [bikehere]"
  else:
    t = unicodedata.normalize('NFKD', input.group(2)).encode('ascii', 'ignore').split(' ')
    if len(t) >= 1:
      if t[0] == 'set':
        if len(t) < 2:
          r='Where da ya live, duncey?'
        else:
          updatedbattr(n.lower(), 'bike',input.group(2)[4:])
          return phenny.say('Saving your weird bike... Is your place bike friendly?' )
      else:
        n=t[0]
        fetch=readdbattr(n.lower(),'bike')
        if fetch:
          l=fetch
        else:
          r=": Give me a bike with .bike set [bikehere]"
  return phenny.say(n + r + l)
bike.commands = ['bike']
bike.example = '.bike set/person [bike]'

def bikephoto(phenny, input): 
  n=input.nick
  r="'s bikes look like "
  l=""
  if not input.group(2):
    fetch=readdbattr(n.lower(),'bikephoto')
    if fetch:
      l=fetch
    else:
      r=": Give me a bikephoto with .bikephoto set [bikephotohere]"
  else:
    t = unicodedata.normalize('NFKD', input.group(2)).encode('ascii', 'ignore').split(' ')
    if len(t) >= 1:
      if t[0] == 'set':
        if len(t) < 2:
          r='Where da ya live, duncey?'
        else:
          updatedbattr(n.lower(), 'bikephoto',input.group(2)[4:])
          return phenny.say('Saving your weird bikephoto... Is your place bikephoto friendly?' )
      else:
        n=t[0]
        fetch=readdbattr(n.lower(),'bikephoto')
        if fetch:
          l=fetch
        else:
          r=": Give me a bikephoto with .bikephoto set [bikephotohere]"
  return phenny.say(n + r + l)
bikephoto.commands = ['bikephoto']
bikephoto.example = '.bikephoto set/person [bikephoto]'







def chainlove(phenny, input): 
  orig = web.get('http://www.chainlove.com')
  soup = BeautifulSoup(orig.replace('</sc\'+\'ript>','</script>').replace("\"src="," src="))
#  print soup
  tl = ((20*60 - abs(int(orig[orig.find("prev_items"):orig.find('],"price":')].split(',')[-1]) - int(time.time()))))
  return phenny.say(soup.html.head.title.string.replace('Chainlove.com: ','http://chainlove.com - ') + " - " +str(tl/60) + ":" + str(tl%60) + " left")
chainlove.commands = ['chainlove']
chainlove.example = '.chainlove'

def steepandcheap(phenny, input): 
  orig = web.get('http://www.steepandcheap.com')
  soup = BeautifulSoup(orig.replace('</sc\'+\'ript>','</script>').replace("\"src="," src="))
#  print soup
  tl = ((20*60 - abs(int(orig[orig.find("prev_items"):orig.find('],"price":')].split(',')[-1]) - int(time.time()))))
  return phenny.say(soup.html.head.title.string.replace('Chainlove.com: ','http://steepandcheap.com - ') + " - " +str(tl/60) + ":" + str(tl%60) + " left")
steepandcheap.commands = ['steepandcheap']
steepandcheap.example = '.steepandcheap'

def google_search(query):  
    results = google_ajax(query) 
    try: return results['responseData']['results'][0]['unescapedUrl'] 
    except IndexError: return None 
    except TypeError:  
        print results 
        return False 

def google_ajax(query): 
   """Search using AjaxSearch, and return its JSON."""
   if isinstance(query, unicode): 
      query = query.encode('utf-8')
   uri = 'http://ajax.googleapis.com/ajax/services/search/web'
   args = '?v=1.0&safe=off&q=' + web.urllib.quote(query)
   handler = web.urllib._urlopener
   web.urllib._urlopener = Grab()
   bytes = web.get(uri + args)
   web.urllib._urlopener = handler
   return web.json(bytes)

class Grab(web.urllib.URLopener):
   def __init__(self, *args):
      self.version = 'Mozilla/5.0 (Phenny)'
      web.urllib.URLopener.__init__(self, *args)
      self.addheader('Referer', 'https://github.com/sbp/phenny')
   def http_error_default(self, url, fp, errcode, errmsg, headers):
      return web.urllib.addinfourl(fp, [headers, errcode], "http:" + url)

def pt(phenny, input): 
   query = 'site:parktool.com ' +input.group(2)
   if not query: 
      return phenny.reply('.pt what?')
   query = query.encode('utf-8')
   uri = google_search(query)
   if uri: 
      phenny.reply(uri)
      if not hasattr(phenny.bot, 'last_seen_uri'):
         phenny.bot.last_seen_uri = {}
      phenny.bot.last_seen_uri[input.sender] = uri
   elif uri is False: phenny.reply("Problem getting data from Google.")
   else: phenny.reply("No results found for that, sorry." % query)
pt.commands = ['pt']
pt.example = '.pt'

def sb(phenny, input): 
   query = 'site:sheldonbrown.com ' +input.group(2)
   if not query: 
      return phenny.reply('.g what?')
   query = query.encode('utf-8')
   uri = google_search(query)
   if uri: 
      phenny.reply(uri)
      if not hasattr(phenny.bot, 'last_seen_uri'):
         phenny.bot.last_seen_uri = {}
      phenny.bot.last_seen_uri[input.sender] = uri
   elif uri is False: phenny.reply("Problem getting data from Google.")
   else: phenny.reply("No results found for that, sorry.")
sb.commands = ['sb']
sb.example = '.sb'

def bikeconversion(phenny, input):
  inp = input.group(0).encode('ascii', 'ignore')
  if inp[0] == '.':
    return
#  print type(inp)
#  print inp
  reg = re.compile("((\d*|\d\.\d) miles)")
  matches = reg.findall(inp)
#  for mat in matches:
#    inp = inp.replace( mat, convertvals(mat))
#    print mat
#    print convertvals(mat)
  #print inp
  return
bikeconversion.rule = r'.*( miles(,|\.| |$)| km( |,|\.| )).*'
bikeconversion.priority = 'high'
bikeconversion.thread = False

def convertvals(imperial):
   q = imperial
   q = q.replace('\xcf\x95', 'phi') # utf-8 U+03D5
   q = q.replace('\xcf\x80', 'pi') # utf-8 U+03C0
   uri = 'http://www.google.com/ig/calculator?q='
   bytes = web.get(uri + web.urllib.quote(q))
   parts = bytes.split('",')
   answer = [p for p in parts if p.startswith('rhs: "')][0][6:]
   if answer:
      answer = answer.decode('unicode-escape')
      answer = ''.join(chr(ord(c)) for c in answer)
      answer = answer.decode('utf-8')
      answer = answer.replace(u'\xc2\xa0', ',')
      answer = answer.replace('<sup>', '^(')
      answer = answer.replace('</sup>', ')')
      answer = web.decode(answer)
      return answer
   else: return 0

def quote(phenny, input): 
  if not input.group(2):
    conn = sqlite3.connect('bicycling.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1 ')
    fetch=cur.fetchone()
    phenny.reply(fetch[0])
  else:
    t = unicodedata.normalize('NFKD', input.group(2)).encode('ascii', 'ignore').split(' ')
    conn = sqlite3.connect('bicycling.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS quotes (quote text)")
    sql="insert or replace into quotes values(?)"
    cur.execute(sql, (input.group(2),))
    conn.commit()
quote.commands = ['quote']
quote.example = '.quote set/person [quote]'

def wiggie(q):
    return str(int(re.search("\d+",q).group(0))*5) + ' '+re.search("\w+$",q).group(0)+'s'

def c(phenny, input): 
    """Google calculator."""
    if not input.group(2):
        return phenny.reply("Nothing to calculate.")
    q = input.group(2).encode('utf-8')
    q = q.replace('\xcf\x95', 'phi') # utf-8 U+03D5
    q = q.replace('\xcf\x80', 'pi') # utf-8 U+03C0
    if "wiggie" in q:
        return phenny.say(wiggie(q))
    uri = 'http://www.google.com/ig/calculator?q='

    addon=""
    if not "to" in q and re.search("m$",q,re.IGNORECASE):
        addon =' to feet'
    if not "to" in q and re.search("km$",q,re.IGNORECASE):
        addon =' to miles'
    if not "to" in q and re.search("c$",q,re.IGNORECASE):
        addon =' to fahrenheit'
    if not "to" in q and re.search("f$",q,re.IGNORECASE):
        addon =' to celsius'
    print uri
    bytes = web.get(uri + web.urllib.quote(q+addon))
    parts = bytes.split('",')
    answer = [p for p in parts if p.startswith('rhs: "')][0][6:]
    if answer: 
        answer = answer.decode('unicode-escape')
        answer = ''.join(chr(ord(c)) for c in answer)
        answer = answer.decode('utf-8')
        answer = answer.replace(u'\xc2\xa0', ',')
        answer = answer.replace('<sup>', '^(')
        answer = answer.replace('<sub>', '_(')
        answer = answer.replace('</sub>', ')_')
        answer = answer.replace('</sup>', ')')
        answer = web.decode(answer)
        phenny.say(answer)
    else: phenny.say('Sorry, no result.')
c.commands = ['c']
c.example = '.c 5 + 3'

if __name__ == '__main__': 
  print __doc__.strip()
