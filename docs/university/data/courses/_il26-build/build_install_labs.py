#!/usr/bin/env python3
"""Build install-labs.json for IL-26 (fragment B: installation labs). All prose original."""
import json, os

OUT = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses/_il26-build/install-labs.json")

def plat(steps, notes=""):
    return {"steps": steps, "notes": notes}

def unsup(notes):
    return {"steps": [], "notes": notes, "supported": False}

labs = []

# ---------------------------------------------------------------- 01 Python
labs.append({
 "id": "IL26-INST-01", "tool": "Python 3.12+ and pip", "category": "core",
 "moduleId": "IL26-M09", "estimatedMinutes": 20,
 "gates": ["IL26-TL-PYTHON-01"],
 "platforms": {
  "windows": plat([
   "Open the Python downloads page at https://www.python.org/downloads/ and click the yellow \"Download Python 3.12.x\" button (take the newest 3.12 or 3.13 point release).",
   "Run the downloaded .exe. On the FIRST installer screen, check the box labeled \"Add python.exe to PATH\" at the very bottom — this is the step most beginners miss, and skipping it breaks every later tool.",
   "Click \"Install Now\" and let the installer finish. Accept the prompt to disable the MAX_PATH length limit if it appears.",
   "Close and reopen your terminal (or PowerShell), then run the verification checkpoints below."
  ], "If you installed without the PATH box checked, uninstall and reinstall — fixing PATH by hand is slower than a clean reinstall."),
  "macos": plat([
   "Open https://www.python.org/downloads/ and click \"Download Python 3.12.x\" to get the macOS 64-bit installer (.pkg).",
   "Run the .pkg and accept the defaults through the wizard.",
   "After install, open the Applications > Python 3.12 folder and double-click \"Install Certificates.command\" so pip can download packages over HTTPS.",
   "Open Terminal and run the verification checkpoints below. macOS ships its own old Python; always call python3/pip3, not python/pip."
  ]),
  "linux": plat([
   "Open a terminal. On Ubuntu/Debian run: sudo apt update && sudo apt install -y python3 python3-pip python3-venv",
   "On Fedora/RHEL run: sudo dnf install -y python3 python3-pip",
   "Confirm with the checkpoints below. If your distro ships an older Python 3, add the deadsnakes PPA (Ubuntu) or use the official tarball rather than building from source."
  ])
 },
 "checkpoints": [
  {"command": "python3 --version", "expected": "Python 3.12.x (or newer, e.g. 3.13.x)", "platforms": ["windows","macos","linux"]},
  {"command": "pip --version", "expected": "pip 24.x from ... (python 3.12)", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "Windows: 'python' is not recognized as an internal or external command", "fix": "You skipped the Add-to-PATH checkbox. Reinstall and check it on the first screen, or run the installer again and choose Modify > add python.exe to PATH."},
  {"symptom": "Windows: typing python opens the Microsoft Store", "fix": "That is the fake app-execution alias. Either turn off the alias in Settings > Apps > Advanced app settings > App execution aliases, or just use py -3 instead of python everywhere."},
  {"symptom": "macOS: pip install fails with SSL certificate errors", "fix": "You skipped Install Certificates.command. Run it from Applications > Python 3.12, then retry pip."},
  {"symptom": "Linux: 'externally-managed-environment' error on pip install", "fix": "Your distro protects system Python. Install packages into a virtualenv instead: python3 -m venv ~/venv && source ~/venv/bin/activate, then pip install."}
 ],
 "costNote": "Free and open source forever. Python has no paid tier and no expiry."
})

# ---------------------------------------------------------------- 02 Git
labs.append({
 "id": "IL26-INST-02", "tool": "Git", "category": "core",
 "moduleId": "IL26-M20", "estimatedMinutes": 15,
 "gates": ["IL26-TL-GIT-01"],
 "platforms": {
  "windows": plat([
   "Open https://git-scm.com/download and let the page pick the Windows installer for you (click \"Click here to download\").",
   "Run the installer. On the PATH screen choose \"Git from the command line and also from 3rd-party software\" (the recommended middle option).",
   "On the line-ending screen choose \"Checkout Windows-style, commit Unix-style line endings\".",
   "On the terminal emulator screen choose \"Use Windows' default console window\" unless you have a reason not to.",
   "Finish the install, open a NEW terminal, and run the checkpoints."
  ]),
  "macos": plat([
   "The simplest route: install Apple's command line tools by running xcode-select --install in Terminal and accepting the prompt — Git comes with them.",
   "Alternatively install Homebrew from https://brew.sh, then run brew install git.",
   "Run the checkpoints to confirm."
  ]),
  "linux": plat([
   "Ubuntu/Debian: sudo apt update && sudo apt install -y git",
   "Fedora/RHEL: sudo dnf install -y git",
   "Run the checkpoints, then set your identity: git config --global user.name \"Your Name\" and git config --global user.email \"your@email.com\" — commits are rejected by most hosts without these."
  ])
 },
 "checkpoints": [
  {"command": "git --version", "expected": "git version 2.4x.x (any recent 2.x)", "platforms": ["windows","macos","linux"]},
  {"command": "git config --global user.name", "expected": "Your name, as you configured it (non-empty)", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "Windows: 'git' is not recognized in a new terminal", "fix": "The installer PATH option was set to Git Bash only. Reinstall and choose \"Git from the command line and also from 3rd-party software\"."},
  {"symptom": "macOS: xcode-select --install says tools already installed but git missing", "fix": "Reset with sudo xcode-select --reset then run xcode-select --install again, or fall back to brew install git."},
  {"symptom": "Push asks for a password and your GitHub password does not work", "fix": "GitHub removed password auth years ago. Create a personal access token (GitHub Settings > Developer settings > Tokens) and use it as the password, or set up SSH keys."}
 ],
 "costNote": "Free and open source forever. Git itself costs nothing; hosting accounts (GitHub, GitLab) have free tiers generous enough for a portfolio."
})

# ---------------------------------------------------------------- 03 VS Code
labs.append({
 "id": "IL26-INST-03", "tool": "Visual Studio Code", "category": "core",
 "moduleId": "IL26-M09", "estimatedMinutes": 15,
 "gates": ["IL26-TL-VSCODE-01"],
 "platforms": {
  "windows": plat([
   "Open https://code.visualstudio.com/download and download the Windows User Installer (64-bit).",
   "Run the installer. On the \"Select Additional Tasks\" screen, check \"Add to PATH\" and \"Add 'Open with Code' action to Windows Explorer context menus\" — both save real time later.",
   "Launch VS Code, open the Extensions panel (Ctrl+Shift+X), and install the \"Python\" extension by Microsoft and the \"Jupyter\" extension by Microsoft. These power the Python and notebook tool-labs.",
   "In a terminal run the checkpoints below."
  ]),
  "macos": plat([
   "Open https://code.visualstudio.com/download and download the macOS build (choose Apple Silicon if your Mac has an M1/M2/M3/M4 chip, Intel otherwise).",
   "Open the .zip, drag Visual Studio Code into Applications, and launch it.",
   "Press Cmd+Shift+P, type \"Shell Command: Install 'code' command in PATH\", and run it so the code command works in Terminal.",
   "Install the Microsoft Python and Jupyter extensions from the Extensions panel (Cmd+Shift+X)."
  ]),
  "linux": plat([
   "Ubuntu/Debian: download the .deb from https://code.visualstudio.com/download and run sudo apt install ./code_*.deb (it adds Microsoft's repo so updates arrive automatically).",
   "Fedora/RHEL: download the .rpm and run sudo dnf install ./code-*.rpm.",
   "Launch with the code command, then install the Microsoft Python and Jupyter extensions."
  ])
 },
 "checkpoints": [
  {"command": "code --version", "expected": "1.9x.x followed by a commit hash line (any recent 1.x)", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "'code' command not found after install", "fix": "Windows: reinstall with \"Add to PATH\" checked. macOS: run the \"Shell Command: Install 'code' command in PATH\" palette command. Linux: log out and back in so the PATH change takes effect."},
  {"symptom": "Python files do not run or show no interpreter", "fix": "Install the Microsoft Python extension, then press Ctrl+Shift+P (Cmd+Shift+P on Mac) and run \"Python: Select Interpreter\" to point at your Python 3.12+ install."},
  {"symptom": "Jupyter notebooks show \"No kernel\"", "fix": "Install the Microsoft Jupyter extension and the ipykernel package: pip install ipykernel, then restart VS Code."}
 ],
 "costNote": "Free forever for individuals. VS Code has no paid tier; the marketplace extensions used in this course are all free."
})

# ---------------------------------------------------------------- 04 Jupyter
labs.append({
 "id": "IL26-INST-04", "tool": "Jupyter Notebook / JupyterLab (via pip)", "category": "core",
 "moduleId": "IL26-M09", "estimatedMinutes": 15,
 "gates": ["IL26-TL-JUPYTER-01"],
 "platforms": {
  "windows": plat([
   "Confirm Python 3.12+ is installed (finish IL26-INST-01 first).",
   "In a terminal run: pip install notebook jupyterlab",
   "Launch with: jupyter lab — your browser should open to the JupyterLab interface automatically. If it does not, copy the http://localhost:8888/... URL printed in the terminal into your browser.",
   "To stop the server, press Ctrl+C in the terminal and confirm shutdown."
  ], "If pip warns about scripts not on PATH, add %APPDATA%\\Python\\Python312\\Scripts to your user PATH."),
  "macos": plat([
   "Confirm Python 3.12+ is installed (finish IL26-INST-01 first).",
   "In Terminal run: pip3 install notebook jupyterlab",
   "Launch with: jupyter lab — your browser opens automatically. Create a test notebook, run print(\"hello\"), and confirm output appears.",
   "Stop the server with Ctrl+C."
  ]),
  "linux": plat([
   "Confirm Python 3.12+ and pip are installed (finish IL26-INST-01 first).",
   "Create a virtualenv to dodge the externally-managed-environment error: python3 -m venv ~/jupyter-env && source ~/jupyter-env/bin/activate",
   "Run: pip install notebook jupyterlab, then jupyter lab. Open the printed URL if the browser does not launch.",
   "Stop with Ctrl+C; reactivate the env with source ~/jupyter-env/bin/activate next session."
  ])
 },
 "checkpoints": [
  {"command": "jupyter --version", "expected": "jupyter_core ... / notebook ... / jupyterlab ... (version lines for the installed packages)", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "'jupyter' is not recognized after pip install", "fix": "The Scripts/bin directory is not on PATH. Reinstall Python with Add-to-PATH (Windows) or add ~/.local/bin to PATH (macOS/Linux): export PATH=\"$HOME/.local/bin:$PATH\"."},
  {"symptom": "Notebook kernel dies immediately on start", "fix": "Install the kernel package explicitly: pip install ipykernel, then in Jupyter choose Kernel > Change kernel > Python 3."},
  {"symptom": "Port 8888 already in use", "fix": "Another server is running. Launch with jupyter lab --port 8889 instead."}
 ],
 "costNote": "Free and open source forever. Jupyter runs locally on your machine; no account, no cloud bill."
})

# ---------------------------------------------------------------- 05 DBeaver
labs.append({
 "id": "IL26-INST-05", "tool": "DBeaver Community Edition", "category": "database",
 "moduleId": "IL26-M08", "estimatedMinutes": 20,
 "gates": ["IL26-TL-DBEAVER-01"],
 "platforms": {
  "windows": plat([
   "Open https://dbeaver.io/download/ and download the Windows 64-bit installer (the .exe, not the zip).",
   "Run the installer with defaults — it bundles its own Java runtime, so you do not need to install Java separately.",
   "Launch DBeaver. On first run it asks to create a sample database; you can decline — you will connect to PostgreSQL/MySQL from later labs.",
   "Open a new connection wizard (Database > New Database Connection) and confirm the driver list loads; drivers download on first use, which requires internet."
  ]),
  "macos": plat([
   "Open https://dbeaver.io/download/ and download the macOS .dmg (Apple Silicon build if you have an M-series Mac).",
   "Open the .dmg, drag DBeaver into Applications, and launch it. If macOS blocks it, right-click > Open to approve the unsigned developer once.",
   "Decline the sample database on first run and confirm the new-connection wizard loads its driver list."
  ]),
  "linux": plat([
   "Ubuntu/Debian: download the .deb from https://dbeaver.io/download/ and run sudo apt install ./dbeaver-ce_*.deb",
   "Fedora/RHEL: download the .rpm and run sudo dnf install ./dbeaver-ce-*.rpm",
   "Launch with dbeaver-ce and confirm the new-connection wizard loads its driver list."
  ])
 },
 "checkpoints": [
  {"command": "Open DBeaver > Help > About (or DBeaver > About DBeaver on macOS)", "expected": "DBeaver Community Edition, version 24.x or newer", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "Driver download fails when creating a connection", "fix": "You need internet on first use per driver. Check DBeaver > Preferences > Connections > Drivers > Maven to change the artifact repository if your network blocks the default."},
  {"symptom": "macOS: app is damaged / cannot be opened", "fix": "Run xattr -cr /Applications/DBeaver.app in Terminal to strip the quarantine attribute, then launch again."},
  {"symptom": "OutOfMemoryError on large result sets", "fix": "Raise the heap in dbeaver.ini (-Xmx1024m to -Xmx4096m) — Community Edition defaults are conservative."}
 ],
 "costNote": "Community Edition is free and open source forever. The paid Pro/Ultimate editions add cloud and NoSQL features the course does not require."
})

# ---------------------------------------------------------------- 06 PostgreSQL
labs.append({
 "id": "IL26-INST-06", "tool": "PostgreSQL 16", "category": "database",
 "moduleId": "IL26-M08", "estimatedMinutes": 25,
 "gates": ["IL26-TL-POSTGRES-01"],
 "platforms": {
  "windows": plat([
   "Open https://www.postgresql.org/download/ , choose Windows, and download the interactive installer from EDB for PostgreSQL 16.",
   "Run the installer. WRITE DOWN the superuser (postgres) password you set — you will need it for every local connection.",
   "Keep the default port 5432 and default locale. On the component screen you can uncheck Stack Builder; keep pgAdmin if you want a web GUI, or skip it since DBeaver covers that role.",
   "After install, open SQL Shell (psql) from the Start menu, press Enter through the defaults, type your postgres password, and run SELECT version(); to confirm."
  ], "The EDB installer is the beginner-safe path on Windows; the zip archive is for advanced users only."),
  "macos": plat([
   "Install Homebrew from https://brew.sh if you do not have it, then run: brew install postgresql@16",
   "Start the service: brew services start postgresql@16",
   "Create your user role: createuser -s $(whoami) — then you can connect without a password over the local socket.",
   "Verify with: psql -c \"SELECT version();\""
  ], "Postgres.app is a fine GUI alternative, but the Homebrew route matches the checkpoints and keeps one package manager for everything."),
  "linux": plat([
   "Ubuntu/Debian: sudo apt update && sudo apt install -y postgresql postgresql-contrib",
   "Start and enable it: sudo systemctl start postgresql && sudo systemctl enable postgresql",
   "Switch to the postgres user to create your role: sudo -u postgres createuser -s $USER, then create your database: sudo -u postgres createdb $USER",
   "Verify with: psql -c \"SELECT version();\" — with no password prompt, since local peer auth trusts your OS user."
  ])
 },
 "checkpoints": [
  {"command": "psql -c \"SELECT version();\"", "expected": "PostgreSQL 16.x ... (a version string mentioning 16)", "platforms": ["windows","macos","linux"]},
  {"command": "psql -c \"SHOW server_version;\"", "expected": "16.x", "platforms": ["macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "psql: could not connect to server — connection refused", "fix": "The service is not running. Windows: start the postgresql-x64-16 service in Services. macOS: brew services restart postgresql@16. Linux: sudo systemctl start postgresql."},
  {"symptom": "password authentication failed for user postgres", "fix": "You mistyped the superuser password from install time. Windows: rerun the EDB installer and reset it. Linux/macOS socket users: connect as your OS user instead of postgres."},
  {"symptom": "role \"yourname\" does not exist", "fix": "Create the role first: as the postgres superuser run CREATE ROLE yourname WITH LOGIN SUPERUSER; then reconnect."},
  {"symptom": "Port 5432 already in use during install", "fix": "Another Postgres (or Docker container) holds the port. Stop the other instance or install on port 5433 and note it for connection strings."
   }],
 "costNote": "Free and open source forever. Local PostgreSQL costs nothing and never expires; managed cloud Postgres (RDS, Cloud SQL) is a separate paid product you do not need here."
})

# ---------------------------------------------------------------- 07 MySQL
labs.append({
 "id": "IL26-INST-07", "tool": "MySQL 8", "category": "database",
 "moduleId": "IL26-M08", "estimatedMinutes": 25,
 "gates": ["IL26-TL-MYSQL-01"],
 "platforms": {
  "windows": plat([
   "Open https://dev.mysql.com/downloads/installer/ and download the MySQL Installer for Windows (the larger ~500 MB bundle includes the server; the small web installer downloads components during setup).",
   "Run the installer, choose the \"Developer Default\" setup type, and walk through the server configuration screens.",
   "On the Accounts and Roles screen, WRITE DOWN the root password you set. On the Windows Service screen keep \"Start the MySQL Server at System Startup\" checked.",
   "Finish, then open MySQL Shell or the legacy Command Line Client from the Start menu, log in as root, and run SELECT VERSION(); to confirm."
  ]),
  "macos": plat([
   "Install Homebrew from https://brew.sh if needed, then run: brew install mysql",
   "Start the service: brew services start mysql",
   "Secure it: mysql_secure_installation — set a root password when prompted (WRITE IT DOWN), and accept the suggested hardening answers.",
   "Verify with: mysql -u root -p -e \"SELECT VERSION();\" (type the root password at the prompt)."
  ]),
  "linux": plat([
   "Ubuntu/Debian: sudo apt update && sudo apt install -y mysql-server",
   "Start and enable: sudo systemctl start mysql && sudo systemctl enable mysql",
   "Run sudo mysql_secure_installation to set a root password and apply the hardening steps.",
   "Verify with: mysql -u root -p -e \"SELECT VERSION();\""
  ])
 },
 "checkpoints": [
  {"command": "mysql --version", "expected": "mysql  Ver 8.0.x ... (an 8.0 version string)", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "Access denied for user 'root'@'localhost'", "fix": "Wrong root password. On Linux, sudo mysql lets the OS root in without a password — use that to reset: ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpassword';"},
  {"symptom": "Can't connect to MySQL server on 'localhost' (10061 / 2002)", "fix": "The service is not running. Windows: start MySQL80 in Services. macOS: brew services restart mysql. Linux: sudo systemctl start mysql."},
  {"symptom": "MySQL Workbench or DBeaver connects but immediately disconnects", "fix": "Check that the server's bind-address allows localhost and that no second MySQL/MariaDB instance is fighting over port 3306."}
 ],
 "costNote": "MySQL Community Server is free under the GPL forever. The paid Enterprise edition is a separate product the course never requires."
})

# ---------------------------------------------------------------- 08 DuckDB
labs.append({
 "id": "IL26-INST-08", "tool": "DuckDB", "category": "database",
 "moduleId": "IL26-M08", "estimatedMinutes": 10,
 "gates": ["IL26-TL-DUCKDB-01"],
 "platforms": {
  "windows": plat([
   "The Python route is fastest: with Python 3.12+ installed run pip install duckdb",
   "For the standalone CLI, open https://duckdb.org/docs/installation/ , download the Windows 64-bit zip, and unzip duckdb.exe somewhere on your PATH (e.g. a folder you add to user PATH).",
   "Verify both with the checkpoints below."
  ]),
  "macos": plat([
   "Python route: pip3 install duckdb",
   "CLI route: brew install duckdb — this gives you the duckdb shell command.",
   "Verify with the checkpoints below."
  ]),
  "linux": plat([
   "Python route: pip install duckdb (use a virtualenv if your distro enforces externally-managed-environment).",
   "CLI route: download the Linux binary from https://duckdb.org/docs/installation/ , unzip, and move duckdb to /usr/local/bin or ~/bin on your PATH.",
   "Verify with the checkpoints below."
  ])
 },
 "checkpoints": [
  {"command": "python3 -c \"import duckdb; print(duckdb.__version__)\"", "expected": "1.x.x (a version number like 1.1.3)", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "pip install duckdb fails to build", "fix": "Use a prebuilt wheel instead of building: upgrade pip first (pip install --upgrade pip) and retry — DuckDB ships wheels for all major platforms, so a build attempt means pip is too old to find them."},
  {"symptom": "duckdb CLI: command not found after unzipping", "fix": "The binary is not on PATH. Either move it to a PATH directory or call it by its full path."},
  {"symptom": "Out of memory on a big CSV read", "fix": "DuckDB is in-process and shares your RAM. Read in chunks, add a LIMIT while exploring, or set PRAGMA memory_limit to a safe value."
  }],
 "costNote": "Free and open source (MIT license) forever. DuckDB is an embedded analytical database — no server, no account, no expiry."
})

# ---------------------------------------------------------------- 09 Tableau Public
labs.append({
 "id": "IL26-INST-09", "tool": "Tableau Public", "category": "bi",
 "moduleId": "IL26-M15", "estimatedMinutes": 20,
 "gates": ["IL26-TL-TABLEAU-PUBLIC-01"],
 "platforms": {
  "windows": plat([
   "Create a free Tableau account at https://public.tableau.com/en-us/s/download if you do not have one (email + password, confirm the verification email).",
   "On the same page, download Tableau Public Desktop for Windows and run the installer with defaults.",
   "Launch Tableau Public and sign in with your new account.",
   "Open a sample: connect to the built-in \"Sample - Superstore\" data source, drag Sales to Columns and Profit to Rows, and confirm a chart renders — you will save workbooks to your public profile in the tool-labs."
  ], "Tableau Public saves ONLY to your public Tableau profile — anything you publish is visible to everyone. Never use real client or employer data here."),
  "macos": plat([
   "Create a free Tableau account at https://public.tableau.com/en-us/s/download (confirm the verification email).",
   "Download Tableau Public Desktop for macOS, open the .dmg, and drag it to Applications.",
   "Launch, sign in, and build the quick Sample - Superstore test chart described above."
  ], "Tableau Public saves ONLY to your public Tableau profile — keep all practice data fictional or public."),
  "linux": unsup("Tableau Public Desktop has no Linux build. Use the Tableau Public web authoring at https://public.tableau.com in a browser to complete the Tableau Public tool-labs, or run the Windows build in a VM.")
 },
 "checkpoints": [
  {"command": "Open Tableau Public > Help > About Tableau", "expected": "Tableau Public, version 2024.x or newer, and you are signed in (your profile name shows in the top bar)", "platforms": ["windows","macos"]}
 ],
 "troubleshoot": [
  {"symptom": "Installer fails with a .NET or WebView2 error on Windows", "fix": "Tableau needs Microsoft Edge WebView2. Install it from Microsoft's WebView2 download page, reboot, and rerun the Tableau installer."},
  {"symptom": "Sign-in loops back to the login screen", "fix": "Clear the app's cached credentials: sign out inside Tableau, close it fully, reopen, and sign in again. Corporate SSO blockers can also interfere — use a personal email account."},
  {"symptom": "Cannot save a workbook locally", "fix": "That is by design in Tableau Public — saving uploads to your public profile. If you need private local files, you need Tableau Desktop (IL26-INST-10)."
  }],
 "costNote": "Free forever. The tradeoff is privacy: every workbook you save is public on the internet. The paid Tableau Desktop/Creator license is not required for this course."
})

# ---------------------------------------------------------------- 10 Tableau Desktop trial
labs.append({
 "id": "IL26-INST-10", "tool": "Tableau Desktop (trial)", "category": "bi",
 "moduleId": "IL26-M03", "estimatedMinutes": 25,
 "gates": ["IL26-TL-TABLEAU-DESKTOP-01"],
 "platforms": {
  "windows": plat([
   "Open https://www.tableau.com/products/desktop/download and start the free trial — you will create a Tableau account with your email.",
   "Download the Windows 64-bit installer and run it with defaults.",
   "Launch Tableau Desktop and activate the trial with your account when prompted (the trial clock starts at activation, so activate only when you are ready to do the Desktop tool-labs).",
   "Connect to Sample - Superstore, build one sheet, and save the .twbx locally to confirm private saving works."
  ], "Do not activate until you are ready to work the Desktop labs — the 14-day clock cannot be paused."),
  "macos": plat([
   "Open https://www.tableau.com/products/desktop/download and start the free trial with your email.",
   "Download the macOS installer (.dmg), drag to Applications, launch, and activate the trial.",
   "Build and locally save one Sample - Superstore sheet to confirm private saving."
  ], "Same warning: activate only when you plan to use it; the trial is 14 days."),
  "linux": unsup("Tableau Desktop has no Linux build. Complete the Desktop tool-labs via Tableau Cloud trial in a browser, or use a Windows/macOS machine or VM.")
 },
 "checkpoints": [
  {"command": "Open Tableau Desktop > Help > About Tableau", "expected": "Tableau Desktop 2024.x or newer, showing trial days remaining", "platforms": ["windows","macos"]}
 ],
 "troubleshoot": [
  {"symptom": "Trial activation says the product key is invalid", "fix": "Trials activate through account sign-in, not a typed key. Make sure you are signing in with the same email you used to start the trial."},
  {"symptom": "Trial expired before you finished the labs", "fix": "Tableau grants one trial per email. The Tableau Public lab (IL26-INST-09) covers most Desktop skills; use Public for remaining practice, keeping data fictional."},
  {"symptom": "Installer blocked by antivirus", "fix": "Temporarily allow the installer in your AV's quarantine list — the official installer from tableau.com is signed. Re-enable protection after install."
  }],
 "costNote": "14-day free trial of Tableau Creator/Desktop. When it expires the app locks until you buy a license; Tableau Public (IL26-INST-09) stays free and covers most visualization skills."
})

# ---------------------------------------------------------------- 11 Tableau Prep Builder trial
labs.append({
 "id": "IL26-INST-11", "tool": "Tableau Prep Builder (trial)", "category": "bi",
 "moduleId": "IL26-M13", "estimatedMinutes": 20,
 "gates": ["IL26-TL-PREP-01"],
 "platforms": {
  "windows": plat([
   "Open https://www.tableau.com/products/prep/download and start the free trial with your email (same account as Desktop if you have one).",
   "Download the Windows 64-bit installer and run it with defaults.",
   "Launch Tableau Prep Builder and activate the trial at the sign-in prompt — again, the clock starts at activation, so time it with the Prep tool-labs.",
   "Open the built-in Superstore sample flow, run it, and confirm the output preview renders."
  ], "Prep Builder and Desktop trials are usually bundled under one Creator trial — activating one may start both clocks."),
  "macos": plat([
   "Open https://www.tableau.com/products/prep/download , start the trial, download the macOS .dmg, and install to Applications.",
   "Launch, activate, and run the sample Superstore flow to confirm."
  ]),
  "linux": unsup("Tableau Prep Builder has no Linux build. Cover the data-prep tool-lab concepts with the browser-based flow authoring in a Tableau Cloud trial, or use a Windows/macOS machine.")
 },
 "checkpoints": [
  {"command": "Open Tableau Prep Builder > Help > About", "expected": "Tableau Prep Builder 2024.x or newer, showing trial days remaining", "platforms": ["windows","macos"]}
 ],
 "troubleshoot": [
  {"symptom": "Flows fail with a Java error on launch", "fix": "Prep bundles its own runtime; a stale TEMP directory or aggressive antivirus usually causes this. Clear %TEMP% (Windows) or /tmp and relaunch."},
  {"symptom": "Cannot connect to a database from a flow", "fix": "Prep needs the same JDBC/ODBC drivers as Desktop. Install the vendor driver (e.g. PostgreSQL JDBC) via the driver download page linked in Prep's connection dialog."}
 ],
 "costNote": "14-day free trial, typically bundled with the Tableau Creator/Desktop trial. After expiry, practice data-prep concepts in Tableau Public or with Python/pandas instead."
})

# ---------------------------------------------------------------- 12 Power BI Desktop
labs.append({
 "id": "IL26-INST-12", "tool": "Power BI Desktop", "category": "bi",
 "moduleId": "IL26-M02", "estimatedMinutes": 25,
 "gates": ["IL26-TL-POWERBI-01"],
 "platforms": {
  "windows": plat([
   "Option A (recommended): open the Microsoft Store app, search \"Power BI Desktop\", and install — the Store version updates itself automatically.",
   "Option B: open https://www.microsoft.com/en-us/download/details.aspx?id=58494 and download the PBIDesktopSetup_x64.exe installer.",
   "Launch Power BI Desktop. Sign in with a Microsoft account (personal or work) to enable publishing; you can also work fully offline without signing in.",
   "Click Get Data > Excel, load any small spreadsheet, and confirm the Data view shows your table — the tool-labs build from there."
  ], "Power BI Desktop itself is free. Publishing to the Power BI service requires a Pro/Premium license, but every course lab runs locally and free."),
  "macos": unsup("Power BI Desktop is Windows-only and Microsoft ships no macOS build. Alternatives: use the Power BI service in a browser at https://app.powerbi.com (import data and build reports there), run Windows in a VM (Parallels/UTM), or use the Microsoft Store version on a Windows machine. The PL-300 tool-labs note which steps differ in the web service."),
  "linux": unsup("Power BI Desktop is Windows-only with no Linux build. Use the Power BI service at https://app.powerbi.com in a browser, or a Windows VM. All data-modeling concepts transfer; only the local file workflow differs.")
 },
 "checkpoints": [
  {"command": "Open Power BI Desktop > File > Help > About", "expected": "Power BI Desktop, version 2.13x.x or newer (monthly releases)", "platforms": ["windows"]}
 ],
 "troubleshoot": [
  {"symptom": "Installer fails with a WebView2 error", "fix": "Install Microsoft Edge WebView2 Runtime from Microsoft's download page, then rerun the Power BI installer."},
  {"symptom": "'We couldn't sign you in' loop", "fix": "You can skip sign-in entirely for local labs — click the X on the sign-in prompt and work offline. Sign-in is only needed to publish to the service."},
  {"symptom": "DAX measure shows an error on refresh", "fix": "This is a formula issue, not an install issue — but first confirm your data loaded: check Data view row counts before debugging the DAX."},
  {"symptom": "macOS/Linux learner cannot follow a Desktop-only step", "fix": "Use the web-service alternative in the platform notes and flag the step in the course forum — the tool-labs mark Desktop-only steps explicitly."
  }],
 "costNote": "Power BI Desktop is free forever. Publishing/sharing via the Power BI service needs a paid Pro license (~$14/user/month) or Premium capacity — the course never requires publishing, so the free Desktop (or web service free tier) is enough."
})

# ---------------------------------------------------------------- 13 Excel + Sheets
labs.append({
 "id": "IL26-INST-13", "tool": "Microsoft Excel (desktop + web) and Google Sheets", "category": "bi",
 "moduleId": "IL26-M16", "estimatedMinutes": 20,
 "gates": ["IL26-TL-EXCEL-01"],
 "platforms": {
  "windows": plat([
   "DESKTOP: if you have Microsoft 365, open Excel from the Start menu and confirm File > Account shows you are licensed. No 365? Install the free Excel mobile/desktop trial from microsoft.com or use Excel for the web below.",
   "WEB: sign in at https://www.microsoft.com/en-us/microsoft-365/free-office-online or office.com with a Microsoft account — Excel for the web is free and covers most course labs.",
   "GOOGLE SHEETS: sign in at sheets.google.com with any Google account — no install needed.",
   "In both, open a blank workbook, type numbers in A1:A5, put =SUM(A1:A5) in A6, and confirm the total calculates."
  ], "Excel for the web lacks Power Query's full desktop features — the M16 tool-labs flag which exercises need desktop Excel."),
  "macos": plat([
   "DESKTOP: install Excel via a Microsoft 365 subscription (App Store or microsoft.com download).",
   "WEB: use Excel for the web at office.com with a free Microsoft account as the no-cost path.",
   "GOOGLE SHEETS: sheets.google.com with any Google account.",
   "Run the same =SUM(A1:A5) smoke test in each."
  ]),
  "linux": plat([
   "There is no Linux desktop Excel. Use Excel for the web at office.com (free Microsoft account) for every Excel exercise.",
   "GOOGLE SHEETS: sheets.google.com — the primary spreadsheet for Linux learners in this course.",
   "Run the =SUM(A1:A5) smoke test in both."
  ], "LibreOffice Calc is a fine offline fallback, but formulas and pivot behavior differ — prefer the web apps for course fidelity.")
 },
 "checkpoints": [
  {"command": "In Excel or Sheets: enter 1..5 in A1:A5 and =SUM(A1:A5) in A6", "expected": "A6 displays 15", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "Excel for the web: Power Query / Get Data options are missing", "fix": "Expected — the web app has a reduced ribbon. The M16 labs mark desktop-only steps; do those on desktop Excel or substitute the Sheets QUERY function where the lab allows."},
  {"symptom": "Formula shows as text instead of calculating", "fix": "The cell is formatted as Text. Change format to General, then re-enter the formula (press F2 then Enter)."},
  {"symptom": "Microsoft 365 trial expired mid-course", "fix": "Fall back to Excel for the web (free) plus Google Sheets — every M16 concept is covered across the two free tools."
  }],
 "costNote": "Google Sheets and Excel for the web are free forever. Desktop Excel requires a Microsoft 365 subscription (or one-time Office license); the course is fully completable on the free web apps."
})

# ---------------------------------------------------------------- 14 R + RStudio
labs.append({
 "id": "IL26-INST-14", "tool": "R and RStudio Desktop", "category": "core",
 "moduleId": "IL26-M25", "estimatedMinutes": 25,
 "gates": ["IL26-TL-R-01"],
 "platforms": {
  "windows": plat([
   "Install R FIRST: open https://cran.r-project.org/ , click Download R for Windows > base > Download R-4.x.x for Windows, and run the installer with defaults.",
   "Then install RStudio: open https://posit.co/download/rstudio-desktop/ , download the Windows installer, and run it with defaults.",
   "Launch RStudio (not RGui). In the Console pane run: install.packages(\"tidyverse\") — accept the offer to install to your personal library, and say yes to compiling if asked.",
   "Verify with the checkpoints below."
  ], "Order matters: RStudio is just an IDE and needs R installed first. The tidyverse install takes several minutes — that is normal."),
  "macos": plat([
   "Install R FIRST: open https://cran.r-project.org/ , click Download R for macOS, and install the .pkg matching your chip (Apple Silicon arm64 vs Intel x86_64).",
   "Then install RStudio from https://posit.co/download/rstudio-desktop/ (matching .dmg) and drag to Applications.",
   "Launch RStudio and run install.packages(\"tidyverse\") in the Console. If a tools popup appears, allow the install.",
   "Verify with the checkpoints below."
  ], "On Apple Silicon Macs, make sure you grabbed the arm64 R build — the Intel build runs but is slower and causes toolchain headaches."),
  "linux": plat([
   "Ubuntu/Debian: sudo apt update && sudo apt install -y r-base r-base-dev",
   "Download the RStudio .deb from https://posit.co/download/rstudio-desktop/ and run sudo apt install ./rstudio-*.deb (installs dependencies automatically).",
   "Fedora/RHEL: sudo dnf install -y R, then install the RStudio .rpm similarly.",
   "Launch rstudio from the terminal or app menu and run install.packages(\"tidyverse\") in the Console."
  ])
 },
 "checkpoints": [
  {"command": "In RStudio Console: R.version.string", "expected": "R version 4.3.x or 4.4.x (any recent 4.x)", "platforms": ["windows","macos","linux"]},
  {"command": "In RStudio Console: library(tidyverse); glimpse(mtcars)", "expected": "A tibble summary of mtcars (32 rows x 11 columns) with no error", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "RStudio opens but says R is not found", "fix": "R is not installed or not on PATH. Install R from CRAN first (this lab's step 1), then restart RStudio."},
  {"symptom": "install.packages fails with 'non-zero exit status' on compilation", "fix": "You are missing build tools. Windows: install Rtools from CRAN. macOS: install Xcode command line tools (xcode-select --install). Linux: install r-base-dev / R-devel."},
  {"symptom": "tidyverse loads but dplyr verbs mask base functions with warnings", "fix": "Normal and harmless — those conflict messages are informational. Your code still works; qualify with dplyr::filter() if you need the dplyr version explicitly."
  }],
 "costNote": "R and RStudio Desktop are free and open source forever. Posit also sells hosted/workbench products you do not need for this course."
})

# ---------------------------------------------------------------- 15 Docker Desktop
labs.append({
 "id": "IL26-INST-15", "tool": "Docker Desktop", "category": "infra",
 "moduleId": "IL26-M13", "estimatedMinutes": 30,
 "gates": ["IL26-TL-DOCKER-01"],
 "platforms": {
  "windows": plat([
   "REQUIRED FIRST: enable virtualization in your BIOS/UEFI and install WSL2. In an admin PowerShell run: wsl --install (reboot when asked), which installs Ubuntu on WSL2 by default.",
   "Open https://www.docker.com/products/docker-desktop/ , download Docker Desktop for Windows (AMD64), and run the installer.",
   "During install keep \"Use WSL 2 instead of Hyper-V\" checked. After install, open Docker Desktop settings > Resources > WSL integration and enable integration with your Ubuntu distro.",
   "Open a NEW terminal and run the checkpoints. The first docker run pulls images and is slow — that is normal."
  ], "Docker Desktop on Windows cannot run without WSL2 or Hyper-V. The WSL2 route is the beginner-safe one."),
  "macos": plat([
   "Open https://www.docker.com/products/docker-desktop/ and download the build matching your chip (Apple Silicon vs Intel).",
   "Open the .dmg, drag Docker to Applications, and launch it. Accept the privileged-helper prompt.",
   "Wait for the whale icon in the menu bar to stop animating (engine started), then run the checkpoints in Terminal."
  ]),
  "linux": plat([
   "Docker Desktop for Linux exists, but the native engine is simpler: follow the official Docker Engine install for your distro (Ubuntu: add Docker's apt repo, then sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin).",
   "Add your user to the docker group: sudo usermod -aG docker $USER, then LOG OUT and back in.",
   "Alternatively install Docker Desktop for Linux from https://www.docker.com/products/docker-desktop/ if you want the GUI.",
   "Run the checkpoints."
  ])
 },
 "checkpoints": [
  {"command": "docker --version", "expected": "Docker version 2x.x.x (any recent version)", "platforms": ["windows","macos","linux"]},
  {"command": "docker run hello-world", "expected": "Hello from Docker! (the hello-world confirmation message)", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "Windows: Docker Desktop stuck on 'Starting...' forever", "fix": "WSL2 is not actually working. Run wsl --status in PowerShell; if WSL2 is missing, run wsl --install and reboot. Also confirm virtualization is enabled in BIOS."},
  {"symptom": "Linux: permission denied on /var/run/docker.sock", "fix": "You skipped the docker group step or have not logged out/in since. Run sudo usermod -aG docker $USER, log out and back in, and retry."},
  {"symptom": "macOS: 'docker: command not found' after installing the app", "fix": "Open Docker Desktop at least once — it installs the CLI symlinks on first launch. Then open a new terminal."},
  {"symptom": "Everything is extremely slow on macOS/Windows", "fix": "File sharing between host and containers is slow. Keep project files inside the Linux filesystem (WSL2 home on Windows) rather than /mnt/c or /Users bind mounts for heavy I/O."
  }],
 "costNote": "Free for personal use, education, and small businesses (under the Docker subscription terms). Large companies need a paid subscription — as an individual learner you are on the free tier."
})

# ---------------------------------------------------------------- 16 dbt Core
labs.append({
 "id": "IL26-INST-16", "tool": "dbt Core (pip)", "category": "infra",
 "moduleId": "IL26-M13", "estimatedMinutes": 20,
 "gates": ["IL26-TL-DBT-01"],
 "platforms": {
  "windows": plat([
   "Finish IL26-INST-01 (Python) and ideally IL26-INST-06 (PostgreSQL) first — dbt needs a database to talk to.",
   "Create a virtualenv: python -m venv ~/dbt-env, then activate it: ~/dbt-env\\Scripts\\activate",
   "Install dbt plus the Postgres adapter: pip install dbt-core dbt-postgres",
   "Scaffold a project: dbt init my_analytics_project (answer the prompts; host localhost, port 5432), then run dbt debug inside the project folder and fix any red checks before continuing."
  ], "Always install dbt in a virtualenv — dbt-core and its adapters pin dependencies aggressively and will fight your global packages."),
  "macos": plat([
   "Finish IL26-INST-01 and IL26-INST-06 first.",
   "Create and activate a virtualenv: python3 -m venv ~/dbt-env && source ~/dbt-env/bin/activate",
   "Run: pip install dbt-core dbt-postgres",
   "Scaffold with dbt init my_analytics_project and validate with dbt debug."
  ]),
  "linux": plat([
   "Finish IL26-INST-01 and IL26-INST-06 first.",
   "Create and activate a virtualenv: python3 -m venv ~/dbt-env && source ~/dbt-env/bin/activate",
   "Run: pip install dbt-core dbt-postgres",
   "Scaffold with dbt init my_analytics_project and validate with dbt debug."
  ], "If pip complains about externally-managed-environment, the virtualenv already solves it — never use --break-system-packages.")
 },
 "checkpoints": [
  {"command": "dbt --version", "expected": "Core: 1.8.x or newer, with plugins: postgres listed", "platforms": ["windows","macos","linux"]},
  {"command": "cd my_analytics_project && dbt debug", "expected": "All checks passed!", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "dbt debug fails: could not connect to database", "fix": "Postgres is not running or your profiles.yml credentials are wrong. Verify psql connects first (IL26-INST-06 checkpoint), then match host/port/user/password in ~/.dbt/profiles.yml."},
  {"symptom": "pip install dbt-core fails with dependency conflicts", "fix": "You installed into global Python alongside other packages. Start fresh: new virtualenv, pip install dbt-core dbt-postgres, nothing else."},
  {"symptom": "'dbt' is not recognized after install", "fix": "Your virtualenv is not activated. Activate it (see platform steps) — the dbt command only exists inside the env."
  }],
 "costNote": "dbt Core is free and open source forever. dbt Cloud (the hosted IDE/scheduler) has a free developer tier; the course uses Core locally so you never need it."
})

# ---------------------------------------------------------------- 17 Airflow
labs.append({
 "id": "IL26-INST-17", "tool": "Apache Airflow (local, via Docker)", "category": "infra",
 "moduleId": "IL26-M13", "estimatedMinutes": 40,
 "gates": ["IL26-TL-AIRFLOW-01"],
 "platforms": {
  "windows": plat([
   "Finish IL26-INST-15 (Docker Desktop) first and confirm docker run hello-world works.",
   "Create a project folder, e.g. C:\\airflow-lab, and inside it download the official docker-compose file: from https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html grab the docker-compose.yaml link and save it into the folder.",
   "In that folder run: docker compose up airflow-init (one-time init), then docker compose up -d",
   "Wait 1-2 minutes, open http://localhost:8080 in a browser, and log in with username airflow / password airflow. Confirm the example DAGs list loads.",
   "Stop with docker compose down when done; your metadata persists in the docker volumes."
  ], "On Windows keep the project folder inside the WSL2 filesystem (\\\\wsl$\\Ubuntu\\home\\...) for acceptable file performance, and give Docker Desktop at least 4 GB RAM in Settings > Resources."),
  "macos": plat([
   "Finish IL26-INST-15 first and confirm docker run hello-world works.",
   "mkdir ~/airflow-lab && cd ~/airflow-lab; download the official docker-compose.yaml from https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html into it.",
   "Run: docker compose up airflow-init, then docker compose up -d",
   "Open http://localhost:8080, log in as airflow/airflow, and confirm the DAG list loads. Stop with docker compose down."
  ]),
  "linux": plat([
   "Finish IL26-INST-15 first (native Docker Engine is fine).",
   "mkdir ~/airflow-lab && cd ~/airflow-lab; download the official docker-compose.yaml from https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html into it.",
   "Run: docker compose up airflow-init, then docker compose up -d",
   "Open http://localhost:8080, log in as airflow/airflow, confirm DAGs load. Stop with docker compose down."
  ], "If port 8080 is taken, edit the ports mapping in docker-compose.yaml (e.g. 8081:8080) before starting.")
 },
 "checkpoints": [
  {"command": "Open http://localhost:8080 and log in (airflow / airflow)", "expected": "The Airflow UI loads showing the example DAGs list", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "airflow-init exits with a permissions error on Linux/macOS", "fix": "The compose file expects your UID. Run echo -e \"AIRFLOW_UID=$(id -u)\" > .env in the project folder, then rerun the init."},
  {"symptom": "localhost:8080 refuses to connect", "fix": "The webserver container is still starting (give it 2 minutes) or it crashed. Check docker compose ps and docker compose logs webserver for the real error."},
  {"symptom": "Docker Desktop runs out of memory and containers keep restarting", "fix": "Raise Docker's memory limit to at least 4 GB (Settings > Resources) and rerun docker compose up -d."},
  {"symptom": "Port 8080 already in use", "fix": "Another service holds it. Change the mapping in docker-compose.yaml to \"8081:8080\" and open http://localhost:8081 instead."
  }],
 "costNote": "Apache Airflow is free and open source forever. This lab runs it locally in Docker — no cloud account, no managed-service bill."
})

# ---------------------------------------------------------------- 18 Snowflake
labs.append({
 "id": "IL26-INST-18", "tool": "Snowflake (30-day trial account)", "category": "cloud",
 "moduleId": "IL26-M14", "estimatedMinutes": 20,
 "gates": ["IL26-TL-SNOWFLAKE-01"],
 "platforms": {
  "windows": plat([
   "Open https://signup.snowflake.com/ and fill in the trial form: name, work-style email, company (your name is fine), country.",
   "Choose the Standard edition, pick a cloud provider/region close to you, and accept the terms.",
   "Confirm the verification email, set your password, and sign in at the account URL Snowflake emails you (bookmark it — it looks like https://<org>-<account>.snowflakecomputing.com).",
   "In a worksheet run: SELECT CURRENT_VERSION(); and confirm a version string returns. Create one warehouse (XS) and one database for the course labs — then SUSPEND the warehouse when idle (auto-suspend set to 5 minutes) so trial credits are not burned."
  ], "Trial credits ($400) burn only while a warehouse runs. Set auto-suspend to 5 minutes on every warehouse and suspend manually when you finish a session."),
  "macos": plat([
   "Same browser-based signup at https://signup.snowflake.com/ — pick Standard edition and a nearby region.",
   "Verify email, set password, bookmark your account URL, and sign in.",
   "Run SELECT CURRENT_VERSION(); in a worksheet, create your XS warehouse + course database, and set auto-suspend to 5 minutes."
  ]),
  "linux": plat([
   "Same browser-based signup at https://signup.snowflake.com/ — pick Standard edition and a nearby region.",
   "Verify email, set password, bookmark your account URL, and sign in.",
   "Run SELECT CURRENT_VERSION(); in a worksheet, create your XS warehouse + course database, and set auto-suspend to 5 minutes."
  ])
 },
 "checkpoints": [
  {"command": "In a Snowflake worksheet: SELECT CURRENT_VERSION();", "expected": "A version string like 8.x.x (one row returned)", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "Verification email never arrives", "fix": "Check spam/junk and wait 10 minutes. Corporate email filters often eat it — a personal Gmail usually works fastest."},
  {"symptom": "Trial credits draining fast", "fix": "A warehouse is running. In the UI go to Admin > Warehouses, suspend everything, and set auto-suspend to 5 minutes on each warehouse."},
  {"symptom": "'Account locked' or login fails after signup", "fix": "You are probably on the wrong account URL. Use the exact URL from Snowflake's welcome email, including the org prefix — bookmark it."
  }],
 "costNote": "30-day free trial with $400 of usage credits. When the trial ends the account is suspended (read-only briefly, then deactivated) — export any course work before day 30. No credit card is required for the trial."
})

# ---------------------------------------------------------------- 19 BigQuery
labs.append({
 "id": "IL26-INST-19", "tool": "Google BigQuery sandbox", "category": "cloud",
 "moduleId": "IL26-M14", "estimatedMinutes": 15,
 "gates": ["IL26-TL-BIGQUERY-01"],
 "platforms": {
  "windows": plat([
   "You need a Google account (any Gmail works). No credit card is required for the sandbox.",
   "Open https://cloud.google.com/bigquery/docs/sandbox and click through to the BigQuery console (console.cloud.google.com/bigquery).",
   "If prompted to create/select a project, create one named e.g. il26-analytics — the sandbox works without enabling billing.",
   "In the console's query editor run: SELECT 1 AS hello; and confirm it returns one row. Then create a dataset named course_data in your project for the labs."
  ], "Sandbox limits: 1 TB of queries/month and 10 GB storage free, tables expire after 60 days, and some features (streaming, DML quotas) are restricted — plenty for the course."),
  "macos": plat([
   "Sign in with any Google account — no credit card needed.",
   "Open the BigQuery console via https://cloud.google.com/bigquery/docs/sandbox, create/select a project (e.g. il26-analytics) without enabling billing.",
   "Run SELECT 1 AS hello; to confirm access, then create the course_data dataset."
  ]),
  "linux": plat([
   "Sign in with any Google account — no credit card needed.",
   "Open the BigQuery console via https://cloud.google.com/bigquery/docs/sandbox, create/select a project (e.g. il26-analytics) without enabling billing.",
   "Run SELECT 1 AS hello; to confirm access, then create the course_data dataset."
  ])
 },
 "checkpoints": [
  {"command": "In the BigQuery console query editor: SELECT 1 AS hello;", "expected": "One row returned with hello = 1", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "Console demands billing be enabled", "fix": "You clicked a feature outside the sandbox (or an old project has billing). Use a fresh project with billing disabled — the sandbox banner should say queries are free within limits."},
  {"symptom": "'Access Denied: Project' on a public dataset", "fix": "Public datasets still bill queries to YOUR project. Make sure your own project (not the public-data project) is selected as the billing/query project."},
  {"symptom": "Tables you made last month are gone", "fix": "Sandbox tables expire after 60 days by design. Re-create them — the course labs use small reproducible datasets for this reason."
  }],
 "costNote": "BigQuery sandbox is free with no credit card: 1 TB of analysis queries per month and 10 GB storage. Tables expire after 60 days. Upgrading to full BigQuery (pay-as-you-go) is optional and never required."
})

# ---------------------------------------------------------------- 20 Databricks
labs.append({
 "id": "IL26-INST-20", "tool": "Databricks Community Edition", "category": "cloud",
 "moduleId": "IL26-M07", "estimatedMinutes": 20,
 "gates": ["IL26-TL-DATABRICKS-01"],
 "platforms": {
  "windows": plat([
   "Open https://www.databricks.com/try-databricks and choose the Community Edition (free) sign-up — not the 14-day full trial unless you want it.",
   "Register with your email, confirm the verification email, and sign in at https://community.cloud.databricks.com (bookmark this).",
   "Create a cluster: Compute > Create — pick the smallest runtime. Community clusters auto-terminate after 2 hours of inactivity.",
   "Create a notebook, attach it to the cluster, and run: spark.range(3).show() — confirm it prints 3 rows."
  ], "Community Edition gives one small cluster at a time and 15 GB of DBFS storage. It is the free-forever tier — do not confuse it with the 14-day paid trial."),
  "macos": plat([
   "Sign up for Community Edition at https://www.databricks.com/try-databricks (choose Community, not the 14-day trial).",
   "Verify email, sign in at https://community.cloud.databricks.com, and bookmark it.",
   "Create the smallest cluster, make a notebook, attach, and run spark.range(3).show() to confirm 3 rows print."
  ]),
  "linux": plat([
   "Sign up for Community Edition at https://www.databricks.com/try-databricks (choose Community, not the 14-day trial).",
   "Verify email, sign in at https://community.cloud.databricks.com, and bookmark it.",
   "Create the smallest cluster, make a notebook, attach, and run spark.range(3).show() to confirm 3 rows print."
  ])
 },
 "checkpoints": [
  {"command": "In a Databricks notebook on your cluster: spark.range(3).show()", "expected": "A 3-row table (id: 0, 1, 2)", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "Cluster is stuck in 'Pending' for many minutes", "fix": "Community Edition shares capacity — pending during peak hours is normal. Wait 10 minutes; if still pending, terminate and recreate."},
  {"symptom": "Notebook says 'detached' and will not run", "fix": "Your cluster auto-terminated after 2 idle hours. Restart it from Compute, wait for Running, then re-attach the notebook."},
  {"symptom": "Signed up but landed in the 14-day paid trial", "fix": "You picked the wrong tile. Community Edition is a separate sign-up at https://www.databricks.com/try-databricks — look for the 'Community Edition' option specifically."
  }],
 "costNote": "Community Edition is free forever: one small cluster, auto-terminates after 2 idle hours, 15 GB storage. The 14-day full-platform trial is separate and converts to paid — the course uses Community Edition only."
})

# ---------------------------------------------------------------- 21 AWS CLI
labs.append({
 "id": "IL26-INST-21", "tool": "AWS CLI and AWS Free Tier account", "category": "cloud",
 "moduleId": "IL26-M06", "estimatedMinutes": 30,
 "gates": ["IL26-TL-AWS-01"],
 "platforms": {
  "windows": plat([
   "ACCOUNT: open https://aws.amazon.com/free/ and create the account — you WILL need a credit card for identity verification (it is not charged by the Free Tier itself). Use a strong root password and enable MFA on the root user immediately.",
   "CLI: download the AWS CLI v2 MSI installer from the AWS CLI install page (linked from the free-tier page docs) and run it with defaults.",
   "In IAM, create an admin IAM user (never use root day-to-day), attach AdministratorAccess, and create an access key for it.",
   "In a NEW terminal run: aws configure — paste the access key ID, secret key, your region (e.g. us-east-1), and output format json. Then run the checkpoint."
  ], "Set a billing alarm on day one: Billing > Budgets > Create budget ($5) with an email alert — the Free Tier has limits and overages bill real money."),
  "macos": plat([
   "ACCOUNT: create at https://aws.amazon.com/free/ (credit card required for verification), enable MFA on root, and set a $5 billing-alarm budget.",
   "CLI: install via the official .pkg from the AWS CLI install docs, or run: brew install awscli",
   "Create the admin IAM user + access key in the console, then run aws configure with key, region (e.g. us-east-1), and json output."
  ]),
  "linux": plat([
   "ACCOUNT: create at https://aws.amazon.com/free/ (credit card required for verification), enable MFA on root, and set a $5 billing-alarm budget.",
   "CLI: download the v2 bundle: curl the awscli-exe-linux-x86_64.zip from the AWS CLI install docs, unzip, and run sudo ./aws/install",
   "Create the admin IAM user + access key, then run aws configure."
  ])
 },
 "checkpoints": [
  {"command": "aws --version", "expected": "aws-cli/2.x.x ... (a v2 version string)", "platforms": ["windows","macos","linux"]},
  {"command": "aws sts get-caller-identity", "expected": "JSON with your UserId, Account, and Arn (proves the key works)", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "'aws' is not recognized after installing the MSI", "fix": "Open a NEW terminal — the MSI updates PATH only for new sessions. If still missing, the default install path is C:\\Program Files\\Amazon\\AWSCLIV2."},
  {"symptom": "aws sts get-caller-identity: InvalidClientTokenId", "fix": "Your access key is wrong or inactive. Regenerate the key in IAM for the same user and rerun aws configure."},
  {"symptom": "Unexpected charges on the Free Tier", "fix": "Check Billing > Bills for the service, terminate the resource, and confirm your budget alarm exists. Common culprits: NAT gateways, forgotten EC2/RDS instances, and data transfer."
  }],
 "costNote": "AWS Free Tier: 12 months of limited EC2/RDS/S3 plus always-free allowances — but a credit card is REQUIRED and overages bill real money. Set the $5 billing alarm in this lab; the course stays inside free-tier limits."
})

# ---------------------------------------------------------------- 22 Azure CLI
labs.append({
 "id": "IL26-INST-22", "tool": "Azure CLI and Azure free account", "category": "cloud",
 "moduleId": "IL26-M14", "estimatedMinutes": 30,
 "gates": ["IL26-TL-AZURE-01"],
 "platforms": {
  "windows": plat([
   "ACCOUNT: open https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account and create the free account — credit card required for verification, $200 credit for the first 30 days.",
   "CLI: download the Azure CLI MSI installer from Microsoft's install docs and run it with defaults.",
   "In a NEW terminal run: az login — a browser window opens; sign in with the same Microsoft account.",
   "Run the checkpoints to confirm the subscription is visible."
  ], "The $200 credit expires after 30 days regardless of use. After that, only the 12-month + always-free services remain — track spend in Cost Management."),
  "macos": plat([
   "ACCOUNT: create the free account at https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account (card required for verification, $200/30-day credit).",
   "CLI: brew install azure-cli (or the .pkg from Microsoft's install docs).",
   "Run az login in Terminal, complete the browser sign-in, and run the checkpoints."
  ]),
  "linux": plat([
   "ACCOUNT: create the free account at https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account (card required for verification, $200/30-day credit).",
   "CLI: Ubuntu/Debian — add Microsoft's apt repo per the install docs, then sudo apt install -y azure-cli. (Or: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash)",
   "Run az login, complete the browser sign-in, and run the checkpoints."
  ])
 },
 "checkpoints": [
  {"command": "az version", "expected": "JSON including \"azure-cli\": \"2.6x.x\" (any recent 2.x)", "platforms": ["windows","macos","linux"]},
  {"command": "az account list --output table", "expected": "A table row showing your subscription name and state Enabled", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "az login opens the browser but never completes", "fix": "Use device-code flow instead: az login --use-device-code, then enter the shown code at microsoft.com/devicelogin in any browser."},
  {"symptom": "'az' is not recognized after MSI install", "fix": "Open a new terminal. The MSI installs to C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin — verify that folder is on PATH."},
  {"symptom": "Free credit burned in days", "fix": "You deployed something pricey (VMs, databases). Delete the resource group containing the experiment and set a budget alert in Cost Management."
  }],
 "costNote": "$200 credit for the first 30 days + 12 months of limited free services + always-free allowances; credit card required. After day 30 the credit vanishes — the course labs fit in the always-free tier."
})

# ---------------------------------------------------------------- 23 GCP SDK
labs.append({
 "id": "IL26-INST-23", "tool": "Google Cloud SDK (gcloud CLI) and GCP free tier", "category": "cloud",
 "moduleId": "IL26-M14", "estimatedMinutes": 25,
 "gates": ["IL26-TL-GCP-01"],
 "platforms": {
  "windows": plat([
   "ACCOUNT: open https://cloud.google.com/free and create the account — credit card required for verification, $300 credit for 90 days.",
   "CLI: download the Google Cloud CLI Windows installer from the install docs and run it (it bundles Python).",
   "In a NEW terminal run: gcloud init — sign in via the browser, pick your new project (or create il26-analytics), and set the default region/zone.",
   "Run the checkpoints."
  ], "The $300 credit lasts 90 days. Enable billing alerts in Billing > Budgets so a forgotten BigQuery job or VM cannot surprise you."),
  "macos": plat([
   "ACCOUNT: create at https://cloud.google.com/free (card required for verification, $300/90-day credit).",
   "CLI: download the macOS archive from the install docs, extract, and run ./google-cloud-sdk/install.sh, then restart the shell (or: brew install --cask google-cloud-sdk).",
   "Run gcloud init, sign in via browser, select/create project, set defaults, and run the checkpoints."
  ]),
  "linux": plat([
   "ACCOUNT: create at https://cloud.google.com/free (card required for verification, $300/90-day credit).",
   "CLI: Ubuntu/Debian — add Google's apt repo per the install docs, then sudo apt install -y google-cloud-cli. Or download the tarball and run ./google-cloud-sdk/install.sh.",
   "Run gcloud init, sign in via browser, select/create project, set defaults, and run the checkpoints."
  ])
 },
 "checkpoints": [
  {"command": "gcloud --version", "expected": "Google Cloud SDK 4xx.x.x with bq/gcloud/gsutil component lines", "platforms": ["windows","macos","linux"]},
  {"command": "gcloud projects list", "expected": "A table listing your project (e.g. il26-analytics) with its project ID", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "gcloud init: browser sign-in hangs", "fix": "Copy the URL it prints into a different browser manually, or rerun with gcloud init --no-browser and paste the code back."},
  {"symptom": "'gcloud' not found after install.sh", "fix": "The installer edits your shell rc file — open a brand-new terminal (or run exec $SHELL) so the PATH change loads."},
  {"symptom": "bq commands say billing must be enabled", "fix": "Some BigQuery features need billing on the project. The sandbox lab (IL26-INST-19) covers the no-billing path; enable billing only if a specific lab requires it, with a budget alert set."
  }],
 "costNote": "$300 credit for 90 days + always-free allowances; credit card required for verification. The course's BigQuery work fits the always-free tier, so the credit is a safety net, not a requirement."
})

# ---------------------------------------------------------------- 24 Streamlit
labs.append({
 "id": "IL26-INST-24", "tool": "Streamlit (pip)", "category": "core",
 "moduleId": "IL26-M18", "estimatedMinutes": 15,
 "gates": ["IL26-TL-STREAMLIT-01"],
 "platforms": {
  "windows": plat([
   "Finish IL26-INST-01 (Python) first.",
   "In a terminal run: pip install streamlit",
   "Smoke-test it: create app.py containing: import streamlit as st  (newline)  st.write(\"Hello, analyst\") — then run: streamlit run app.py",
   "Your browser should open to http://localhost:8501 showing \"Hello, analyst\". Stop with Ctrl+C."
  ]),
  "macos": plat([
   "Finish IL26-INST-01 first.",
   "Run: pip3 install streamlit",
   "Create the two-line app.py, run streamlit run app.py, and confirm the greeting renders at http://localhost:8501. Stop with Ctrl+C."
  ]),
  "linux": plat([
   "Finish IL26-INST-01 first (use a virtualenv if your distro enforces externally-managed-environment).",
   "Run: pip install streamlit",
   "Create app.py, run streamlit run app.py, confirm http://localhost:8501 shows the greeting. Stop with Ctrl+C."
  ])
 },
 "checkpoints": [
  {"command": "streamlit --version", "expected": "Streamlit, version 1.3x.x (any recent 1.x)", "platforms": ["windows","macos","linux"]},
  {"command": "streamlit hello", "expected": "Launches the demo app in your browser at http://localhost:8501", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "'streamlit' is not recognized after pip install", "fix": "Scripts dir not on PATH — same fix as the Jupyter lab: add %APPDATA%\\Python\\Python312\\Scripts (Windows) or ~/.local/bin (macOS/Linux) to PATH."},
  {"symptom": "Browser shows a blank page at localhost:8501", "fix": "An ad-blocker or corporate proxy is interfering. Try an incognito window, or run streamlit run app.py --server.headless true and open the Network URL it prints."},
  {"symptom": "Port 8501 already in use", "fix": "Run streamlit run app.py --server.port 8502 and open http://localhost:8502 instead."
  }],
 "costNote": "Streamlit's open-source library is free forever and runs locally. Streamlit Community Cloud (hosting) is free for public apps; the course deploys locally only."
})

# ---------------------------------------------------------------- 25 PowerPoint
labs.append({
 "id": "IL26-INST-25", "tool": "PowerPoint for data storytelling", "category": "office",
 "moduleId": "IL26-M18", "estimatedMinutes": 15,
 "gates": ["IL26-TL-POWERPOINT-01"],
 "platforms": {
  "windows": plat([
   "DESKTOP: with a Microsoft 365 subscription, open PowerPoint from the Start menu and confirm File > Account shows a licensed product.",
   "FREE: sign in at office.com with a Microsoft account and open PowerPoint for the web — free and sufficient for every M18 storytelling lab.",
   "Create a blank deck, insert one chart (Insert > Chart > Clustered Column), and confirm the linked Excel data sheet opens — this is the workflow the labs use."
  ], "PowerPoint for the web cannot run VBA macros or some Designer features — the M18 labs avoid both."),
  "macos": plat([
   "DESKTOP: install PowerPoint via Microsoft 365 (App Store or microsoft.com).",
   "FREE: PowerPoint for the web at office.com with a Microsoft account.",
   "Build the one-chart smoke test above to confirm the chart data-sheet workflow."
  ]),
  "linux": plat([
   "No Linux desktop build — use PowerPoint for the web at office.com (free Microsoft account) for all M18 decks.",
   "Build the one-chart smoke test in the web app."
  ], "LibreOffice Impress can open .pptx in a pinch, but chart formatting shifts — submit course decks from the web app.")
 },
 "checkpoints": [
  {"command": "Create a blank presentation, Insert > Chart > Clustered Column", "expected": "A chart appears with its editable data sheet open", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "PowerPoint desktop says 'unlicensed product'", "fix": "Sign in under File > Account with the Microsoft account holding your 365 subscription, or switch to the free web app at office.com."},
  {"symptom": "Charts paste as static images from Excel", "fix": "Use Paste Special > Microsoft Excel Chart Object (linked) instead of plain paste, so the chart stays editable and refreshable."},
  {"symptom": "Fonts shift when opening a deck on another machine", "fix": "Embed fonts before sharing: File > Options > Save > Embed fonts in the file. The M18 labs require embedded fonts on submitted decks."
  }],
 "costNote": "PowerPoint for the web is free forever with a Microsoft account. Desktop PowerPoint needs Microsoft 365; Google Slides (free) is an accepted substitute for every M18 lab."
})

# ---------------------------------------------------------------- 26 XML / XPath / XSLT
labs.append({
 "id": "IL26-INST-26", "tool": "XML editors (VS Code XML extension) + XPath/XSLT tooling (Python lxml)", "category": "data",
 "moduleId": "IL26-M09", "estimatedMinutes": 15,
 "gates": ["IL26-TL-XML-01"],
 "platforms": {
  "windows": plat([
   "Finish IL26-INST-03 (VS Code) and IL26-INST-01 (Python) first.",
   "In VS Code open Extensions (Ctrl+Shift+X), search \"XML\" and install \"XML\" by Red Hat (marketplace page: https://marketplace.visualstudio.com/items?itemName=redhat.vscode-xml). It adds validation, formatting, and XPath evaluation.",
   "In a terminal run: pip install lxml",
   "Verify with the checkpoints: the XPath query should return ['Chai', 'Chang'] from the sample XML."
  ], "lxml ships prebuilt wheels on Windows — if pip tries to compile it, upgrade pip first."),
  "macos": plat([
   "Finish IL26-INST-03 and IL26-INST-01 first.",
   "Install the Red Hat XML extension in VS Code (Cmd+Shift+X, search XML).",
   "Run: pip3 install lxml",
   "Run the checkpoint XPath query and confirm the two product names print."
  ]),
  "linux": plat([
   "Finish IL26-INST-03 and IL26-INST-01 first (use a virtualenv if needed).",
   "Install the Red Hat XML extension in VS Code.",
   "Run: pip install lxml — on Linux this may need system libs (sudo apt install libxml2-dev libxslt1-dev) if no wheel is available for your platform.",
   "Run the checkpoint XPath query."
  ])
 },
 "checkpoints": [
  {"command": "python3 -c \"from lxml import etree; d=etree.fromstring(b'<catalog><p><n>Chai</n></p><p><n>Chang</n></p></catalog>'); print(d.xpath('//n/text()'))\"", "expected": "['Chai', 'Chang']", "platforms": ["windows","macos","linux"]}
 ],
 "troubleshoot": [
  {"symptom": "pip install lxml tries to compile and fails", "fix": "Upgrade pip (pip install --upgrade pip) so it finds the prebuilt wheel. On Linux without a wheel, install libxml2-dev and libxslt1-dev system packages first."},
  {"symptom": "VS Code shows no XML validation or formatting", "fix": "You installed a different XML extension. You need \"XML\" by Red Hat specifically — check the publisher name in the Extensions panel."},
  {"symptom": "xpath() returns an empty list on a namespaced document", "fix": "lxml requires namespace prefixes in XPath. Pass namespaces={'ns': 'http://...'} and query //ns:n instead of //n."
  }],
 "costNote": "Free and open source forever (Red Hat XML extension is free; lxml is BSD-licensed). No accounts, no trials."
})

# ---------------------------------------------------------------- assemble
prereqOrder = [
 "IL26-INST-02",  # Git first — everything else gets cloned/versioned
 "IL26-INST-03",  # VS Code — the editor for all code labs
 "IL26-INST-01",  # Python + pip — foundation for Jupyter, dbt, Streamlit, lxml
 "IL26-INST-04",  # Jupyter
 "IL26-INST-24",  # Streamlit
 "IL26-INST-14",  # R + RStudio
 "IL26-INST-26",  # XML tooling (needs VS Code + Python)
 "IL26-INST-05",  # DBeaver
 "IL26-INST-06",  # PostgreSQL
 "IL26-INST-07",  # MySQL
 "IL26-INST-08",  # DuckDB
 "IL26-INST-16",  # dbt Core (needs Python + Postgres)
 "IL26-INST-15",  # Docker Desktop
 "IL26-INST-17",  # Airflow (needs Docker)
 "IL26-INST-12",  # Power BI Desktop
 "IL26-INST-09",  # Tableau Public
 "IL26-INST-10",  # Tableau Desktop trial (activate late — 14-day clock)
 "IL26-INST-11",  # Tableau Prep trial (activate late — 14-day clock)
 "IL26-INST-13",  # Excel/Sheets
 "IL26-INST-25",  # PowerPoint
 "IL26-INST-19",  # BigQuery sandbox (no card needed — do early)
 "IL26-INST-20",  # Databricks Community Edition (free forever)
 "IL26-INST-18",  # Snowflake trial (30-day clock — activate late)
 "IL26-INST-21",  # AWS CLI + Free Tier
 "IL26-INST-22",  # Azure CLI + free account
 "IL26-INST-23",  # GCP SDK + free tier
]

doc = {"prereqOrder": prereqOrder, "installLabs": labs}

with open(OUT + ".tmp", "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)
    f.write("\n")
os.replace(OUT + ".tmp", OUT)

# validate
d = json.load(open(OUT))
assert len(d["installLabs"]) == 26, len(d["installLabs"])
assert len(d["prereqOrder"]) == 26
ids = [l["id"] for l in d["installLabs"]]
assert len(set(ids)) == 26 and set(ids) == set(d["prereqOrder"])
for l in d["installLabs"]:
    for k in ["id","tool","category","moduleId","estimatedMinutes","gates","platforms","checkpoints","troubleshoot","costNote"]:
        assert k in l, (l["id"], k)
    assert len(l["checkpoints"]) >= 1
    assert len(l["troubleshoot"]) >= 2
    assert len(l["gates"]) >= 1
    for c in l["checkpoints"]:
        assert all(k in c for k in ["command","expected","platforms"])
print("OK: 26 labs written and validated ->", OUT)
