from rest_framework import serializers

from .models import Candidate


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'age', 'gender', 'email', 'phone_number']
        read_only_fields = ['id']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('Name cannot be empty')
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                'Name must be at least 2 characters long')
        return value

    def validate_age(self, value):
        if value <= 0:
            raise serializers.ValidationError('Age must be a positive integer')
        if value > 100:
            raise serializers.ValidationError('Invalid Age')
        return value

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError(
                'Phone number must consist of at least 10 digits'
            )
        return value
