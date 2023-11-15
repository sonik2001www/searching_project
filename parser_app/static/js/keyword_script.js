function autoResize(id) {
    var textarea = document.getElementById(id);
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
}

$(document).ready(function() {
    var originalBackgroundColor; // Зберігаємо початковий колір фону

    $("#file-upload").on("change", function() {
        const label = $("#file-label"); // Отримуємо елемент мітки за його ID
        const deleteButton = $("#delete-file"); // Отримуємо кнопку "Delete File" за її ID
        const textarea = $("#text"); // Отримуємо текстову область за її ID

        if (this.files.length > 0) {
            label.text("Change File"); // Змінюємо текст мітки
            deleteButton.show(); // Показуємо кнопку "Delete File"
            textarea.prop('disabled', true); // Забороняємо вводити текст в текстову область
            textarea.val(""); // Очищаємо вміст текстової області
            textarea.attr("placeholder", "Text input is disabled when a file is selected."); // Змінюємо плейсхолдер
        } else {
            label.text("Upload File"); // Скидаємо текст мітки, якщо файл не вибрано
            deleteButton.hide(); // Приховуємо кнопку "Delete File"
            textarea.prop('disabled', false); // Дозволяємо вводити текст в текстову область
            textarea.attr("placeholder", "Enter text"); // Відновлюємо плейсхолдер
        }
    });

    $("#delete-file").on("click", function() {
        // Коли натиснута кнопка "Delete File", скидаємо значення і властивості
        $("#file-upload").val(""); // Скидаємо значення файлового інпута
        $("#file-label").text("Upload File"); // Скидаємо текст мітки
        $(".custom-file-upload").css("background-color", originalBackgroundColor); // Відновлюємо колір фону
        $(this).hide(); // Приховуємо кнопку "Delete File"
        $("#text").prop('disabled', false); // Дозволяємо вводити текст в текстову область
        $("#text").attr("placeholder", "Enter text"); // Відновлюємо плейсхолдер
    });
});


var images = document.querySelectorAll('img');

// Пройтися по кожному зображенню і виконати заміну
images.forEach(function(image) {
    // Отримати початковий src
    var originalSrc = image.getAttribute('src');

    // Перевірити, чи src містить 'output' та не містить '/static/'
    if (originalSrc.includes('output') && !originalSrc.includes('/static/')) {
        // Виконати заміну src, додаючи '/static', якщо він не вже має '/'
        var newSrc = "/static/" + originalSrc + "?version=1.1";
        image.setAttribute('src', newSrc);
    }
});
