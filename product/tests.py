from django.test import TestCase
from product.models.category import Category
from product.models.product import Product
from product.serializers.category_serializer import CategorySerializer
from product.serializers.product_serializer import ProductSerializer
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from product.factories import UserFactory

from django.test import TestCase
from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category",
            slug="test-category",
            description="This is a test category",
            active=True
        )

    def test_category_creation(self):
        self.assertEqual(self.category.title, "Test Category")
        self.assertEqual(self.category.slug, "test-category")
        self.assertEqual(self.category.description, "This is a test category")
        self.assertTrue(self.category.active)

    def test_category_str_representation(self):
        self.assertEqual(str(self.category), "Test Category")


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category",
            slug="test-category",
            description="This is a test category",
            active=True
        )
        self.serializer = CategorySerializer(instance=self.category)

    def test_category_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["title", "description", "active", "slug"]))

    def test_category_serializer_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["title"], "Test Category")
        self.assertEqual(data["slug"], "test-category")
        self.assertEqual(data["description"], "This is a test category")
        self.assertTrue(data["active"])

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category",
            slug="test-category",
            description="This is a test category",
            active=True
        )
        self.product = Product.objects.create(
            title="Test Product",
            description="This is a test product",
            price=100,
            active=True
        )
        self.product.category.add(self.category)

    def test_product_creation(self):
        self.assertEqual(self.product.title, "Test Product")
        self.assertEqual(self.product.description, "This is a test product")
        self.assertEqual(self.product.price, 100)
        self.assertTrue(self.product.active)
        self.assertIn(self.category, self.product.category.all())


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category",
            slug="test-category",
            description="This is a test category",
            active=True
        )
        self.product = Product.objects.create(
            title="Test Product",
            description="This is a test product",
            price=100,
            active=True
        )
        self.product.category.add(self.category)
        self.serializer = ProductSerializer(instance=self.product)

    def test_product_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["title", "description", "price", "active", "category"]))

    def test_product_serializer_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["title"], "Test Product")
        self.assertEqual(data["description"], "This is a test product")
        self.assertEqual(data["price"], 100)
        self.assertTrue(data["active"])
        self.assertEqual(len(data["category"]), 1)
        self.assertEqual(data["category"][0]["title"], "Test Category")
        self.assertEqual(data["category"][0]["slug"], "test-category")
        self.assertEqual(data["category"][0]["description"], "This is a test category")
        self.assertTrue(data["category"][0]["active"])

@pytest.mark.django_db
class TestProductViewSet(APITestCase):

    # Criando uma instância de Product para os testes
    def setUp(self):
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        token.save()

        self.list_url = reverse('product-list', kwargs={'version': 'v1'})
        self.product = Product.objects.create(
            title='World of Warcraft Shadowlands',
            description='Expansão "Shadowlands" para o jogo base World of Warcraft.',
            price=150,
        )

    # Testando se o get da listagem dos produtos irá retornar status 200
    def test_list_products(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testando se o post de um novo produto irá retornar 201
    def test_create_product(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        data = {
            'title': 'World of Warcraft (1 mo.)',
            'description': 'Adiciona 1 mês de assinatura à conta.',
            'price': '35'
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)