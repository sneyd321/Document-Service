from server import db, app
from sqlalchemy.exc import IntegrityError, OperationalError



class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    houseId = db.Column(db.Integer(), nullable=False, unique=True)
    documentURL = db.Column(db.String(120))
    province = db.Column(db.String(30))
    description = db.Column(db.String(500))
    name = db.Column(db.String(100))
    
    def __init__(self, **kwargs):
        """**kwargs firstName, lastName, email, password, phoneNumber"""
        self.houseId = kwargs.get("houseId", "")
        self.documentURL = None
        self.province = kwargs.get("province", "")
        self.description = kwargs.get("description", "")
        self.name = kwargs.get("name", "")
        

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            db.session.close()
            return True
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            db.session.close()
            return False

    def update(self):
        rows = Document.query.filter(Document.houseId == self.houseId).update(self.toDict(), synchronize_session=False)
        if rows == 1:
            try:
                db.session.commit()
                db.session.close()
                return True
            except OperationalError:
                db.session.rollback()
                db.session.close()
                return False
        return False

    
        
    def toDict(self):
        return {
            Document.houseId: self.houseId,
            Document.documentURL: self.documentURL,
            Document.province: self.province,
            Document.description: self.description,
            Document.name: self.name
        }

    def toJson(self):
        return {
            "houseId": self.houseId,
            "documentURL": self.documentURL,
            "province": self.province,
            "description": self.description,
            "name": self.name
        }

        

    def __repr__(self):
        return "< Document: " + self.documentURL + " >"


