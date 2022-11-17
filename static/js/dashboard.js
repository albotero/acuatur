var socket = io();

socket.on('response', function(data) {
  if (data['result'] != 'ok') {
    alert(`Ocurrió un error:\n${data}`);
  }
  location.reload();
});

function add_user() {
  var html = `
  <form id="frm-nuevo-usuario">
    <table>
      <tr>
        <th>Usuario:</td>
        <td><input type="text" name="user" /></td>
      </tr>
      <tr>
        <th>Nombre:</td>
        <td><input type="text" name="name" onkeyup="suggest_pass(this);" onkeypress="suggest_pass(this);" /></td>
      </tr>
      <tr>
        <th>Contrase&ntilde;a:</td>
        <td><input type="text" name="password" /></td>
      </tr>
      <tr>
        <th>Roles:</td>
        <td>
          <ul id="roles">
            <li><label><input type="checkbox" value="user" checked disabled />Usuario</label></li>
            <li><label><input type="checkbox" value="admin" />Administrador</label></li>
          </ul>
        </td>
      </tr>
    </table>
  </form>`;

  $.confirm('Agregar turno', html, 'Agregar', 'Cancelar', () => {
    // Validate data
    if ($('#frm-nuevo-usuario')[0].reportValidity()) {
      // Get data in dicts
      var data = { 'add_user': {} };
      $.each($('#frm-nuevo-usuario').serializeArray(), function(i, field) {
        data['add_user'][field.name] = field.value;
      });
      // Add roles
      var roles = [];
      $("ul#roles :checked").each(function() {
          roles.push(this.value);
      });
      data['add_user']['roles'] = roles.join(',');
      // Send data to server
      socket.emit('admin', data);
      // Remove dialog
      $('#dialog').dialog('close');
    }
  }, false);
}

function suggest_pass(element) {
  // Get first name of user
  var password = $(element).val().split(' ')[0];
  // Capitalize name
  password = password.charAt(0).toUpperCase() + password.slice(1).toLowerCase();
  // Add special characters
  password = password.replace(/[AaÁá]/g,'4')
                     .replace(/[EeÉé]/g,'3')
                     .replace(/[IiÍí]/g,'1')
                     .replace(/[OoÓó]/g,'0')
                     .replace(/[Úú]/g,'u');
  // Add random number
  password += '$' + Math.floor(Math.random() * 10000 + 1);
  // Show suggested password
  $('#frm-nuevo-usuario input[name=password]').val(password);
}

function rem_user(user) {
  html = `
  <p class="del-schedule">Eliminar Usuario</p>
  <p>¿Est&aacute; seguro que desea eliminar al usuario <i><b>${user}</b></i>?</p>
  <p>Esta acción no se puede revertir.</p>
  `;
  $.confirm('Eliminar Usuario', html, 'Eliminar', 'Cancelar', () => {
    // Send data to server
    socket.emit('admin', { 'rem_user': user });
  });
}

function add_empl(group_id, group_name) {
  var html = `
  <form id="frm-nuevo-usuario">
    <table>
      <tr>
        <th>ID:</td>
        <td><input type="text" name="id" /></td>
      </tr>
      <tr>
        <th>Nombre:</td>
        <td><input type="text" name="name" onkeyup="suggest_pass(this);" onkeypress="suggest_pass(this);" /></td>
      </tr>
    </table>
  </form>`;

  $.confirm(`Agregar a ${group_name}`, html, 'Agregar', 'Cancelar', () => {
    // Validate data
    if ($('#frm-nuevo-usuario')[0].reportValidity()) {
      // Get data in dicts
      var data = { 'add_empl': { 'group': group_id } };
      $.each($('#frm-nuevo-usuario').serializeArray(), function(i, field) {
        data['add_empl'][field.name] = field.value;
      });
      // Send data to server
      socket.emit('admin', data);
      // Remove dialog
      $('#dialog').dialog('close');
    }
  }, false);
}

function rem_empl(id, group, group_name) {
  html = `
  <p class="del-schedule">Eliminar</p>
  <p>¿Est&aacute; seguro que desea eliminar al usuario <i><b>${id}</b></i> del grupo <i><b>${group_name}</b></i>?</p>
  <p>Esta acción no se puede revertir.</p>
  `;
  $.confirm('Eliminar del grupo', html, 'Eliminar', 'Cancelar', () => {
    // Send data to server
    socket.emit('admin', { 'rem_empl': {'id': id, 'group': group} });
  });
}