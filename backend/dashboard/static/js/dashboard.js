document.addEventListener('DOMContentLoaded', function() {
    var socialLoginButtons = document.querySelectorAll('.social-login-btn');
    var loginStatus = document.getElementById('loginStatus');
    var socialAccounts = document.getElementById('socialAccounts');
    var logoutButtons = document.getElementById('logoutButtons');
    var sessionLogoutBtn = document.getElementById('sessionLogout');
    var jwtLogoutBtn = document.getElementById('jwtLogout');

    function updateLoginStatus() {
        var accessToken = localStorage.getItem('access_token');
        if (accessToken) {
            loginStatus.innerHTML = '<p>已登入</p>';
            logoutButtons.style.display = 'block';
            fetchSocialAccounts();
        } else {
            loginStatus.innerHTML = '<p>未登入</p>';
            logoutButtons.style.display = 'none';
            socialAccounts.innerHTML = '';
        }
    }

    function fetchSocialAccounts() {
        fetch('/api/allauth/social/accounts', {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
        })
        .then(response => response.json())
        .then(data => {
            let accountsHtml = '<h2>已綁定的社交帳號</h2>';
            data.social_accounts.forEach(account => {
                accountsHtml += `
                    <div class="account-item">
                        <p>提供商: ${account.provider}</p>
                        <p>UID: ${account.uid}</p>
                        <button class="unbind-btn" data-id="${account.id}">解除綁定</button>
                    </div>
                `;
            });
            socialAccounts.innerHTML = accountsHtml;

            document.querySelectorAll('.unbind-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    unbindSocialAccount(this.dataset.id);
                });
            });
        })
        .catch(error => console.error('Error:', error));
    }

    function unbindSocialAccount(accountId) {
        fetch('/api/allauth/social/accounts', {
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                account_id: accountId
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            fetchSocialAccounts();
        })
        .catch(error => console.error('Error:', error));
    }

    sessionLogoutBtn.addEventListener('click', function() {
        fetch('/api/allauth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            updateLoginStatus();
        })
        .catch(error => console.error('Error:', error));
    });

    jwtLogoutBtn.addEventListener('click', function() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        updateLoginStatus();
    });

    socialLoginButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            var url = this.href;
            localStorage.removeItem('loginStatus');

            var popup = window.open(url, 'socialLogin', 'width=600,height=600');

            var loginCheckInterval = setInterval(function() {
                if (localStorage.getItem('loginStatus') === 'success') {
                    clearInterval(loginCheckInterval);
                    localStorage.removeItem('loginStatus');
                    handleLoginSuccess();
                }
            }, 1000);
            
            function handleLoginSuccess() {
                console.log('登入成功');
                var accessToken = localStorage.getItem('access_token');
                var refreshToken = localStorage.getItem('refresh_token');

                if (accessToken) {
                    console.log('Access token 已儲存');
                }
                if (refreshToken) {
                    console.log('Refresh token 已儲存');
                }
                
                updateLoginStatus();
                fetchSocialAccounts();
            }
        });
    });

    updateLoginStatus();
});
