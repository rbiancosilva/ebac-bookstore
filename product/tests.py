from django.test import TestCase
from product.models.category import Category
from product.models.product import Product
from product.serializers.category_serializer import CategorySerializer
from product.serializers.product_serializer import ProductSerializer

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