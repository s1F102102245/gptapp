document.addEventListener('DOMContentLoaded', function() {
    var grid = document.querySelector('.grid');

    document.addEventListener('mousemove', function(event) {
        var rect = grid.getBoundingClientRect();
        var centerX = rect.left + (rect.width/2);
        var centerY = rect.top + (rect.height/2); // "rect.top" を "rect.top" に修正
        
        // Calculate the distance from the center of the image to the mouse
        var deltaX = (event.clientX - centerX) / 15; // Dividing by 10 to slow the movement
        var deltaY = (event.clientY - centerY) / 15; // Dividing by 10 to slow the movement

        // Apply the transformation to the image in the reverse direction
        grid.style.transform = `translate(-50%, -50%) translate(${deltaX}px, ${deltaY}px)`;
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var grid = document.querySelector('.map');

    document.addEventListener('mousemove', function(event) {
        var rect = grid.getBoundingClientRect();
        var centerX = rect.left + (rect.width / 2);
        var centerY = rect.top + (rect.height / 2); // "rect.top" を "rect.top" に修正
        
        // Calculate the distance from the center of the image to the mouse
        var deltaX = (event.clientX - centerX) / 25; // Dividing by 10 to slow the movement
        var deltaY = (event.clientY - centerY) / 25; // Dividing by 10 to slow the movement

        // Apply the transformation to the image in the reverse direction
        grid.style.transform = `translate(-50%, -50%) translate(${deltaX}px, ${deltaY}px)`;
    });
});

