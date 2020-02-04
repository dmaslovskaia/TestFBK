from flask.cli import FlaskGroup

from app import app, db, Region

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
  db.drop_all()
  db.create_all()
  db.session.commit()

@cli.command("init_db")
def init_db():
    db.session.add(Region(region_code=1, region_name="Adygeya Republic"))
    db.session.add(Region(region_code=2, region_name="Bashkortostan Republic"))
    db.session.add(Region(region_code=3, region_name="Buryatiya Republic"))
    db.session.add(Region(region_code=4, region_name="Altaj Republic"))
    db.session.add(Region(region_code=5, region_name="Dagestan Republic"))
    db.session.add(Region(region_code=8, region_name="Kalmykiya Republic"))
    db.session.add(Region(region_code=99, region_name="Unknown region"))
    db.session.commit()

if __name__ == "__main__":
  cli()
