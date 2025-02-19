from rest_framework import serializers
from product.models.product import Product, Category
from product.serializers.category_serializer import CategorySerializer
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    class Meta:
        model = Product
        fields = ["title", "description", "price", "active", "category"]

    def create(self, validated_data):
        # Extract the nested 'category' data
        categories_data = validated_data.pop('category')
        
        # Create the Product instance
        product = Product.objects.create(**validated_data)
        
        # Create or update the nested Category instances
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            product.category.add(category)
        
        return product

    def update(self, instance, validated_data):
        # Extract the nested 'category' data
        categories_data = validated_data.pop('category')
        
        # Update the Product instance
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        
        # Clear existing categories and add the new ones
        instance.category.clear()
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            instance.category.add(category)
        
        return instance