from . import document
from flask import request, Response, jsonify, render_template, abort
from server.api.models import Document


def create_ontario_documents(houseId):
    document = Document(houseId=houseId, province="Ontario", name="Residential Tenancy Agreement (Standard Form of Lease) (047-2229E)", description="Landlords of most private residential rental units must use this form (standard lease) when they enter into a tenancy with a tenant. Until February 28, 2021, a landlord and tenant may use either the old or updated version of the standard lease for their tenancy agreement. For most residential tenancies, new agreements signed on or after March 1, 2021 must use the updated standard lease, dated December, 2020.")
    return document.insert()


@document.route("House/<int:houseId>/Province/<string:province>/Document/<string:name>", methods=["PUT"])
def update_document(houseId, province, name):
    documnetData = request.get_json()
    if not documnetData or "documentURL" not in documnetData:
        return Response("Error Invalid Response", status=400)
    document = Document.query.filter(Document.houseId == houseId).filter(Document.province == province).filter(Document.name == name).first()
    if document:
        document.documentURL = documnetData["documentURL"]
        if document.update():
            return Response(status=200)
    return Response(status=400)


@document.route("Document/<int:houseId>")
def get_homeowner_by_id(houseId):
    if Document.query.filter(Document.houseId == houseId).first():
        return jsonify([document.toJson() for document in Document.query.filter(Document.houseId == houseId).all()])
    else:
        if create_ontario_documents(houseId):
            return jsonify([document.toJson() for document in Document.query.filter(Document.houseId == houseId).all()])
        return Response(response="Error: Creating documents")


@document.route("Document/<int:houseId>/Tenant")
def get_tenant_documents(houseId):
    if Document.query.filter(Document.houseId == houseId).first():
        return jsonify([document.toJson() for document in Document.query.filter(Document.houseId == houseId).all()])
    return Response(status=404)



