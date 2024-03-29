var socket = io();
var dict_update = {'schedule_id': schedule_id};

function send_update() {
  // Send data to server
  socket.emit('update_schedule', dict_update);
  // Reset changes
  dict_update = {'schedule_id': schedule_id};
}

socket.on('response', function(data) {
  if (data['result'] != 'ok') {
    alert(`Ocurrió un error:\n${data}\nSe actualizará la página para recargar los datos`);
    location.reload();
    return;
  }
  // Update summaries
  $('table.summary').html(data['summary']);
  $('table.cext').html(data['cext']);
  $('table.cen').html(data['cen']);
  $('table.extra').html(data['extra']);
  // Add shifts if apply
  if ('add' in data) {
    shift_html = `
    <div class="employee-shift" id="${data['add']['id']}">
      <div class="del" onclick="rem_shift(this);">x</div>
      <div class="employee_id">${data['add']['employee_id']}</div>
      <div class="hours">${data['add']['hours']}</div>
    </div>`;
    $(`#${data['add']['day']}-${data['add']['shift']} > div:last`).before(shift_html);
    toggle_printable();
  }
});

function rem_shift(obj) {
  obj = $(obj).parent();
  dict_update['rem'] = obj.attr('id');
  obj.remove();
  send_update();
}

function toggle_printable() {
  $('.shift').each(function() {
    if ($(this).children().length > 2)
      $(this).removeClass('noprint');
    else
      $(this).addClass('noprint');
  });
}

toggle_printable();

function add_shift(obj) {
  var day = $(obj).parent().siblings('.title').text();
  var shift = $(obj).parent().attr("class").split(' ')[1];
  var shift_title = $(obj).siblings('.title').text();
  var shift_key = shift.includes('_') ? shift.split('_')[1] : shift;

  var html = `
  <form id="frm-nuevo-turno">
    <table>
      <tr>
        <th>Fecha:</td>
        <td>${day}/${month.replace(' ', '/')}</td>
        <input type="hidden" name="day" value="${day}" />
      </tr>
      <tr>
        <th>Anestesi&oacute;logo:</td>
        <td>
          <select name="employee_id">`;

  for (const [key, value] of Object.entries(anestesiologos)) {
    html += `<option value="${key}">${key} - ${value}&nbsp;&nbsp;</option>`
  }

  html += `</select>
        </td>
      </tr>
      <tr>
        <th>Turno:</td>
        <td>${shift_title}</td>
        <input type="hidden" name="shift" value="${shift}" />
      </tr>
      <tr>
        <th>Horas:</td>
        <td>`;

  if (shift_key in shift_hours) {
    html += shift_hours[shift_key];
    html += `<input type="hidden" name="hours" value="${shift_hours[shift_key]}" />`;
  } else {
    html += `<input type="number" name="hours" required />`;
  }

  html += `</td>
      </tr>
    </table>
  </form>
  <script type="text/javascript">$('select[name=employee_id]').focus();</script>
  `;

  $.confirm('Agregar turno', html, 'Agregar', 'Cancelar', () => {
    // Validate data
    if ($('#frm-nuevo-turno')[0].reportValidity()) {
      // Get data in dicts
      var data = {};
      $.each($('#frm-nuevo-turno').serializeArray(), function(i, field) {
        data[field.name] = $.isNumeric(field.value) ? parseInt(field.value) : field.value;
      });
      // Send data
      dict_update['add'] = data;
      send_update();
      // Remove dialog
      $('#dialog').dialog('close');
    }
  }, false);
}
