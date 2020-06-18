import mongoengine as me


class Document(me.Document):
    title = me.StringField(required=True)
    path = me.StringField()
    link = me.StringField()
    type = me.StringField()
    status = me.StringField(required=True)

    @staticmethod
    def get_document_by_id(id):
        return Document.objects(id=id).first()

    @staticmethod
    def validate_document(document):
        document.status = 'validated'
        document.save()
