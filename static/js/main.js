var socket = io();

function enviar_update() {
  // Envía los datos al servidor
  dict_actualizar['tmp'] = tmp;
  console.log('enviando...', dict_actualizar);
  socket.emit('update_perio', dict_actualizar);
}

socket.on('response_time', function(datos) {
  // Actualiza hora y créditos
  for (var val in datos) {
    $(`#${val}`).text(datos[val]);
  }

  if ($('#cred').text().replace('.', '') <= 15) {
    $('#cred').toggleClass('alerta');
    $('#cred-tiempo').toggleClass('alerta');
  }
});
