from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import escape, strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



from startup.models import Airport, Tag, Flight, Hotel, City, CityTag, CityHotel, AirportFlight, CityInPlan, DateInPlan, Plan, CityGraph

from datetime import datetime

import json
import requests
import random

flight_key1 = "####################################"
flight_request = "https://www.googleapis.com/qpxExpress/v1/trips/search?key="+flight_key1

def index(request):
    return render(request,'startup/index.html')
    
def login_page(request):
    return render(request,'startup/login.html')
    
def signup_page(request):
    return render(request,'startup/registration.html')

def plan(request, key):
    return render(request,'startup/plan.html', {'key': key})
    
def plan_page(request):
    hash = str(random.getrandbits(128))[0:7]
    return HttpResponseRedirect(reverse('plan', kwargs={'key': hash}))

@csrf_exempt
def login_view(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username = username, password = password)
	if user is not None:
		if user.is_active:
			login(request, user)
			# Should redirect to previous page as well
			return HttpResponseRedirect(reverse('index'))
		else:
			return HttpResponse("Disabled account")
	else:
		return HttpResponse("Invalid login")

# logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@csrf_exempt
def signup(request):
  username = escape(strip_tags(request.POST['username']))
  email = escape(strip_tags(request.POST['email']))
  password = escape(strip_tags(request.POST['password']))
  first=escape(strip_tags(request.POST['firstname']))
  last = escape(strip_tags(request.POST['lastname']))
  user = User.objects.create_user(username=username, email=email, password=password, first_name=first, last_name=last)
  return HttpResponseRedirect(reverse('index'))
  

def flight_query(request):
    return HttpResponse("test")
    

def query_flights(request_dict):

	url = flight_request
	payload = request_dict
	headers = {"Content-Type": "application/json"}

	response = requests.post(url, data=json.dumps(payload), headers=headers)
	
	return response.json()


# @login_required(login_url='/login_page/')   
def create_plan(request):
    c = request.GET['source']
    c = c.split(',')
    city = c[0].strip()
    state = c[1].strip()
    source = City.objects.get(city=city, state = state)
    plan_key = request.GET['plan_key']
    start = datetime.strptime(request.GET['start_date'], '%m/%d/%Y')
    end = datetime.strptime(request.GET['end_date'], '%m/%d/%Y')
    cities = json.loads(request.GET['cities'])
    elem = Plan.objects.filter(key=plan_key)
    budget = int(float(request.GET['budget']))
    weight = []
    
    def helper1(request, plan_key, start, end, cities, elem):
        p = Plan(owner=request.user, key=plan_key, source=source, budget=budget)
        p.save()
        d = DateInPlan(start=start, end=end, plan=p)
        d.save()
        for c in cities:
            c = c.split(',')
            city = c[0].strip()
            state = c[1].strip()
            obj = City.objects.get(city=city, state = state)
            weight.append(obj)
            cp = CityInPlan(city=obj, plan=p, owner=request.user)
            cp.save()
        return weight
    
    def helper2(request, plan_key, start, end, cities, elem):
        elem = elem[0]
        dp = DateInPlan.objects.get(plan=elem)
        if start.date() > dp.start:
            dp.start = start
        if end.date() < dp.end:
            dp.end = end
        dp.save()
        for c in cities:
            c = c.split(',')
            city = c[0].strip()
            state = c[1].strip()
            obj = City.objects.get(city=city, state = state)
            weight.append(obj)
            cp = CityInPlan(city=obj, plan=elem, owner=request.user)
            cp.save()
        return weight
    
    if len(elem) == 0:
        weight = helper1(request, plan_key, start, end, cities, elem)
    else:
        weight = helper2(request, plan_key, start, end, cities, elem)
    
    return HttpResponse("Y:")
    
    
def update_city_weight(source, destination):
    one = CityGraph.objects.filter(one=source, two=destination)
    if one.exists() == False:
        two = CityGraph.objects.filter(one=destination, two=source)
        if two.exists() == False:
            c = CityGraph(one=source, two=destination, weight = 1)
            c.save()
        else:
            two = two[0]
            nw = two.weight+1
            two.weight = nw
            two.save()
    else:
        one = one[0]
        nw = one.weight+1
        one.weight = nw
        one.save()

def get_city_weight(source, destination):
    one = CityGraph.objects.filter(one=source, two=destination)
    if one.exists() == False:
        two = CityGraph.objects.filter(one=destination, two=source)
        if two.exists() == False:
            return 0
        else:
            two = two[0]
            return two.weight
    else:
        one = one[0]
        return one.weight
        
def get_intersection(request):
    plan_key = request.GET['plan_key']
    res = get_max_destinations(Plan.objects.get(key=plan_key))
    ans = map(lambda x: x.city+", "+x.state, res)
    final = []
    for i in ans:
        if i not in final:
            final.append(i)
    return HttpResponse(json.dumps(final), content_type = "application/json")
    
    
def get_max_destinations(plan):
    all_cities = CityInPlan.objects.filter(plan = plan)
    map1 = {}
    map2 = {}
    for c in all_cities:
        c = c.city
        if c in map1:
            current_count = map1[c]
            
            new_count = current_count+1
            map1[c] = new_count
            if new_count in map2:
                map2[new_count] = map2[new_count]+[c]
            else:
                map2[new_count] = [c]
        else:
            new_count = 1
            map1[c] = new_count
            if new_count in map2:
                map2[new_count] = map2[new_count]+[c]
            else:
                map2[new_count] = [c]
    
    members = len(get_plan_members(plan))
    if members in map2:
        return map2[members]
    else:
        nc = members-1
        while nc >= 0:
            if nc in map2:
                return map2[nc]
            nc -= 1
        
    
    return []

def get_members(request):
    key = request.GET['plan_key']
    if key == "":
        ans = []
    else:
        plan = Plan.objects.filter(key=key)
        if plan.exists() == False:
            ans = []
        else:
            plan = plan[0]
            ans = get_plan_members(plan)
    
    return HttpResponse(json.dumps(ans), content_type = "application/json")

def get_plan_members(plan):
    all_cities = CityInPlan.objects.filter(plan=plan)
    ans = []
    for c in all_cities:
        if c.owner.first_name in ans:
            1
        else:
            ans.append(c.owner.first_name)
    return ans
        
def populate_cities(request):
    with open("txt/new.txt") as f:
        content = f.readlines()
    
    for line in content:
        try:
        	s = line.split(',')
        	s = map(lambda x: x.strip(), s)
        	airport_name = s[0]
        	city = s[1]
        	state = s[2]
        	airport_code = s[3]
        	city_object = City.objects.filter(city=city)
        	if len(city_object) == 0:
        	    city_object = City(city=city, state=state)
        	    city_object.save()
        	else:
        	    city_object = city_object[0]
        	    a = Airport(name=airport_name, code=airport_code, city=city_object)
    	        a.save()
        except:
            1
    
    
    with open("txt/one.txt") as f:
        one = f.readlines()

    with open("txt/two.txt") as f:
        two = f.readlines()
    
    with open("txt/fare.txt") as f:
        fare = f.readlines()
    
    
    for i in xrange(0, len(fare)):
        source = one[i].strip().split(',')
        source_city = source[0].strip()
        source_state = source[1][0:4].strip()
        destination = two[i].strip().split(',')
        destination_city = destination[0].strip()
        destination_state = destination[1][0:4].strip()
        fare2 = int(float(fare[i].strip()))
        if "/" in source_city:
            source_city = source_city.split("/")[0].strip()
        if "/" in destination_city:
            destination_city = destination_city.split("/")[0].strip()
        
        try:
            c_source = City.objects.get(city=source_city, state=source_state)
            c_destination = City.objects.get(city=destination_city, state=destination_state)
            source_airports = Airport.objects.get_city_airports(c_source)
            destination_airports = Airport.objects.get_city_airports(c_destination)
            for s in source_airports:
                for d in destination_airports:
                    af = AirportFlight(fromFlight=s, toFlight=d,flight=fare2)
                    af.save()
        except:
            print "ERROR"
    return HttpResponse("Done")


def get_hotels(dest, start_date, end_date, per_night):
    
    start_date = datetime.strptime('2015 '+str(start_date), '%Y %j').strftime('%m/%d/%Y')
    
    end_date = datetime.strptime('2015 '+str(end_date), '%Y %j').strftime('%m/%d/%Y')
    start = start_date.split('/')
    end = end_date.split('/')
    
    start = start[2]+start[0]+start[1]
    end = end[2]+end[0]+end[1]
    
    dest = dest.city
    dest = dest.replace(" ", "%20")
    
    url = "https://www.priceline.com/pws/v0/stay/retail/listing/"
    url+= dest
    url+="?rguid=3459hjdfdf&check-in="+start
    url+="&check-out="+end
    url+="&currency=USD&responseoptions=DETAILED_HOTEL,NEARBY_ATTR&rooms=1"
    url+="&sort=HDR&offset=0&page-size=5&max-price="+str(int(per_night))
    response = requests.get(url)
    res = response.json()
    if 'hotels' in res:
        return res['hotels']
    else:
        return []

def can_add_city(request):
    source = request.GET['source']
    destination = request.GET['destination']
    budget = int(request.GET['budget'])
    start = datetime.strptime(request.GET['start_date'], '%m/%d/%Y')
    end = datetime.strptime(request.GET['end_date'], '%m/%d/%Y')
    
    ans = {'status':validate_city(source, destination, budget, start, end)}
    return HttpResponse(json.dumps(ans), content_type = "application/json")
    

# bool
def validate_city(s, d, budget, start_date, end_date):
    mn = 10000000
    airport_source = Airport.objects.filter(city=s)
    airport_destination = Airport.objects.filter(city=d)
    for i in airport_source:
        for j in airport_destination:
            air = AirportFlight.objects.filter(fromFlight=i, toFlight=j)
            for a in air:
                flycost = a.getAverageFlight()
                if flycost < mn:
                    mn = flycost
                    break
    
    flycost = mn
    remain = budget - flycost
    
    if (remain <= 0):
        return False
        
    return True
    
    
def get_recommendations(request):
    c = request.GET['source']
    c = c.split(',')
    city = c[0].strip()
    state = c[1].strip()
    source = City.objects.get(city=city, state = state)
    if 'cities' in request.GET:
        current_cities = json.loads(request.GET['cities'])
    else:
        current_cities = []
    budget = int(float(request.GET['budget']))
    start = datetime.strptime(request.GET['start_date'], '%m/%d/%Y').timetuple().tm_yday
    end = datetime.strptime(request.GET['end_date'], '%m/%d/%Y').timetuple().tm_yday
    
    result = get_recommendations_internal(source, current_cities, budget, start, end)
    
    res = map(lambda x: x.city+", "+x.state, result)
    
    ans = []
    for i in res:
        if i not in ans:
            ans.append(i)
    
    return HttpResponse(json.dumps(ans), content_type = "application/json")

def validate_hotel(s, d, budget, start_date, end_date):
    per_night = (float(budget-250) / float((end_date - start_date)))
    
    
    h = get_hotels(d, start_date, end_date, per_night) 
    
    
    if h == []:
        return False
    return True

def get_recommendations_internal(source, current_cities, budget, start_date, end_date):

        pc = AirportFlight.objects.getCitiesWithin(source, budget)
        pc2 = filter (lambda d: validate_city(source,d, budget, start_date, end_date) , pc)
        
        tuples = map( lambda d: (d, get_city_weight(source, d)), pc2)
        
        tuples = [ (d,w) for (d,w) in tuples if (d.city+", "+d.state) not in current_cities ]
        
        tuples.sort(key=lambda tup: tup[1], reverse=True)
        
        if len(tuples) > 4:
            tuples = tuples[:4]
    
        tuples = map(lambda (d,w): d, tuples)
        
        ans = filter (lambda d: validate_hotel(source,d, budget, start_date, end_date) , tuples)
        return ans



def get_flights(start, end, source, dest):
    start = datetime.strftime(start, '%Y-%m-%d')
    end = datetime.strftime(end, '%Y-%m-%d')
    data = {
      "request": {
        "slice": [
          {
            "origin": source,
            "destination": dest,
            "date": start
          },
          {
            "origin": dest,
            "destination": source,
            "date": end
          }
        ],
        "passengers": {
          "adultCount": 1,
          "infantInLapCount": 0,
          "infantInSeatCount": 0,
          "childCount": 0,
          "seniorCount": 0
        },
        "solutions": 10
      }
    }
    response = query_flights(data)
    return response
    
def compute_plan(request):
    key = request.GET['plan_key']
    
    plan = Plan.objects.filter(key=key)
    if plan.exists() == False:
        ans = {}
    else:
        plan = plan[0]
        dp = DateInPlan.objects.get(plan=plan)
        dest = get_max_destinations(plan)[0]
        ap = Airport.objects.filter(city=plan.source)[0]
        ap2 = Airport.objects.filter(city=dest)[0]
        f = get_flights(dp.start, dp.end, ap.code, ap2.code)
        st = dp.start.timetuple().tm_yday
        end = dp.end.timetuple().tm_yday

        h = get_hotels(dest, st, end, plan.budget/(end-st))
        h2 = []
        for i in h:
            d = {}
            d['name'] = i['name']
            d['stars'] = i['starRating']
            d['price'] = i['ratesSummary']['minPrice']
            d['rating'] = i['overallGuestRating']
            d['image'] = i['thumbnailUrl']
            h2.append(d)
        
        f2 = []
        if 'trips' in f:
            if 'tripOption' in f['trips']:
                for j in f['trips']['tripOption']:
                    d = {}
                    d['price'] = j['saleTotal']
                    d['source'] = ap.city.city
                    d['destination'] = ap2.city.city
                    f2.append(d)
        
        ans = {'hotels':h2, 'flights': f2, 'destination': ap2.city.city}
    return HttpResponse(json.dumps(ans), content_type = "application/json")
  
    



###############################################################################
def date_to_int(date_tuple):
    one,two = date_tuple
    one = datetime.strptime(one, '%m/%d/%Y').timetuple().tm_yday
    two = datetime.strptime(two, '%m/%d/%Y').timetuple().tm_yday
    return one,two

def int_to_date(int_tuple):
    one,two = int_tuple
    one = '2015 '+ str(one)
    two = '2015 '+ str(two)
    one = datetime.strptime(one, '%Y %j').strftime('%m/%d/%Y')
    two = datetime.strptime(two, '%Y %j').strftime('%m/%d/%Y')
    return one,two


def formatt (intersec):
    l = list(intersec)
    l.sort()
    
    if l == []:
        return []
    ans = []
    
    init = l[0]
    
    for i in range(1, len(l)):
        nxt = l[i]
        if nxt == (l[i-1]+1):
            continue
        
        ans.append((init, (l[i-1] +1)))
        init = nxt
    
    ans.append((init, (l[-1]+1) ))
    return ans
    
#convert tuple to list and then to a set.
def toRangeSet (tup):
    st = tup[0]
    end = tup[1]
    return set(range(st, end)) #end is inclusive
    
#l is a list of list of tuples of start and end dates in python date format
#return overlapping start and end date
def overlapper(l):
    #set of all common days
    intersec = set([])
    
    intersec = geto (l, intersec, 0)

    ans = map(int_to_date, formatt(intersec))
    return ans
    
    
def geto(l, intersec, n):
    if (l == []):
        return intersec
    else:
        musabs = map(date_to_int ,l[0]) # list of (st, end) tuples
        daysetL = (map (toRangeSet, musabs))
        
        dayset = set([])
        for i in daysetL:
            dayset = dayset.union (i)
        
        if (n==0):
            return geto (l[1:], dayset, 1)

        intersec = set.intersection(intersec, dayset)
        
        return geto (l[1:], intersec, (n+1))