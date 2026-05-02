from datetime import datetime, date
from pathlib import Path
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.iiko_mvp import Restaurant, ReportImport, PurchasePriceEvent, ImportStatus, Alert, AlertSeverity
from app.services.subject_parser import parse_subject
from app.services.report_parser.r02_purchase_prices import R02PurchasePricesParser
from app.services.alerts import evaluate_price_trend
router=APIRouter(tags=['iiko'])
UPLOAD_DIR=Path('backend/uploads'); UPLOAD_DIR.mkdir(parents=True,exist_ok=True)
@router.get('/restaurants')
def get_restaurants(db:Session=Depends(get_db)): return db.query(Restaurant).all()
@router.post('/restaurants')
def create_restaurant(name:str=Form(...), code:str=Form(...), city:str=Form(None), timezone:str=Form('UTC'), db:Session=Depends(get_db)):
    r=Restaurant(name=name, code=code.upper(), city=city, timezone=timezone); db.add(r); db.commit(); db.refresh(r); return r
@router.post('/imports/manual-upload')
def manual_upload(restaurant_code:str=Form(...), report_code:str=Form(...), report_date_start:date|None=Form(None), report_date_end:date|None=Form(None), file:UploadFile=File(...), db:Session=Depends(get_db)):
    rest=db.query(Restaurant).filter_by(code=restaurant_code.upper()).first()
    if not rest: raise HTTPException(404,'Restaurant not found')
    dst=UPLOAD_DIR/f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}"; 
    with dst.open('wb') as f: shutil.copyfileobj(file.file,f)
    meta=parse_subject(f'[{restaurant_code}] {report_code} {report_date_start or date.today()}', file.filename) or {}
    imp=ReportImport(restaurant_id=rest.id, report_code=report_code, report_date_start=report_date_start, report_date_end=report_date_end or report_date_start, source='manual', original_filename=file.filename, stored_file_path=str(dst), status=ImportStatus.pending, raw_metadata=meta)
    db.add(imp); db.flush()
    if report_code=='R02':
      parsed=R02PurchasePricesParser().parse(str(dst)); imp.raw_metadata=parsed['raw_metadata']
      for row in parsed['rows']: db.add(PurchasePriceEvent(restaurant_id=rest.id, report_import_id=imp.id, **row))
      if parsed['rows']:
        first,last=parsed['rows'][0]['unit_price_with_vat'],parsed['rows'][-1]['unit_price_with_vat']; sev,delta=evaluate_price_trend(first,last)
        if sev in ('yellow','red'): db.add(Alert(restaurant_id=rest.id,severity=AlertSeverity[sev],alert_type='purchase_price_growth',title='Рост закупочной цены',message=f'Рост: {delta:.1f}%'))
    imp.status=ImportStatus.parsed; imp.processed_at=datetime.utcnow(); db.commit(); return {'import_id':imp.id,'status':imp.status.value}
@router.get('/restaurants/{id}/alerts')
def alerts(id:int,db:Session=Depends(get_db)): return db.query(Alert).filter_by(restaurant_id=id).all()
@router.get('/restaurants/{id}/imports')
def imports(id:int,db:Session=Depends(get_db)): return db.query(ReportImport).filter_by(restaurant_id=id).all()
@router.get('/restaurants/{id}/dashboard')
def dashboard(id:int,db:Session=Depends(get_db)): return {'restaurant_id':id,'latest_imports':db.query(ReportImport).filter_by(restaurant_id=id).count()}
@router.post('/email/check-now')
def check_now(): return {'status':'queued'}
@router.post('/telegram/test-alert/{restaurant_id}')
def t(restaurant_id:int,db:Session=Depends(get_db)):
    a=Alert(restaurant_id=restaurant_id,severity=AlertSeverity.yellow,alert_type='test',title='Test',message='test'); db.add(a); db.commit(); return {'status':'created'}
