from rest_framework import serializers

from registration.models import Person, PersonEmail, PersonType, RegistrationSession, PersonTypeAutoList, Registration, MembershipCard

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'gender', 'phone_number')