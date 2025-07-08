# 🎮 Retro To-Do List App

A nostalgic to-do list application built with Python Flask and styled with NES.css for that classic 8-bit gaming aesthetic!

## Features

- ✅ Add new tasks (quests)
- 🎯 Mark tasks as completed
- 🗑️ Delete individual tasks
- 🧹 Clear all completed tasks
- 📊 View task statistics
- 📱 Responsive design
- 🎮 Retro gaming UI with NES.css

## Screenshots

The app features a beautiful retro gaming interface with:
- Pixel-perfect fonts (Press Start 2P)
- Classic Nintendo-style buttons and containers
- Gradient backgrounds
- Task statistics badges
- Mobile-responsive layout

## Installation

1. **Clone or download this project**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser and visit:**
   ```
   http://localhost:5000
   ```

## Usage

- **Add Task**: Type your task in the input field and click "Add Task" or press Ctrl+Enter
- **Complete Task**: Click the "Done" button to mark a task as completed
- **Undo Task**: Click "Undo" to mark a completed task as pending
- **Delete Task**: Click "Delete" to remove a task permanently
- **Clear Completed**: Use the "Clear Completed" button to remove all finished tasks

## File Structure

```
ToDoList/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── tasks.json         # Task storage (created automatically)
├── templates/
│   └── index.html     # Main HTML template with NES.css
└── README.md          # This file
```

## Technical Details

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, NES.css framework
- **Data Storage**: JSON file (tasks.json)
- **Styling**: NES.css for retro gaming aesthetic
- **Fonts**: Press Start 2P (Google Fonts)

## Customization

You can customize the app by:
- Modifying colors in the CSS section of `templates/index.html`
- Adding new task properties in `app.py`
- Implementing additional features like categories, due dates, etc.
- Adding sound effects using Web Audio API

## Dependencies

- Flask 3.0.0
- Werkzeug 3.0.1

## Browser Support

Works on all modern browsers including:
- Chrome/Chromium
- Firefox
- Safari
- Edge

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to fork this project and submit pull requests for any improvements!

---

Made with ❤️ using Flask & NES.css
