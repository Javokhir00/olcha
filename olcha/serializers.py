from rest_framework import serializers
from .models import (
    Category, Product, ProductImage, Comment,
    Attribute, AttributeKey, AttributeValue
)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'



class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeKey
        fields = '__all__'



class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'



class AttributeSerializer(serializers.ModelSerializer):
    attribute_key = AttributeKeySerializer()
    attribute_value = AttributeValueSerializer()

    class Meta:
        model = Attribute
        fields = '__all__'

    def create(self, validated_data):
        key_data = validated_data.pop('attribute_key')
        value_data = validated_data.pop('attribute_value')

        key = AttributeKey.objects.create(**key_data)
        value = AttributeValue.objects.create(**value_data)

        return Attribute.objects.create(attribute_key=key, attribute_value=value, **validated_data)




class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'



class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
