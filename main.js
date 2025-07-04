const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process'); // Ligne ajoutée

let flaskProcess; // Ligne ajoutée

function createWindow() {
  const win = new BrowserWindow({
    width: 900,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      devTools: false
    },
  });

  win.loadFile(path.join(__dirname, 'frontend', 'login.html'));
  win.setMenu(null);
}

app.whenReady().then(() => {
  // Ligne ajoutée (lance Flask)
  flaskProcess = spawn('python', ['backend/classify_server.py']);
  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (flaskProcess) flaskProcess.kill(); // Ligne ajoutée
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});