from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes_by_action = {
        'create': [AllowAny],
        'default': [IsAuthenticated]
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes_by_action['default']]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    @action(methods=['POST'], detail=True)
    def rate_movie(self, request, pk=None):

        if 'stars' in request.data:

            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()

                serializer = RatingSerializer(rating, many=False)
                response = {
                    'message': 'Rating updated',
                    'result': serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
                
            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                
                serializer = RatingSerializer(rating, many=False)
                response = {
                    'message': 'Rating created',
                    'result': serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'Provide stars for this movie'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def update(self, request, *args, **kwargs):
        response = {'message': 'You can not update rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You can not create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)    
