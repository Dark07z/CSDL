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
    from app.models import ThaiLoai, NhaCungCap, ChiNhanh, Sach, BanSao, NhanVien, ThanhVien, TheThuVien, DonMuon
    from datetime import date, timedelta
    import re
    from app.config import Config

    def ensure_missing_records(model, records, key_name):
        existing_keys = {
            value for (value,) in db.session.query(getattr(model, key_name)).all()
            if value is not None
        }
        for record in records:
            if getattr(record, key_name) not in existing_keys:
                db.session.add(record)

    def ensure_book_copies(ma_sach, desired_count, branch_id):
        existing_numbers = set()
        for (ma_ban_sao,) in db.session.query(BanSao.ma_ban_sao).filter(BanSao.ma_sach == ma_sach).all():
            match = re.search(r'BS(\d+)$', ma_ban_sao or '')
            if match:
                existing_numbers.add(int(match.group(1)))

        next_number = 1
        while len(existing_numbers) < desired_count:
            while next_number in existing_numbers:
                next_number += 1

            ma_ban_sao = f'{ma_sach}-BS{str(next_number).zfill(3)}'
            db.session.add(BanSao(
                ma_ban_sao=ma_ban_sao,
                ma_sach=ma_sach,
                ma_chi_nhanh=branch_id,
                ngay_nhap=date.today()
            ))
            existing_numbers.add(next_number)
            next_number += 1

    today = date.today()
    
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
        NhaCungCap(ma_ncc='NCC01', ten_ncc='Fahasa', dia_chi='Hà Nội', sdt='0243.123.456', email='contact@fahasa.com'),
        NhaCungCap(ma_ncc='NCC02', ten_ncc='Tiki Trading', dia_chi='TP.HCM', sdt='0288.123.456', email='contact@tiki.vn'),
        NhaCungCap(ma_ncc='NCC03', ten_ncc='Nhã Nam', dia_chi='Hà Nội', sdt='0243.456.789', email='contact@nhanam.vn'),
        NhaCungCap(ma_ncc='NCC04', ten_ncc='NXB Trẻ', dia_chi='TP.HCM', sdt='0283.111.222', email='info@nxbtre.com.vn'),
        NhaCungCap(ma_ncc='NCC05', ten_ncc='First News', dia_chi='TP.HCM', sdt='0283.222.333', email='info@firstnews.com.vn'),
        NhaCungCap(ma_ncc='NCC06', ten_ncc='NXB Chính trị', dia_chi='Hà Nội', sdt='0243.987.654', email='info@nxbctqh.vn'),
        NhaCungCap(ma_ncc='NCC07', ten_ncc='Nhà sách Phương Nam', dia_chi='TP.HCM', sdt='0283.333.444', email='info@phuongnam.com.vn'),
        NhaCungCap(ma_ncc='NCC08', ten_ncc='Alpha Books', dia_chi='Hà Nội', sdt='0243.654.321', email='info@alphabooks.vn'),
        NhaCungCap(ma_ncc='NCC09', ten_ncc='Nhà sách Kim Đồng', dia_chi='Hà Nội', sdt='0243.456.789', email='info@kimdong.com.vn'),
    ]
    
    # Thêm chi nhánh
    chi_nhanh_list = [
        ChiNhanh(ma_chi_nhanh='CN01', ten_chi_nhanh='Thư viện trung tâm Hà Nội', dia_chi='123 Phố Huế, Hoàn Kiếm, Hà Nội', sdt='0243.123.456'),
        ChiNhanh(ma_chi_nhanh='CN02', ten_chi_nhanh='Thư viện quận Đống Đa', dia_chi='456 Trần Hưng Đạo, Đống Đa, Hà Nội', sdt='0243.456.789'),
        ChiNhanh(ma_chi_nhanh='CN03', ten_chi_nhanh='Thư viện quận 1 TP.HCM', dia_chi='789 Nguyễn Huệ, Quận 1, TP.HCM', sdt='0288.123.456'),
    ]

    sach_list = [
        Sach(ma_sach='S001', ten_sach='Dế Mèn Phiêu Lưu Ký', tac_gia='Tô Hoài', nam_xb=2022, nha_xb='NXB Kim Đồng', so_luong=5, ma_tl='TL01', ma_ncc='NCC09'),
        Sach(ma_sach='S002', ten_sach='Cho Tôi Xin Một Vé Đi Tuổi Thơ', tac_gia='Nguyễn Nhật Ánh', nam_xb=2021, nha_xb='NXB Trẻ', so_luong=4, ma_tl='TL01', ma_ncc='NCC04'),
        Sach(ma_sach='S003', ten_sach='Tôi Thấy Hoa Vàng Trên Cỏ Xanh', tac_gia='Nguyễn Nhật Ánh', nam_xb=2020, nha_xb='NXB Trẻ', so_luong=4, ma_tl='TL01', ma_ncc='NCC04'),
        Sach(ma_sach='S004', ten_sach='Đắc Nhân Tâm', tac_gia='Dale Carnegie', nam_xb=2019, nha_xb='NXB Tổng hợp TP.HCM', so_luong=6, ma_tl='TL05', ma_ncc='NCC01'),
        Sach(ma_sach='S005', ten_sach='Nhà Giả Kim', tac_gia='Paulo Coelho', nam_xb=2018, nha_xb='NXB Văn học', so_luong=5, ma_tl='TL01', ma_ncc='NCC03'),
        Sach(ma_sach='S006', ten_sach='Tuổi Trẻ Đáng Giá Bao Nhiêu', tac_gia='Rosie Nguyễn', nam_xb=2021, nha_xb='NXB Hội Nhà Văn', so_luong=4, ma_tl='TL05', ma_ncc='NCC03'),
        Sach(ma_sach='S007', ten_sach='Bố Già', tac_gia='Mario Puzo', nam_xb=2017, nha_xb='NXB Văn học', so_luong=3, ma_tl='TL01', ma_ncc='NCC05'),
        Sach(ma_sach='S008', ten_sach='Không Gia Đình', tac_gia='Hector Malot', nam_xb=2016, nha_xb='NXB Kim Đồng', so_luong=3, ma_tl='TL01', ma_ncc='NCC09'),
        Sach(ma_sach='S009', ten_sach='Sapiens: Lược Sử Loài Người', tac_gia='Yuval Noah Harari', nam_xb=2022, nha_xb='NXB Thế Giới', so_luong=5, ma_tl='TL02', ma_ncc='NCC02'),
        Sach(ma_sach='S010', ten_sach='Lược Sử Thời Gian', tac_gia='Stephen Hawking', nam_xb=2018, nha_xb='NXB Trẻ', so_luong=3, ma_tl='TL02', ma_ncc='NCC04'),
        Sach(ma_sach='S011', ten_sach='Vũ Trụ Trong Vỏ Hạt Dẻ', tac_gia='Stephen Hawking', nam_xb=2020, nha_xb='NXB Trẻ', so_luong=3, ma_tl='TL02', ma_ncc='NCC04'),
        Sach(ma_sach='S012', ten_sach='Tự Truyện Một Geisha', tac_gia='Arthur Golden', nam_xb=2019, nha_xb='NXB Văn học', so_luong=3, ma_tl='TL01', ma_ncc='NCC01'),
        Sach(ma_sach='S013', ten_sach='Sherlock Holmes Toàn Tập', tac_gia='Arthur Conan Doyle', nam_xb=2021, nha_xb='NXB Văn học', so_luong=5, ma_tl='TL04', ma_ncc='NCC05'),
        Sach(ma_sach='S014', ten_sach='Harry Potter và Hòn Đá Phù Thủy', tac_gia='J.K. Rowling', nam_xb=2023, nha_xb='NXB Trẻ', so_luong=6, ma_tl='TL04', ma_ncc='NCC04'),
        Sach(ma_sach='S015', ten_sach='Mật Mã Da Vinci', tac_gia='Dan Brown', nam_xb=2018, nha_xb='NXB Trẻ', so_luong=4, ma_tl='TL01', ma_ncc='NCC05'),
        Sach(ma_sach='S016', ten_sach='Cánh Đồng Bất Tận', tac_gia='Nguyễn Ngọc Tư', nam_xb=2017, nha_xb='NXB Trẻ', so_luong=3, ma_tl='TL01', ma_ncc='NCC04'),
        Sach(ma_sach='S017', ten_sach='Số Đỏ', tac_gia='Vũ Trọng Phụng', nam_xb=2016, nha_xb='NXB Văn học', so_luong=3, ma_tl='TL01', ma_ncc='NCC03'),
        Sach(ma_sach='S018', ten_sach='Tắt Đèn', tac_gia='Ngô Tất Tố', nam_xb=2015, nha_xb='NXB Văn học', so_luong=4, ma_tl='TL01', ma_ncc='NCC03'),
        Sach(ma_sach='S019', ten_sach='7 Thói Quen Của Người Thành Đạt', tac_gia='Stephen R. Covey', nam_xb=2021, nha_xb='NXB Tổng hợp TP.HCM', so_luong=5, ma_tl='TL05', ma_ncc='NCC01'),
        Sach(ma_sach='S020', ten_sach='Người Tình Sputnik', tac_gia='Haruki Murakami', nam_xb=2020, nha_xb='NXB Hội Nhà Văn', so_luong=3, ma_tl='TL01', ma_ncc='NCC07'),
    ]

    thanh_vien_list = [
        ThanhVien(ma_thanh_vien='TV001', ho_ten='Nguyễn Minh Anh', sdt='0912345671', email='minhanh@example.com', ghi_chu='Độc giả thường xuyên'),
        ThanhVien(ma_thanh_vien='TV002', ho_ten='Trần Thu Hà', sdt='0912345672', email='thuha@example.com', ghi_chu='Ưu tiên sách văn học'),
        ThanhVien(ma_thanh_vien='TV003', ho_ten='Lê Quang Huy', sdt='0912345673', email='quanghuy@example.com', ghi_chu='Sinh viên'),
        ThanhVien(ma_thanh_vien='TV004', ho_ten='Phạm Ngọc Lan', sdt='0912345674', email='ngoclan@example.com', ghi_chu='Mượn sách thiếu nhi cho con'),
        ThanhVien(ma_thanh_vien='TV005', ho_ten='Võ Thanh Tùng', sdt='0912345675', email='thanhtung@example.com', ghi_chu='Yêu thích sách kỹ năng'),
    ]

    nhan_vien_list = [
        NhanVien(ma_nv='NV001', ho_ten='Nguyễn Thị Mai', dia_chi='Hà Nội', sdt='0901112221', email='mai@example.com', ma_chi_nhanh='CN01'),
        NhanVien(ma_nv='NV002', ho_ten='Lê Đức Long', dia_chi='Hà Nội', sdt='0901112222', email='long@example.com', ma_chi_nhanh='CN02'),
        NhanVien(ma_nv='NV003', ho_ten='Phạm Anh Khoa', dia_chi='TP.HCM', sdt='0901112223', email='khoa@example.com', ma_chi_nhanh='CN03'),
        NhanVien(ma_nv='NV004', ho_ten='Trần Khánh Linh', dia_chi='Hà Nội', sdt='0901112224', email='linh@example.com', ma_chi_nhanh='CN01'),
        NhanVien(ma_nv='NV005', ho_ten='Vũ Minh Tuấn', dia_chi='TP.HCM', sdt='0901112225', email='tuan@example.com', ma_chi_nhanh='CN02'),
    ]

    the_thu_vien_list = [
        TheThuVien(ma_the='THE001', ma_thanh_vien='TV001', ngay_cap=today - timedelta(days=60), ngay_het_han=today + timedelta(days=305), trang_thai='Hoạt động'),
        TheThuVien(ma_the='THE002', ma_thanh_vien='TV002', ngay_cap=today - timedelta(days=55), ngay_het_han=today + timedelta(days=310), trang_thai='Hoạt động'),
        TheThuVien(ma_the='THE003', ma_thanh_vien='TV003', ngay_cap=today - timedelta(days=50), ngay_het_han=today + timedelta(days=315), trang_thai='Hoạt động'),
        TheThuVien(ma_the='THE004', ma_thanh_vien='TV004', ngay_cap=today - timedelta(days=45), ngay_het_han=today + timedelta(days=320), trang_thai='Hoạt động'),
        TheThuVien(ma_the='THE005', ma_thanh_vien='TV005', ngay_cap=today - timedelta(days=40), ngay_het_han=today + timedelta(days=325), trang_thai='Hoạt động'),
    ]

    don_muon_list = [
        DonMuon(ma_don_muon='DM001', ma_thanh_vien='TV001', ma_ban_sao='S001-BS001', ma_nv='NV001', ngay_muon=today - timedelta(days=45), han_tra=today - timedelta(days=15), ngay_tra_thuc_te=today - timedelta(days=10), phu_phat=Config.FINE_PER_DAY * 5, trang_thai='Đã trả'),
        DonMuon(ma_don_muon='DM002', ma_thanh_vien='TV002', ma_ban_sao='S002-BS001', ma_nv='NV002', ngay_muon=today - timedelta(days=40), han_tra=today - timedelta(days=10), ngay_tra_thuc_te=today - timedelta(days=12), phu_phat=0, trang_thai='Đã trả'),
        DonMuon(ma_don_muon='DM003', ma_thanh_vien='TV003', ma_ban_sao='S003-BS001', ma_nv='NV003', ngay_muon=today - timedelta(days=20), han_tra=today + timedelta(days=10), ngay_tra_thuc_te=None, phu_phat=0, trang_thai='Đang mượn'),
        DonMuon(ma_don_muon='DM004', ma_thanh_vien='TV004', ma_ban_sao='S004-BS001', ma_nv='NV004', ngay_muon=today - timedelta(days=35), han_tra=today - timedelta(days=5), ngay_tra_thuc_te=None, phu_phat=0, trang_thai='Quá hạn'),
        DonMuon(ma_don_muon='DM005', ma_thanh_vien='TV005', ma_ban_sao='S005-BS001', ma_nv='NV005', ngay_muon=today - timedelta(days=10), han_tra=today + timedelta(days=20), ngay_tra_thuc_te=None, phu_phat=0, trang_thai='Đang mượn'),
        DonMuon(ma_don_muon='DM006', ma_thanh_vien='TV001', ma_ban_sao='S006-BS001', ma_nv='NV001', ngay_muon=today - timedelta(days=55), han_tra=today - timedelta(days=25), ngay_tra_thuc_te=today - timedelta(days=20), phu_phat=Config.FINE_PER_DAY * 5, trang_thai='Đã trả'),
        DonMuon(ma_don_muon='DM007', ma_thanh_vien='TV002', ma_ban_sao='S007-BS001', ma_nv='NV002', ngay_muon=today - timedelta(days=30), han_tra=today, ngay_tra_thuc_te=today, phu_phat=0, trang_thai='Đã trả'),
        DonMuon(ma_don_muon='DM008', ma_thanh_vien='TV003', ma_ban_sao='S008-BS001', ma_nv='NV003', ngay_muon=today - timedelta(days=25), han_tra=today + timedelta(days=5), ngay_tra_thuc_te=today - timedelta(days=2), phu_phat=0, trang_thai='Đã trả'),
        DonMuon(ma_don_muon='DM009', ma_thanh_vien='TV004', ma_ban_sao='S009-BS001', ma_nv='NV004', ngay_muon=today - timedelta(days=50), han_tra=today - timedelta(days=20), ngay_tra_thuc_te=today - timedelta(days=18), phu_phat=Config.FINE_PER_DAY * 2, trang_thai='Đã trả'),
        DonMuon(ma_don_muon='DM010', ma_thanh_vien='TV005', ma_ban_sao='S010-BS001', ma_nv='NV005', ngay_muon=today - timedelta(days=15), han_tra=today + timedelta(days=15), ngay_tra_thuc_te=None, phu_phat=0, trang_thai='Đang mượn'),
    ]
    
    ensure_missing_records(ThaiLoai, thai_loai_list, 'ma_tl')
    ensure_missing_records(NhaCungCap, nha_cung_cap_list, 'ma_ncc')
    ensure_missing_records(ChiNhanh, chi_nhanh_list, 'ma_chi_nhanh')

    ensure_missing_records(Sach, sach_list, 'ma_sach')
    ensure_missing_records(ThanhVien, thanh_vien_list, 'ma_thanh_vien')
    ensure_missing_records(NhanVien, nhan_vien_list, 'ma_nv')
    ensure_missing_records(TheThuVien, the_thu_vien_list, 'ma_the')

    default_branch = db.session.get(ChiNhanh, 'CN01') or db.session.query(ChiNhanh).first()
    if default_branch:
        for sach in sach_list:
            ensure_book_copies(sach.ma_sach, sach.so_luong, default_branch.ma_chi_nhanh)

    ensure_missing_records(DonMuon, don_muon_list, 'ma_don_muon')

    db.session.commit()

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(debug=True, host='0.0.0.0', port=5000)
