from flask import Blueprint, redirect, url_for, render_template, request
from book.models import Book
from book.forms import BookForm
from book import db
from datetime import datetime
from book.views.auth_views import login_required

# Blueprint("별칭", 실행되는 모듈명 가져오기, url_prefix="/" )
bp = Blueprint("book", __name__, url_prefix="/book")


# 로그인 한 후에 이 작업들이 실행됨.
@login_required
@bp.route("/create/", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        form = BookForm()
        if form.validate_on_submit():

            book = Book(
                title=form.title.data,
                author=form.author.data,
                price=form.price.data,
                description=form.description.data,
                created=datetime.now(),
            )
            db.session.add(book)
            db.session.commit()
            return redirect(url_for("book.list"))
    return render_template("book/create.html", form=form)


@bp.route("/list/")
def list():
    # 페이지 나누기
    # ?page=2

    page = request.args.get("page", type=int, default=1)

    books = Book.query.order_by(Book.code.desc())
    books = books.paginate(page=page, per_page=10)
    return render_template("book/list.html", books=books)


@bp.route("/detail/<int:code>/")
def detail(code):
    book = Book.query.get_or_404(code)
    return render_template("book/detail.html", book=book)


@bp.route("/edit/<int:code>/", methods=["GET", "POST"])
@login_required
def edit(code):
    book = Book.query.get_or_404(code)

    if request.method == "POST":
        form = BookForm()
        if form.validate_on_submit():
            form.populate_obj(book)  # 원본 todo과 form 에 담긴 변경된 todo 비교
            db.session.commit()
            return redirect(url_for("book.detail", code=code))
    else:
        form = BookForm(obj=book)  # form과 book 연결
    return render_template("book/edit.html", form=form)


@bp.route("/remove/<int:code>/")
@login_required
def remove(code):
    book = Book.query.get_or_404(code)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("book/list"))
