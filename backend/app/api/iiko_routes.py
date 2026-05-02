from datetime import datetime, date
from pathlib import Path
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
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


@router.get('/dashboard/{id}', response_class=HTMLResponse, tags=['ui'])
def dashboard_page(id:int, db:Session=Depends(get_db)):
    rest=db.query(Restaurant).filter_by(id=id).first()
    if not rest:
        raise HTTPException(404,'Restaurant not found')
    imports=db.query(ReportImport).filter_by(restaurant_id=id).order_by(ReportImport.created_at.desc()).limit(10).all()
    alerts_items=db.query(Alert).filter_by(restaurant_id=id).order_by(Alert.created_at.desc()).limit(10).all()
    total_imports=db.query(ReportImport).filter_by(restaurant_id=id).count()
    parsed_count=db.query(ReportImport).filter_by(restaurant_id=id,status=ImportStatus.parsed).count()
    failed_count=db.query(ReportImport).filter_by(restaurant_id=id,status=ImportStatus.failed).count()
    unknown_count=db.query(ReportImport).filter_by(restaurant_id=id,status=ImportStatus.unknown).count()
    red_count=db.query(Alert).filter_by(restaurant_id=id,severity=AlertSeverity.red).count()
    yellow_count=db.query(Alert).filter_by(restaurant_id=id,severity=AlertSeverity.yellow).count()

    imports_html=''.join([f"<tr><td>{x.created_at:%Y-%m-%d %H:%M}</td><td>{x.report_code or '-'}<\/td><td>{x.source}<\/td><td><span class='badge {x.status.value}'>{x.status.value}<\/span><\/td><td>{x.original_filename or '-'}<\/td><\/tr>" for x in imports]) or "<tr><td colspan='5'>Нет импортов<\/td><\/tr>"
    alerts_html=''.join([f"<tr><td>{a.created_at:%Y-%m-%d %H:%M}</td><td><span class='badge {a.severity.value}'>{a.severity.value}<\/span><\/td><td>{a.title}<\/td><td>{a.message}<\/td><\/tr>" for a in alerts_items]) or "<tr><td colspan='4'>Нет алертов<\/td><\/tr>"

    return f"""
    <!doctype html>
    <html lang='ru'>
      <head>
        <meta charset='UTF-8' />
        <meta name='viewport' content='width=device-width, initial-scale=1.0' />
        <title>Dashboard — {rest.code}</title>
        <style>
          body {{ font-family: Inter, Arial, sans-serif; background:#0b1220; color:#e5e7eb; margin:0; }}
          .wrap {{ max-width:1200px; margin:24px auto; padding:0 16px; }}
          .head {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; }}
          .cards {{ display:grid; gap:10px; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); margin-bottom:18px; }}
          .card {{ background:#111827; border:1px solid #1f2937; border-radius:12px; padding:14px; }}
          .num {{ font-size:26px; font-weight:700; margin-top:6px; }}
          table {{ width:100%; border-collapse: collapse; background:#111827; border:1px solid #1f2937; border-radius:12px; overflow:hidden; }}
          th,td {{ padding:10px; border-bottom:1px solid #1f2937; text-align:left; vertical-align:top; }}
          th {{ color:#9ca3af; font-weight:600; }}
          .grid2 {{ display:grid; gap:16px; grid-template-columns:1fr 1fr; }}
          .badge {{ padding:2px 8px; border-radius:999px; font-size:12px; }}
          .parsed {{ background:#065f46; }} .failed {{ background:#7f1d1d; }} .unknown {{ background:#92400e; }} .pending {{ background:#1e3a8a; }}
          .red {{ background:#b91c1c; }} .yellow {{ background:#a16207; }} .green {{ background:#166534; }}
          a {{ color:#93c5fd; }}
          @media (max-width: 900px) {{ .grid2 {{ grid-template-columns:1fr; }} }}
        </style>
      </head>
      <body>
        <div class='wrap'>
          <div class='head'>
            <h1>📊 Dashboard — {rest.name} ({rest.code})</h1>
            <a href='/docs'>Swagger API<\/a>
          </div>
          <div class='cards'>
            <div class='card'><div>Импортов всего</div><div class='num'>{total_imports}<\/div><\/div>
            <div class='card'><div>Parsed</div><div class='num'>{parsed_count}<\/div><\/div>
            <div class='card'><div>Failed</div><div class='num'>{failed_count}<\/div><\/div>
            <div class='card'><div>Unknown</div><div class='num'>{unknown_count}<\/div><\/div>
            <div class='card'><div>Red alerts</div><div class='num'>{red_count}<\/div><\/div>
            <div class='card'><div>Yellow alerts</div><div class='num'>{yellow_count}<\/div><\/div>
          </div>

          <div class='grid2'>
            <div>
              <h2>Последние импорты</h2>
              <table><thead><tr><th>Дата</th><th>Отчёт</th><th>Источник</th><th>Статус</th><th>Файл</th></tr></thead><tbody>{imports_html}</tbody></table>
            </div>
            <div>
              <h2>Последние алерты</h2>
              <table><thead><tr><th>Дата</th><th>Severity</th><th>Title</th><th>Message</th></tr></thead><tbody>{alerts_html}</tbody></table>
            </div>
          </div>
        </div>
      </body>
    </html>
    """
