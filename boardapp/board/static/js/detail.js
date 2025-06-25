// 삭제 버튼 클릭 시 confirm('정말 삭제하시겠습니까?') 띄우기

const elements = document.querySelectorAll(".delete");

elements.forEach((ele) => {
  ele.addEventListener("click", (e) => {
    // a 기능 중지
    e.preventDefault();

    // href 가져오기
    const href = e.target.getAttribute("href");
    console.log(href);

    if (confirm("정말 삭제하시겠습니까?")) {
      location.href = href;
    }
  });
});
