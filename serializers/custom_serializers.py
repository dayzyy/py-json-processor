from serializers.base_serializers import JSONSerializer, SerializerMeta
from models.custom_models import Student, Room

class StudentJSONSerializer(JSONSerializer):
    class Meta(SerializerMeta):
        model = Student
        fields = ['id', 'name', 'room']

class RoomJSONSerializer(JSONSerializer):
    class Meta(SerializerMeta):
        model = Room
        fields = ['id', 'name']
