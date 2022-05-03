from rest_framework import serializers

from post.models import Category, Image, Post, Rating, Favorite, Comments, Comments


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rating',)


class FavoriteSerializers(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = Favorite
        fields = '__all__'


class CommentsSerializers(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Comments
        fields = '__all__'


class PostImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    images = PostImageSerializers(many=True, read_only=True)
    comments = CommentsSerializers(many=True, read_only=True)
    created_at = serializers.DateTimeField(format='%D/%M/%Y %H:%M:%s', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'owner', 'name', 'description', 'price', 'category', 'images', 'comments', 'created_at')

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        product = Post.objects.create(**validated_data)
        for image in images_data.getlist('images'):
            Image.objects.create(product=product, image=image)
        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rating_result = 0
        for i in instance.rating.all():
            rating_result += int(i.rating)

        if instance.rating.all().count() == 0:
            representation['rating'] = rating_result
        else:
            representation['rating'] = rating_result / instance.rating.all().count()
        representation['likes'] = instance.like.filter(like=True).count()
        return representation

        representation['favorite'] = instance.favorite.filter(favorite=True).data
        return representation


