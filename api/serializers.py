from rest_framework import serializers

from .models import Hospital, Person, Contact, MedicalCondition


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ["id", "name", "city"]


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["first_name", "last_name", "email"]


class ContactSerializer(serializers.ModelSerializer):
    person_email = serializers.EmailField(write_only=True)
    medical_condition_name = serializers.CharField(write_only=True)

    class Meta:
        model = Contact
        fields = [
            "created_at",
            "updated_at",
            "status",
            "person_email",
            "medical_condition_name",
        ]

        extra_kwargs = {
            "created_at": {"required": False},
            "updated_at": {"required": False},
        }

    def create(self, validated_data):
        person_email = validated_data.pop("person_email")
        medical_condition_name = validated_data.pop("medical_condition_name")

        person, _ = Person.objects.get_or_create(
            email=person_email, defaults=validated_data.get("person", {})
        )
        medical_condition, _ = MedicalCondition.objects.get_or_create(
            name=medical_condition_name
        )

        contact = Contact.objects.create(
            **validated_data, person=person, medical_condition=medical_condition
        )
        return contact
