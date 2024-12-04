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
function showFlashMessage() {
  const flashMessage = document.createElement('div');
  flashMessage.className = 'flash-message';
  flashMessage.innerHTML = `
      <span>Courses saved successfully! Redirecting...</span>
  `;
  document.body.appendChild(flashMessage);
  
  // Add the show class to trigger the fade in
  setTimeout(() => {
      flashMessage.classList.add('show');
  }, 100);
  
  // Remove the message after 3 seconds
  setTimeout(() => {
      flashMessage.classList.remove('show');
      setTimeout(() => {
          flashMessage.remove();
      }, 300); // Wait for fade out animation
  }, 3000);
}

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
          showFlashMessage();
          
          // Redirect after saving
          setTimeout(() => {
              window.location.href = '/assessments';
          }, 1500);
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
});

// Initialize
setExistingCourses();
searchInput.addEventListener("input", handleSearch);

// Show all courses initially
tableRows.forEach((row) => {
  row.style.display = "";
});