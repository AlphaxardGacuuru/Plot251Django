from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import WaterReadings, WaterPayments
from dateutil.relativedelta import relativedelta
from django.db.models import Count, F, Value, Sum
import datetime

from django.db.models import F

# Create your views here.

today = datetime.date.today()
months = ['zero', 'January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
# lastMonth = today.month - 1

# Get last month
lastMonth = today + relativedelta(months=-1)
lastMonth = lastMonth.strftime("%Y-%m")

# Get two months ago
lastMonth2 = today + relativedelta(months=-2)
lastMonth2 = lastMonth2.strftime("%Y-%m")


def index(request):
    users = get_user_model().objects.order_by('id')
    getUsers = {}

    for user in users:
        lastReading = WaterReadings.objects.filter(
            apartment=user.username,
            created_at__contains=lastMonth
        ).values_list('reading', flat=True).last
        lastReading2 = WaterReadings.objects.filter(
            apartment=user.username,
            created_at__contains=lastMonth2
        ).values_list('reading', flat=True).first()
        waterPayment = WaterPayments.objects.filter(
            id=user.id,
            created_at__contains=lastMonth
        ).values_list('payment', flat=True).first()
        getUsers[user.id] = {
            'username': user.username,
            'name': user.first_name + ' ' + user.last_name,
            'email': user.email,
            'lastReading': lastReading,
            'lastReading2': lastReading2,
            'paid': waterPayment
        }

    lastReadingTot = WaterReadings.objects.filter(
        created_at__contains=lastMonth
    ).aggregate(Sum('reading')).get("reading__sum")
    lastReadingTot2 = WaterReadings.objects.filter(
        created_at__contains=lastMonth2
    ).aggregate(Sum('reading')).get("reading__sum")
    waterPaymentTot = WaterPayments.objects.filter(
        created_at__contains=lastMonth
    ).aggregate(Sum('payment')).get("payment__sum")
    month = months[today.month]
    context = {
        'users': users,
        'getUsers': getUsers,
        'lastReading': lastReading,
        'lastReadingTot': lastReadingTot,
        'lastReadingTot2': lastReadingTot2,
        'waterPaymentTot': waterPaymentTot,
        'units': 'units',
        'today': today,
        'month': month,
    }
    return render(request, 'water/index.html', context)
