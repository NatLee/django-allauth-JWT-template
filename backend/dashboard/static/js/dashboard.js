
// 獲取頁面中的重要元素
var socialLoginButtons = document.querySelectorAll('.social-login-btn');
var socialAccounts = document.getElementById('socialAccounts');

var jwtStatusText = document.getElementById('jwtStatusText');
var jwtLogoutBtn = document.getElementById('jwtLogoutBtn');

// 更新登入狀態的函數
function updateLoginStatus() {
    var accessToken = localStorage.getItem('access_token');
    if (accessToken) {
        jwtStatusText.innerHTML = '🟩';
        jwtLogoutBtn.style.display = 'block';
        fetchSocialAccounts();
    } else {
        jwtStatusText.innerHTML = '🟥';
        jwtLogoutBtn.style.display = 'none';
        socialAccounts.innerHTML = '';
    }
}

// 獲取用戶綁定的社交帳號
function fetchSocialAccounts() {
    fetch('/api/allauth/social/accounts', {
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
    })
    .then(response => response.json())
    .then(data => {
        let accountsHtml = '<h2>已綁定的社交帳號</h2>';
        // 範例資料：
        // data.social_accounts = [
        //     { id: 1, provider: 'google', uid: '123456789' },
        //     { id: 2, provider: 'microsoft', uid: '987654321' }
        // ];
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

        // 為每個解除綁定按鈕添加點擊事件
        document.querySelectorAll('.unbind-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                unbindSocialAccount(this.dataset.id);
            });
        });
    })
    .catch(error => console.error('Error:', error));
}


// 解除綁定社交帳號
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
        console.log(data.message); // 範例：'社交帳號解除綁定成功'
        fetchSocialAccounts(); // 重新獲取社交帳號列表
    })
    .catch(error => console.error('Error:', error));
}

// Session 登出
function sessionLogout() {
    fetch('/api/allauth/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // 範例：'登出成功'
        updateLoginStatus();
    }).catch(error => console.error('Error:', error));
}

// JWT 登出（僅清除本地 token）
function jwtLogout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    updateLoginStatus();
}

function handleLoginSuccess() {
    console.log('登入成功');
    var accessToken = localStorage.getItem('access_token');
    var refreshToken = localStorage.getItem('refresh_token');

    // 範例 token：
    // accessToken: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    // refreshToken: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'

    if (accessToken) {
        console.log('Access token 已儲存');
    }
    if (refreshToken) {
        console.log('Refresh token 已儲存');
    }
    
    updateLoginStatus();
    fetchSocialAccounts();
}

document.addEventListener('DOMContentLoaded', function() {
    // 為每個社交登入按鈕添加點擊事件
    socialLoginButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            var url = this.href;
            localStorage.removeItem('loginStatus');

            // 打開彈出窗口進行社交登入
            var popup = window.open(url, 'socialLogin', 'width=600,height=600');

            // 檢查登入狀態
            var loginCheckInterval = setInterval(function() {
                if (localStorage.getItem('loginStatus') === 'success') {
                    clearInterval(loginCheckInterval);
                    localStorage.removeItem('loginStatus');
                    handleLoginSuccess();
                }
            }, 1000);

        });
    });

    // 初始化：更新登入狀態
    updateLoginStatus();
});
