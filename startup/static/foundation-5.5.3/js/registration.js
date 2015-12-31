function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode
    if (charCode >= 48 && charCode <= 57)
        return false;

    return true;
}
// This example displays an address form, using the autocomplete feature
// of the Google Places API to help users fill in the information.

