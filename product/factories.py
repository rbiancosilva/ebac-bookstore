import factory
from django.contrib.auth.models import User
from product.models import Category, Product
class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("pystr")
    slug = factory.Faker("pystr")
    description = factory.Faker("pystr")
    active = factory.Iterator([True, False])
    class Meta:
        model = Category
class ProductFactory(factory.django.DjangoModelFactory):
    price = factory.Faker("pyint")
    category = factory.LazyAttribute(CategoryFactory)
    title = factory.Faker("pystr")
    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.category.add(category)
    class Meta:
        model = Product

class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("pystr")
    email = factory.Faker("pystr")

    class Meta:
        model = User