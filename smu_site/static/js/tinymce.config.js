tinymce.init({
  selector: '#myTextarea',

  plugins: [
    'advlist', 'autolink', 'link', 'image', 'lists', 'charmap', 'preview', 'anchor', 'pagebreak',
    'searchreplace', 'wordcount', 'visualblocks', 'visualchars', 'code', 'fullscreen', 'insertdatetime',
    'media', 'table', 'emoticons', 'template', 'accordion'
  ],
  toolbar: 'undo redo | styles | accordion | bold italic | alignleft aligncenter alignright alignjustify | ' +
    'bullist numlist outdent indent | link image | print preview media fullscreen | ' +
    'forecolor backcolor emoticons | help | googlemap | insertcarousel',

  setup: function (editor) {
    editor.ui.registry.addButton('googlemap', {
      text: 'Insert Map',
      onAction: function () {
        let link = prompt("Enter the link here.");

        if (link !== "") {
          const mapCode = '<iframe src="' + link + '" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>';
          editor.insertContent(mapCode);
        }
      },
    });

    editor.ui.registry.addButton('insertcarousel', {
      text: 'Insert Carousel',
      onAction: function () {
        // Custom logic to get carousel information (you can use a modal or prompt)
        // For simplicity, I'm using dummy base64-encoded images
        let base64Images = [];

        let carouselCode = '<hr class="carosuel_no_show"/><h3 class="carosuel_no_show"> Carousel starts here | Карусель начинается здесь (<span style="color:red"><i>добавьте изображения в середине. не удаляйте эту строку </i></span>)</h3><div class="carousel-container"><div class="carousel">';

        carouselCode += '</div></div><h3 class="carosuel_no_show"> Carousel Ends here | Карусель заканчивается здесь</h3><hr class="carosuel_no_show"/><br/><br/>';

        if (carouselCode !== "") {
          editor.insertContent(carouselCode);
        }
      },
    });
  },

  init_instance_callback: function (editor) {
    var freeTiny = document.querySelector('.tox .tox-notification--in');
    freeTiny.style.display = 'none';
  },
  menu: {
    favs: { title: 'My Favorites', items: 'code visualaid | searchreplace | emoticons' }
  },
  menubar: 'favs file edit view insert format tools table help',

  image_title: true,
  // enable automatic uploads of images represented by blob or data URIs
  automatic_uploads: true,
  // add custom filepicker to Image dialog
  file_picker_types: 'image',
  file_picker_callback: function (cb, value, meta) {
    // You can still keep this part for uploading images via the file picker
    var input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.setAttribute('accept', 'image/*');

    input.onchange = function () {
      var file = this.files[0];
      var reader = new FileReader();

      reader.onload = function () {
        var id = 'blobid' + (new Date()).getTime();
        var blobCache = tinymce.activeEditor.editorUpload.blobCache;
        var base64 = reader.result.split(',')[1];
        var blobInfo = blobCache.create(id, file, base64);
        blobCache.add(blobInfo);

        // call the callback and populate the Title field with the file name
        cb(blobInfo.blobUri(), { title: file.name });

        // Do not add the image to the carousel here
        // It will be added after the "Save" button is clicked
      };
      reader.readAsDataURL(file);
    };

    // Open the file picker
    input.click();

    // Add event listener for the "Save" button click in the file picker
    input.addEventListener('change', function () {
      editor.on('filepicker', function (e) {
        // Check if the "Save" button was clicked
        if (e.meta.file_picker_mode === tinymce.ui.FilePicker.Modes.IMAGE) {
          // If the current context is a carousel, add the uploaded image to it
          if (tinymce.activeEditor.dom.getParent(tinymce.activeEditor.selection.getNode(), 'div.carousel')) {
            var carousel = tinymce.activeEditor.selection.getNode();
            var newSlide = document.createElement('div');
            newSlide.innerHTML = '<img src="' + e.meta.file.data + '" alt="' + e.meta.file.name + '" style="max-width:200px !important">';
            carousel.appendChild(newSlide);
          }
        }
      });
    });
  }
});
