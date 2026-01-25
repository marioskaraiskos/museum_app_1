from app import db, Exhibit, Event, Service, News, events_data

if __name__ == '__main__':
    with __import__('app').app.app_context():
        db.create_all()

        # Add sample exhibits if none exist
        if Exhibit.query.count() == 0:
            samples = [
                ("Ancient Pottery", "A collection of pottery from ancient civilizations."),
                ("Medieval Armor", "Armors and weapons from the medieval period."),
                ("Modern Photography", "Selected works from contemporary photographers."),
            ]
            for t, d in samples:
                db.session.add(Exhibit(title=t, description=d))
            db.session.commit()
            print('Inserted sample exhibits')

        # Add sample services if none exist
        if Service.query.count() == 0:
            samples = [
                ("Guided Tours", "Daily guided tours with expert guides."),
                ("Accessibility Support", "Wheelchair accessible routes and assistance."),
            ]
            for t, d in samples:
                db.session.add(Service(title=t, description=d))
            db.session.commit()
            print('Inserted sample services')

        # Import events_data into Event table if none exist
        if Event.query.count() == 0:
            for e in events_data:
                db.session.add(Event(title=e['title'], date=e['date'], start=e.get('start'), end=e.get('end'), description=e.get('description')))
            db.session.commit()
            print('Imported events_data into events table')

        # No-op for News (admins can add via UI)
        print('Migration complete')
