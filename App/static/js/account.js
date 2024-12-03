const searchInput = document.getElementById("search_box");
const searchDropdown = document.getElementById("search-dropdown");
const selectedCourses = document.getElementById("selected_courses");
const tableBody = document.getElementById("courseTableBody");
const tableRows = tableBody.querySelectorAll("tr.course-row");

// Add click event listeners to table rows
tableRows.forEach((row) => {
  row.addEventListener("click", (event) => {
    event.stopPropagation();
    const courseCode = row.querySelector("td").textContent.trim();
    addCourse(courseCode);
  });
});

function handleSearch(e) {
  e.preventDefault();
  const searchTerm = searchInput.value.toLowerCase().trim();

  tableRows.forEach((row) => {
    const courseCode = row.querySelector("td").textContent.toLowerCase().trim();
    
    // Show row if courseCode contains search term (partial match)
    if (courseCode.includes(searchTerm)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });

  // Show/hide dropdown based on search input
  if (searchTerm.length > 0) {
    searchDropdown.style.display = "block";
  } else {
    searchDropdown.style.display = "none";
  }
}

function addCourse(course) {
  if (!myCourses.includes(course)) {
    myCourses.push(course);
    const courseElement = document.createElement("p");
    courseElement.textContent = course;
    courseElement.classList.add("selected-course");
    selectedCourses.appendChild(courseElement);
    const courseCodesInput = document.getElementById("courseCodesInput");
    courseCodesInput.value = JSON.stringify(myCourses);
  }
  resetSearch();
}

function resetSearch() {
  searchInput.value = "";
  searchDropdown.style.display = "none";
}

function setExistingCourses() {
  myCourses.forEach(course => {
    const courseElement = document.createElement("p");
    courseElement.textContent = course;
    courseElement.classList.add("selected-course");
    selectedCourses.appendChild(courseElement);
    const courseCodesInput = document.getElementById("courseCodesInput");
    courseCodesInput.value = JSON.stringify(myCourses);
  });
}

// Initialize
setExistingCourses();
searchInput.addEventListener("input", handleSearch);