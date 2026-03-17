$(document).ready(function () {

  $('#password').on('input', function () {
    const val = $(this).val();
    let strength = 0;
    if (val.length >= 6)          strength += 33;
    if (/[A-Z]/.test(val))        strength += 33;
    if (/[0-9!@#$%]/.test(val))   strength += 34;
    let color = 'bg-danger', text = 'Weak';
    if (strength > 33 && strength <= 66) { color = 'bg-warning'; text = 'Medium'; }
    if (strength > 66) { color = 'bg-success'; text = 'Strong'; }
    $('#strengthBar').css('width', strength + '%').attr('class', 'progress-bar ' + color);
    $('#strengthText').text(text);
  });

  $('#registerForm').on('submit', function (e) {
    let valid = true;
    const name = $('#name').val().trim();
    if (name === '') {
      $('#name').addClass('is-invalid');
      $('#nameError').text('Name is required.');
      valid = false;
    } else { $('#name').removeClass('is-invalid').addClass('is-valid'); }

    const email = $('#email').val().trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      $('#email').addClass('is-invalid');
      $('#emailError').text('Enter a valid email address.');
      valid = false;
    } else { $('#email').removeClass('is-invalid').addClass('is-valid'); }

    const pwd = $('#password').val();
    if (pwd.length < 6) {
      $('#password').addClass('is-invalid');
      $('#passwordError').text('Password must be at least 6 characters.');
      valid = false;
    } else { $('#password').removeClass('is-invalid').addClass('is-valid'); }

    if (!valid) e.preventDefault();
  });

  $('#loginForm').on('submit', function (e) {
    let valid = true;
    const email = $('#email').val().trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      $('#email').addClass('is-invalid');
      $('#emailError').text('Enter a valid email address.');
      valid = false;
    } else { $('#email').removeClass('is-invalid'); }

    if ($('#password').val() === '') {
      $('#password').addClass('is-invalid');
      $('#passwordError').text('Password is required.');
      valid = false;
    } else { $('#password').removeClass('is-invalid'); }

    if (!valid) e.preventDefault();
  });

  $('#bookForm').on('submit', function (e) {
    let valid = true;
    if ($('#doctor_id').val() === '') {
      $('#doctor_id').addClass('is-invalid');
      $('#doctorError').text('Please select a doctor.');
      valid = false;
    } else { $('#doctor_id').removeClass('is-invalid'); }

    const today = new Date().toISOString().split('T')[0];
    if ($('#apptDate').val() === '' || $('#apptDate').val() < today) {
      $('#apptDate').addClass('is-invalid');
      $('#dateError').text('Please select a valid future date.');
      valid = false;
    } else { $('#apptDate').removeClass('is-invalid'); }

    if ($('#apptTime').val() === '') {
      $('#apptTime').addClass('is-invalid');
      $('#timeError').text('Please select a time.');
      valid = false;
    } else { $('#apptTime').removeClass('is-invalid'); }

    if ($('#reason').val().trim() === '') {
      $('#reason').addClass('is-invalid');
      $('#reasonError').text('Please enter a reason for your visit.');
      valid = false;
    } else { $('#reason').removeClass('is-invalid'); }

    if (!valid) e.preventDefault();
  });

});
$('#addDoctorForm').on('submit', function (e) {
    let valid = true;

    const name = $('#docName').val().trim();
    if (name === '') {
      $('#docName').addClass('is-invalid');
      $('#docNameError').text('Doctor name is required.');
      valid = false;
    } else { $('#docName').removeClass('is-invalid'); }

    const specialty = $('#docSpecialty').val();
    if (!specialty) {
      $('#docSpecialty').addClass('is-invalid');
      $('#docSpecialtyError').text('Please select a specialty.');
      valid = false;
    } else { $('#docSpecialty').removeClass('is-invalid'); }

    if (!valid) e.preventDefault();
  });