import graphene 
from graphene_django import DjangoObjectType

from .models import Track 

class TrackType(DjangoObjectType):
    class Meta:
        model = Track


class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description, url):
        #kwargs.get('title')
        user = info.context.user 

        if user.is_anonymous:
            raise Exception('Log in to add track')

        track = Track(title=title, description=description, 
            url=url, posted_by=user)
        track.save()
        return CreateTrack(track=track)


class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType)

    def resolve_tracks(self, info):
        return Track.objects.all()


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()