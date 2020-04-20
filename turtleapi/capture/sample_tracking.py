from turtleapi import db
from turtleapi.models.turtlemodels import Sample, SampleTracking
from sqlalchemy.orm import load_only, defer

def add_tracking_entry(data):
    sample = db.session.query(Sample).filter_by(sample_id=data['sample_id']).first()

    entry = SampleTracking(
        sample=sample,
        date=data['date'],
        notes=data['notes']
    )
    db.session.add(entry)
    db.session.commit()
    return 'Successfully added tracking entry'

def update_tracking_entry(sample_tracking_id, data):
    entry = db.session.query(SampleTracking).filter_by(sample_tracking_id=sample_tracking_id).first()
    entry.date = data['date']
    entry.notes = data['notes']
    db.session.commit()
    return 'Successfully updated tracking entry'

def delete_tracking_entry(sample_tracking_id):
    db.session.query(SampleTracking).filter_by(sample_tracking_id=sample_tracking_id).delete()
    db.session.commit()
    return 'Successfully deleted tracking entry'

def get_sample(sample_id):
    query_result = db.session.query(Sample).filter_by(sample_id=sample_id).first()
    return query_result.to_dict(max_nesting=2)

def add_sample(sample):
    new_sample = Sample(
        encounter_id=sample['encounter_id'],
        entered_by=sample['entered_by'],
        entered_date=sample['entered_date'][0:10],
        sample_type=sample['sample_type'],
        received_by=sample['received_by'],
        purpose_of_sample=sample['purpose_of_sample'],
        notes=sample['notes']
    )
    db.session.add(new_sample)
    db.session.commit()
    return 'Successfully added sample'

def update_sample(sample):
    queried_sample = db.session.query(Sample).filter_by(sample_id=sample['sample_id']).first()
    queried_sample.sample_type = sample['sample_type']
    queried_sample.received_by = sample['received_by']
    queried_sample.purpose_of_sample = sample['purpose_of_sample']
    queried_sample.notes = sample['notes']
    db.session.commit()
    return 'Successfully updated sample'

def delete_sample(sample_id):
    db.session.query(Sample).filter_by(sample_id=sample_id).delete()
    db.session.commit()
    return 'Successfully deleted sample'