from datetime import datetime, date
from pathlib import Path
from sqlalchemy.orm import Session
from app.models.iiko_mvp import Restaurant, ReportImport, PurchasePriceEvent, ImportStatus, Alert, AlertSeverity
from app.services.subject_parser import parse_subject
from app.services.report_parser.r02_purchase_prices import R02PurchasePricesParser
from app.services.alerts import evaluate_price_trend

UPLOAD_DIR=Path('backend/uploads'); UPLOAD_DIR.mkdir(parents=True,exist_ok=True)

def process_uploaded_file(db:Session, *, restaurant_code:str, report_code:str, filename:str, source_path:Path, report_date_start:date|None=None, report_date_end:date|None=None, source:str='manual'):
    rest=db.query(Restaurant).filter_by(code=restaurant_code.upper()).first()
    if not rest: raise ValueError('Restaurant not found')
    meta=parse_subject(f'[{restaurant_code}] {report_code} {report_date_start or date.today()}', filename) or {}
    imp=ReportImport(restaurant_id=rest.id, report_code=report_code, report_date_start=report_date_start, report_date_end=report_date_end or report_date_start, source=source, original_filename=filename, stored_file_path=str(source_path), status=ImportStatus.pending, raw_metadata=meta)
    db.add(imp); db.flush()
    if report_code=='R02':
        parsed=R02PurchasePricesParser().parse(str(source_path)); imp.raw_metadata=parsed['raw_metadata']
        for row in parsed['rows']: db.add(PurchasePriceEvent(restaurant_id=rest.id, report_import_id=imp.id, **row))
        if parsed['rows']:
            first,last=parsed['rows'][0]['unit_price_with_vat'],parsed['rows'][-1]['unit_price_with_vat']
            sev,delta=evaluate_price_trend(first,last)
            if sev in ('yellow','red'):
                db.add(Alert(restaurant_id=rest.id,severity=AlertSeverity[sev],alert_type='purchase_price_growth',title='Рост закупочной цены',message=f'Рост: {delta:.1f}%'))
    else:
        imp.status=ImportStatus.unknown
    if imp.status!=ImportStatus.unknown: imp.status=ImportStatus.parsed
    imp.processed_at=datetime.utcnow(); db.commit(); return imp
