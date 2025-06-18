from flask import Flask, render_template, request, redirect

app = Flask(__name__)


# 자바 컨트롤러 getMappting 과 같은 기능, "라우트"라고 부름 |  경로에 의거해 부르는 상황
@app.route("/")
def index():
    return "Hello!"


@app.route("/create", methods=["GET", "POST"])  # == @GetMapping("/create")
def create():
    if request.method == "GET":
        return render_template("create.html")
    else:
        name = request.form["name"]
        print(f"name {name}")
    return redirect("/")


@app.route("/read/<int:post_id>")  # == @GetMapping("/read/1")
def read(post_id):
    return f"Read {post_id}"
