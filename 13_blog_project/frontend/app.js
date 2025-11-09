const API_BASE = 'http://localhost:8070/api';
let token = localStorage.getItem('token');
let currentUser = null;

// 页面加载时检查登录状态
document.addEventListener('DOMContentLoaded', function() {
    checkAuthStatus();
    loadPosts();
});

// 检查认证状态
function checkAuthStatus() {
    if (token) {
        // 验证token是否有效
        fetch(`${API_BASE}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                logout();
                throw new Error('Token invalid');
            }
        })
        .then(user => {
            currentUser = user;
            showUserInfo();
        })
        .catch(error => {
            console.error('Auth check failed:', error);
            logout();
        });
    }
}

// 显示登录表单
function showLogin() {
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('registerForm').classList.add('hidden');
}

// 显示注册表单
function showRegister() {
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.remove('hidden');
}

// 显示用户信息
function showUserInfo() {
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.add('hidden');
    document.getElementById('userInfo').classList.remove('hidden');
    document.getElementById('createPostSection').classList.remove('hidden');
    document.getElementById('usernameDisplay').textContent = currentUser.username;
}

// 用户注册
async function register() {
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    const email = document.getElementById('registerEmail').value;

    if (!username || !password) {
        alert('请填写用户名和密码');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
                email: email
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('注册成功，请登录');
            showLogin();
            // 清空注册表单
            document.getElementById('registerUsername').value = '';
            document.getElementById('registerPassword').value = '';
            document.getElementById('registerEmail').value = '';
        } else {
            alert('注册失败: ' + (data.detail || '未知错误'));
        }
    } catch (error) {
        console.error('注册失败:', error);
        alert('注册失败');
    }
}

// 用户登录
async function login() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    if (!username || !password) {
        alert('请填写用户名和密码');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            token = data.access_token;
            localStorage.setItem('token', token);
            currentUser = data.user;
            showUserInfo();
            // 清空登录表单
            document.getElementById('loginUsername').value = '';
            document.getElementById('loginPassword').value = '';
            loadPosts(); // 重新加载文章
        } else {
            alert('登录失败: ' + (data.detail || '未知错误'));
        }
    } catch (error) {
        console.error('登录失败:', error);
        alert('登录失败');
    }
}

// 用户退出
function logout() {
    token = null;
    currentUser = null;
    localStorage.removeItem('token');
    document.getElementById('userInfo').classList.add('hidden');
    document.getElementById('createPostSection').classList.add('hidden');
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('posts-container').innerHTML = '';
    loadPosts(); // 重新加载文章（不显示编辑删除按钮）
}

// 获取认证请求头
function getAuthHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// 加载所有文章
async function loadPosts() {
    try {
        const response = await fetch(`${API_BASE}/posts`);
        const posts = await response.json();
        displayPosts(posts);
    } catch (error) {
        console.error('加载文章失败:', error);
    }
}

// 显示文章列表
function displayPosts(posts) {
    const container = document.getElementById('posts-container');
    container.innerHTML = '';

    posts.forEach(post => {
        const postElement = document.createElement('div');
        postElement.className = 'post';
        
        let actionsHtml = '';
        // 只有登录用户才能看到编辑删除按钮，且只能操作自己的文章
        if (currentUser && post.author_id === currentUser.id) {
            actionsHtml = `
                <div class="actions">
                    <button onclick="openEditModal(${post.id}, '${post.title.replace(/'/g, "\\'")}', '${post.content.replace(/'/g, "\\'")}')">编辑</button>
                    <button onclick="deletePost(${post.id})">删除</button>
                </div>
            `;
        }

        postElement.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.content}</p>
            <small>作者: ${post.author_name} | 创建时间: ${new Date(post.created_at).toLocaleString()}</small>
            ${actionsHtml}
        `;
        container.appendChild(postElement);
    });
}

// 创建新文章
async function createPost() {
    if (!currentUser) {
        alert('请先登录');
        return;
    }

    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;

    if (!title || !content) {
        alert('请填写标题和内容');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/posts`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                title: title,
                content: content
            })
        });

        if (response.ok) {
            document.getElementById('title').value = '';
            document.getElementById('content').value = '';
            loadPosts(); // 重新加载文章列表
        } else {
            const data = await response.json();
            alert('创建文章失败: ' + (data.detail || '未知错误'));
        }
    } catch (error) {
        console.error('创建文章失败:', error);
    }
}

// 打开编辑模态框
function openEditModal(id, title, content) {
    if (!currentUser) {
        alert('请先登录');
        return;
    }
    
    document.getElementById('editId').value = id;
    document.getElementById('editTitle').value = title;
    document.getElementById('editContent').value = content;
    document.getElementById('editModal').style.display = 'block';
}

// 关闭编辑模态框
function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

// 更新文章
async function updatePost() {
    const id = document.getElementById('editId').value;
    const title = document.getElementById('editTitle').value;
    const content = document.getElementById('editContent').value;

    try {
        const response = await fetch(`${API_BASE}/posts/${id}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                title: title,
                content: content
            })
        });

        if (response.ok) {
            closeEditModal();
            loadPosts(); // 重新加载文章列表
        } else {
            const data = await response.json();
            alert('更新文章失败: ' + (data.detail || '未知错误'));
        }
    } catch (error) {
        console.error('更新文章失败:', error);
    }
}

// 删除文章
async function deletePost(id) {
    if (!currentUser) {
        alert('请先登录');
        return;
    }

    if (!confirm('确定要删除这篇文章吗？')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/posts/${id}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });

        if (response.ok) {
            loadPosts(); // 重新加载文章列表
        } else {
            const data = await response.json();
            alert('删除文章失败: ' + (data.detail || '未知错误'));
        }
    } catch (error) {
        console.error('删除文章失败:', error);
    }
}