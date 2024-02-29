class BaseClass:

    json_fields = []

    def serialize(self):
        ret={}

        for field in self.json_fields:
            if hasattr(self, field):  # check if exists in the object being serialized
                ret[field] = getattr(self, field)

        return ret
