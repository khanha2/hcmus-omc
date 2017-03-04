$(document).ready(function() {
    function showMessage(message) {
        $('#message').text(message);
        $('#message-form').show();
    }

    function login() {
        $('#message-form').hide();
        if ($('#username').val().length === 0) {
            showMessage('Tên đăng nhập không được rỗng.')
            return;
        }
        if ($('#password').val().length === 0) {
            showMessage('Mật khẩu không được rỗng.');
            return;
        }
        $.ajax({
            url: loginUrl,
            type: 'POST',
            data: {
                username: $('#username').val(),
                password: $('#password').val(),
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    showMessage('Tên đăng nhập hoặc mật khẩu chưa đúng.');
                }
            }
        });
    }

    $('.form-control').on('keypress', function(e) {
        if (e.which == 13) {
            login();
        }
    });

    $('#btn-login').on('click', function(e) {
        e.preventDefault();
        login();
    });
});
