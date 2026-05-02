from app.services.subject_parser import parse_subject

def test_r02_subject(): assert parse_subject('[SOCHI] R02 Закупочные цены 2026-04-20_2026-04-26')['report_code']=='R02'
def test_r01_subject(): assert parse_subject('[ROSTOV] R01 Продажи за период 2026-05-01')['report_code']=='R01'
def test_unknown_code(): assert parse_subject('[ROSTOV] XYZ 2026-05-01')['report_code']=='UNKNOWN'
