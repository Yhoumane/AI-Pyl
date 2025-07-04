const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('api', {
  classifyImage: (file) => {
    return new Promise((resolve, reject) => {
      const formData = new FormData()
      formData.append('file', file)

      fetch('http://localhost:5000/predict', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => resolve(data))
      .catch(error => reject(error))
    })
  }
})