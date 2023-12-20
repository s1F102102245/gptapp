
// フォームデータを保持するJavaScript
document.getElementById('ocr_form').addEventListener('submit', function(event) {
    event.preventDefault();  // フォームの通常の送信を防ぐ
    var formData = new FormData(this);

    // フォームデータを非同期で送信（サーバーサイドにデータを送信する処理を追加する必要があります）
    fetch('/your-upload-endpoint/', {
        method: 'POST',
        body: formData
    });
});

document.getElementById('chat_form').addEventListener('submit', function(event) {
    event.preventDefault();  // フォームの通常の送信を防ぐ
    var formData = new FormData(this);

    // フォームデータを非同期で送信（サーバーサイドにデータを送信する処理を追加する必要があります）
    fetch('/your-chat-endpoint/', {
        method: 'POST',
        body: formData
    });
});
