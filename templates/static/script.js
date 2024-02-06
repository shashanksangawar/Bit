// --------------Side Bar--------------
let logout = document.querySelector(".logout");
let arrow = document.querySelectorAll(".arrow");
for (var i = 0; i < arrow.length; i++) {
  arrow[i].addEventListener("click", (e)=>{
let arrowParent = e.target.parentElement.parentElement;//selecting main parent of arrow
arrowParent.classList.toggle("showMenu");
  });
}

let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".bx-menu");
let calculatorContainer = document.querySelector(".calculator-container");
let chartContainer = document.querySelector(".chart-container");

sidebarBtn.addEventListener("click", ()=>{
  logout.classList.toggle("active");
  sidebar.classList.toggle("close");
  calculatorContainer.classList.toggle("display");
  chartContainer.classList.toggle("display");
});

