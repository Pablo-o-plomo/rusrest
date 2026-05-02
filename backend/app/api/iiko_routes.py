from datetime import datetime, date
from pathlib import Path
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.iiko_mvp import Restaurant, ReportImport, PurchasePriceEvent, ImportStatus, Alert, AlertSeverity
from app.services.subject_parser import parse_subject
from app.services.report_parser.r02_purchase_prices import R02PurchasePricesParser
from app.services.email_collector import check_email_now
from app.services.imports import process_uploaded_file, UPLOAD_DIR
router=APIRouter(tags=['iiko'])
@router.get('/restaurants')
def get_restaurants(db:Session=Depends(get_db)): return db.query(Restaurant).all()
@router.post('/restaurants')
def create_restaurant(name:str=Form(...), code:str=Form(...), city:str=Form(None), timezone:str=Form('UTC'), db:Session=Depends(get_db)):
    r=Restaurant(name=name, code=code.upper(), city=city, timezone=timezone); db.add(r); db.commit(); db.refresh(r); return r
@router.post('/imports/manual-upload')
def manual_upload(restaurant_code:str=Form(...), report_code:str=Form(...), report_date_start:date|None=Form(None), report_date_end:date|None=Form(None), file:UploadFile=File(...), db:Session=Depends(get_db)):
    rest=db.query(Restaurant).filter_by(code=restaurant_code.upper()).first()
    if not rest: raise HTTPException(404,'Restaurant not found')
    dst=UPLOAD_DIR/f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    with dst.open('wb') as f: shutil.copyfileobj(file.file,f)
    try:
        imp=process_uploaded_file(db, restaurant_code=restaurant_code, report_code=report_code, filename=file.filename, source_path=dst, report_date_start=report_date_start, report_date_end=report_date_end, source='manual')
        return {'import_id':imp.id,'status':imp.status.value}
    except ValueError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(422, f'Parse failed: {e}')

@router.get('/restaurants/{id}/alerts')
def alerts(id:int,db:Session=Depends(get_db)): return db.query(Alert).filter_by(restaurant_id=id).all()
@router.get('/restaurants/{id}/imports')
def imports(id:int,db:Session=Depends(get_db)): return db.query(ReportImport).filter_by(restaurant_id=id).all()
@router.get('/restaurants/{id}/dashboard')
def dashboard(id:int,db:Session=Depends(get_db)): return {'restaurant_id':id,'latest_imports':db.query(ReportImport).filter_by(restaurant_id=id).count()}
@router.post('/email/check-now')
def check_now():
    return check_email_now()
@router.post('/telegram/test-alert/{restaurant_id}')
def t(restaurant_id:int,db:Session=Depends(get_db)):
    a=Alert(restaurant_id=restaurant_id,severity=AlertSeverity.yellow,alert_type='test',title='Test',message='test'); db.add(a); db.commit(); return {'status':'created'}
