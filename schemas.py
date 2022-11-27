from app import ma
from models import Magazine


class MagazineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Magazine
        fields = ("title", "publisher")