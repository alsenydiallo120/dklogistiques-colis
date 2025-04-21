$('#id_produits').change(function () {
    var prix = $(this).find('option:selected').attr("data-prixachat")
    var designation = $(this).find('option:selected').attr("data-designation")
    var id = $(this).find('option:selected').val()
    $('#designation').val(designation)
    $('#id').val(id)
    $('#id_prix').val(prix)
  })

  $('tbody').on('click', '.edit_cart', function () {
    $('#id_panier').val($(this).attr('data-id'))
    $('#quantity').val($(this).attr('data-quantite'))
    href = $(this).attr('data-href')
    $('#form_edit').attr('action', href)
})

  $('tbody').on('click', '.delete_cart', function () {
    $('#id_panier').val($(this).attr('data-id'))
    href = $(this).attr('data-href')
    $('#form_delete').attr('action', href)
})