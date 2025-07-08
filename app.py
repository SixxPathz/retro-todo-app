from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import json
import os
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Error loading tasks: {e}")
            if os.path.exists(TASKS_FILE):
                backup_name = f"tasks_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                os.rename(TASKS_FILE, backup_name)
            return []
    return []

def save_tasks(tasks):
    try:
        if os.path.exists(TASKS_FILE):
            backup_name = f"tasks_backup.json"
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                with open(backup_name, 'w', encoding='utf-8') as backup:
                    backup.write(f.read())
        
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving tasks: {e}")
        flash('Error saving tasks. Please try again.', 'error')

def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task.get('id', 0) for task in tasks) + 1

def validate_task(task_text):
    if not task_text or not task_text.strip():
        return False, "Task cannot be empty"
    if len(task_text.strip()) > 500:
        return False, "Task is too long (max 500 characters)"
    return True, ""

@app.route('/')
def index():
    tasks = load_tasks()
    search = request.args.get('search', '')
    filter_status = request.args.get('filter', 'all')
    
    if search:
        tasks = [task for task in tasks if search.lower() in task['text'].lower()]
    
    if filter_status == 'completed':
        tasks = [task for task in tasks if task['completed']]
    elif filter_status == 'pending':
        tasks = [task for task in tasks if not task['completed']]
    
    today = datetime.now().date().strftime('%Y-%m-%d')
    for task in tasks:
        if task.get('due_date') and not task['completed']:
            try:
                due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date().strftime('%Y-%m-%d')
                task['is_overdue'] = due_date < today
            except ValueError:
                task['is_overdue'] = False
        else:
            task['is_overdue'] = False
    
    def sort_key(task):
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        return (
            task['completed'],
            priority_order.get(task.get('priority', 'medium'), 1),
            task['created_at']
        )
    
    tasks.sort(key=sort_key)
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('index.html', tasks=tasks, search=search, filter_status=filter_status, today=today, current_date=current_date)

@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    priority = request.form.get('priority', 'medium')
    due_date = request.form.get('due_date', '')
    
    is_valid, error_msg = validate_task(task_text)
    if not is_valid:
        flash(error_msg, 'error')
        return redirect(url_for('index'))
    
    tasks = load_tasks()
    new_task = {
        'id': get_next_id(tasks),
        'text': task_text.strip(),
        'completed': False,
        'priority': priority,
        'due_date': due_date if due_date else None,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    tasks.append(new_task)
    save_tasks(tasks)
    flash('Task added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    task_text = request.form.get('task')
    priority = request.form.get('priority', 'medium')
    due_date = request.form.get('due_date', '')
    
    is_valid, error_msg = validate_task(task_text)
    if not is_valid:
        flash(error_msg, 'error')
        return redirect(url_for('index'))
    
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['text'] = task_text.strip()
            task['priority'] = priority
            task['due_date'] = due_date if due_date else None
            task['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            break
    save_tasks(tasks)
    flash('Task updated successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            task['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if task['completed']:
                task['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                task.pop('completed_at', None)
            break
    save_tasks(tasks)
    status = "completed" if any(task['id'] == task_id and task['completed'] for task in tasks) else "pending"
    flash(f'Task marked as {status}!', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    original_count = len(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]
    
    if len(tasks) < original_count:
        save_tasks(tasks)
        flash('Task deleted successfully!', 'success')
    else:
        flash('Task not found!', 'error')
    return redirect(url_for('index'))

@app.route('/clear_completed')
def clear_completed():
    tasks = load_tasks()
    completed_count = len([task for task in tasks if task['completed']])
    tasks = [task for task in tasks if not task['completed']]
    save_tasks(tasks)
    flash(f'{completed_count} completed tasks cleared!', 'success')
    return redirect(url_for('index'))

@app.route('/stats')
def get_stats():
    tasks = load_tasks()
    total = len(tasks)
    completed = len([task for task in tasks if task['completed']])
    pending = total - completed
    
    high_priority = len([task for task in tasks if task.get('priority') == 'high' and not task['completed']])
    
    overdue = 0
    today = datetime.now().date()
    for task in tasks:
        if not task['completed'] and task.get('due_date'):
            try:
                due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                if due_date < today:
                    overdue += 1
            except ValueError:
                pass
    
    return jsonify({
        'total': total,
        'completed': completed,
        'pending': pending,
        'high_priority': high_priority,
        'overdue': overdue
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
