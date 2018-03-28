from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import datetime,json,logging,requests
from juntrax_server.settings import handlerfile
from models import ChoiceLimit

key = 'AIzaSyAE7zO6cW496vGREW7ZpTkmQ0iY-RkcvVU'

def counted(f):	# decorator for check limit per hour
	def wrapped(*args, **kwargs):
		wrapped.calls += 1
		time_hours = datetime.datetime.now() + datetime.timedelta(hours=1)
		count = wrapped.calls
		choice = ChoiceLimit.objects.all()
		if not choice:
			limit = 10
		else:
			limit = choice[0].choice
		if count < limit and datetime.datetime.now() < time_hours:
			return f(*args, **kwargs)
		else:
			return Response('Todays limit for API exceeded, Only 10 times per hour',status=status.HTTP_201_CREATED)
	wrapped.calls = 0
	return wrapped

def request_logging(uri,code): #Common function for maintaing the log for each request
		logging.info('Request Time ==> %s' % str(datetime.datetime.now()))
		logging.info('Request API Name ==> %s ' % uri)
		logging.info('Request Status Code ==> %s ' % code)

class ServerUptime(viewsets.ViewSet):
	def list(self, request):
		try:
			uri = request.META.get('PATH_INFO')
			if uri:
				server_up = []
				with open(handlerfile) as f:
					f = f.readlines()
					for i in f:
						if 'server_uptime' in i: 
							server_uptime = i.split('server_uptime')
							server_up.append(server_uptime[1])
				server_up_date1 = datetime.datetime.strptime(server_up[0].split('\n')[0], ' %Y-%m-%d %H:%M:%S')
				server_up_date2 = datetime.datetime.strptime(server_up[len(server_up)-1].split('\n')[0], ' %Y-%m-%d %H:%M:%S')
				upfrom_last = server_up_date2 - server_up_date1 
				upfrom_last = str(upfrom_last)
				code = 'HTTP_201_CREATED'
				request_logging(uri,code)
				data = {'serverupfrom last':upfrom_last,'serveruptime details':server_up}
				return Response(data,status=status.HTTP_201_CREATED)
			else:
				code = 'HTTP_404_NOT_FOUND'
				request_logging(uri,code)
				return Response('API Not Found',status=status.HTTP_404_NOT_FOUND)
		except:
			code = 'HTTP_500_INTERNAL_SERVER_ERROR'
			request_logging(uri,code)
			return Response('Internal Server Error',status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RequestLogging(viewsets.ViewSet):
	def list(self, request):
		try:
			uri = request.META.get('PATH_INFO')
			if uri:
				timefrom = json.dumps(request.GET.get('from'))
				timeto = json.dumps(request.GET.get('to'))
				request_log = []
				with open(handlerfile) as f:
					f = f.readlines()
					for i in range(len(f)):
						if 'server_uptime' not in f[i]:
							log_time = f[i].split(',')
							if timefrom != 'null' and timeto != 'null':							
								if json.dumps(log_time[0]) == timefrom:
									j=i
									for j in range(i,len(f)): 
										log_time = f[j].split(',')
										request_log.append(log_time)
										if json.dumps(log_time[0]) == timeto:
											break
									break								
							elif timefrom != 'null' and timeto == 'null':
								if json.dumps(log_time[0]) == timefrom:
									j=i
									for j in range(i,len(f)): 
										log_time = f[j].split(',')
										request_log.append(log_time)
									break
							else:
								request_log.append(f[i])
				code = 'HTTP_201_CREATED'
				request_logging(uri,code)
				return Response(request_log,status=status.HTTP_201_CREATED)
			else:
				code = 'HTTP_404_NOT_FOUND'
				request_logging(uri,code)
				return Response('API Not Found',status=status.HTTP_404_NOT_FOUND)
		except:
			code = 'HTTP_500_INTERNAL_SERVER_ERROR'
			request_logging(uri,code)
			return Response('Internal Server Error',status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GoogleReverseGeocoding(viewsets.ViewSet):
	@counted
	def list(self, request):
		uri = request.META.get('PATH_INFO')
		if uri:
			try:
				latlng = request.GET.get('latlng')
				if latlng:
					# google API for ReverseGeocoding 
					url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+latlng+'&key='+key
					resp = requests.get(url)
					resp = resp.json()
					code = 'HTTP_201_CREATED'
					if resp.get('status') == 'OK':
						resp = resp.get('results')[0].get('formatted_address')
						request_logging(uri,code)
						return Response(resp,status=status.HTTP_201_CREATED)
					elif resp.get('status') == 'ZERO_RESULTS':
						request_logging(uri,code)
						return Response('ZERO_RESULTS',status=status.HTTP_201_CREATED)
					elif resp.get('status') == 'OVER_QUERY_LIMIT':
						request_logging(uri,code)
						return Response('OVER_QUERY_LIMIT',status=status.HTTP_201_CREATED)
					elif resp.get('status') == 'REQUEST_DENIED':
						request_logging(uri,code)
						return Response('REQUEST_DENIED',status=status.HTTP_201_CREATED)
					elif resp.get('status') == 'INVALID_REQUEST':
						request_logging(uri,code)
						return Response('INVALID_REQUEST',status=status.HTTP_201_CREATED)
					elif resp.get('status') == 'UNKNOWN_ERROR':
						request_logging(uri,code)
						return Response('UNKNOWN_ERROR',status=status.HTTP_201_CREATED)
				else:
					code = 'HTTP_201_CREATED'
					request_logging(uri,code)
					return Response('Invalid Request Latlng Missing ',status=status.HTTP_500_INTERNAL_SERVER_ERROR)					

			except:
				code = 'HTTP_500_INTERNAL_SERVER_ERROR'
				request_logging(uri,code)
				return Response('Internal Server Error',status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else:
			code = 'HTTP_404_NOT_FOUND'
			request_logging(uri,code)
			return Response('API Not Found',status=status.HTTP_404_NOT_FOUND)

class LimitChange(viewsets.ViewSet):
	def create(self, request):
		uri = request.META.get('PATH_INFO')
		if uri:
			#if request.user == 'admin' checking here for the user is admin for now allow for every user
			data = json.dumps(request.data)
			data = json.loads(data)
			limit = data.get('limit')
			if limit:
				obj = ChoiceLimit.objects.filter(pk=1)
				if obj:
					ChoiceLimit.objects.update(choice = limit)
				else:
					ChoiceLimit.objects.create(choice=limit)
			code = 'HTTP_201_CREATED'
			request_logging(uri,code)
			return Response({"Limit Updated":limit},status=status.HTTP_201_CREATED)
		else:
			code = 'HTTP_404_NOT_FOUND'
			request_logging(uri,code)
			return Response('API Not Found',status=status.HTTP_404_NOT_FOUND)