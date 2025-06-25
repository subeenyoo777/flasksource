from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    request,
    session,
    flash,
    g,
)
from werkzeug.security import check_password_hash, generate_password_hash
from book.forms import UserForm, UserLoginForm
from book.models import User
from book import db
import functools

# Blueprint("별칭", 실행되는 모듈명 가져오기, url_prefix="/" )
bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == "GET" else ""
            return redirect(url_for("auth.login", next=_next))
        return view(*args, **kwargs)

    return wrapped_view


@bp.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("main.index"))


@bp.route("/login/", methods=["GET", "POST"])
def login():

    form = UserLoginForm()
    if request.method == "POST" and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session["user_id"] = user.id
            # _next 가져오기(로그인하지 않고 경로를 요청하는 경우 로그인 이후 움직일 경로)
            _next = request.args.get("next", "")
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for("main.index"))

        flash(error)
    return render_template("auth/login.html", form=form)


@bp.before_app_request  # 라우팅 함수보다 항상 먼저 실행해주세요
def load_logged_in_user():
    # 세션에서 정보 가져오기
    user_id = session.get("user_id")
    if user_id is None:  # (js) = undefined
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route("/signup/", methods=["GET", "POST"])
def signup():
    form = UserForm()

    if request.method == "POST" and form.validate_on_submit():

        # 동일한 id 확인
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(
                username=form.username.data,
                password=generate_password_hash(form.password1.data),  # = 암호화
                email=form.email.data,
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("main.index"))
        else:
            flash("이미 존재하는 사용자입니다.")  # 오류 고의 발생

    return render_template("auth/signup.html", form=form)
