$.extend({
  confirm: function(titulo, mensaje, texto_si, texto_no, funcion_si, cerrar=true) {
    $('<div id="dialog"></div>').dialog({
      // Remove the closing 'X' from the dialog
      open: function(event, ui) { $('.ui-dialog-titlebar-close').hide(); },
      width: 400,
      buttons: [{
        text: texto_si,
        click: function() {
          funcion_si();
          if (cerrar) $(this).dialog('close');
        }
      },
      {
        text: texto_no,
        click: function() {
          $(this).dialog('close');
        }
      }],
      close: function(event, ui) { $(this).remove(); },
      resizable: false,
      title: titulo,
      modal: true
    }).html(mensaje);
  }
});
