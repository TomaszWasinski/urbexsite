import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: 'user%s@email.com' % n)
    username = factory.Sequence(lambda n: 'user%s' % n)
    password = factory.PostGenerationMethodCall('set_password', 'pass')
