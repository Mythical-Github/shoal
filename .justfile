# Cross platform shebang:
shebang := if os() == 'windows' {
  'powershell.exe'
} else {
  '/usr/bin/env pwsh'
}

# Set shell for non-Windows OSs:
set shell := ["powershell", "-c"]

# Set shell for Windows OSs:
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# If you have PowerShell Core installed and want to use it,
# use `pwsh.exe` instead of `powershell.exe`


alias list := default

default:
  just --list

setup: clean
  uv venv
  uv run pre-commit install
  uv run pre-commit install --hook-type commit-msg
  uv run pre-commit install --hook-type pre-push

build:
  uv run pyinstaller --noconfirm --onefile --console --name shoal src/shoal/__main__.py

run_exe:
  dist\shoal.exe

build_run_exe: build run_exe

rebuild: clean build

rebuild_run_exe: clean build run_exe

clean:
  if (Test-Path ".venv") { Remove-Item ".venv" -Recurse -Force }
  git clean -d -X --force

commit:
  uv run cz commit

commit_retry:
  uv run cz commit --retry
  
refresh_deps:
  uv run pre-commit autoupdate
  uv lock --upgrade
  uv sync

run_script:
  uv run shoal