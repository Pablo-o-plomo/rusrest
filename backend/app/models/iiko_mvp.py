from __future__ import annotations
import enum
from datetime import datetime, date
from sqlalchemy import String, Integer, DateTime, Boolean, Date, ForeignKey, Numeric, Text, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class AlertSeverity(str, enum.Enum): green='green'; yellow='yellow'; red='red'; unknown='unknown'
class ImportStatus(str, enum.Enum): pending='pending'; parsed='parsed'; failed='failed'; unknown='unknown'

class Restaurant(Base):
    __tablename__='restaurants'
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    name: Mapped[str]=mapped_column(String(200)); code: Mapped[str]=mapped_column(String(120), unique=True)
    city: Mapped[str|None]=mapped_column(String(120)); timezone: Mapped[str]=mapped_column(String(64), default='UTC')
    is_active: Mapped[bool]=mapped_column(Boolean, default=True); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
class ReportTypeRef(Base):
    __tablename__='report_types'; id: Mapped[int]=mapped_column(Integer, primary_key=True)
    report_code: Mapped[str]=mapped_column(String(10), unique=True); report_name_ru: Mapped[str]=mapped_column(String(200)); iiko_report_name: Mapped[str|None]=mapped_column(String(255)); frequency: Mapped[str|None]=mapped_column(String(50)); is_active: Mapped[bool]=mapped_column(Boolean, default=True)
class ReportImport(Base):
    __tablename__='report_imports'; id: Mapped[int]=mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int|None]=mapped_column(ForeignKey('restaurants.id')); report_code: Mapped[str|None]=mapped_column(String(20)); report_name_ru: Mapped[str|None]=mapped_column(String(200)); report_date_start: Mapped[date|None]=mapped_column(Date); report_date_end: Mapped[date|None]=mapped_column(Date)
    source: Mapped[str]=mapped_column(String(30), default='manual'); email_subject: Mapped[str|None]=mapped_column(String(500)); email_from: Mapped[str|None]=mapped_column(String(255)); email_message_id: Mapped[str|None]=mapped_column(String(255)); original_filename: Mapped[str|None]=mapped_column(String(255)); stored_file_path: Mapped[str|None]=mapped_column(String(500)); status: Mapped[ImportStatus]=mapped_column(Enum(ImportStatus), default=ImportStatus.pending); error_message: Mapped[str|None]=mapped_column(Text); raw_metadata: Mapped[dict]=mapped_column(JSON, default=dict); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow); processed_at: Mapped[datetime|None]=mapped_column(DateTime)
class PurchasePriceEvent(Base):
    __tablename__='purchase_price_events'; id: Mapped[int]=mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int]=mapped_column(ForeignKey('restaurants.id')); report_import_id: Mapped[int]=mapped_column(ForeignKey('report_imports.id'))
    product_name: Mapped[str|None]=mapped_column(String(250)); product_code: Mapped[str|None]=mapped_column(String(120)); arrival_datetime: Mapped[datetime|None]=mapped_column(DateTime); supplier_name: Mapped[str|None]=mapped_column(String(250)); invoice_number: Mapped[str|None]=mapped_column(String(120)); supplier_product_name: Mapped[str|None]=mapped_column(String(250)); unit: Mapped[str|None]=mapped_column(String(50)); price_with_vat: Mapped[float|None]=mapped_column(Numeric(12,2)); unit_price_with_vat: Mapped[float|None]=mapped_column(Numeric(12,2)); pricelist_price: Mapped[float|None]=mapped_column(Numeric(12,2)); price_deviation_rub: Mapped[float|None]=mapped_column(Numeric(12,2)); price_deviation_percent: Mapped[float|None]=mapped_column(Numeric(8,2)); raw_data: Mapped[dict]=mapped_column(JSON, default=dict); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
class Alert(Base):
    __tablename__='alerts'; id: Mapped[int]=mapped_column(Integer, primary_key=True); restaurant_id: Mapped[int|None]=mapped_column(ForeignKey('restaurants.id')); severity: Mapped[AlertSeverity]=mapped_column(Enum(AlertSeverity)); alert_type: Mapped[str]=mapped_column(String(80)); title: Mapped[str]=mapped_column(String(200)); message: Mapped[str]=mapped_column(Text); data: Mapped[dict]=mapped_column(JSON, default=dict); is_sent: Mapped[bool]=mapped_column(Boolean, default=False); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow); sent_at: Mapped[datetime|None]=mapped_column(DateTime)
