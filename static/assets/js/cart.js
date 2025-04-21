$(document).ready(function () {
    $('#id_produits').change(function () {
      prix = $(this).find('option:selected').attr("data-prix")
      id = $(this).find('option:selected').val()
      $('#id_prix').val(prix)
      $('#id').val(id)
      $('#id').val(id)
    })
  })