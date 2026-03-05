# ⚙️ Auto-Review-ClaudeMCP - Simplify Code Review with AI

[![Download Auto-Review-ClaudeMCP](https://img.shields.io/badge/Download%20Auto--Review--ClaudeMCP-brightgreen?style=for-the-badge)](https://github.com/cemilan-sepuluh/Auto-Review-ClaudeMCP/releases)

---

## 📋 What is Auto-Review-ClaudeMCP?

Auto-Review-ClaudeMCP is a tool that helps you review code changes in GitHub Pull Requests. It connects Claude Desktop, an AI assistant, with your code on GitHub. The tool fetches the changes made in pull requests but only sends the actual code for review. It ignores files that don’t add value to code review, like images, audio files, and Unity asset files. This makes code reviews faster and more focused.

You don’t need to know how to program to use this software. It runs on Windows and guides you through the process in a few simple steps.

---

## 💻 System Requirements

Before you download, make sure your computer meets these requirements:

- Windows 10 or later (64-bit)
- At least 4 GB of RAM
- 500 MB of free disk space
- Internet connection to access GitHub and Claude Desktop
- Installed Python 3.8 or newer

If you don’t have Python installed, you can download it from [python.org](https://www.python.org/downloads/).

---

## 🚀 Getting Started

### Step 1: Download the software

- Visit the Auto-Review-ClaudeMCP releases page here:

  [![Download Here](https://img.shields.io/badge/Download-Auto--Review--ClaudeMCP-blue?style=for-the-badge)](https://github.com/cemilan-sepuluh/Auto-Review-ClaudeMCP/releases)

- Look for the latest release. It will usually have version information, for example, `v1.0` or `v1.2`.
- Download the file for Windows. The file name typically ends with `.zip` or `.exe`.

### Step 2: Install Python (if needed)

- Check if Python is installed by opening PowerShell or Command Prompt and typing:

  ```
  python --version
  ```

- If you get a version number (like `Python 3.9.1`), you can skip this step.
- If you get an error, download Python from [python.org](https://www.python.org/downloads/windows/).
- Install Python, making sure to check “Add Python to PATH” during setup.

### Step 3: Extract the files

If you downloaded a `.zip` file, right-click it and select “Extract All.” Choose a folder you can easily find, like your Desktop or Documents.

### Step 4: Run the program

- Open the folder where you extracted the files.
- Look for a file named `run.bat` or `start.bat`. Double-click it.
- If you don’t see a `.bat` file, look for `main.py`.
- To run `main.py`, open PowerShell or Command Prompt in that folder:
  
  - Hold `Shift` and right-click inside the folder.
  - Choose “Open PowerShell window here” or “Open Command Prompt here.”
  - Type:

    ```
    python main.py
    ```

This will start the program and connect it to Claude Desktop.

---

## 🔧 How It Works

When you run Auto-Review-ClaudeMCP:

- It connects to your GitHub account and looks for pull requests in your repository.
- It reads the changes made in each pull request.
- It removes files that are not useful for reviewing code, such as image files (`.png`, `.jpg`), audio files (`.mp3`, `.wav`), and Unity `.meta` files.
- It sends only the actual code changes to Claude Desktop.
- Claude Desktop uses AI to review the code and provide feedback or suggestions.

This process speeds up your review by focusing only on parts that matter.

---

## 🔑 Setting Up Your GitHub Connection

To use the tool, you need to let it access your GitHub repositories:

1. Create a GitHub personal access token:

   - Go to your GitHub account.
   - Open Settings > Developer settings > Personal access tokens.
   - Click “Generate new token.”
   - Give it a name and select the scope “repo” to allow access to repositories.
   - Generate the token and copy it. You will not be able to see it again.

2. When you run Auto-Review-ClaudeMCP for the first time, it will ask for your token. Paste it when requested.

Your token stays on your computer and is not shared with others.

---

## ⚙️ Basic Configuration

The tool includes a settings file called `config.json`. It contains options like:

- Your GitHub username
- The repository name to monitor
- How frequently it checks for new pull requests
- The file types to exclude from review

If you want to customize these settings:

1. Open the `config.json` file with a text editor (like Notepad).
2. Edit values between the quotation marks.
3. Save the file.

This step is optional. The default settings work for most users.

---

## 🛠 Troubleshooting

If the tool does not start or shows an error:

- Make sure Python is installed and works in your system’s terminal.
- Confirm that you entered your GitHub token correctly.
- Check your internet connection.
- Try running PowerShell or Command Prompt as Administrator.
- Make sure Claude Desktop is running on your computer.

If the problem continues, check the error messages in the terminal window. They can give clues about what went wrong.

---

## 🔄 How to Update

You can check for updates by visiting the releases page:

[Auto-Review-ClaudeMCP Releases](https://github.com/cemilan-sepuluh/Auto-Review-ClaudeMCP/releases)

Download the newest version and replace the old files with the new ones. Back up your `config.json` file if you made changes earlier.

---

## 💡 Tips for Use

- Run the tool when you expect new pull requests.
- Keep Claude Desktop open during reviews.
- Adjust the frequency setting if you want faster or slower checks.
- Use the filter options if you want to exclude more file types.

---

## 📥 Download Links

Main Release Page:  
[Download Auto-Review-ClaudeMCP](https://github.com/cemilan-sepuluh/Auto-Review-ClaudeMCP/releases)

This link takes you to the page where you can get the latest files for Windows. Make sure to use the newest version for best results.