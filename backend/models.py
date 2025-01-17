from config import db
from datetime import datetime

# construct a class for a Job offer
class JobOffer(db.Model):
    """

        Class representing a job offer.

        Attributes:
        - id: Unique identifier for the job offer.
        - title: The title of the job position.
        - company: Name of the company offering the job.
        - location: Location where the job is based.
        - salary: Salary offered for the job.
        - description: Detailed description of the job.
        - hiring_manager: The name of the hiring manager for the job.
        - created_at: The time when the job offer was created.
        - updated_at: The time when the job offer was last updated.

        Methods:
        - to_json: Serializes the job offer fields to a JSON-compatible dictionary.

    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False,  nullable=False)
    company = db.Column(db.String(50), unique=False, nullable=True)
    location = db.Column(db.String(50), unique=False, nullable=True)
    salary = db.Column(db.String(50), unique=False, nullable=True)
    description = db.Column(db.Text, unique=False, nullable=True)
    hiring_manager = db.Column(db.String(50), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # take fields and convert to json
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "salary": self.salary,
            "description": self.description,
            "hiringManager": self.hiring_manager,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }


