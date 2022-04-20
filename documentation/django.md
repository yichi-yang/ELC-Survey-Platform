# Django REST framework 

Here's an introduction to Django Rest framework. 

This guide was written using the official [docs](https://www.django-rest-framework.org/).

## Model

A model is a Python class that stores data.

### Example
This example model defines a Survey, which has a title and description.
```python
class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
```

Running `python manage.py migrate` turns the Survey model into a database table like this: 

```sql
CREATE TABLE myapp_survey (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(200) NOT NULL,
    "description" varchar(200) NOT NULL
);
```

Models can be found in ```backend\survey\models.py```

Read more about Models [here](https://docs.djangoproject.com/en/4.0/topics/db/models/)

## Serializers

Serializers translate Models to python data types into other formats such as ```json```.

Serializers also can deserialize, allowing incoming data to be converted to python data types and into a Model.

### Example

```python
class SurveySerializer(serializers.ModelSerializer):
    id = IntegerField(read_only=True)
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description']
```
The ```fields``` entry specifies which fields we want, and we can remove fields if we wish to not serialize them.

We can also specify that the id field is ```read only```.

Serializers can be found in ```backend\survey\serializers.py```

Read more about Serializers [here](https://www.django-rest-framework.org/api-guide/serializers/)


## Viewsets

ViewSets are used to handle requests.

Instead of method handlers such as ```.get()``` or ```.post()```, viewsets provides actions such as ```.list()``` and ```.create()```


There are many ways to create a viewset, but there we use ```ModelViewSet``` to minimize the code and simplify the logic of a viewset. 

We use ```ModelViewSet``` class that provide the actions ```.list()```, ```.retrieve()```, ```.create()```, ```.update()```, ```.partial_update()```, and ```.destroy()```


### Example

```python
class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Survey.objects.all()
```

Here we specify the serializer and who has permission to access this viewset. Also, the ```queryset``` defines the ```get``` request to return all entries of the ```Survey``` Model.

Viewsets can be found in ```backend\survey\views.py```

Read more about Viewsets [here](https://www.django-rest-framework.org/api-guide/viewsets/)

## Permissions
Like we specified above, ```permissions``` tells django who has access to an endpoint.  

### Example

```python
permission_classes = [IsAuthenticatedOrReadOnly]
```

This means that ```authenticated``` users are allowed to perform any request. ```Unauthenticated``` users will only be permitted if the request method is ```GET```, ```HEAD``` or ```OPTIONS```.

Django provides a lot of permission classes that you can find [here](https://www.django-rest-framework.org/api-guide/permissions/).

You can also create your own custom permissions.

### Example

```python
class IsAuthenticatedOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in ['POST', 'OPTIONS'] or
            request.user and
            request.user.is_authenticated
        )
```
This permission class allows unauthenticated users to access ```POST``` and ```OPTIONS``` requests while authenticated users can access all requests.

Our custom permissions are in ```backend\survey\permissions.py```.

## Routing

Routers define the url for the endpoints.

### Example

```python
router = routers.DefaultRouter()
router.register(
    r'surveys',
    SurveyViewSet,
    basename='survey'
)
```
We specify the ```SurveyViewSet``` as our request handler. And set the URL prefix to ```survey```.

```python
urlpatterns = [
    path(r'', include(router.urls))
]
```
This specifys that we want to include the survey router url.

Our survey API routers can be found in ```backend\survey\urls.py```

Additionally, the parent URL prefix for our endpoint is ```\api``` which we specify in ```backend\elcform\urls.py```

```python
path('api/', include('survey.urls'))
```

This means that all the urls in our survey app will be prefixed by ```\api```.

Read more about Routers [here](https://www.django-rest-framework.org/api-guide/routers/)