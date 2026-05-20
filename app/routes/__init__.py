from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.database import db
from app.models import *
from datetime import datetime, timedelta
from sqlalchemy import desc

bp = Blueprint('main', __name__)

# ===================== TRANG CHỦ =====================

@bp.route('/')
def index():
    """Trang chủ - Dashboard"""
    stats = {
        'total_sach': db.session.query(Sach).count(),
        'total_thanh_vien': db.session.query(ThanhVien).count(),
        'total_nhan_vien': db.session.query(NhanVien).count(),
        'don_muon_dang_hoat': db.session.query(DonMuon).filter_by(trang_thai='Đang mượn').count(),
        'don_muon_qua_han': db.session.query(DonMuon).filter_by(trang_thai='Quá hạn').count(),
    }
    return render_template('index.html', stats=stats)

# ===================== QUẢN LÝ SÁCH =====================

@bp.route('/sach')
def danh_sach_sach():
    """Danh sách sách"""
    page = request.args.get('page', 1, type=int)
    sach = db.paginate(db.select(Sach), page=page, per_page=10)
    return render_template('sach/danh_sach.html', sach=sach)

@bp.route('/sach/them', methods=['GET', 'POST'])
def them_sach():
    """Thêm sách mới"""
    if request.method == 'POST':
        try:
            ma_sach = request.form.get('ma_sach')
            ten_sach = request.form.get('ten_sach')
            tac_gia = request.form.get('tac_gia')
            nam_xb = int(request.form.get('nam_xb') or 0)
            nha_xb = request.form.get('nha_xb')
            so_luong = int(request.form.get('so_luong') or 0)
            ma_tl = request.form.get('ma_tl')
            ma_ncc = request.form.get('ma_ncc')
            # Kiểm tra trùng mã sách trước khi thêm để tránh UNIQUE constraint
            if ma_sach and db.session.get(Sach, ma_sach):
                flash(f'Mã sách "{ma_sach}" đã tồn tại. Vui lòng chọn mã khác.', 'danger')
                return redirect(url_for('main.danh_sach_sach'))

            sach_moi = Sach(
                ma_sach=ma_sach,
                ten_sach=ten_sach,
                tac_gia=tac_gia,
                nam_xb=nam_xb,
                nha_xb=nha_xb,
                so_luong=so_luong,
                ma_tl=ma_tl,
                ma_ncc=ma_ncc
            )
            db.session.add(sach_moi)
            db.session.commit()

            # Sau khi sach_moi đã commit, tạo bản sao (BanSao) tương ứng với số lượng nếu có chi nhánh
            try:
                default_branch = db.session.query(ChiNhanh).first()
                if default_branch and so_luong > 0:
                    for i in range(so_luong):
                        ma_bs = f"{ma_sach}-BS{str(i+1).zfill(3)}"
                        ban_sao = BanSao(
                            ma_ban_sao=ma_bs,
                            ma_sach=ma_sach,
                            ma_chi_nhanh=default_branch.ma_chi_nhanh,
                            ngay_nhap=datetime.now().date()
                        )
                        db.session.add(ban_sao)
                    db.session.commit()
            except Exception:
                db.session.rollback()
            flash(f'Thêm sách "{ten_sach}" thành công!', 'success')
            return redirect(url_for('main.danh_sach_sach'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    
    the_loai = db.session.query(ThaiLoai).all()
    nha_cung_cap = db.session.query(NhaCungCap).all()
    return render_template('sach/them.html', the_loai=the_loai, nha_cung_cap=nha_cung_cap)

@bp.route('/sach/<ma_sach>/sua', methods=['GET', 'POST'])
def sua_sach(ma_sach):
    """Sửa thông tin sách"""
    sach = db.session.get(Sach, ma_sach)
    if not sach:
        flash('Không tìm thấy sách', 'danger')
        return redirect(url_for('main.danh_sach_sach'))
    
    if request.method == 'POST':
        try:
            sach.ten_sach = request.form.get('ten_sach')
            sach.tac_gia = request.form.get('tac_gia')
            sach.nam_xb = int(request.form.get('nam_xb') or 0)
            sach.nha_xb = request.form.get('nha_xb')
            sach.so_luong = int(request.form.get('so_luong') or 0)
            sach.ma_tl = request.form.get('ma_tl')
            sach.ma_ncc = request.form.get('ma_ncc')
            
            # Nếu tăng số lượng, tạo thêm bản sao tương ứng
            try:
                existing_count = db.session.query(BanSao).filter_by(ma_sach=sach.ma_sach).count()
                if sach.so_luong > existing_count:
                    default_branch = db.session.query(ChiNhanh).first()
                    if default_branch:
                        for i in range(existing_count, sach.so_luong):
                            ma_bs = f"{sach.ma_sach}-BS{str(i+1).zfill(3)}"
                            ban_sao = BanSao(
                                ma_ban_sao=ma_bs,
                                ma_sach=sach.ma_sach,
                                ma_chi_nhanh=default_branch.ma_chi_nhanh,
                                ngay_nhap=datetime.now().date()
                            )
                            db.session.add(ban_sao)
            except Exception:
                pass

            db.session.commit()
            flash('Cập nhật sách thành công!', 'success')
            return redirect(url_for('main.danh_sach_sach'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    
    the_loai = db.session.query(ThaiLoai).all()
    nha_cung_cap = db.session.query(NhaCungCap).all()
    return render_template('sach/sua.html', sach=sach, the_loai=the_loai, nha_cung_cap=nha_cung_cap)

@bp.route('/sach/<ma_sach>/xoa', methods=['POST'])
def xoa_sach(ma_sach):
    """Xóa sách"""
    sach = db.session.get(Sach, ma_sach)
    if sach:
        try:
            db.session.delete(sach)
            db.session.commit()
            flash('Xóa sách thành công!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    return redirect(url_for('main.danh_sach_sach'))

# ===================== QUẢN LÝ THÀNH VIÊN =====================

@bp.route('/thanh-vien')
def danh_sach_thanh_vien():
    """Danh sách thành viên"""
    page = request.args.get('page', 1, type=int)
    thanh_vien = db.paginate(db.select(ThanhVien), page=page, per_page=10)
    return render_template('thanh_vien/danh_sach.html', thanh_vien=thanh_vien)

@bp.route('/thanh-vien/them', methods=['GET', 'POST'])
def them_thanh_vien():
    """Thêm thành viên mới"""
    if request.method == 'POST':
        try:
            from datetime import date, timedelta
            
            ma_thanh_vien = request.form.get('ma_thanh_vien')
            ho_ten = request.form.get('ho_ten')
            sdt = request.form.get('sdt')
            email = request.form.get('email')
            ghi_chu = request.form.get('ghi_chu')
            
            thanh_vien_moi = ThanhVien(
                ma_thanh_vien=ma_thanh_vien,
                ho_ten=ho_ten,
                sdt=sdt,
                email=email,
                ghi_chu=ghi_chu,
                ngay_dang_ky=date.today()
            )
            
            # Tạo thẻ thư viện
            ma_the = f"THE-{ma_thanh_vien}"
            the_thu_vien = TheThuVien(
                ma_the=ma_the,
                ma_thanh_vien=ma_thanh_vien,
                ngay_cap=date.today(),
                ngay_het_han=date.today() + timedelta(days=365),
                trang_thai='Hoạt động'
            )
            
            db.session.add(thanh_vien_moi)
            db.session.add(the_thu_vien)
            db.session.commit()
            flash(f'Thêm thành viên "{ho_ten}" thành công!', 'success')
            return redirect(url_for('main.danh_sach_thanh_vien'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    
    return render_template('thanh_vien/them.html')

@bp.route('/thanh-vien/<ma_thanh_vien>/sua', methods=['GET', 'POST'])
def sua_thanh_vien(ma_thanh_vien):
    """Sửa thông tin thành viên"""
    thanh_vien = db.session.get(ThanhVien, ma_thanh_vien)
    if not thanh_vien:
        flash('Không tìm thấy thành viên', 'danger')
        return redirect(url_for('main.danh_sach_thanh_vien'))
    
    if request.method == 'POST':
        try:
            thanh_vien.ho_ten = request.form.get('ho_ten')
            thanh_vien.sdt = request.form.get('sdt')
            thanh_vien.email = request.form.get('email')
            thanh_vien.ghi_chu = request.form.get('ghi_chu')
            
            db.session.commit()
            flash('Cập nhật thành viên thành công!', 'success')
            return redirect(url_for('main.danh_sach_thanh_vien'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    
    return render_template('thanh_vien/sua.html', thanh_vien=thanh_vien)

# ===================== QUẢN LÝ NHÂN VIÊN =====================

@bp.route('/nhan-vien')
def danh_sach_nhan_vien():
    """Danh sách nhân viên"""
    page = request.args.get('page', 1, type=int)
    nhan_vien = db.paginate(db.select(NhanVien), page=page, per_page=10)
    return render_template('nhan_vien/danh_sach.html', nhan_vien=nhan_vien)

@bp.route('/nhan-vien/them', methods=['GET', 'POST'])
def them_nhan_vien():
    """Thêm nhân viên mới"""
    if request.method == 'POST':
        try:
            ma_nv = request.form.get('ma_nv')
            ho_ten = request.form.get('ho_ten')
            dia_chi = request.form.get('dia_chi')
            sdt = request.form.get('sdt')
            email = request.form.get('email')
            ma_chi_nhanh = request.form.get('ma_chi_nhanh')
            
            nhan_vien_moi = NhanVien(
                ma_nv=ma_nv,
                ho_ten=ho_ten,
                dia_chi=dia_chi,
                sdt=sdt,
                email=email,
                ma_chi_nhanh=ma_chi_nhanh,
                ngay_vao=datetime.now().date()
            )
            
            db.session.add(nhan_vien_moi)
            db.session.commit()
            flash(f'Thêm nhân viên "{ho_ten}" thành công!', 'success')
            return redirect(url_for('main.danh_sach_nhan_vien'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    
    chi_nhanh = db.session.query(ChiNhanh).all()
    return render_template('nhan_vien/them.html', chi_nhanh=chi_nhanh)

# ===================== QUẢN LÝ MƯỢN / TRẢ =====================

@bp.route('/don-muon')
def danh_sach_don_muon():
    """Danh sách đơn mượn"""
    page = request.args.get('page', 1, type=int)
    trang_thai = request.args.get('trang_thai', None)
    
    query = db.select(DonMuon)
    if trang_thai:
        query = query.where(DonMuon.trang_thai == trang_thai)
    
    don_muon = db.paginate(query, page=page, per_page=10)
    return render_template('don_muon/danh_sach.html', don_muon=don_muon, trang_thai=trang_thai)

@bp.route('/don-muon/them', methods=['GET', 'POST'])
def them_don_muon():
    """Mượn sách mới"""
    if request.method == 'POST':
        try:
            from datetime import date, timedelta
            
            ma_don_muon = request.form.get('ma_don_muon')
            ma_thanh_vien = request.form.get('ma_thanh_vien')
            ma_ban_sao = request.form.get('ma_ban_sao')
            ma_nv = request.form.get('ma_nv')
            ngay_muon = date.today()
            han_tra = ngay_muon + timedelta(days=30)

            # Chỉ cho mượn nếu bản sao chưa có đơn mượn đang hoạt động
            active_loan = db.session.query(DonMuon).filter(
                DonMuon.ma_ban_sao == ma_ban_sao,
                DonMuon.trang_thai.in_(['Đang mượn', 'Quá hạn'])
            ).first()
            if active_loan:
                flash('Bản sao này đang được mượn. Hãy chọn bản sao khác.', 'danger')
                return redirect(url_for('main.them_don_muon'))

            if not db.session.get(BanSao, ma_ban_sao):
                flash('Không tìm thấy bản sao sách.', 'danger')
                return redirect(url_for('main.them_don_muon'))
            
            don_muon_moi = DonMuon(
                ma_don_muon=ma_don_muon,
                ma_thanh_vien=ma_thanh_vien,
                ma_ban_sao=ma_ban_sao,
                ma_nv=ma_nv,
                ngay_muon=ngay_muon,
                han_tra=han_tra,
                trang_thai='Đang mượn'
            )
            
            db.session.add(don_muon_moi)
            db.session.commit()
            flash('Tạo đơn mượn thành công!', 'success')
            return redirect(url_for('main.danh_sach_don_muon'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    
    thanh_vien = db.session.query(ThanhVien).all()
    active_borrowed = db.session.query(DonMuon.ma_ban_sao).filter(
        DonMuon.trang_thai.in_(['Đang mượn', 'Quá hạn'])
    ).subquery()
    ban_sao = db.session.query(BanSao).filter(~BanSao.ma_ban_sao.in_(db.select(active_borrowed.c.ma_ban_sao))).all()
    nhan_vien = db.session.query(NhanVien).all()
    return render_template('don_muon/them.html', thanh_vien=thanh_vien, ban_sao=ban_sao, nhan_vien=nhan_vien)

@bp.route('/don-muon/<ma_don_muon>/tra', methods=['GET', 'POST'])
def tra_sach(ma_don_muon):
    """Trả sách"""
    don_muon = db.session.get(DonMuon, ma_don_muon)
    if not don_muon:
        flash('Không tìm thấy đơn mượn', 'danger')
        return redirect(url_for('main.danh_sach_don_muon'))
    
    if request.method == 'POST':
        try:
            from datetime import date
            from app.config import Config
            
            don_muon.ngay_tra_thuc_te = date.today()
            
            # Kiểm tra trả muộn
            if don_muon.ngay_tra_thuc_te > don_muon.han_tra:
                don_muon.trang_thai = 'Quá hạn'
                days_late = (don_muon.ngay_tra_thuc_te - don_muon.han_tra).days
                don_muon.phu_phat = days_late * Config.FINE_PER_DAY
            else:
                don_muon.trang_thai = 'Đã trả'
                don_muon.phu_phat = 0
            
            db.session.commit()
            flash('Trả sách thành công!', 'success')
            return redirect(url_for('main.danh_sach_don_muon'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    
    from datetime import date
    ngay_hom_nay = date.today()
    phi_phat_du_kien = 0
    if ngay_hom_nay > don_muon.han_tra:
        phi_phat_du_kien = (ngay_hom_nay - don_muon.han_tra).days * 5000

    return render_template(
        'don_muon/tra.html',
        don_muon=don_muon,
        ngay_hom_nay=ngay_hom_nay,
        phi_phat_du_kien=phi_phat_du_kien
    )

# ===================== QUẢN LÝ THẺ THƯ VIỆN =====================

@bp.route('/the-thu-vien')
def danh_sach_the_thu_vien():
    """Danh sách thẻ thư viện"""
    page = request.args.get('page', 1, type=int)
    the_thu_vien = db.paginate(db.select(TheThuVien), page=page, per_page=10)
    return render_template('the_thu_vien/danh_sach.html', the_thu_vien=the_thu_vien)

# ===================== QUẢN LÝ CHI NHÁNH =====================

@bp.route('/chi-nhanh')
def danh_sach_chi_nhanh():
    """Danh sách chi nhánh"""
    chi_nhanh = db.session.query(ChiNhanh).all()
    return render_template('chi_nhanh/danh_sach.html', chi_nhanh=chi_nhanh)

@bp.route('/chi-nhanh/them', methods=['GET', 'POST'])
def them_chi_nhanh():
    """Thêm chi nhánh mới"""
    if request.method == 'POST':
        try:
            ma_chi_nhanh = request.form.get('ma_chi_nhanh')
            ten_chi_nhanh = request.form.get('ten_chi_nhanh')
            dia_chi = request.form.get('dia_chi')
            sdt = request.form.get('sdt')
            
            chi_nhanh_moi = ChiNhanh(
                ma_chi_nhanh=ma_chi_nhanh,
                ten_chi_nhanh=ten_chi_nhanh,
                dia_chi=dia_chi,
                sdt=sdt
            )
            
            db.session.add(chi_nhanh_moi)
            db.session.commit()
            flash('Thêm chi nhánh thành công!', 'success')
            return redirect(url_for('main.danh_sach_chi_nhanh'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    
    return render_template('chi_nhanh/them.html')
