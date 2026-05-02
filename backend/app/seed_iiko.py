from app.db.session import SessionLocal
from app.models.iiko_mvp import Restaurant, ReportTypeRef
from app.services.report_types import REPORT_TYPES

def run():
    db=SessionLocal()
    for code,name in [('SOCHI','Klevo Sochi'),('ROSTOV','Klevo Rostov'),('SAKHALIN','Klevo Sakhalin'),('MOSCOW_AVIAPARK','Klevo Aviapark')]:
        if not db.query(Restaurant).filter_by(code=code).first(): db.add(Restaurant(code=code,name=name))
    for code,meta in REPORT_TYPES.items():
        if not db.query(ReportTypeRef).filter_by(report_code=code).first(): db.add(ReportTypeRef(report_code=code,report_name_ru=meta['name_ru']))
    db.commit(); db.close(); print('seeded')
if __name__=='__main__': run()
