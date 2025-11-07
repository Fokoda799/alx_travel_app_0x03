from rest_framework import serializers
from .models import CustomUser, Listing, Booking, Review

# host details
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "phone_number"]


class ListingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = "__all__"  
        # or list explicitly:
        # fields = ["id", "host", "name", "description", "location", "price_per_night", "created_at"]


class BookingSerializer(serializers.ModelSerializer):
    # property = ListingSerializer(read_only=True)
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"
        # You could also exclude auto fields like created_at if you don’t need them
        # exclude = ["created_at"]

    def validate(self, data):
        """
        Extra validation at the serializer level
        (runs in addition to model.clean()).
        """
        if data["end_date"] <= data["start_date"]:
            raise serializers.ValidationError("End date must be after start date.")

        return data

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model.
    - Shows which property and user the review is for
    - Makes the API response more informative
    """
    property = ListingSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = "__all__"
