var weekCounter = 0;

document.addEventListener('DOMContentLoaded', function() {
  const colors = {
    Assignment: "#3397b9",
    Quiz: "#499373",
    Project: "#006064",
    Exam: "#CC4E4E",
    Presentation: "#cc7a50",
    Other: "#C29203",
    Pending: "#999999",
    Clash: "#ff4d4d"  // New color for clash detection
  }

  const calendarEvents = [];
  
  const levelFilter = document.getElementById('level');
  levelFilter.addEventListener('change', function() {
    levelEvents = [];
    const selectedValue = levelFilter.value;
    otherAssessments.forEach((item) => {
      code = item.courseCode.replace(' ', '');
      if (code[4] == selectedValue) {
        if (item.startDate && item.endDate) {
          const eventEl = document.createElement('div');
          eventEl.classList.add('fc-event', 'fc-h-event', 'fc-daygrid-event', 'fc-daygrid-block-event');
  
          eventEl.dataset.color = '#800080';
          eventEl.style.backgroundColor = '#800080';
          
          const eventObj = {
            id: item.caNum,
            title: item.courseCode + '-' + item.a_ID,
            backgroundColor: '#800080',
            editable: false
          };
  
          const isFullDay = item.startTime === '00:00:00' && (item.endTime === '23:59:00' || item.endTime === '00:00:00');
          eventObj.start = item.startDate + 'T' + item.startTime;
          eventObj.end = item.endDate + 'T' + item.endTime;
          eventObj.allDay = isFullDay;
          levelEvents.push(eventObj);
        }
      }
    });
    const allEvents = calendarEvents.concat(levelEvents);
    calendar.setOption('events', allEvents);
    calendar.render();
  });

  const courseFilter = document.getElementById('courses');
  courseFilter.addEventListener('change', function() {
    courseEvents = [];
    const selectedValue = courseFilter.value;
    otherAssessments.forEach((item) => {
      if (item.courseCode == selectedValue) {
        if (item.startDate && item.endDate) {
          const eventEl = document.createElement('div');
          eventEl.classList.add('fc-event', 'fc-h-event', 'fc-daygrid-event', 'fc-daygrid-block-event');
  
          eventEl.dataset.color = '#800080';
          eventEl.style.backgroundColor = '#800080';
          
          const eventObj = {
            id: item.caNum,
            title: item.courseCode + '-' + item.a_ID,
            backgroundColor: '#800080',
            editable: false
          };
  
          const isFullDay = item.startTime === '00:00:00' && (item.endTime === '23:59:00' || item.endTime === '00:00:00');
          eventObj.start = item.startDate + 'T' + item.startTime;
          eventObj.end = item.endDate + 'T' + item.endTime;
          eventObj.allDay = isFullDay;
          courseEvents.push(eventObj);
        }
      }
    });
    const allEvents = calendarEvents.concat(courseEvents);
    calendar.setOption('events', allEvents);
    calendar.render();
  });

  myCourses.forEach((course) => {
    const courseCard = document.createElement('div');
    courseCard.classList.add('course-card');

    const title = document.createElement('h3');
    title.textContent = course;
    courseCard.appendChild(title);

    const eventsContainer = document.createElement('div');
    eventsContainer.classList.add('course-events');

    assessments.forEach((a) => {
      if (a.courseCode == course) {
        const eventEl = document.createElement('div');
        eventEl.classList.add('fc-event', 'fc-h-event', 'fc-daygrid-event', 'fc-daygrid-block-event');

        const typeOfAssessment = getTypeOfAssessment(a.a_ID);
        var color = colors[typeOfAssessment];
        if (a.clashDetected) {
          color = colors.Clash; // Use clash color instead of pending
        }
        eventEl.dataset.color = color;
        eventEl.style.backgroundColor = color;
        
        const eventObj = {
          id: a.caNum,
          title: course + '-' + a.a_ID,
          backgroundColor: color,
          extendedProps: {
            clashDetected: a.clashDetected
          }
        };

        if (a.startDate && a.endDate) {
          const isFullDay = a.startTime === '00:00:00' && (a.endTime === '23:59:00' || a.endTime === '00:00:00');
          eventObj.start = a.startDate + 'T' + a.startTime;
          eventObj.end = a.endDate + 'T' + a.endTime;
          eventObj.allDay = isFullDay;
          calendarEvents.push(eventObj);
        } else {
          eventEl.setAttribute('data-event-id', a.caNum);
          eventEl.innerHTML = '<div class="fc-event-main">' + course + '-' + a.a_ID + '</div>';
          if (a.clashDetected) {
            eventEl.title = 'Warning: Assessment clash detected';
          }
          eventsContainer.appendChild(eventEl);
        }
      }
    });

    courseCard.appendChild(eventsContainer);
    document.getElementById('courses-list').appendChild(courseCard);
  });

  var containerEl = document.getElementById('courses-list');      
  new FullCalendar.Draggable(containerEl, {
    itemSelector: '.fc-event',
    eventData: function(eventEl) {
      return {
        title: eventEl.innerText.trim(),
        backgroundColor: eventEl.dataset.color,
        id: eventEl.dataset.eventId
      }
    }
  });

  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
      left: 'prev,next,today',
      center: 'title',    
      right: 'semesterView,dayGridMonth,timeGridWeek,timeGridDay'
    },
    views: {
      semesterView: {
        type: 'dayGridMonth',
        duration: { weeks: 13 }, 
        buttonText: 'Semester',
        visibleRange: {
          start: semester.start,
          end: semester.end
        }
      }
    },
    editable: true,
    selectable: true,
    droppable: true,
    events: calendarEvents,
    eventResize: function(info) {
      toEditItem(info.event);
    },
    eventDrop: function(info) {
      toEditItem(info.event);
    },
    drop: function(arg) {
      newItem(arg);
      arg.draggedEl.parentNode.removeChild(arg.draggedEl);
    },
    eventDidMount: function(info) {
      // Add tooltip for clash information
      if (info.event.extendedProps && info.event.extendedProps.clashDetected) {
        info.el.title = 'Warning: Assessment clash detected';
      }
    }
  });
  calendar.render();
});

function toEditItem(event) {
  const id = event.id;
  const sDate = formatDate(new Date(event.start));
  const eDate = event.end ? formatDate(new Date(event.end)) : sDate;
  let sTime = formatTime(new Date(event.start));
  let eTime = formatTime(new Date(event.end || event.start));

  if (event.allDay || !sTime || !eTime) {
      sTime = '00:00:00';
      eTime = '23:59:00';
  }

  $.ajax({
      url: '/calendar',
      method: 'POST',
      data: {
          id: id,
          startDate: sDate,
          endDate: eDate,
          startTime: sTime,
          endTime: eTime
      },
      success: function(response) {
          // Update event color based on clash status
          event.setProp('backgroundColor', response.clashDetected ? colors.Clash : getTypeColor(event));
          // Only reload if there was an error
          if (response.error) {
              location.reload();
          }
      },
      error: function(xhr, status, error) {
          console.error('Error:', error);
          location.reload();
      }
  });
}

// Update newItem function similarly
function newItem(event) {
  const id = event.draggedEl.dataset.eventId;
  const sDate = formatDate(new Date(event.date));
  const eDate = sDate;
  let sTime = formatTime(new Date(event.date));
  let eTime = sTime;

  if (event.allDay || !sTime || !eTime) {
      sTime = '00:00:00';
      eTime = '23:59:00';
  }

  $.ajax({
      url: '/calendar',
      method: 'POST',
      data: {
          id: id,
          startDate: sDate,
          endDate: eDate,
          startTime: sTime,
          endTime: eTime
      },
      success: function(response) {
          if (response.error) {
              location.reload();
          } else {
              // Update the event's appearance without reloading
              const fcEvent = calendar.getEventById(id);
              if (fcEvent) {
                  fcEvent.setProp('backgroundColor', response.clashDetected ? colors.Clash : getTypeColor(fcEvent));
              }
          }
      },
      error: function(xhr, status, error) {
          console.error('Error:', error);
          location.reload();
      }
  });
}

function formatDate(dateObj) {
  let year = dateObj.getFullYear();
  let month = dateObj.getMonth() + 1;
  let day = dateObj.getDate();

  let paddedMonth = month.toString();
  if (paddedMonth.length < 2) {
    paddedMonth = "0" + paddedMonth;
  }

  let paddedDate = day.toString();
  if (paddedDate.length < 2) {
    paddedDate = "0" + paddedDate;
  }

  let toStoreDate = `${year}-${paddedMonth}-${paddedDate}`;
  return toStoreDate;
}

function formatTime(timeObj) {
  let hours = timeObj.getHours().toString().padStart(2, '0');
  let minutes = timeObj.getMinutes().toString().padStart(2, '0');
  let seconds = timeObj.getSeconds().toString().padStart(2, '0');
  let toStoreTime = `${hours}:${minutes}:${seconds}`;
  return toStoreTime;
}

function getTypeOfAssessment(eventName) {
  if (eventName.toLowerCase().includes("assignment")) {
    return "Assignment";
  } else if (eventName.toLowerCase().includes("exam")) {
    return "Exam";
  } else if (eventName.toLowerCase().includes("project")) {
    return "Project";
  } else if (eventName.toLowerCase().includes("quiz")) {
    return "Quiz";
  } else if (eventName.toLowerCase().includes("presentation")) {
    return "Presentation";
  }
  return "Other";
}