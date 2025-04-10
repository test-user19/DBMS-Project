// Initialize Lucide icons
lucide.createIcons();

const API_BASE_URL = 'http://127.0.0.1:5000/api';

// Show dashboard
function showDashboard() {
  document.getElementById('landing').style.display = 'none';
  document.getElementById('dashboard').style.display = 'block';
  // Load students list on dashboard show
  loadStudents();
}

// Switch between dashboard tabs
function switchTab(tab) {
  // Hide all forms
  document.getElementById('students-form').style.display = 'none';
  document.getElementById('attendance-form').style.display = 'none';
  document.getElementById('performance-form').style.display = 'none';
  document.getElementById('reports-section').style.display = 'none';

  // Show selected form
  if (tab === 'students') {
    document.getElementById('students-form').style.display = 'block';
  } else if (tab === 'attendance') {
    document.getElementById('attendance-form').style.display = 'block';
  } else if (tab === 'performance') {
    document.getElementById('performance-form').style.display = 'block';
  } else if (tab === 'reports') {
    document.getElementById('reports-section').style.display = 'block';
    // Initially load students list in reports
    switchReportTab('students-list');
  }

  // Update active tab
  const tabs = document.querySelectorAll('.tabs .tab');
  tabs.forEach(t => t.classList.remove('active'));
  event.target.classList.add('active');
}

// Handle form submissions
async function handleStudentSubmit() {
  await addStudent();
}

async function handleAttendanceSubmit() {
  await markAttendance();
}

async function handlePerformanceSubmit() {
  await addPerformance();
}

// Switch between report tabs
function switchReportTab(reportType) {
  const content = document.getElementById('reports-content');
  document.getElementById('student-list').style.display = 'none';
  document.getElementById('attendance-report').style.display = 'none';
  document.getElementById('performance-report').style.display = 'none';
  document.getElementById('bulk-attendance-form').style.display = 'none';
  document.getElementById('attendance-summary').style.display = 'none';
  document.getElementById('average-performance').style.display = 'none';
  document.getElementById('monthly-view').style.display = 'none';
  console.log(content)

  if (reportType === 'students-list') {
    content.innerHTML = ''
    document.getElementById('student-list').style.display = 'block';
    loadStudents();
  } else if (reportType === 'attendance-report') {
    document.getElementById('attendance-report').style.display = 'block';
    content.innerHTML = `<h3>Attendance Report</h3><label for="attendance_report_date">Select Date:</label><input type="date" id="attendance_report_date"><button onclick="loadAttendance()" class="btn" style="margin-top: 0.5rem;">Load Report</button>`;
  } else if (reportType === 'performance-report') {
    document.getElementById('performance-report').style.display = 'block';
    content.innerHTML = `<h3>Performance Report</h3><label for="performance_report_student_id">Enter Student ID:</label><input type="number" id="performance_report_student_id"><button onclick="loadPerformance()" class="btn" style="margin-top: 0.5rem;">Load Report</button>`;
  } else if (reportType === 'bulk-attendance') {
    content.innerHTML = ''
    document.getElementById('bulk-attendance-form').style.display = 'block';
  } else if (reportType === 'attendance-summary') {
    content.innerHTML = ''
    document.getElementById('attendance-summary').style.display = 'block';
    loadAttendanceSummary();
  } else if (reportType === 'average-performance') {
    content.innerHTML = ''
    document.getElementById('average-performance').style.display = 'block';
    loadAveragePerformance();
  } else if (reportType === 'monthly-view') {
    content.innerHTML = ''
    document.getElementById('monthly-view').style.display = 'block';
    // loadLatestAttendance();
  }

  // Update active tab
  const tabs = document.querySelectorAll('#reports-section .tabs .tab');
  tabs.forEach(t => t.classList.remove('active'));
  const clickedTab = Array.from(tabs).find(tab => tab.textContent.toLowerCase().replace(' ', '-') === reportType);
  if (clickedTab) {
    clickedTab.classList.add('active');
  }
}

async function addStudent() {
  const name = document.getElementById('name').value;
  const roll_number = document.getElementById('roll_number').value;
  const dob = document.getElementById('dob').value;
  const email = document.getElementById('email').value;
  const phone = document.getElementById('phone').value;

  const data = { name, roll_number, dob, email, phone };
  const response = await fetch(`${API_BASE_URL}/students`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const result = await response.json();
  alert(result.message);
  if (response.ok) {
    document.getElementById('students-form').reset();
    loadStudents(); // Reload student list after adding
  }
}

async function markAttendance() {
  const student_id = document.getElementById('student_id_attendance').value;
  const attendance_date = document.getElementById('attendance_date').value;
  const status = document.getElementById('status').value;
  const notes = document.getElementById('attendance_notes').value;

  const data = {
    attendance_date: attendance_date,
    student_statuses: [
      {
        student_id: parseInt(student_id),
        status: status,
        notes: notes
      }
    ]
  };
  const response = await fetch(`${API_BASE_URL}/attendance/bulk`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const result = await response.json();
  console.log(result)
  if (response.ok) {
    alert(result.message);
    document.getElementById('attendance-form').reset();
  } else {
    alert(result.error)
  }
}

async function addPerformance() {
  const student_id = document.getElementById('student_id_performance').value;
  const subject = document.getElementById('subject').value;
  const exam_date = document.getElementById('exam_date').value;
  const marks = document.getElementById('marks').value;
  // const grade = document.getElementById('grade').value;
  const notes = document.getElementById('performance_notes').value;

  const data = { student_id: parseInt(student_id), subject, exam_date, marks: parseFloat(marks), notes };
  const response = await fetch(`${API_BASE_URL}/performance`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const result = await response.json();
  alert(result.message);
  if (response.ok) {
    document.getElementById('performance-form').reset();
  }
}

async function loadStudents() {
  const response = await fetch(`${API_BASE_URL}/students`);
  const students = await response.json();
  let html = '<table><thead><tr><th>ID</th><th>Name</th><th>Roll Number</th><th>Actions</th></tr></thead><tbody>';
  students.forEach(student => {
    html += `<tr>
            <td>${student.student_id}</td>
            <td>${student.name}</td>
            <td>${student.roll_number}</td>
            <td>
          <button class="delete-btn" onclick="deleteStudent(${student.student_id})">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 6h18"></path>
              <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
              <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
              <line x1="10" y1="11" x2="10" y2="17"></line>
              <line x1="14" y1="11" x2="14" y2="17"></line>
            </svg>
            Delete
          </button>
        </td>
        </tr>`;
  });
  html += '</tbody></table>';
  document.getElementById('student-list').innerHTML = html;
}

async function loadAttendance() {
  const date = document.getElementById('attendance_report_date').value;
  if (!date) {
    alert('Please select a date.');
    return;
  }
  const response = await fetch(`${API_BASE_URL}/attendance/${date}`);
  const attendanceRecords = await response.json();
  let html = '<table><thead><tr><th>Student Name</th><th>Date</th><th>Status</th><th>Notes</th></tr></thead><tbody>';
  attendanceRecords.forEach(record => {
    html += `<tr><td>${record.student_name}</td><td>${record.attendance_date}</td><td>${record.status}</td><td>${record.notes || ''}</td></tr>`;
  });
  html += '</tbody></table>';
  document.getElementById('attendance-report').innerHTML = html;
}

async function loadPerformance() {
  const student_id = document.getElementById('performance_report_student_id').value;
  if (!student_id) {
    alert('Please enter a Student ID.');
    return;
  }
  const response = await fetch(`${API_BASE_URL}/performance/student/${student_id}`);
  const performanceRecords = await response.json();
  let html = '<table><thead><tr><th>Subject</th><th>Exam Date</th><th>Marks</th><th>Grade</th><th>Notes</th></tr></thead><tbody>';
  performanceRecords.forEach(record => {
    html += `<tr><td>${record.subject}</td><td>${record.exam_date || ''}</td><td>${record.marks !== null ? record.marks : ''}</td><td>${record.grade || ''}</td><td>${record.notes || ''}</td></tr>`;
  });
  html += '</tbody></table>';
  document.getElementById('performance-report').innerHTML = html;
}

async function prepareBulkAttendance() {
  const date = document.getElementById('bulk_attendance_date').value;
  if (!date) {
    alert('Please select a date for bulk attendance.');
    return;
  }
  const response = await fetch(`${API_BASE_URL}/students`);
  const students = await response.json();
  let formHtml = '<table><thead><tr><th>Student Name</th><th>Status</th><th>Notes</th></tr></thead><tbody>';
  students.forEach(student => {
    formHtml += `<tr><td>${student.name} (ID: ${student.student_id})</td><td><select id="status_${student.student_id}"><option value="Present">Present</option><option value="Absent">Absent</option><option value="Late">Late</option></select></td><td><input type="text" id="notes_${student.student_id}"></td></tr>`;
  });
  formHtml += '</tbody></table><button onclick="recordBulkAttendance()" class="btn" style="margin-top: 0.5rem;">Record Bulk Attendance</button>';
  document.getElementById('bulk-attendance-form-content').innerHTML = formHtml;
}

async function recordBulkAttendance() {
  const date = document.getElementById('bulk_attendance_date').value;
  const studentStatuses = [];
  const studentListResponse = await fetch(`${API_BASE_URL}/students`);
  const students = await studentListResponse.json();
  students.forEach(student => {
    const status = document.getElementById(`status_${student.student_id}`).value;
    const notes = document.getElementById(`notes_${student.student_id}`).value;
    studentStatuses.push({ student_id: student.student_id, status: status, notes: notes });
  });

  const data = { attendance_date: date, student_statuses: studentStatuses };
  const response = await fetch(`${API_BASE_URL}/attendance/bulk`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const result = await response.json();
  if (response.ok) {
    alert(result.message);
    document.getElementById('bulk-attendance-form-content').innerHTML = '';
    document.getElementById('bulk_attendance_date').value = '';
  } else {
    alert(result.error);
  }
}

async function loadAttendanceSummary() {
  const response = await fetch(`${API_BASE_URL}/views/attendance_summary`);
  const summaryData = await response.json();
  let html = '<table><thead><tr><th>Student ID</th><th>Name</th><th>Total Present Days</th></tr></thead><tbody>';
  summaryData.forEach(item => {
    html += `<tr><td>${item.student_id}</td><td>${item.name}</td><td>${item.total_present_days}</td></tr>`;
  });
  html += '</tbody></table>';
  document.getElementById('attendance-summary').innerHTML = html;
}

async function loadAveragePerformance() {
  const response = await fetch(`${API_BASE_URL}/views/average_performance`);
  const performanceData = await response.json();
  let html = '<table><thead><tr><th>Student ID</th><th>Name</th><th>Average Marks</th></tr></thead><tbody>';
  performanceData.forEach(item => {
    html += `<tr><td>${item.student_id}</td><td>${item.name}</td><td>${item.average_marks !== null ? item.average_marks.toFixed(2) : 'N/A'}</td></tr>`;
  });
  html += '</tbody></table>';
  document.getElementById('average-performance').innerHTML = html;
}

async function loadLatestAttendance() {
  const response = await fetch(`${API_BASE_URL}/views/latest_attendance`);
  const latestAttendanceData = await response.json();
  let html = '<table><thead><tr><th>Student ID</th><th>Name</th><th>Latest Status</th><th>Latest Date</th></tr></thead><tbody>';
  latestAttendanceData.forEach(item => {
    html += `<tr><td>${item.student_id}</td><td>${item.name}</td><td>${item.latest_attendance_status || 'N/A'}</td><td>${item.latest_attendance_date || 'N/A'}</td></tr>`;
  });
  html += '</tbody></table>';
  document.getElementById('monthly-view').innerHTML = html;
}
async function deleteStudent(studentId) {
  if (confirm(`Are you sure you want to delete student with ID: ${studentId}?`)) {
    const response = await fetch(`${API_BASE_URL}/students/${studentId}`, {
      method: 'DELETE',
    });

    if (response.ok) {
      alert(`Student with ID: ${studentId} deleted successfully!`);
      loadStudents(); // Reload the student list
    } else {
      const errorData = await response.json();
      alert(`Error deleting student with ID: ${studentId}: ${errorData.error || 'An unknown error occurred.'}`);
    }
  }
}



let currentDate = new Date();
let presentDates = [];
const months = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

function getDaysInMonth(year, month) {
  return new Date(year, month + 1, 0).getDate();
}

function getFirstDayOfMonth(year, month) {
  return new Date(year, month, 1).getDay();
}

function navigateMonth(direction) {
  if (direction === 'prev') {
    currentDate.setMonth(currentDate.getMonth() - 1);
  } else {
    currentDate.setMonth(currentDate.getMonth() + 1);
  }
  loadMonthlyAttendance();
}

async function loadMonthlyAttendance() {
  const studentId = document.getElementById('studentId').value;
  const month = currentDate.getMonth() + 1;
  const year = currentDate.getFullYear();

  if (!studentId) {
    alert('Please enter Student ID.');
    return;
  }

  const attendanceData = {
    studentId: parseInt(studentId),
    month: month,
    year: year
  };

  const response = await fetch(`${API_BASE_URL}/attendance/monthly`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(attendanceData)
  });

  const data = await response.json();
  if (response.ok) {
    presentDates = data.presentDates || [];
    renderCalendar();
  } else {
    alert('Failed to load attendance data.');
    presentDates = [];
    renderCalendar();
  }
}

function renderCalendar() {
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();
  const daysInMonth = getDaysInMonth(year, month);
  const firstDayOfMonth = getFirstDayOfMonth(year, month);

  document.getElementById('monthYear').textContent = `${months[month]} ${year}`;
  const calendarEl = document.getElementById('calendar');
  calendarEl.innerHTML = '';

  for (let i = 0; i < firstDayOfMonth; i++) {
    const emptyDay = document.createElement('div');
    emptyDay.className = 'empty';
    calendarEl.appendChild(emptyDay);
  }

  for (let day = 1; day <= daysInMonth; day++) {
    const dateString = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    const dayEl = document.createElement('div');
    dayEl.textContent = day;
    if (presentDates.includes(dateString)) {
      dayEl.className = 'present';
    }
    calendarEl.appendChild(dayEl);
  }
}

// Initial render
renderCalendar();
