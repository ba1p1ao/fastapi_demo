const API_BASE_URL = 'http://localhost:8100';

// DOM 加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadTasks();
    
    // 添加任务表单提交事件
    document.getElementById('add-task-form').addEventListener('submit', function(e) {
        e.preventDefault();
        addTask();
    });
});

// 加载所有任务
async function loadTasks() {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`);
        const tasks = await response.json();
        displayTasks(tasks);
    } catch (error) {
        console.error('加载任务失败:', error);
    }
}

// 显示任务列表
function displayTasks(tasks) {
    const container = document.getElementById('tasks-container');
    container.innerHTML = '';
    
    tasks.forEach(task => {
        const taskElement = document.createElement('div');
        taskElement.className = `task-item ${task.is_completed ? 'completed' : ''}`;
        taskElement.innerHTML = `
            <div class="task-title">${task.title}</div>
            <div class="task-description">${task.description || '无描述'}</div>
            <div class="task-actions">
                <button class="complete-btn" onclick="toggleTask(${task.id}, ${!task.is_completed})">
                    ${task.is_completed ? '标记为未完成' : '标记为完成'}
                </button>
                <button class="delete-btn" onclick="deleteTask(${task.id})">删除</button>
            </div>
        `;
        container.appendChild(taskElement);
    });
}

// 添加新任务
async function addTask() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description
            })
        });
        
        if (response.ok) {
            // 清空表单
            document.getElementById('add-task-form').reset();
            // 重新加载任务列表
            loadTasks();
        } else {
            console.error('添加任务失败');
        }
    } catch (error) {
        console.error('添加任务失败:', error);
    }
}

// 切换任务完成状态
async function toggleTask(id, isCompleted) {
    try {
        // 首先获取当前任务
        const response = await fetch(`${API_BASE_URL}/tasks/${id}`);
        const task = await response.json();
        
        // 更新任务状态
        const updateResponse = await fetch(`${API_BASE_URL}/tasks/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ...task,
                is_completed: isCompleted
            })
        });
        
        if (updateResponse.ok) {
            loadTasks();
        } else {
            console.error('更新任务失败');
        }
    } catch (error) {
        console.error('更新任务失败:', error);
    }
}

// 删除任务
async function deleteTask(id) {
    if (!confirm('确定要删除这个任务吗？')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadTasks();
        } else {
            console.error('删除任务失败');
        }
    } catch (error) {
        console.error('删除任务失败:', error);
    }
}