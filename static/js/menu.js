$('nav').hover(function(){
  $('.menu').toggleClass('change');
});

$('li').click(function(){
  $('li').removeClass('selected');
  $(this).addClass('selected');
});

function open_schedule(id) {
  location.replace(`/schedule/${id}`);
}

function duplicate_schedule(id) {

}

function delete_schedule(mo, gr, id) {
  html = `
  <p class="del-schedule">${gr} ${mo}</p>
  <p>¿Est&aacute; seguro que desea eliminar el cuadro de turnos?</p>
  <p>Esta acción no se puede revertir.</p>
  `;
  $.confirm('Eliminar Cuadro de Turnos', html, 'Eliminar', 'Cancelar', () => {
    $(`<form action="/del-schedule" method="POST">
        <input type="hidden" name="id" value="${id}" />
      </form>`).appendTo('body').submit();
  }, false);
}

function new_schedule() {
  html = `
    <form id="frm-new-schedule" action="/schedule" method="POST">
      <table>
        <tr>
          <th>Mes:</th>
          <td><input type="month" name="month" required></td>
        </tr>
        <tr>
          <th>Grupo:</th>
          <td>
            <select name="group" onchange="show_group(this.value);" required>`;
  for (var g in groups) {
    html += `<option value="${g}">${groups[g]['str']}</option>`;
  }
  html += ` </select>
          </td>
        </tr>
        <tr>
          <td colspan="2">
            <div id="employees" class="list"></div>
            <img src onerror="show_group('${Object.keys(groups)[0]}');">
          </td>
        </tr>
      </table>
    </form>
    `;

  $.confirm('Nuevo Cuadro de Turnos', html, 'Agregar', 'Cancelar', () => {
    // Validate data
    if ($('#frm-new-schedule')[0].reportValidity()) {
      // Send data
      $('#frm-new-schedule')[0].submit();
    }
  }, false);
}

function show_group(val) {
  html = '<ul>';
  for (var e in groups[val]['list']) {
    html += `<li>${groups[val]['list'][e]}</li>`;
  }
  html += '</ul>'
  $('#employees').html(html);
}
