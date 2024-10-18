from flask import request, jsonify
from config import app, db
from models import JobOffer, Note


# GET method
@app.route("/job-offers", methods=["GET"])
# get all offers from the database
def get_joboffers():
    job_offers = JobOffer.query.all()
    # from the python object, return JSON
    json_job_offers = list(map(lambda x: x.to_json(), job_offers))
    return jsonify({"job_offers": json_job_offers})


# POST method
@app.route("/create-job-offer", methods=["POST"])
def create_offer():
    title = request.json.get("title")
    company = request.json.get("company")
    location = request.json.get("location")
    salary = request.json.get("salary")
    description = request.json.get("description")
    hiring_manager = request.json.get("hiringManager")

    # Check if the title (for now the only non-nullable field) is not empty
    # If it is, return an error that specifies it
    if not title:
        return (
            jsonify({"message": "Title is required"}),
            400
        )
    # create an instance of the class with the properties from the request
    new_job_offer = JobOffer(title=title, company=company, location=location, salary=salary,
                             description=description, hiring_manager=hiring_manager)

    # try to add the class to the database
    try:
        db.session.add(new_job_offer)
        db.session.commit()  # write to the database
    # if there is an exception, return the message
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Job offer created"}), 201


# UPDATE method
@app.route("/update-job-offer/<int:job_offer_id>", methods=["PATCH"])
# specify the offer id (primary key)
def update_job_offer(job_offer_id):
    job_offer = JobOffer.query.get(job_offer_id)

    # error if not found
    if not job_offer:
        return jsonify({"message": "Job offer not found"}), 404

    # change the data, leave as-is if not changed
    data = request.json
    job_offer.title = data.get("title", job_offer.title)
    job_offer.company = data.get("company", job_offer.company)
    job_offer.location = data.get("location", job_offer.location)
    job_offer.salary = data.get("salary", job_offer.salary)
    job_offer.description = data.get("description", job_offer.description)
    job_offer.hiring_manager = data.get("hiringManager", job_offer.hiring_manager)

    db.session.commit()

    return jsonify({"message": "Job offer updated"}), 200


# DELETE method
@app.route("/delete-job-offer/<int:job_offer_id>", methods=["DELETE"])
# specific to one job offer id
def delete_job_offer(job_offer_id):
    job_offer = JobOffer.query.get(job_offer_id)

    # throw error if not found
    if not job_offer:
        return jsonify({"message": "Job offer not found"}), 404

    # delete otherwise
    db.session.delete(job_offer)
    db.session.commit()

    # inform the user
    return jsonify({"message": "Job offer deleted"}), 200


@app.route("/<int:job_id>/get-notes", methods=["GET"])
def get_job_notes(job_id):
    notes = Note.query.filter_by(job_id=job_id).all()
    json_notes = list(map(lambda x: x.to_json(), notes))
    return jsonify({"notes": json_notes})

@app.route("/<int:job_id>/create-note", methods=["POST"])
def create_note(job_id):
    note_title = request.json.get("note_title")
    note = request.json.get("note")

    if not note_title:
        return (
            jsonify({"message": "Title is required"}),
            400
        )
    # create an instance of the class with the properties from the request
    new_note = Note(note_title=note_title, note = note, job_id=job_id)

    # try to add the class to the database
    try:
        db.session.add(new_note)
        db.session.commit()  # write to the database
    # if there is an exception, return the message
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Note created"}), 201

@app.route("/<int:job_id>/update-note/<int:note_id>", methods=["PATCH"])
def update_note(job_id, note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"message": "Note not found"}), 404

    data = request.json
    note.note_title = data.get("note_title", note.note_title)
    note.note = data.get("note", note.note)

    db.session.commit()

    return jsonify({"message": "Note updated"}), 200

@app.route("/<int:job_id>/delete-note/<int:note_id>", methods=["DELETE"])
def delete_note(job_id, note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"message": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({"message": "Note deleted"}), 200



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
