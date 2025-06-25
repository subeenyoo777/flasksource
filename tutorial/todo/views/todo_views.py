from flask import Blueprint, render_template, request, redirect, url_for
from todo.models import Todo
from todo.forms import TodoForm
from datetime import datetime
from todo import db

# Blueprint("별칭", 실행되는 모듈명 가져오기, url_prefix="/" )
bp = Blueprint("todo", __name__, url_prefix="/todo")


@bp.route("/edit/<int:id>/", methods=["GET", "POST"])
def edit(id):
    todo = Todo.query.get_or_404(id)
    if request.method == "POST":
        form = TodoForm()
        if form.validate_on_submit():
            form.populate_obj(todo)  # 원본 todo과 form 에 담긴 변경된 todo 비교
            db.session.commit()
            return redirect(url_for("todo.detail", id=id))
    else:
        form = TodoForm(obj=todo)
    return render_template("todo/todo_edit.html", form=form)


@bp.route("/done/<int:id>/")
def done(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = True
    db.session.commit()
    return redirect(url_for("todo.detail", id=todo.id))


@bp.route("/done/list/")
def done_list():
    todos = Todo.query.filter(Todo.completed == 1).order_by(Todo.id.desc())
    return render_template("todo/done_list.html", todos=todos)


@bp.route("/list/")
def list():
    todos = Todo.query.filter(Todo.completed == 0).order_by(Todo.id.desc())
    return render_template("todo/todo_list.html", todos=todos)


@bp.route("/detail/<int:id>/")
def detail(id):
    todo = Todo.query.get_or_404(id)
    return render_template("todo/todo_detail.html", todo=todo)


@bp.route("/register/", methods=["GET", "POST"])
def register():
    form = TodoForm()

    if request.method == "POST" and form.validate_on_submit():
        todo = Todo(
            title=form.title.data,
            description=form.description.data,
            important=form.important.data,
            created=datetime.now(),
        )
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("todo/todo_create.html", form=form)
