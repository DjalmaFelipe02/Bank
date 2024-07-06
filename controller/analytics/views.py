from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import calendar  # Importar o módulo calendar
from django.utils.translation import gettext as _

from extract.models import Values

@login_required
def analytics(request):
    year = request.GET.get('year', timezone.now().year)
    user = request.user

    # Filtrar os dados para o ano específico
    start_date = timezone.datetime(int(year), 1, 1)
    end_date = timezone.datetime(int(year), 12, 31, 23, 59, 59)

    values = Values.objects.filter(date__range=(start_date, end_date), account=user)

    # Estrutura dos dados para o gráfico
    monthly_data = []
    for month in range(1, 13):
        entries_data = values.filter(date__month=month, type='D').annotate(day=TruncDay('date')).values('day').annotate(count=Count('id')).order_by('day')
        exits_data = values.filter(date__month=month, type='O').annotate(day=TruncDay('date')).values('day').annotate(count=Count('id')).order_by('day')
        
        day_ranges = {
            '1-5': {'entries': 0, 'exits': 0}, 
            '6-10': {'entries': 0, 'exits': 0}, 
            '11-15': {'entries': 0, 'exits': 0}, 
            '16-20': {'entries': 0, 'exits': 0}, 
            '21-25': {'entries': 0, 'exits': 0}, 
            '26-31': {'entries': 0, 'exits': 0}
        }

        for entry in entries_data:
            day = entry['day'].day
            if 1 <= day <= 5:
                day_ranges['1-5']['entries'] += entry['count']
            elif 6 <= day <= 10:
                day_ranges['6-10']['entries'] += entry['count']
            elif 11 <= day <= 15:
                day_ranges['11-15']['entries'] += entry['count']
            elif 16 <= day <= 20:
                day_ranges['16-20']['entries'] += entry['count']
            elif 21 <= day <= 25:
                day_ranges['21-25']['entries'] += entry['count']
            elif 26 <= day <= 31:
                day_ranges['26-31']['entries'] += entry['count']

        for exit in exits_data:
            day = exit['day'].day
            if 1 <= day <= 5:
                day_ranges['1-5']['exits'] += exit['count']
            elif 6 <= day <= 10:
                day_ranges['6-10']['exits'] += exit['count']
            elif 11 <= day <= 15:
                day_ranges['11-15']['exits'] += exit['count']
            elif 16 <= day <= 20:
                day_ranges['16-20']['exits'] += exit['count']
            elif 21 <= day <= 25:
                day_ranges['21-25']['exits'] += exit['count']
            elif 26 <= day <= 31:
                day_ranges['26-31']['exits'] += exit['count']

        # Obter o nome completo do mês usando o módulo calendar e _ faz a tradução para o português
        month_name = _(calendar.month_name[month])

        monthly_data.append({
            'month': month_name,  # Passar o nome completo do mês para o template
            'day_ranges': day_ranges
        })

    context = {
        'year': year,
        'monthly_data': monthly_data
    }

    return render(request, 'analytics/analytics.html', context)
