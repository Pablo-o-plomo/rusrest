from datetime import datetime
from pathlib import Path
from imap_tools import MailBox
from app.core.config import settings
from app.db.session import SessionLocal
from app.services.subject_parser import parse_subject
from app.services.imports import process_uploaded_file, UPLOAD_DIR

ALLOWED_EXT=('.xlsx','.xls','.csv')

def check_email_now()->dict:
    processed=0; failed=0
    with MailBox(settings.email_host).login(settings.email_user, settings.email_password, settings.email_folder) as mailbox:
        for msg in mailbox.fetch('(UNSEEN)'):
            handled=False
            for att in msg.attachments:
                if not att.filename.lower().endswith(ALLOWED_EXT):
                    continue
                handled=True
                dst=UPLOAD_DIR/f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{att.filename}"
                Path(dst).write_bytes(att.payload)
                meta=parse_subject(msg.subject or '', att.filename)
                db=SessionLocal()
                try:
                    if meta:
                        process_uploaded_file(db, restaurant_code=meta['restaurant_code'], report_code=meta['report_code'], filename=att.filename, source_path=dst, report_date_start=meta['report_date_start'], report_date_end=meta['report_date_end'], source='email')
                        processed+=1
                    else:
                        failed+=1
                except Exception:
                    failed+=1
                finally:
                    db.close()
            if handled:
                mailbox.flag(msg.uid, '\\Seen', True)
    return {'processed':processed,'failed':failed}
