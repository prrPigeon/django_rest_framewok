from fullgame.models import GameCategory, Game, Player, PlayerScore
from fullgame.serializers import GameCategorySerializer, GameSerializer, PlayerSerializer, PlayerScoreSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
# sledeci importi za authentifikaciju
from django.contrib.auth.models import User
from fullgame.serializers import UserSerializer
from rest_framework import permissions
from fullgame.permissions import IsOwnerOrReadOnly
# sledeci import za throttling
from rest_framework.throttling import ScopedRateThrottle
# sledeci importi za filtiranje , importi su bundlovani (razlika u verzijama kurs je dj==1.1, ovo je dj==3.0.3)
# import django_filters.rest_framework
from django_filters import rest_framework as filters
# from rest_framework import filters
from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'
    # sledeci varijable za throttling
    throttle_scope = 'game-categories'
    thorttle_classes = (ScopedRateThrottle, )
    # sledeci atributi za filtiranje
    filter_fields = ('name',)
    search_fields = ('^name',) # ^ start search match
    ordering_fields = ('name',)

class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'
    # sledeci varijable za throttling
    throttle_scope = 'game-categories'
    thorttle_classes = (ScopedRateThrottle, )


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'
    # permission_classes dodat za autentifikaciju
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    # sledeci dict za filtriranje
    filter_fields = (
        'name', 'game_category', 'release_date', 'played', 'owner',
    )
    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name', 'release_date',
    )
    # sledeci method je dodat radi potreba autentifikacije
    def perform_create(self, serializer):
        # Pass an additional owner field to create method
        # To set the owner to the user received in the request.
        serializer.save(owner=self.request.user)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'
    # permission_classes dodat za autentifikaciju
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'
    # sledeci block za filtriranje
    filter_fields = ('name', 'gender',)
    search_fields = ('^name',)
    ordering_fields = ('name',)


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'


# sledeca klasa za filtriranje
class PlayerScoreFilter(filters.FilterSet):
    min_score = filters.NumberFilter(field_name='score', lookup_expr='gte')
    max_score =  filters.NumberFilter(field_name='score', lookup_expr='lte')
    from_score_date =  filters.DateTimeFilter(field_name='score_date', lookup_expr='gte')
    to_score_date =  filters.DateTimeFilter(field_name='score_date', lookup_expr='lte')
    player_name =  filters.AllValuesFilter(field_name='player__name')
    game_name =  filters.AllValuesFilter(field_name='game__name')

    class Meta:
        model = PlayerScore
        fields = ('score', 'from_score_date', 'to_score_date', 'min_score', 'max_score',\
                # player__name will be accessed as player_name
                'player_name',\
                # game__name will be accessed as game_name
                'game_name',
                )

class PlayerScoreList(generics.ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    filter_class = PlayerScoreFilter
    name = 'playerscore-list'


class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'players': reverse(PlayerList.name, request=request),
            'game-categories': reverse(GameCategoryList.name, request=request),
            'games': reverse(GameList.name, request=request),
            'scores': reverse(PlayerScoreList.name, request=request),
            # users je dodat kad i UserList i UserDetail klase
            'users': reverse(UserList.name, request=request)
            })

# komande za testove
# python manage.py test -v 2
# coverage report -m
# coverage html