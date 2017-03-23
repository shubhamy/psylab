from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import StrategySerializer
from .models import Strategy, Ticker

# Create your views here.l
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def strategy_view(request, **kwargs):
    """
    Saving Strategies
    """
    if request.method == 'POST':
        try:
            ticker = Ticker.objects.get(symbol=request.data['ticker'])
        except Exception as e:
            return Response(status=404, data={'error': e.message})
        if Strategy.objects.filter(name=request.data['name'], user=request.user):
            return Response(status=400, data={'error': 'Strategy name: %s already exists. Choose a different name.' % (request.data['name'])})
        strategy = Strategy.objects.create(
                name=request.data['name'],
                user=request.user,
                strategy=request.data['strategy'],
                ticker=ticker
            )
        strategySerializer = StrategySerializer(instance=strategy)
        return Response(status=200, data=strategySerializer.data)

    elif request.method == 'GET':
        strategies = Strategy.objects.filter(user=request.user)
        strategiesSerializer = StrategySerializer(strategies, many=True)
        return Response(status=200, data=strategiesSerializer.data)

    elif request.method == 'PUT':
        try:
            instance = Strategy.objects.get(pk=kwargs['pk'], user=request.user)
            instance.strategy = request.data['strategy']
            instance.name = request.data['name']
            instance.is_active = request.data['is_active']
            instance.ticker = Ticker.objects.filter(symbol=request.data['ticker'])[0]
            instance.save()
            return Response(status=200)
        except Exception as e:
            return Response(status=404, data={'error': e.message})

    elif request.method == 'DELETE':
        try:
            instance = Strategy.objects.get(pk=kwargs['pk'], user=request.user)
            instance.delete()
            return Response(status=200)
        except Exception as e:
            return Response(status=404, data={'error': e.message})
