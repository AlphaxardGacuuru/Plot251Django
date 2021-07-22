from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import WaterReadings, WaterPayments
import datetime
# Create your views here.

today = datetime.date.today()
months = ['zero', 'January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
lastMonth = today.month - 1
# lastMonth.strftime("%Y-%m")

def index(request):
	users = get_user_model().objects.order_by('id')
	getUsers = {}
	for user in users:
		waterReading = WaterReadings.objects.filter(
			apartment=user.username, created_at__contains=today.strftime("%Y-%m")
			).values_list('reading', flat=True).first()
		waterPayment = WaterPayments.objects.order_by('-created_at')
		getUsers[user.id] = {
			'username': user.username,
			'name': user.first_name + user.last_name,
			'email': user.email,
			'units': waterReading,
			'litres': today,
			'bill': user.email,
			'paid': user.email
		}
	month = months[today.month]
	context = {
        'users': users,
        'getUsers': getUsers,
        'waterReadings': 'waterReadings',
        'waterPayments': 'waterPayments',
        'units': 'units',
        'today': today,
        'month': month,
    }
	return render(request, 'water/index.html', context)
