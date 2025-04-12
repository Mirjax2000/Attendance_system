# Installation Guide

## Prerequisites

### 1. Install Visual C++ Build Tools
- Download and install [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Or use this command in PowerShell (as administrator):
```shell
winget install Microsoft.VisualStudio.2022.BuildTools --force --override "--passive --wait --add Microsoft.VisualStudio.Workload.VCTools;includeRecommended"
```
> ⚠️ **Note**: Restart your computer after installation

### 2. Install CMake
- Download and install [CMake](https://github.com/Kitware/CMake/releases/download/v4.0.0-rc4/cmake-4.0.0-rc4-windows-x86_64.msi)
- Make sure to check "Add CMake to PATH" during installation

## Project Setup

### 1. Install UV Package Manager
```shell
pip install uv
```

### 2. Clone the Repository
```shell
git clone https://github.com/Mirjax2000/Attendance_system.git
cd Attendance_system
```

### 3. Create and Activate Virtual Environment
```shell
uv venv
.venv\Scripts\activate
```

### 4. Install dlib
Open "Developer Command Prompt for VS 2022" and navigate to your project directory, then run:
```shell
uv add dlib
```

### 5. Install Project Dependencies
```shell
uv sync
```

## Verification
To verify the installation, try importing dlib in Python:
```shell
python -c "import dlib; print(dlib.__version__)"
```

If no errors occur, the installation was successful.
