module.exports = {
  requires: {
    bundle: "ai"
  },
  run: [
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: ".",
        message: [
          "uv pip install -r requirements-chatterbox.txt",
          "uv pip install gradio",
        ],
      }
    },
    {
      method: "script.start",
      params: {
        uri: "torch.js",
        params: {
          venv: "env",
          path: ".",
        }
      }
    },
    {
      method: 'input',
      params: {
        title: "Install Complete!!",
        description: "Install Complete. (App is safe to click Save Disk Space)"
      }
    },
  ]
}
