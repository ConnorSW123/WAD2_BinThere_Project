$(document).ready(function() {
    $('#about-btn').click(function() {
        alert('You clicked the button using jQuery!');
    });
});

$('.ouch').click(function() {
    alert('You clicked me! Ouch!');
});

$('p').hover(
    function() {
        $(this).css('color', 'red');
    }, 
    function() {
        $(this).css('color', 'black');
    }
);

$("#about-btn").removeClass('btn-primary').addClass('btn-success');

$('#about-btn').click(function() {
    msgStr = $('#msg').html();  // Get the current HTML content of the #msg element
    msgStr = msgStr + ' ooo, fancy!';  // Append the text to the existing content
    $('#msg').html(msgStr);  // Update the HTML content of the #msg element
});

