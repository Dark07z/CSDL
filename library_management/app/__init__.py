import os
from flask import Flask
from app.config import config
from app.database import db
from app.routes import bp

def create_app(config_name='development'):
    """Tạo ứng dụng Flask"""
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(config[config_name])
    
    # Init database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(bp)
    
    # Create sample data
    with app.app_context():
        db.create_all()
        create_sample_data()
    
    return app

def create_sample_data():
    """Tạo dữ liệu mẫu"""
    from app.models import ThaiLoai, NhaCungCap, ChiNhanh
    from datetime import date, timedelta
    
    # Kiểm tra xem đã có dữ liệu chưa
    if db.session.query(ThaiLoai).count() > 0:
        return
    
    # Thêm thể loại
    thai_loai_list = [
        ThaiLoai(ma_tl='TL01', ten_tl='Văn học'),
        ThaiLoai(ma_tl='TL02', ten_tl='Khoa học'),
        ThaiLoai(ma_tl='TL03', ten_tl='Lịch sử'),
        ThaiLoai(ma_tl='TL04', ten_tl='Truyện tranh'),
        ThaiLoai(ma_tl='TL05', ten_tl='Tự giúp'),
    ]
    
    # Thêm nhà cung cấp
    nha_cung_cap_list = [
        NhaCungCap(ma_ncc='NCC01', ten_ncc='Nhà xuất bản Trẻ', dia_chi='Hà Nội', sdt='0243.123.456', email='info@nxb-tre.com'),
        NhaCungCap(ma_ncc='NCC02', ten_ncc='Nhà xuất bản Kim Đồng', dia_chi='Hà Nội', sdt='0243.456.789', email='info@nxb-kimdong.com'),
        NhaCungCap(ma_ncc='NCC03', ten_ncc='Nhà xuất bản Thế Giới', dia_chi='TP.HCM', sdt='0288.123.456', email='info@nxb-thegioi.com'),
    ]
    
    # Thêm chi nhánh
    chi_nhanh_list = [
        ChiNhanh(ma_chi_nhanh='CN01', ten_chi_nhanh='Thư viện trung tâm Hà Nội', dia_chi='123 Phố Huế, Hoàn Kiếm, Hà Nội', sdt='0243.123.456'),
        ChiNhanh(ma_chi_nhanh='CN02', ten_chi_nhanh='Thư viện quận Đống Đa', dia_chi='456 Trần Hưng Đạo, Đống Đa, Hà Nội', sdt='0243.456.789'),
        ChiNhanh(ma_chi_nhanh='CN03', ten_chi_nhanh='Thư viện quận 1 TP.HCM', dia_chi='789 Nguyễn Huệ, Quận 1, TP.HCM', sdt='0288.123.456'),
    ]
    
    db.session.add_all(thai_loai_list)
    db.session.add_all(nha_cung_cap_list)
    db.session.add_all(chi_nhanh_list)
    db.session.commit()

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(debug=True, host='0.0.0.0', port=5000)
