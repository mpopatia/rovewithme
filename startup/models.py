from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
	account = models.ForeignKey(User, unique=True)

class Tag(models.Model):
    tag = models.CharField(max_length=100)
	
class Flight(models.Model):
    price = models.IntegerField(default=0, unique = True)

class Hotel(models.Model):
    price = models.IntegerField(default=0, unique = True)

class City(models.Model):
    city = models.CharField(max_length=2000)
    state = models.CharField(max_length=200)
    
    
    def getTags(self):
        return CityTag.objects.getTagsByCity(self)


class AirportManager(models.Manager):
    def get_city_airports(self, city):
        return super(AirportManager, self).filter(city=city)

class Airport(models.Model):
    name = models.CharField(max_length=2000)
    code = models.CharField(max_length=4000, unique = True)
    city = models.ForeignKey('City')
    objects = AirportManager()
    

class CityTagManager(models.Manager):
    def getTagsByCity(self, city):
        filtered = super(CityTagManager, self).filter(city=city)
        ans = []
        for i in filtered:
            ans = ans + i.city
        return ans
    def getCitiesByTag(self, tag):
        filtered = super(CityTagManager, self).filter(tag = tag)
        ans = []
        for i in filtered:
            ans = ans + i.tag
        return ans
        
class CityTag(models.Model):
    objects = CityTagManager()
    city = models.ForeignKey('City')
    tag = models.ForeignKey('Tag')
    class Meta:
        unique_together = ("city", "tag")

class CityHotel(models.Model):
    hotel = models.ForeignKey('Hotel')
    city = models.ForeignKey('City')

class AirportFlightManager(models.Manager):
    def getCitiesWithin(self, source, budget):
        airports = Airport.objects.filter(city=source)
        ans = []
        for a in airports:
            destinations = AirportFlight.objects.filter(fromFlight = a)
            for d in destinations:
                if d.getAverageFlight() <= budget:
                    c = d.toFlight.city
                    if c not in ans:
                        ans += [c]
        return ans
        

class AirportFlight(models.Model):
    fromFlight = models.ForeignKey('Airport', related_name="fromFlight")
    toFlight = models.ForeignKey('Airport', related_name="toFlight")
    flight = models.IntegerField(default=0)
    objects = AirportFlightManager()
    
    def getAverageFlight(self):
        return self.flight*2
        

class CityInPlan(models.Model):
    city = models.ForeignKey('City')
    plan = models.ForeignKey('Plan')
    owner = models.ForeignKey(User, null=True, blank=True)
    
class DateInPlan(models.Model):
    start = models.DateField()
    end = models.DateField()
    plan = models.ForeignKey('Plan')

class Plan(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True)
    key = models.CharField(max_length=2000, null=True, blank=True, unique=True)
    budget = models.IntegerField(default=0)
    source = models.ForeignKey('City', null=True, blank=True)
    
class CityGraph(models.Model):
    one = models.ForeignKey('City', related_name='one')
    two = models.ForeignKey('City', related_name='two')
    weight = models.IntegerField(default=0)