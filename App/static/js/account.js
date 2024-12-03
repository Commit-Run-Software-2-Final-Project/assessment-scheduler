const searchInput = document.getElementById("search_box");
const searchDropdown = document.getElementById("search-dropdown");
const selectedCourses = document.getElementById("selected_courses");
const tableBody = document.getElementById("courseTableBody");
const tableRows = tableBody.querySelectorAll("tr.course-row");
const saveForm = document.getElementById('save-course-form');

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
    
    // If search is empty, show all courses
    if (searchTerm === "") {
      row.style.display = "";
    }
    // Otherwise, filter based on search term
    else if (courseCode.includes(searchTerm)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
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
  // Just clear the search input without hiding courses
  searchInput.value = "";
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

const flashMessage = document.createElement('div');
flashMessage.className = 'flash-message';
flashMessage.innerHTML = `
    <span>Courses saved successfully!</span>
`;
document.body.appendChild(flashMessage);

// Add form submit handler
saveForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Submit the form using fetch
    fetch('/account', {
        method: 'POST',
        body: new FormData(this)
    })
    .then(response => {
        if (response.ok) {
            // Show success message
            flashMessage.classList.add('show');
            
            // Hide message after 3 seconds
            setTimeout(() => {
                flashMessage.classList.remove('show');
            }, 3000);
            
            // Optional: Redirect after saving
            setTimeout(() => {
                window.location.href = '/assessments';
            }, 1500);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // You could also show an error message here
    });
});

// Initialize
setExistingCourses();
searchInput.addEventListener("input", handleSearch);

// Show all courses initially
tableRows.forEach((row) => {
  row.style.display = "";
});