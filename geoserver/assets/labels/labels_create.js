/**
 * Created by minjoon on 4/28/15.
 */
var arr = [];
var x = 0;
var y = 0;

var canvas = document.getElementById('myCanvas');
var context = canvas.getContext('2d');
var imageObj = new Image();
imageObj.src = diagram_url;


function drawAnnotations() {
    context.font = "20px Arial";
    context.strokeStyle = "#ff0000";
    context.fillStyle = "#000000";
    for (i = 0; i < arr.length; i++) {
        context.beginPath();
        var x = arr[i]['x'];
        var y = arr[i]['y'];
        context.arc(x, y, 10, 0, 2*Math.PI);
        context.stroke();
        if (x > imageObj.width/2.0) {
            x -= 15;
        }
        if (y < imageObj.height/2.0) {
            y += 15;
        }
        context.fillText(arr[i]['label'], x, y);
    }
}

imageObj.onload = function() {
    context.drawImage(imageObj, 0, 0);
    drawAnnotations();
};

$(document).ready(function() {
    $('#myCanvas').click(function(e) {
        $('#input_label').focus();
        var offset = $(this).offset();
        x = e.pageX - offset.left;
        y = e.pageY - offset.top;
    });

    if ($('#id_text').val() != "") {
        arr = JSON.parse($('#id_text').val());
    }
});

$('#input_type').keypress(function (e) {
    var key = e.which;
    if(key == 13)  // the enter key code
    {
        $('#button_add').click();
        return false;
    }
});

$('#button_add').click(function(e) {
    var text = $('#id_text').val();
    if (text === "") {
        arr = [];
    } else {
        arr = JSON.parse(text);
    }
    var dict = {'x':Math.round(x), 'y':Math.round(y), 'label': $('#input_label').val(), 'type': $('#input_type').val()};
    arr.push(dict);
    drawAnnotations();
    $('#id_text').val(JSON.stringify(arr));
    $('#input_type').blur();
    $('#input_type').val('');
    $('#input_label').val('');
});
