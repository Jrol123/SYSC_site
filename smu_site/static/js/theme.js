var mode = localStorage.getItem("mode");
      $('html').attr(mode, '');

$(document).ready(function(){

    $( "#dark-mode-toggless" ).on( "click", function() {
      localStorage.setItem("mode", "data-dark-mode");
      var mode = localStorage.getItem("mode");
      $('html').attr(mode, '');
      $('html').removeAttr("light-dark-mode");
      $('html').removeAttr("black-dark-mode");


    });

    $( "#light-mode-toggless" ).on( "click", function() {
      localStorage.setItem("mode", "light-dark-mode");
      var mode = localStorage.getItem("mode");
      $('html').attr(mode, '');
      $('html').removeAttr("data-dark-mode");
      $('html').removeAttr("black-dark-mode");
    
    });

    $( "#black-mode-toggless" ).on( "click", function() {
      localStorage.setItem("mode", "black-dark-mode");
      var mode = localStorage.getItem("mode");
      $('html').attr(mode, '');
      $('html').removeAttr("data-dark-mode");
      $('html').removeAttr("light-dark-mode");

    
    });

  });

    

  
