from rest_framework import serializers
from .models import Product, ProductImage
import json


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']  # Include `id` for retrieving existing images


class ProductSerializer(serializers.ModelSerializer):
    gallery_images = ProductImageSerializer(many=True, read_only=True)  # For retrieving gallery images
    uploaded_gallery_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )  # For adding new gallery images
    deleted_gallery_images = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )  # For deleting gallery images

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
            'cover_image',
            'gallery_images',
            'uploaded_gallery_images',
            'deleted_gallery_images',
        ]

    def validate_deleted_gallery_images(self, value):
        if isinstance(value, str):  # If it's a string, try to parse it
            try:
                value = json.loads(value)  # Parse the string as a JSON array
            except json.JSONDecodeError:
                raise serializers.ValidationError("Invalid format for deleted_gallery_images. Expected a list of integers.")
        elif not isinstance(value, list):  # Ensure it's a list
            raise serializers.ValidationError("deleted_gallery_images must be a list of integers.")

        # Ensure all elements in the list are integers
        if not all(isinstance(item, int) for item in value):
            raise serializers.ValidationError("All items in deleted_gallery_images must be integers.")

        return value



    def update(self, instance, validated_data):
        # Retrieve optional fields
        uploaded_gallery_images = validated_data.get('uploaded_gallery_images', None)
        deleted_gallery_images = validated_data.get('deleted_gallery_images', None)

        print("Uploaded Images:", uploaded_gallery_images)
        print("Deleted Gallery Images:", deleted_gallery_images)

        # Update only provided fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Add new gallery images (if provided)
        if uploaded_gallery_images:
            for image in uploaded_gallery_images:
                ProductImage.objects.create(product=instance, image=image)

        # Delete specified gallery images (if provided)
        if deleted_gallery_images:
            ProductImage.objects.filter(id__in=deleted_gallery_images, product=instance).delete()

        return instance
