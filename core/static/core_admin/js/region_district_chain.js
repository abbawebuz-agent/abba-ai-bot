/*
 * T10: Viloyat -> Tuman cascade (admin change form).
 * Tanlangan viloyat (region) bo'yicha tuman (district) autocomplete'ini filtrlaydi.
 *
 * Ishlash printsipi:
 *  - Django admin autocomplete GET so'rovi (field_name=district) ga
 *    tanlangan region id ni `&region=` qilib qo'shamiz (ajaxSend hook).
 *  - Backend (UzDistrictAdmin.get_search_results) shu region bo'yicha filtrlaydi.
 *  - Region o'zgarsa — eski district tanlovini tozalaymiz.
 */
(function () {
  function ready(fn) {
    if (document.readyState !== 'loading') { fn(); }
    else { document.addEventListener('DOMContentLoaded', fn); }
  }
  ready(function () {
    if (typeof django === 'undefined' || !django.jQuery) { return; }
    var $ = django.jQuery;

    // Autocomplete so'roviga tanlangan region'ni qo'shamiz.
    $(document).ajaxSend(function (event, jqxhr, settings) {
      try {
        if (settings.url && settings.url.indexOf('field_name=district') !== -1) {
          var region = $('#id_region').val();
          if (region) {
            var sep = settings.url.indexOf('?') === -1 ? '?' : '&';
            settings.url += sep + 'region=' + encodeURIComponent(region);
          }
        }
      } catch (e) { /* no-op */ }
    });

    // Region o'zgarsa — district tanlovini tozalaymiz (boshqa viloyatniki qolmasin).
    $(document).on('change', '#id_region', function () {
      var $d = $('#id_district');
      if ($d.length) { $d.val(null).trigger('change'); }
    });
  });
})();
