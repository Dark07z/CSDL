from app.database import db
from datetime import datetime

# ===================== BẢNG THU VIỆN CƠ BẢN =====================

class ThaiLoai(db.Model):
    """Thể loại sách"""
    __tablename__ = 'thai_loai'
    
    ma_tl = db.Column(db.String(10), primary_key=True)
    ten_tl = db.Column(db.String(100), nullable=False)
    
    sach = db.relationship('Sach', backref='thai_loai', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ThaiLoai {self.ma_tl}>'

class NhaCungCap(db.Model):
    """Nhà cung cấp (nhà xuất bản)"""
    __tablename__ = 'nha_cung_cap'
    
    ma_ncc = db.Column(db.String(10), primary_key=True)
    ten_ncc = db.Column(db.String(150), nullable=False)
    dia_chi = db.Column(db.String(255))
    sdt = db.Column(db.String(15))
    email = db.Column(db.String(100))
    
    sach = db.relationship('Sach', backref='nha_cung_cap', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<NhaCungCap {self.ma_ncc}>'

class Sach(db.Model):
    """Sách"""
    __tablename__ = 'sach'
    
    ma_sach = db.Column(db.String(10), primary_key=True)
    ten_sach = db.Column(db.String(200), nullable=False)
    tac_gia = db.Column(db.String(150))
    nam_xb = db.Column(db.Integer)
    nha_xb = db.Column(db.String(150))
    so_luong = db.Column(db.Integer, default=0)
    ma_tl = db.Column(db.String(10), db.ForeignKey('thai_loai.ma_tl'), nullable=False)
    ma_ncc = db.Column(db.String(10), db.ForeignKey('nha_cung_cap.ma_ncc'))
    
    ban_sao = db.relationship('BanSao', backref='sach', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Sach {self.ma_sach}>'

class ChiNhanh(db.Model):
    """Chi nhánh thư viện"""
    __tablename__ = 'chi_nhanh'
    
    ma_chi_nhanh = db.Column(db.String(10), primary_key=True)
    ten_chi_nhanh = db.Column(db.String(150), nullable=False)
    dia_chi = db.Column(db.String(255))
    sdt = db.Column(db.String(15))
    
    ban_sao = db.relationship('BanSao', backref='chi_nhanh', lazy=True, cascade='all, delete-orphan')
    nhan_vien = db.relationship('NhanVien', backref='chi_nhanh', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ChiNhanh {self.ma_chi_nhanh}>'

class BanSao(db.Model):
    """Bản sao của sách tại chi nhánh"""
    __tablename__ = 'ban_sao'
    
    ma_ban_sao = db.Column(db.String(20), primary_key=True)
    tinh_trang = db.Column(db.String(50), default='Khỏe')  # Khỏe, Hư hỏng
    ngay_nhap = db.Column(db.Date, default=datetime.now)
    ma_sach = db.Column(db.String(10), db.ForeignKey('sach.ma_sach'), nullable=False)
    ma_chi_nhanh = db.Column(db.String(10), db.ForeignKey('chi_nhanh.ma_chi_nhanh'), nullable=False)
    
    don_muon = db.relationship('DonMuon', backref='ban_sao', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<BanSao {self.ma_ban_sao}>'

# ===================== BẢNG NHÂN VIÊN =====================

class NhanVien(db.Model):
    """Nhân viên thư viện"""
    __tablename__ = 'nhan_vien'
    
    ma_nv = db.Column(db.String(10), primary_key=True)
    ho_ten = db.Column(db.String(150), nullable=False)
    dia_chi = db.Column(db.String(255))
    sdt = db.Column(db.String(15))
    email = db.Column(db.String(100))
    ma_chi_nhanh = db.Column(db.String(10), db.ForeignKey('chi_nhanh.ma_chi_nhanh'), nullable=False)
    ngay_vao = db.Column(db.Date, default=datetime.now)
    
    ca_lam = db.relationship('CaLam', backref='nhan_vien', lazy=True, cascade='all, delete-orphan')
    don_muon = db.relationship('DonMuon', foreign_keys='DonMuon.ma_nv', backref='nhan_vien', lazy=True)
    
    def __repr__(self):
        return f'<NhanVien {self.ma_nv}>'

class CaLam(db.Model):
    """Ca làm việc của nhân viên"""
    __tablename__ = 'ca_lam'
    
    ma_ca_lam = db.Column(db.String(10), primary_key=True)
    ma_nv = db.Column(db.String(10), db.ForeignKey('nhan_vien.ma_nv'), nullable=False)
    thoi_gian_bat_dau = db.Column(db.Time, nullable=False)
    thoi_gian_ket_thuc = db.Column(db.Time, nullable=False)
    
    def __repr__(self):
        return f'<CaLam {self.ma_ca_lam}>'

# ===================== BẢNG ĐỘC GIẢ =====================

class ThanhVien(db.Model):
    """Thành viên / Độc giả"""
    __tablename__ = 'thanh_vien'
    
    ma_thanh_vien = db.Column(db.String(10), primary_key=True)
    ho_ten = db.Column(db.String(150), nullable=False)
    sdt = db.Column(db.String(15))
    email = db.Column(db.String(100))
    ngay_dang_ky = db.Column(db.Date, default=datetime.now)
    ghi_chu = db.Column(db.Text)
    
    the_thu_vien = db.relationship('TheThuVien', backref='thanh_vien', lazy=True, cascade='all, delete-orphan', uselist=False)
    don_muon = db.relationship('DonMuon', backref='thanh_vien', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ThanhVien {self.ma_thanh_vien}>'

class TheThuVien(db.Model):
    """Thẻ thư viện"""
    __tablename__ = 'the_thu_vien'
    
    ma_the = db.Column(db.String(10), primary_key=True)
    ma_thanh_vien = db.Column(db.String(10), db.ForeignKey('thanh_vien.ma_thanh_vien'), nullable=False)
    ngay_cap = db.Column(db.Date, default=datetime.now)
    ngay_het_han = db.Column(db.Date, nullable=False)
    trang_thai = db.Column(db.String(50), default='Hoạt động')  # Hoạt động, Hết hạn, Khóa
    
    def __repr__(self):
        return f'<TheThuVien {self.ma_the}>'

# ===================== BẢNG MƯỢN / TRẢ =====================

class DonMuon(db.Model):
    """Đơn mượn sách"""
    __tablename__ = 'don_muon'
    
    ma_don_muon = db.Column(db.String(20), primary_key=True)
    ma_thanh_vien = db.Column(db.String(10), db.ForeignKey('thanh_vien.ma_thanh_vien'), nullable=False)
    ma_ban_sao = db.Column(db.String(20), db.ForeignKey('ban_sao.ma_ban_sao'), nullable=False)
    ma_nv = db.Column(db.String(10), db.ForeignKey('nhan_vien.ma_nv'), nullable=False)
    
    ngay_muon = db.Column(db.Date, default=datetime.now, nullable=False)
    han_tra = db.Column(db.Date, nullable=False)
    ngay_tra_thuc_te = db.Column(db.Date)
    phu_phat = db.Column(db.Float, default=0)
    trang_thai = db.Column(db.String(50), default='Đang mượn')  # Đang mượn, Đã trả, Quá hạn
    
    def __repr__(self):
        return f'<DonMuon {self.ma_don_muon}>'
    
    def calculate_fine(self, fine_per_day):
        """Tính phí phạt nếu trả muộn"""
        from datetime import datetime as dt
        if self.trang_thai == 'Quá hạn':
            actual_return = self.ngay_tra_thuc_te or dt.now().date()
            if actual_return > self.han_tra:
                days_late = (actual_return - self.han_tra).days
                return days_late * fine_per_day
        return 0
