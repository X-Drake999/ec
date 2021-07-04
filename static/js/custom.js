$(function(){
    
    $('.product-detail-description-open').click(function(){
        $('.product-detail-short-description').removeClass('active');
        $('.product-detail-short-description').addClass('inactive');
        $('.product-detail-description-open').removeClass('active');
        $('.product-detail-description-open').addClass('inactive');
        $('.product-detail-full-description').removeClass('inactive');
        $('.product-detail-full-description').addClass('active');
        
        return false;
    });

    $('#SetDescriptionDefault').click(function(){
        $('#id_description').val('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.');
        
        return false;
    });

    
    

});