#!/usr/bin/env python
# coding=utf-8
"""
"""
import re
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
from BeautifulSoup import BeautifulSoup

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

def karma(phenny, input):
  inp = input.group(0).encode('ascii', 'ignore')
  if inp[0] == '.':
    return
  for i in inp.split(' '):
      if (i.endswith('++') or i.endswith('++;') or i.endswith('--') or i.endswith('--;')):
          karm=i.split('++')[0]
          if '--' in karm:
              karm=i.split('--')[0]
          if karm == '':
              break
          print('karm is ' + karm)
          fetch=sqlquery('karma', karm,'karma')
          if not fetch:
              k=1
          else:
              if '--' in i:
                  k=int(fetch[1])-1
              else:
                  k=int(fetch[1])+1
          sqlrepsert('karma', karm, k ,'karma text primary key, karm text')
          phenny.say(karm + ' has ' + str(k) +' karma')
  return 
karma.rule = r'.*(\+\+|\-\-).*'
karma.priority = 'high'
karma.thread = False

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
        fetch=sqlquery('location', input.group(2))
        if fetch:
            arg=fetch[1].split(".")[0]
            if arg.isdigit():
                arg=fetch[1].split(";")[0] #fetched something so use location from said nick
            else:
                arg=fetch[1].split(".")[0] #fetched something so use location from said nick
        else:
            arg=input.group(2) # look up arguments given (place)
    else:
        fetch=sqlquery('location', input.nick)
        if fetch:
            arg=fetch[1].split(".")[0] #fetched something so use location from said nick
            if arg.isdigit():
                arg=fetch[1].split(";")[0] #fetched something so use location from said nick
            else:
                arg=fetch[1].split(".")[0] #fetched something so use location from said nick
        else:
            arg=""
        if not arg:
            return phenny.say("Location please?")
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
    fetch=sqlquery('location', input.group(2))
    if fetch:
      arg=fetch[1].split(".")[0] #fetched something so use location from said nick
      if arg.isdigit():
        arg=fetch[1].split(";")[0] #fetched something so use location from said nick
      else:
        arg=fetch[1].split(".")[0] #fetched something so use location from said nick
    else:
      arg=input.group(2) # look up arguments given (place)
  else:
    fetch=sqlquery('location', input.nick) # no arguments look up nick
    if fetch:
      arg=fetch[1].split(".")[0] #fetched something so use location from said nick
      if arg.isdigit():
        arg=fetch[1].split(";")[0] #fetched something so use location from said nick
      else:
        arg=fetch[1].split(".")[0] #fetched something so use location from said nick
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
    return phenny.reply(wunderj['current_observation']['observation_location']['city'] + ' is currently ' + wunderj['current_observation']['weather'] + ' Temp: ' + wunderj['current_observation']['temperature_string'] + ' Wind: ' + str(wunderj['current_observation']['wind_mph']) + 'MPH (' + str(wunderj['current_observation']['wind_kph']) + ' KPH / ' + str( "%.1f" % float(wunderj['current_observation']['wind_kph']*0.27777777)) + ' M/S)' + ' ' + wunderj['current_observation']['wind_dir'] + ' Humidity: ' + wunderj['current_observation']['relative_humidity']  )
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
  if not input.group(2):
    fetch=sqlquery('photo', input.nick)
    if fetch:
      return phenny.reply(fetch[1])
    else:
      return phenny.say('Either give me a .photo set with a photo or go find a camera that won\'t break while taking a picture of you and get back to me')
  else:
    t = input.group(2).split(' ')
    if len(t) >= 1:
      if t[0] == 'set':
        if len(t) < 2:
          return phenny.say('Set what?')
        else:
          sqlrepsert('photo',input.nick, input.group(2)[4:],'person text primary key, photo text')
          return phenny.say('Saving your photo.. Don\'t we look handsome today?' )
      else:
          fetch=sqlquery('photo', t[0])
          if fetch:
            return phenny.say(fetch[0] + ' looks like ' + fetch[1])
          else:
            return phenny.reply('Someone is unphotogenic.. If you don\'t have a photo set yet, use .photo set <photo>')
photo.commands = ['photo']
photo.example = '.photo set/person [photo]'

def location(phenny, input): 
  if not input.group(2):
    fetch=sqlquery('location', input.nick)
    if fetch:
      return phenny.reply(fetch[1])
    else:
      return phenny.say('Either give me a .location set with a location or go find out where you live and get back to me')
  else:
    t = unicodedata.normalize('NFKD', input.group(2)).encode('ascii', 'ignore').split(' ')
    if len(t) >= 1:
      if t[0] == 'set':
        if len(t) < 2:
          return phenny.say('Set what?')
        else:
          sqlrepsert('location',input.nick, input.group(2)[4:],'person text primary key, location text')
          return phenny.say('Saving your weird location... Is your place bike friendly?' )
      else:
          fetch=sqlquery('location', t[0])
          if fetch:
            return phenny.say(fetch[0] + ' lives in ' + fetch[1])
          else:
            return phenny.reply('Dude, you must live on Mars!?! If you don\'t have a location set yet, use .location set <location>')
location.commands = ['location']
location.example = '.location set/person [location]'

def about(phenny, input): 
  conn = sqlite3.connect('bicycling.db')
  cur = conn.cursor()
  if not input.group(2):
    cur.execute('SELECT * FROM about WHERE person=? LIMIT 1', (input.nick,))
    fetch=cur.fetchone()
    if fetch:
      return phenny.say('Interesting fact about ' + input.nick + ': ' + fetch[1])
    else:
      return phenny.say('Either tell me your life story or write a tolstoy novel and publish it!')
  else:
    cur.execute("CREATE TABLE IF NOT EXISTS about (person text primary key, link text)")
    t = unicodedata.normalize('NFKD', input.group(2)).encode('ascii', 'ignore').split(' ')
    if len(t) >= 1:
      if t[0] == 'set':
        sql="insert or replace into about values(?, ?)"
        if len(t) < 2:
          return phenny.say('Set what?')
        else:
          cur.execute(sql, (input.nick, input.group(2)[4:]))
          conn.commit()
          return phenny.say('Saving your life story!')
      else:
          cur.execute('SELECT * FROM about WHERE person=? LIMIT 1', (t[0],))
          fetch=cur.fetchone()
          if fetch:
            return phenny.say('Interesting fact about ' + t[0] + ': ' + fetch[1])
          else:
            return phenny.say('ERROR: ' + t[0] + ' is a terrible redditor and has not set their life story.  SOLUTION: ' + t[0] + ' needs to message me .about set [biography here]')
about.commands = ['about']
about.example = '.about set/person [biography here]'

def strava(phenny, input):
    if input.group(2):
        t = input.group(2).split(' ')
        if t[0] == 'set' and len(t)>1:
            sqlrepsert('strava', input.nick, t[1] ,'person text primary key, strava text')
            return phenny.reply('Strava set up nicely, try it?')
        else:
            fetch=sqlquery('strava', t[0])
            if fetch:
                q=fetch[1]
            else:
                q=input.group(2)
    else:
        fetch=sqlquery('strava', input.nick)
        if fetch:
            q=fetch[1]
        else:
            return
    print('q'+q)
    saresp=urllib2.urlopen('http://www.strava.com/api/v1/rides/' + q).read()
    print 'saresp'
    pprint.pprint(saresp)
    erract=False
    if 'error' in saresp:
        erract=True
    else:
        js2resp=json.loads(saresp)
    pprint.pprint(erract)
    sresp=web.get('http://www.strava.com/api/v1/rides?athleteName=' + q);
    print 'sresp'
    pprint.pprint(sresp)
    if erract==True:
        if 'rides' in sresp:
            jsresp=json.loads(sresp)
            jsrespid=jsresp['rides'][0]
            print 'jsrepsid'
            pprint.pprint(jsrespid)
            s2resp=web.get('http://www.strava.com/api/v1/rides/' + str(jsresp['rides'][0]['id']))
            js2resp=json.loads(s2resp)
            print 'js2resp'
            pprint.pprint(js2resp)
        else:
            phenny.reply('something gone wrong tell krisfremen')
            return
    phenny.reply(js2resp['ride']['athlete']['username'] + ' rode ' + "%.2f" % float(js2resp['ride']['distance']/1000)  + ' km ('+ "%.2f" % float((js2resp['ride']['distance']/1000)*0.621371)  +' mi) in ' + str(datetime.timedelta(seconds=js2resp['ride']['elapsedTime'])) + ' (' +str(datetime.timedelta(seconds=js2resp['ride']['movingTime'])) + ' moving) averaging ' + "%.2f" % float(js2resp['ride']['averageSpeed']*3.6) + ' kph (' + "%.2f" % float((js2resp['ride']['averageSpeed']*3.6)*0.621371) + ' mph) climbing ' +  "%.2f" % float((js2resp['ride']['elevationGain'])) + 'm on ' + time.strftime('%b %d, %Y',time.strptime(js2resp['ride']['startDate'],'%Y-%m-%dT%H:%M:%SZ')) + ' titled ' + js2resp['ride']['name'])
strava.commands = ['strava']
strava.example = '.strava [username/id]'

def bikephoto(phenny, input): 
  conn = sqlite3.connect('bicycling.db')
  cur = conn.cursor()
  if not input.group(2):
    cur.execute('SELECT * FROM bikephoto WHERE person=? LIMIT 1', (input.nick,))
    fetch=cur.fetchone()
    if fetch:
      return phenny.say('Here is ' + input.nick + '\'s pride and joy : ' + fetch[1])
    else:
      return phenny.say('Either give me a set with a picture or a person or bust a move and take a picture of your bicycle')
  else:
    cur.execute("CREATE TABLE IF NOT EXISTS bikephoto (person text primary key, link text)")
    t = unicodedata.normalize('NFKD', input.group(2)).encode('ascii', 'ignore').split(' ')
    if len(t) >= 1:
      if t[0] == 'set':
        sql="insert or replace into bikephoto values(?, ?)"
        if len(t) < 2:
          return phenny.say('Set what?')
        else:
          cur.execute(sql, (input.nick, input.group(2)[4:]))
          conn.commit()
          return phenny.say('Saving your precious bike!')
      else:
          cur.execute('SELECT * FROM bikephoto WHERE person=? LIMIT 1', (t[0],))
          fetch=cur.fetchone()
          if fetch:
            return phenny.say('Here is ' + t[0] + '\'s pride and joy : ' + fetch[1])
          else:
            return phenny.say('ERROR: ' + t[0] + ' is a terrible redditor and has not set their bike photo.  SOLUTION: ' + t[0] + ' needs to message me .bikephoto set http://link.to/bike.jpg')
bikephoto.commands = ['bikephoto', 'prideandjoy']
bikephoto.example = '.bikephoto set/person [photo]'

def bike(phenny, input): 
  conn = sqlite3.connect('bicycling.db')
  cur = conn.cursor()
  if not input.group(2):
    cur.execute('SELECT * FROM bike WHERE LOWER(person)=LOWER(?) LIMIT 1', (input.nick,))
    fetch=cur.fetchone()
    if fetch:
      return phenny.say(fetch[0] + ' has ' + fetch[1])
    else:
      return phenny.say('Either give me a set with some text or a person or bust a move and write up a nice description of it')
  else:
    cur.execute("CREATE TABLE IF NOT EXISTS bike (person text primary key, link text)")
    t = input.group(2).split(' ')
    if len(t) >= 1:
      if t[0] == 'set':
        sql="insert or replace into bike values(?, ?)"
        if len(t) < 2:
          return phenny.say('What kinda bike you have, hmm?')
        else:
          cur.execute(sql, (input.nick, input.group(2)[4:]))
          conn.commit()
          return phenny.say('Saving your precious bike!')
      else:
          cur.execute('SELECT * FROM bike WHERE LOWER(person)=LOWER(?) LIMIT 1 COLLATE NOCASE', (t[0],))
          fetch=cur.fetchone()
          if fetch:
            return phenny.say(fetch[0] + ' has ' + fetch[1])
          else:
            return phenny.reply('Dude, where\'s my bike?!')
bike.commands = ['bike']
bike.example = '.bike set/person [text]'

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
   else: phenny.reply("No results found for that, sorry." % query)
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

if __name__ == '__main__': 
  print __doc__.strip()
