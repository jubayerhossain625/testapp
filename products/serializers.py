from rest_framework import serializers
from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']  # Include `id` for retrieving existing images


class ProductSerializer(serializers.ModelSerializer):
    gallery_images = ProductImageSerializer(many=True, read_only=True)  # For retrieving gallery images
    uploaded_gallery_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )  # For adding new gallery images

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'cover_image', 'gallery_images', 'uploaded_gallery_images']

    def create(self, validated_data):
        uploaded_gallery_images = validated_data.pop('uploaded_gallery_images', [])
        product = Product.objects.create(**validated_data)
        for image in uploaded_gallery_images:
            ProductImage.objects.create(product=product, image=image)
        return product

    def update(self, instance, validated_data):
        uploaded_gallery_images = validated_data.pop('uploaded_gallery_images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Clear existing gallery images if new ones are provided
        if uploaded_gallery_images:
            instance.gallery_images.all().delete()
            for image in uploaded_gallery_images:
                ProductImage.objects.create(product=instance, image=image)

        return instance
