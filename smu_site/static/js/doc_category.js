// Jquery version
// $('select').change(function() {
//   var cur = $(this).val();
//   if(cur == 'all'){
//     $('ul.list > li[data-cat]').css('display','list-item');
//   } else {
//     $('ul.list > li[data-cat]').css('display','list-item');
//     $('ul.list > li:not([data-cat="'+ cur +'"])').css('display','none');
//   }
// });

const selectElement = document.querySelector('select');
const items = document.querySelectorAll('ul > li[data-cat]');

selectElement.addEventListener('change', (event) => {
  var cur = event.target.value;
  if(cur == 'all'){
    items.forEach(function (item, index) {
      item.style.display = 'block';
    });
  } else {
    items.forEach(function (item, index) {
      var item_cat = item.getAttribute('data-cat');
      if (cur == item_cat){
        item.style.display = 'block';
      } else {
        item.style.display = 'none';
      }
      // console.log(item_cat); // The element
    });
  }
});



items.forEach(function (el, index) {
  var title = el.querySelector('.list__item-title');
  var desc = el.querySelector('.list__item-description');
  title.onclick = function() {
    var display = desc.style.display;
    if(display == 'block' || desc.classList.contains('list__item-description--open')){
      // desc.style.display = 'none';
      desc.classList.remove('list__item-description--open');
    } else {
      // desc.style.display = 'block';
      desc.classList.add('list__item-description--open');
    }
  };
});