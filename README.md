# 🚀 Advanced Computer Control UI Agent with GPT-4 Vision and PyAutoGUI 🎛️

This project demonstrates an advanced AI-powered UI automation agent 🎉 leveraging computer vision and multimodal capabilities of GPT-4, allowing direct computer control through natural language instructions. Designed for macOS, the agent integrates a sequence of powerful features that collaboratively execute user-defined goals by automating UI actions.

## ✨ Key Features

### 🧠 Intelligent Task Execution with GPT-4 Vision
- **🎯 Goal-Oriented Input**: Accepts high-level user goals via the command line and translates them into actionable steps.
- **📝 Dynamic Task Planning**: Utilizes GPT-4 Vision to interpret the screen, enabling it to generate, adjust, and refine task plans based on the UI context.
- **👀 Computer Vision for Enhanced Control**: Uses GPT-4 Vision’s multimodal capabilities for on-screen interpretation, streamlining interactions and enhancing decision accuracy.

### 🔄 Action and Feedback Loop
- **🔍 OODA Loop Framework**: Employs the Observe-Orient-Decide-Act loop for real-time decision-making, adapting to any changes or unexpected UI states.
- **🗣️ User Feedback Integration**: Receives and integrates user feedback after each action, ensuring the agent continually aligns with the user’s objectives.
- **🔄 Automated Retry Mechanism**: Automatically retries failed actions up to 3 times before prompting user intervention, enhancing robustness in diverse scenarios.

### 📋 Comprehensive Logging and Error Handling
- **📜 Transparent Logging**: Logs all actions with detailed timestamps and rationales, allowing users to track each step and review decision processes.
- **⚙️ Configurable Parameters**: Adjustable settings for retries, timeouts, and logging levels, giving users full control over the agent’s behavior.

## 📂 Project Structure

- `src/`
  - `app.py`: Main application script, orchestrates user interactions and initiates task flows.
  - `LLMHelper.py`: Manages communication with GPT-4 API, processing user goals and responses.
  - `AutoHelper.py`: Core module for command execution, including retries and error handling.
  - `WebAgentHelper.py`: Simplifies web navigation and URL handling.
  - `pyautoguihelper.py`: Provides custom wrappers around PyAutoGUI functions for seamless GUI actions.
- `logs/`: 🗄️ Stores session logs and error reports.
- `config/`: ⚙️ Configurable parameters for task behavior, retries, and logging.
- `.env`: 🔑 Environment variables file for API keys and sensitive information. An example .env.example is provided.
- `Dockerfile`: 🐳 Docker configuration for easy deployment and environment consistency.
- `docker-compose.yml`: Docker Compose configuration to streamline setup.

## 📋 Prerequisites

- **🐳 Docker and Docker Compose**: Ensure both are installed to run the application in a containerized environment.
- **🔑 OpenAI API Key**: Necessary for connecting with GPT-4 Vision.

## 🚀 Quick Start

1. **Configure the OpenAI API Key**:
   - Open the `.env` file and replace `your_openai_api_key` with your OpenAI API key.

2. **Run the Application**:
   - Build and run the application with Docker:
     ```bash
     docker-compose up
     ```

3. **Define Goals**:
   - Input a goal in the terminal and observe as the agent processes it and automates UI actions based on the goal.

## 💻 Usage Example

```bash
docker-compose up

