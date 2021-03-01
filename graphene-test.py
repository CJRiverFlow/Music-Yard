import graphene
import uuid
import json 
from datetime import datetime

class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()

class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value = datetime.now())
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        return 'https://cloudinary.com/{}/{}'.format(self.username,self. id)

class CreateUser(graphene.Mutation):
    user = graphene.Field(User) 

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        user =  User(username=username)
        return CreateUser(user=user)

class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return "world"

    def resolve_is_admin(self, info):
        return True
    
    def resolve_users(self, info, limit=None):
        return [
            User(username="Saitama"),
            User(username="Genos")
        ][:limit]

class CreatePost(graphene.Mutation):
    post = graphene.Field(Post) 
    
    class Arguments:
        title = graphene.String()
        content = graphene.String()
    
    def mutate(self, info, title, content):
        if info.context.get('is_anonymous'):
            raise Exception('Not for your eyes')
        post = Post(title=title, content=content)
        return CreatePost(post=post)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()

schema = graphene.Schema(query=Query, mutation = Mutation)


result = schema.execute(
     '''
     {
         users(limit:2){
             id
             username
             createdAt
             avatarUrl
         }
     }
     '''
 )

"""
result = schema.execute(
    '''
    mutation myMutation ($username: String!){
        createUser(username:$username){
            user {
                id
                username
                createdAt
            }
        }
    }
    ''',    
variable_values = {'username':'Potricacio'}
)
"""
"""
result = schema.execute(
    '''
    mutation {
        createPost(title:"First Post", content:"This is good"){
            post {
                title
                content
            }
        }
    }
    ''',
    context = {"is_anonymous":False}
)
"""
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))