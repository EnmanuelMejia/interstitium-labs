"""Batch 15: Linux & Systems PDFs — 18 visual guides."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *
from reportlab.lib.colors import HexColor, white

CAT = "LINUX / SYSTEMS"


def _code(c, x, y, lines, w=468, h=None):
    """Dark terminal-style code block anchored at top y; returns bottom y."""
    lh = 15
    hh = (h if h else 18 + len(lines) * lh)
    yy = y - hh
    c.setFillColor(HexColor("#1A1A2E")); c.roundRect(x, yy, w, hh, 6, fill=1, stroke=0)
    c.setFillColor(HexColor("#06D6A0")); c.setFont(MONO_FONT, 9.5)
    ty = y - 18
    for ln in lines:
        c.drawString(x + 10, ty, ln[:78]); ty -= lh
    return yy


def _table(c, x, y, headers, rows, widths, fs=9.5):
    """Simple striped table anchored at top y; returns bottom y."""
    rh = 23
    total = sum(widths)
    c.setFillColor(ACCENT); c.rect(x, y - rh, total, rh, fill=1, stroke=0)
    c.setFillColor(white); c.setFont(TITLE_FONT, fs)
    cx = x
    for htxt, w in zip(headers, widths):
        c.drawString(cx + 7, y - rh + 8, htxt); cx += w
    yy = y - rh
    c.setFont(BODY_FONT, fs)
    for i, row in enumerate(rows):
        c.setFillColor(BOX_BLUE if i % 2 == 0 else white)
        c.rect(x, yy - rh, total, rh, fill=1, stroke=0)
        c.setFillColor(INK)
        cx = x
        for cell, w in zip(row, widths):
            c.drawString(cx + 7, yy - rh + 8, str(cell)[:42]); cx += w
        yy -= rh
    return yy


def _checklist(c, x, y, items, fs=10.5, gap=22):
    c.setFont(BODY_FONT, fs)
    for it in items:
        c.setFillColor(GREEN); c.circle(x + 5, y - 4, 6, fill=1, stroke=0)
        c.setFillColor(white); c.setFont(TITLE_FONT, 8)
        c.drawCentredString(x + 5, y - 7, "✓")
        c.setFillColor(INK); c.setFont(BODY_FONT, fs)
        c.drawString(x + 18, y - 4, it)
        y -= gap
    return y


# =====================================================================
# 1. Linux Filesystem
# =====================================================================
def pdf_filesystem(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Linux Filesystem\nVisual Guide",
               "FHS hierarchy, inodes, links, mounts,\nand the virtual filesystems /proc and /sys.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "The FHS Hierarchy",
                       "One tree, rooted at /. Everything is a file or a directory.")
    box(c, 246, 500, 120, 44, BOX_PURP, "/", "the root — one tree", font_size=14)
    dirs = [("/bin", "essentials"), ("/etc", "config"), ("/home", "users"),
            ("/var", "changing data"), ("/usr", "programs"), ("/opt", "add-ons"),
            ("/tmp", "temp"), ("/dev", "devices")]
    fills = [BOX_BLUE, BOX_GREEN, BOX_ORANGE, BOX_TEAL, BOX_BLUE, BOX_GREEN, BOX_ORANGE, BOX_TEAL]
    for i, (d, s) in enumerate(dirs):
        xx = 72 + (i % 4) * 120; yy = 400 - (i // 4) * 84
        box(c, xx, yy, 108, 56, fills[i], d, s, font_size=10)
        arrow(c, 306, 500, xx + 54, yy + 56, color=MUTED, width=1)
    note(c, 72, 170, 468, "No drive letters: disks are mounted INTO this single tree. /mnt and /media hold removable mounts.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Inodes: Files Are Just Numbers",
                       "A filename is a label; the inode holds the metadata.")
    box(c, 72, 380, 200, 170, BOX_BLUE, "inode 1048577",
        "mode · owner · size · times · block pointers", font_size=10)
    for i, lbl in enumerate(["data block A", "data block B", "data block C"]):
        box(c, 360, 480 - i * 62, 150, 44, BOX_GREEN, lbl, "4 KiB", font_size=9)
        arrow(c, 272, 465 - i * 0, 360, 502 - i * 62, color=ACCENT, width=1.5)
    box(c, 72, 300, 200, 44, BOX_ORANGE, '"report.pdf"', "directory entry → inode #", font_size=9)
    arrow(c, 172, 344, 172, 380, color=ORANGE, width=2)
    note(c, 72, 190, 468, "ls -i shows the inode number. Deleting a filename removes the DIRECTORY ENTRY; data dies only when the link count hits zero.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Hard Links vs Soft Links",
                       "Same data, different relationships.")
    box(c, 72, 480, 150, 44, BOX_BLUE, "file_a.txt", "hard link", font_size=10)
    box(c, 72, 420, 150, 44, BOX_BLUE, "file_b.txt", "hard link", font_size=10)
    box(c, 280, 430, 150, 70, BOX_GREEN, "inode 42", "link count = 2", font_size=10)
    arrow(c, 222, 502, 280, 480, color=ACCENT, width=2)
    arrow(c, 222, 442, 280, 455, color=ACCENT, width=2)
    box(c, 72, 300, 150, 44, BOX_ORANGE, "link_c", "symlink → file_a.txt", font_size=10)
    box(c, 280, 300, 150, 44, BOX_RED, "dangling", "target deleted → broken", font_size=10)
    arrow(c, 222, 322, 280, 322, color=RED, width=2, label="path, not inode")
    yy = bullet_list(c, 72, 240,
        ["Hard link: another NAME for the same inode. Same filesystem only. Deleting one name is safe.",
         "Symlink: a tiny file holding a PATH. Can cross filesystems, can dangle, has its own inode.",
         "ln file_a file_b (hard)   ·   ln -s file_a link_c (soft)"],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "Mounts: Grafting Disks Onto the Tree",
                       "mount attaches a device at a directory — the mount point.")
    box(c, 72, 480, 150, 52, BOX_TEAL, "/dev/sda1", "→  /  (root)", font_size=10)
    box(c, 246, 480, 150, 52, BOX_TEAL, "/dev/sdb1", "→  /data", font_size=10)
    box(c, 420, 480, 150, 52, BOX_TEAL, "tmpfs", "→  /dev/shm", font_size=10)
    box(c, 186, 360, 240, 60, BOX_BLUE, "/", "one unified tree", font_size=11)
    box(c, 236, 290, 140, 44, BOX_GREEN, "/data", "lives on sdb1", font_size=10)
    arrow(c, 306, 360, 306, 334, color=ACCENT, width=2, label="grafted")
    yy = _code(c, 72, 240, ["$ mount | grep ' /data'", "/dev/sdb1 on /data type ext4 (rw,relatime)",
                             "$ df -h /data   # space per MOUNT, not per dir"])
    note(c, 72, 120, 468, "Bind mounts (--bind) graft one directory onto another — same data, two paths. /etc/fstab makes mounts survive reboot.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "/proc and /sys: The Kernel as Files",
                       "Pseudo-filesystems: reading a file queries the live kernel.")
    box(c, 72, 470, 220, 120, BOX_ORANGE, "/proc", "/proc/1/cmdline · cpuinfo · meminfo", font_size=10)
    box(c, 320, 470, 220, 120, BOX_TEAL, "/sys", "/sys/power/state · /sys/block/sda", font_size=10)
    arrow(c, 292, 530, 320, 530, color=MUTED, width=1.5, label="both virtual")
    yy = _code(c, 72, 430, ["$ cat /proc/cpuinfo | grep 'model name' | head -1",
                             "$ cat /proc/meminfo | head -2",
                             "$ echo mem | sudo tee /sys/power/state   # suspend!"])
    yy = bullet_list(c, 72, yy - 36,
        ["Nothing on disk: these files are generated on read by the kernel.",
         "/proc/<pid>/ exposes every process — cmdline, environ, fd/, status.",
         "/sys exposes devices and tunables; writing a value changes kernel behavior live."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "Putting It Together: Where Things Live",
                       "A quick placement map for daily work.")
    yy = _table(c, 72, y, ["Path", "What goes there", "Backed up?"],
        [["/etc", "System configuration", "YES"],
         ["/home", "User data", "YES"],
         ["/var/log", "Logs", "maybe"],
         ["/var/lib", "App state (DBs)", "YES"],
         ["/tmp, /run", "Ephemeral", "NO"],
         ["/usr", "Programs (read-only-ish)", "reinstallable"],
         ["/opt", "Third-party apps", "reinstallable"]],
        [90, 240, 138], fs=10)
    note(c, 72, 170, 468, "Rule of thumb: separate /home and /var onto their own mounts — a runaway log can't take down the OS.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Linux Filesystem",
        ["One tree rooted at / — disks are grafted on via mounts, never drive letters.",
         "Inodes hold metadata; filenames are just directory entries pointing at inode numbers.",
         "Hard links share an inode (same fs); symlinks store a path and can dangle.",
         "/proc and /sys are live kernel APIs disguised as files — read for insight, write to tune.",
         "Know where things live: /etc config, /var/log logs, /home users, /tmp ephemeral."],
        pg)
    c.save()


# =====================================================================
# 2. Permissions & Ownership
# =====================================================================
def pdf_permissions(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Permissions & Ownership\nVisual Guide",
               "rwx bits, octal math, special bits,\nACLs, and umask — who can do what.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "Reading ls -l: The 9 Permission Bits",
                       "Three triplets: owner, group, others.")
    yy = _code(c, 72, y, ["$ ls -l deploy.sh", "-rwxr-xr-- 1 enmanuel devs 2048 Oct 9 deploy.sh"])
    segs = [("rwx", BOX_GREEN, "owner"), ("r-x", BOX_BLUE, "group"), ("r--", BOX_ORANGE, "other")]
    xx = 72
    for txt, fill, lbl in segs:
        box(c, xx, yy - 90, 150, 56, fill, txt, lbl, font_size=13)
        xx += 158
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, yy - 110, "r = read (4)    w = write (2)    x = execute (1)  —  '-' means denied")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Octal Notation: Bit Math",
                       "Each triplet is one octal digit: add r(4) + w(2) + x(1).")
    yy = _table(c, 72, y, ["Bits", "Octal", "Meaning"],
        [["rwx", "7", "full control"], ["rw-", "6", "read + write"],
         ["r-x", "5", "read + execute"], ["r--", "4", "read only"],
         ["---", "0", "nothing"]], [90, 80, 298], fs=10.5)
    yy = _code(c, 72, yy - 30, ["$ chmod 755 script.sh    # rwxr-xr-x : runnable by all, writable by owner",
                                 "$ chmod 644 notes.txt   # rw-r--r-- : classic data file",
                                 "$ chmod 600 id_rsa      # rw------- : private keys stay private"])
    note(c, 72, 130, 468, "Mnemonic: 7 = do anything, 5 = look but don't touch, 6 = edit but don't run, 0 = locked out.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Ownership: Users and Groups",
                       "Every file has exactly one owner user and one owner group.")
    box(c, 72, 470, 150, 56, BOX_BLUE, "user: enmanuel", "owner", font_size=10)
    box(c, 231, 470, 150, 56, BOX_GREEN, "group: devs", "owner group", font_size=10)
    box(c, 390, 470, 150, 56, BOX_ORANGE, "other", "everyone else", font_size=10)
    arrow(c, 147, 470, 147, 440, color=ACCENT, width=2)
    arrow(c, 306, 470, 306, 440, color=ACCENT, width=2)
    arrow(c, 465, 470, 465, 440, color=ACCENT, width=2)
    box(c, 186, 360, 240, 56, BOX_PURP, "deploy.sh", "-rwxr-xr--", font_size=10)
    yy = _code(c, 72, 320, ["$ chown enmanuel:devs deploy.sh     # change owner and group",
                             "$ chgrp ops report.csv              # group only",
                             "$ chown -R www-data:www-data /srv/www   # recursive"])
    note(c, 72, 150, 468, "Only root (or CAP_CHOWN) can give away ownership. Group membership is the collaboration mechanism — add users to the group, don't chmod 777.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "Special Bits: setuid, setgid, Sticky",
                       "A fourth octal digit for privilege tricks.")
    yy = _table(c, 72, y, ["Bit", "Octal", "Symbol", "Effect"],
        [["setuid", "4", "s in owner-x", "run as the FILE OWNER (passwd)"],
         ["setgid", "2", "s in group-x", "run as file group; dirs: inherit group"],
         ["sticky", "1", "t in other-x", "/tmp: delete only your own files"]],
        [70, 60, 110, 228], fs=10)
    yy = _code(c, 72, yy - 30, ["$ ls -l /usr/bin/passwd", "-rwsr-xr-x 1 root root 68208 ... /usr/bin/passwd",
                                 "$ chmod 4755 prog     # setuid",
                                 "$ chmod 2750 shared/  # setgid dir: new files inherit group",
                                 "$ chmod 1777 /tmp     # sticky"])
    note(c, 72, 130, 468, "setuid root binaries are the classic privilege-escalation target — audit them: find / -perm -4000 2>/dev/null.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "ACLs: Finer Than Owner/Group/Other",
                       "Named users and groups get their own entries.")
    yy = _code(c, 72, y, ["$ setfacl -m u:lahiri:rw project.db",
                           "$ setfacl -m g:auditors:r report.pdf",
                           "$ getfacl project.db",
                           "# file: project.db",
                           "# owner: enmanuel   # group: devs",
                           "user::rw-   user:lahiri:rw-   group::r--   mask::rw-   other::---"])
    yy = bullet_list(c, 72, yy - 36,
        ["Use ACLs when one file needs exceptions beyond a single group — don't spawn groups for one-offs.",
         "The mask caps every named entry: chmod g-x can silently tighten ACLs. Check getfacl after chmod.",
         "Default ACLs on a directory auto-apply to new children: setfacl -d -m u:lahiri:rw dir/."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "umask: Default Permissions for New Files",
                       "umask SUBTRACTS from the max: 777 for dirs, 666 for files.")
    box(c, 72, 470, 130, 56, BOX_BLUE, "base 777", "directories", font_size=11)
    box(c, 222, 470, 130, 56, BOX_RED, "− umask 022", "subtract", font_size=11)
    box(c, 372, 470, 130, 56, BOX_GREEN, "= 755", "rwxr-xr-x", font_size=11)
    arrow(c, 202, 498, 222, 498, color=ACCENT, width=2)
    arrow(c, 352, 498, 372, 498, color=ACCENT, width=2)
    box(c, 72, 380, 130, 56, BOX_BLUE, "base 666", "files", font_size=11)
    box(c, 222, 380, 130, 56, BOX_RED, "− umask 022", "subtract", font_size=11)
    box(c, 372, 380, 130, 56, BOX_GREEN, "= 644", "rw-r--r--", font_size=11)
    arrow(c, 202, 408, 222, 408, color=ACCENT, width=2)
    arrow(c, 352, 408, 372, 408, color=ACCENT, width=2)
    yy = _code(c, 72, 340, ["$ umask        # 0022", "$ umask 027    # stricter: new files 640, new dirs 750"])
    note(c, 72, 150, 468, "Files never get +x from umask math (base is 666) — executability must be granted explicitly with chmod +x.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Permissions & Ownership",
        ["Nine bits in three triplets (owner/group/other); octal adds r=4, w=2, x=1 per triplet.",
         "Every file has one user owner and one group owner — groups are the collaboration tool.",
         "Special bits: setuid (run as owner), setgid (run as group / inherit group), sticky (own-files-only delete).",
         "ACLs grant per-user/per-group exceptions; watch the mask after chmod.",
         "umask subtracts from 777/666 defaults — new files are never born executable."],
        pg)
    c.save()


# =====================================================================
# 3. Processes
# =====================================================================
def pdf_processes(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Linux Processes\nVisual Guide",
               "fork/exec, process states, signals,\nnice values, and zombies.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "fork() + exec(): How Processes Are Born",
                       "Clone yourself, then become someone else.")
    box(c, 72, 460, 180, 64, BOX_BLUE, "parent (PID 100)", "running bash", font_size=10)
    box(c, 366, 460, 174, 64, BOX_GREEN, "child (PID 101)", "exact copy", font_size=10)
    arrow(c, 252, 492, 366, 492, color=ACCENT, width=2.5, label="fork()")
    box(c, 366, 340, 174, 64, BOX_ORANGE, "PID 101 → nginx", "new program image", font_size=10)
    arrow(c, 453, 460, 453, 404, color=ORANGE, width=2.5, label="exec()")
    yy = bullet_list(c, 72, 300,
        ["fork() duplicates the parent: same memory, same file descriptors, new PID.",
         "exec() replaces the child's memory with a new program — PID stays the same.",
         "The shell does fork+exec for every command you run. Daemons double-fork to detach."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Process States: R S D T Z",
                       "What the STAT column in ps really means.")
    states = [("R", BOX_GREEN, "running/\nrunnable"), ("S", BOX_BLUE, "sleeping\n(interruptible)"),
              ("D", BOX_ORANGE, "uninterruptible\n(disk I/O)"), ("T", BOX_PURP, "stopped\n(Ctrl+Z)"),
              ("Z", BOX_RED, "zombie\n(dead, unreaped)")]
    for i, (s, fill, lbl) in enumerate(states):
        xx = 72 + i * 100
        box(c, xx, 480, 88, 64, fill, s, lbl.split("\n")[0], font_size=13)
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 8)
        for j, ln in enumerate(lbl.split("\n")[1:]):
            c.drawCentredString(xx + 44, 462 - j * 11, ln)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "running → sleep (waits) → wake → running …   stop (T) → continue → running")
    c.drawString(72, 398, "exit → ZOMBIE until parent calls wait() → truly gone")
    note(c, 72, 250, 468, "D state can't be killed — not even SIGKILL. It's stuck in a kernel syscall (usually storage). Z is already dead: it holds only an exit code, waiting for its parent to collect it.")
    yy = _code(c, 72, 210, ["$ ps -eo pid,stat,comm | head", "  PID STAT COMMAND", "    1 Ss   systemd", "  842 Z    [worker] <defunct>"])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Signals: Messages to Processes",
                       "kill doesn't kill — it SENDS A SIGNAL. Default is TERM.")
    yy = _table(c, 72, y, ["Signal", "#", "Default action"],
        [["SIGTERM", "15", "polite ask to exit (catchable)"],
         ["SIGKILL", "9", "instant death, uncatchable"],
         ["SIGHUP", "1", "hangup → daemons reload config"],
         ["SIGINT", "2", "Ctrl+C"],
         ["SIGSTOP", "19", "pause (uncatchable)"],
         ["SIGCONT", "18", "resume"],
         ["SIGUSR1/2", "10/12", "app-defined"]],
        [90, 50, 328], fs=10)
    yy = _code(c, 72, yy - 30, ["$ kill 1234        # SIGTERM — always try this first",
                                 "$ kill -9 1234    # SIGKILL — last resort, no cleanup",
                                 "$ kill -HUP 842   # ask daemon to reload config"])
    note(c, 72, 120, 468, "Escalation ladder: TERM → wait → KILL. Jumping straight to -9 skips cleanup handlers and can corrupt state.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "nice: Who Gets the CPU First",
                       "Niceness −20 (greedy) … 0 … +19 (polite). Only root lowers niceness.")
    for i, (n, lbl) in enumerate([("-20", "hog"), ("0", "default"), ("+19", "yield")]):
        xx = 72 + i * 160
        fill = BOX_RED if i == 0 else (BOX_BLUE if i == 1 else BOX_GREEN)
        box(c, xx, 480, 148, 60, fill, n, lbl, font_size=13)
    arrow(c, 222, 510, 392, 510, color=MUTED, width=2, label="nicer →")
    box(c, 72, 360, 468, 60, BOX_ORANGE, "CFS scheduler", "nice shifts your share of CPU time — it is NOT a hard cap", font_size=10)
    yy = _code(c, 72, 320, ["$ nice -n 10 ./batch-job &     # start polite",
                             "$ renice -n 5 -p 1234        # adjust a running process",
                             "$ chrt --rr 50 ./rt-task    # real-time class (root): beats ALL nice values"])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "Zombies & Orphans",
                       "Dead-but-listed vs parentless-but-adopted.")
    box(c, 72, 470, 180, 60, BOX_RED, "zombie", "exited; parent hasn't wait()ed", font_size=10)
    box(c, 360, 470, 180, 60, BOX_BLUE, "orphan", "parent died; adopted by init/systemd", font_size=10)
    arrow(c, 252, 500, 360, 500, color=MUTED, width=1.5, label="different!")
    yy = bullet_list(c, 72, 420,
        ["Zombies hold no memory — just a PID and exit code. They vanish when the parent reaps them.",
         "A pile of zombies means the PARENT is buggy (not calling wait), not the children.",
         "Cure: fix or restart the parent. Killing zombies is impossible — they're already dead.",
         "Orphans are harmless: PID 1 adopts them and reaps them properly."],
        font_size=10.5, gap=24)
    yy = _code(c, 72, yy - 30, ["$ ps -eo pid,ppid,stat,comm | awk '$3 ~ /Z/'   # find zombies + their parents"])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "Inspecting Processes",
                       "The daily toolkit.")
    yy = _code(c, 72, y, ["$ ps aux --sort=-%cpu | head        # top CPU hogs",
                           "$ ps -ef --forest                  # tree view of parents/children",
                           "$ top   # or htop: interactive, F9 to signal, F6 to sort",
                           "$ pidof nginx  ·  pgrep -af python  # find by name",
                           "$ cat /proc/1234/status            # the raw truth"])
    yy = bullet_list(c, 72, yy - 36,
        ["ps aux: one snapshot. top/htop: live view. Learn htop's F-keys — faster than flags.",
         "/proc/<pid>/ is the source of truth every tool reads: cmdline, environ, fd/, io, status.",
         "Load average 3 numbers = 1/5/15 min run-queue depth; compare against CPU core count."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Linux Processes",
        ["Every process is born from fork() + exec(); PID 1 (systemd) adopts orphans.",
         "States: R running, S sleeping, D unkillable I/O wait, T stopped, Z zombie awaiting reaping.",
         "kill sends signals — escalate TERM → KILL, never start at -9.",
         "nice −20…+19 shifts CPU share; real-time classes beat nice entirely.",
         "Zombies are a parent bug, not a child bug — fix the parent, don't chase the dead."],
        pg)
    c.save()


# =====================================================================
# 4. systemd
# =====================================================================
def pdf_systemd(path):
    c = new_canvas(path); pg = 1
    title_page(c, "systemd\nVisual Guide",
               "Units, dependencies, targets,\ntimers, and journald logging.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "Units: Everything Is a Unit",
                       "Services are just one unit type among many.")
    units = [(".service", BOX_BLUE, "long-running\ndaemon"), (".socket", BOX_GREEN, "socket\nactivation"),
             (".target", BOX_ORANGE, "grouping/\nsync point"), (".timer", BOX_TEAL, "cron\nreplacement"),
             (".mount", BOX_PURP, "/etc/fstab\nentry"), (".path", BOX_RED, "trigger on\nfile change")]
    for i, (u, fill, lbl) in enumerate(units):
        xx = 72 + (i % 3) * 160; yy2 = 470 - (i // 3) * 90
        box(c, xx, yy2, 148, 72, fill, u, lbl.split("\n")[0], font_size=11)
    yy = _code(c, 72, 280, ["[Unit]", "Description=My API", "After=network-online.target", "",
                             "[Service]", "ExecStart=/opt/api/server", "Restart=always", "",
                             "[Install]", "WantedBy=multi-user.target"])
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 108, "A unit file = metadata (Unit) + behavior (Service) + enablement (Install)")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Dependencies: Wants vs Requires",
                       "Ordering (After) is separate from requirement (Wants/Requires).")
    box(c, 72, 460, 180, 60, BOX_BLUE, "app.service", "Wants=db.service", font_size=10)
    box(c, 360, 460, 180, 60, BOX_GREEN, "db.service", "After=db.service", font_size=10)
    arrow(c, 252, 500, 360, 500, color=GREEN, width=2.5, label="Wants: start it, don't fail if it fails")
    box(c, 72, 350, 180, 60, BOX_BLUE, "app.service", "Requires=db.service", font_size=10)
    box(c, 360, 350, 180, 60, BOX_RED, "db.service", "fails → app fails too", font_size=10)
    arrow(c, 252, 380, 360, 380, color=RED, width=2.5, label="Requires: hard dependency")
    note(c, 72, 230, 468, "After= only orders startup — it does NOT pull the other unit in. You need Wants/Requires for that. Forgetting this is the #1 broken-unit cause.")
    yy = _code(c, 72, 190, ["$ systemctl list-dependencies app.service   # see the graph"])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Targets: Boot Milestones",
                       "Targets replaced SysV runlevels — they're just grouping units.")
    box(c, 72, 500, 150, 52, BOX_TEAL, "sysinit.target", "early boot", font_size=10)
    box(c, 231, 500, 150, 52, BOX_BLUE, "basic.target", "sockets/timers", font_size=10)
    box(c, 390, 150, 150, 52, BOX_GREEN, "multi-user.target", "servers (RL3)", font_size=10)
    box(c, 390, 420, 150, 52, BOX_ORANGE, "graphical.target", "desktop (RL5)", font_size=10)
    arrow(c, 222, 526, 231, 526, color=ACCENT, width=2)
    arrow(c, 381, 526, 465, 446, color=ACCENT, width=2)
    arrow(c, 381, 526, 465, 526, color=ACCENT, width=2)
    yy = _table(c, 72, 380, ["SysV runlevel", "systemd target", "Use"],
        [["0", "poweroff.target", "halt"], ["1", "rescue.target", "single user"],
         ["3", "multi-user.target", "server"], ["5", "graphical.target", "desktop"],
         ["6", "reboot.target", "reboot"]], [110, 170, 188], fs=10)
    yy = _code(c, 72, yy - 30, ["$ systemctl get-default          # boot target",
                                 "$ systemctl isolate rescue.target   # drop to single-user live"])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "Timers: cron, but With Dependencies",
                       "A .timer unit triggers a matching .service unit.")
    box(c, 72, 470, 220, 64, BOX_TEAL, "backup.timer", "OnCalendar=daily · Persistent=true", font_size=10)
    box(c, 320, 470, 220, 64, BOX_BLUE, "backup.service", "ExecStart=/opt/backup/run", font_size=10)
    arrow(c, 292, 502, 320, 502, color=TEAL, width=2.5, label="triggers")
    yy = _table(c, 72, 400, ["Timer wins over cron when…", "cron wins when…"],
        [["job must run AFTER network/db is up", "one-liner on any unix"],
         ["you need jitter, accuracy, calendars", "no root/systemd (containers)"],
         ["missed runs must catch up (Persistent)", "you want zero unit files"],
         ["logs must land in the journal", "simplicity beats features"]],
        [234, 234], fs=10)
    yy = _code(c, 72, yy - 30, ["$ systemctl list-timers --all   # what runs when"])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "journald: One Log to Rule Them All",
                       "Structured logging — query by unit, boot, priority, time.")
    yy = _code(c, 72, y, ["$ journalctl -u nginx.service -f        # follow one service",
                           "$ journalctl -p err -b                # errors since this boot",
                           "$ journalctl --since '1 hour ago' -u app",
                           "$ journalctl -o json-pretty -u app | jq .MESSAGE",
                           "$ journalctl --disk-usage             # cap with SystemMaxUse="])
    yy = bullet_list(c, 72, yy - 36,
        ["stdout/stderr of every service is captured automatically — no log files to rotate by hand.",
         "Logs are indexed by _SYSTEMD_UNIT, _PID, PRIORITY: filtering beats grep on text files.",
         "Volatile by default (/run/log/journal); set Storage=persistent to keep across reboots.",
         "Forward to syslog or a shipper (ForwardToSyslog) when you need central aggregation."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "Debugging a Failed Unit",
                       "A repeatable 4-step drill.")
    steps = [("1", BOX_RED, "systemctl status X", "exit code + recent log"),
             ("2", BOX_ORANGE, "journalctl -u X -b", "full story this boot"),
             ("3", BOX_BLUE, "systemd-analyze verify", "unit file syntax"),
             ("4", BOX_GREEN, "run ExecStart by hand", "reproduce outside systemd")]
    xx = 72
    for n, fill, lbl, sub in steps:
        box(c, xx, 470, 108, 72, fill, n + "  " + lbl, sub, font_size=9)
        if xx < 400:
            arrow(c, xx + 108, 506, xx + 120, 506, color=ACCENT, width=2)
        xx += 120
    note(c, 72, 340, 468, "After editing any unit: systemctl daemon-reload — systemd caches unit files and will happily run the stale copy.")
    yy = _code(c, 72, 300, ["$ systemctl is-failed '*.service'   # failed units right now",
                             "$ systemctl --failed",
                             "$ systemd-analyze blame | head     # what slowed this boot"])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "systemd",
        ["Units come in types (.service/.socket/.target/.timer/.mount/.path) — learn the family, not just services.",
         "After orders; Wants/Requires pull in. Ordering without requirement is the classic broken unit.",
         "Targets are boot milestones replacing runlevels; isolate rescue.target to debug.",
         "Timers beat cron when jobs need dependencies, catch-up, or journal logging.",
         "journalctl queries structured logs by unit/boot/priority — status, journal, verify, reproduce."],
        pg)
    c.save()


# =====================================================================
# 5. Linux Networking Commands
# =====================================================================
def pdf_net_commands(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Linux Networking Commands\nVisual Guide",
               "An ip / ss / tcpdump / dig workflow\nfor diagnosing connectivity, step by step.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "The Diagnostic Ladder",
                       "Always climb bottom-up: local config → route → peer → ports → DNS → packets.")
    ladder = [("ip addr", BOX_BLUE, "do I have an address?"),
              ("ip route", BOX_TEAL, "where do packets go?"),
              ("ping", BOX_GREEN, "is the peer reachable?"),
              ("ss -tlnp", BOX_ORANGE, "is anything listening?"),
              ("dig", BOX_PURP, "does the name resolve?"),
              ("tcpdump", BOX_RED, "what's actually on the wire?")]
    yy2 = 560
    for lbl, fill, sub in ladder:
        box(c, 186, yy2 - 56, 240, 52, fill, lbl, sub, font_size=10)
        if yy2 < 560:
            arrow(c, 306, yy2, 306, yy2 + 4, color=MUTED, width=1.5)
        # draw arrow upward between boxes
        yy2 -= 62
    # redraw arrows properly between consecutive boxes
    note(c, 72, 120, 468, "Skipping rungs wastes hours: checking DNS before confirming you have an IP is the classic trap. Each rung eliminates a whole layer.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "ip: Addresses, Links, Routes",
                       "The modern replacement for ifconfig / route / arp.")
    yy = _code(c, 72, y, ["$ ip -brief addr            # addresses at a glance",
                           "$ ip route show default    # where outbound traffic goes",
                           "$ ip neigh                 # ARP table: IP ↔ MAC",
                           "$ ip -s link               # interface counters + errors",
                           "$ sudo ip addr add 10.0.0.5/24 dev eth0   # temporary"])
    yy = bullet_list(c, 72, yy - 36,
        ["No address on the interface? Nothing above this rung can work — fix DHCP or static config first.",
         "Missing default route = 'I can ping LAN but not the internet.' Check ip route.",
         "RX/TX errors or drops climbing in ip -s link → suspect cable, duplex, or driver."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "ss: Who's Listening, Who's Connected",
                       "Faster, richer netstat. Memorize -tulnp.")
    yy = _code(c, 72, y, ["$ ss -tlnp            # TCP listening sockets + owning processes",
                           "$ ss -tup state established   # live connections",
                           "$ ss -s               # socket summary counters"])
    yy = _table(c, 72, yy - 30, ["Symptom", "ss tells you", "Meaning"],
        [["connection refused", "nothing LISTEN on that port", "service down / wrong port"],
         ["hangs, no refuse", "SYN-SENT stuck", "firewall dropping, or routing blackhole"],
         ["works locally only", "listens on 127.0.0.1", "bind address too narrow"]],
        [140, 160, 168], fs=10)
    note(c, 72, 150, 468, "Read the flags: t=TCP u=UDP l=listening n=numeric (no DNS lag) p=process. -tlnp is the single most useful networking command on a server.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "dig: Interrogate DNS Directly",
                       "Ask specific servers, follow the delegation chain.")
    box(c, 72, 470, 120, 52, BOX_BLUE, "root", "dig . NS", font_size=10)
    box(c, 212, 470, 120, 52, BOX_GREEN, ".dev TLD", "referral", font_size=10)
    box(c, 352, 470, 150, 52, BOX_ORANGE, "authoritative", "final answer", font_size=10)
    arrow(c, 192, 496, 212, 496, color=ACCENT, width=2)
    arrow(c, 332, 496, 352, 496, color=ACCENT, width=2)
    yy = _code(c, 72, 430, ["$ dig +short example.dev A            # just the answer",
                             "$ dig @8.8.8.8 example.dev          # ask a specific resolver",
                             "$ dig +trace example.dev            # walk the whole chain yourself",
                             "$ dig -x 93.184.216.34             # reverse lookup"])
    note(c, 72, 150, 468, "+trace is the lie detector: it shows every delegation, exposing lame delegations and stale glue your resolver hides.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "tcpdump: Read the Wire",
                       "When tools disagree, capture packets and look.")
    yy = _code(c, 72, y, ["$ sudo tcpdump -i eth0 -n port 443 -c 20",
                           "$ sudo tcpdump -i any 'tcp[tcpflags] & tcp-syn != 0'   # SYNs only",
                           "$ sudo tcpdump -i eth0 host 10.0.0.8 and port 53 -w dns.pcap"])
    yy = bullet_list(c, 72, yy - 36,
        ["-n: skip DNS resolution (faster, no observer effect). -c: stop after N packets.",
         "Filter language (BPF): host, port, net, and/or/not — capture less, see more.",
         "See SYNs with no SYN-ACKs? The far side or a firewall is dropping you. See RSTs? Actively refused.",
         "Save with -w, analyze later in Wireshark — tcpdump for capture, GUI for forensics."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "Putting It Together: 'Can't Reach the App'",
                       "A 90-second triage script.")
    yy = _code(c, 72, y, ["$ ip -brief addr && ip route show default   # 1. local stack sane?",
                           "$ ping -c2 <gateway> && ping -c2 8.8.8.8  # 2. L3 works?",
                           "$ ss -tlnp | grep :8080                   # 3. app listening?",
                           "$ dig +short app.internal                 # 4. name resolves?",
                           "$ curl -sv http://app.internal:8080/      # 5. app answers?",
                           "$ sudo tcpdump -i any port 8080 -c 30     # 6. packets prove it"])
    note(c, 72, 180, 468, "Document each rung's result as you go — 'ping OK, ss shows LISTEN on 127.0.0.1 only' is a diagnosis, not a shrug.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Linux Networking Commands",
        ["Diagnose bottom-up: ip addr → ip route → ping → ss → dig → tcpdump. Never skip rungs.",
         "ss -tlnp replaces netstat — listening sockets plus owning processes in one shot.",
         "dig +trace walks the delegation chain yourself; don't trust a single resolver's word.",
         "tcpdump with BPF filters is the ground truth when tools disagree — capture, then analyze.",
         "Record each rung's verdict; a triage log turns 'it's down' into a diagnosis."],
        pg)
    c.save()


# =====================================================================
# 6. Bash Scripting
# =====================================================================
def pdf_bash(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Bash Scripting\nVisual Guide",
               "Pipes, redirection, expansions, quoting,\nstrict mode, and functions.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "Pipes & Redirection: Plumbing Data",
                       "stdout becomes someone else's stdin; files catch the streams.")
    box(c, 72, 480, 130, 56, BOX_BLUE, "cmd1", "stdout →", font_size=11)
    box(c, 241, 480, 130, 56, BOX_GREEN, "cmd2", "stdin → stdout →", font_size=11)
    box(c, 410, 480, 130, 56, BOX_ORANGE, "cmd3", "> out.txt", font_size=11)
    arrow(c, 202, 508, 241, 508, color=ACCENT, width=2.5, label="|")
    arrow(c, 371, 508, 410, 508, color=ACCENT, width=2.5, label="|")
    yy = _table(c, 72, 420, ["FD", "Name", "Redirect"],
        [["0", "stdin", "< in.txt"],
         ["1", "stdout", "> out.txt  (>> appends)"],
         ["2", "stderr", "2> err.log"],
         ["1+2", "both", "> all.log 2>&1   (order matters!)"]],
        [50, 90, 328], fs=10.5)
    note(c, 72, 150, 468, "2>&1 must come AFTER the file redirect: '> f 2>&1' merges into f; '2>&1 > f' sends stderr to the OLD stdout (the terminal). Order is everything.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Expansions: Bash Rewrites Your Line First",
                       "Seven expansions run before the command executes — in order.")
    exps = [("brace", BOX_BLUE, "{a,b}"), ("tilde", BOX_GREEN, "~/ → home"),
            ("parameter", BOX_ORANGE, "$var ${v:-d}"), ("command", BOX_TEAL, "$(cmd)"),
            ("arithmetic", BOX_PURP, "$((1+2))"), ("word split", BOX_RED, "splits on IFS"),
            ("glob", BOX_BLUE, "*.log")]
    for i, (e, fill, s) in enumerate(exps):
        xx = 72 + (i % 4) * 120; yy2 = 500 - (i // 4) * 84
        w = 108 if i < 4 else 108
        box(c, xx, yy2, w, 60, fill, e, s, font_size=9)
        if i < 6:
            nx = 72 + ((i + 1) % 4) * 120; ny = 500 - ((i + 1) // 4) * 84
            arrow(c, xx + w, yy2 + 30, nx, ny + 30, color=MUTED, width=1.2)
    yy = _code(c, 72, 300, ['files=(/var/log/*.log)     # glob expands NOW, safely into array',
                             'echo "count: ${#files[@]}"',
                             'name=${1:-world}           # default if unset — see step 4'])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Quoting: Three Levels of Protection",
                       "Unquoted → split + glob. Double → expand but don't split. Single → literal.")
    yy = _table(c, 72, y, ["Quoting", "$var", "$(cmd)", "*.log", "Use when"],
        [["none", "expands", "runs", "globs", "you WANT splitting (rare)"],
         ['"double"', "expands", "runs", "literal", "ALMOST ALWAYS — default choice"],
         ["'single'", "literal", "literal", "literal", "regexes, awk, literal dollars"]],
        [80, 70, 70, 70, 178], fs=10)
    yy = _code(c, 72, yy - 30, ['f="my file.txt"; rm "$f"     # quoted: one arg. Unquoted: TWO args!',
                                 "echo '$HOME'  # prints $HOME — single quotes = literal",
                                 'echo "$HOME"  # prints /home/enmanuel'])
    note(c, 72, 130, 468, "Rule: quote every variable expansion unless you can state why it must split. ShellCheck (shellcheck.net) enforces this automatically — run it on every script.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "Strict Mode: set -euo pipefail",
                       "Four switches that turn silent corruption into loud failure.")
    modes = [("-e", BOX_RED, "exit on any\nfailed command"), ("-u", BOX_ORANGE, "exit on use of\nUNSET variable"),
             ("-o pipefail", BOX_TEAL, "pipeline fails if\nANY stage fails"), ("-x*", BOX_PURP, "trace (debug\nonly)")]
    for i, (m, fill, s) in enumerate(modes):
        box(c, 72 + i * 120, 470, 108, 72, fill, m, s.split("\n")[0], font_size=11)
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 8)
        for j, ln in enumerate(s.split("\n")[1:]):
            c.drawCentredString(72 + i * 120 + 54, 452 - j * 11, ln)
    yy = _code(c, 72, 430, ["#!/usr/bin/env bash", "set -euo pipefail",
                             "IFS=$'\\n\\t'",
                             'name=${1:?"usage: $0 <name>"}   # -u friendly required arg'])
    note(c, 72, 180, 468, "Gotchas: -e ignores failures in `if` conditions and `||` fallbacks (by design). grep finding nothing exits 1 — guard it: grep -q x f || true.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "Functions: Named, Testable Blocks",
                       "local keeps variables from leaking; return carries status, echo carries data.")
    yy = _code(c, 72, y, ["backup() {", "  local src=$1 dest=$2          # local: no globals polluted",
                           '  [[ -d $src ]] || { echo "no src" >&2; return 1; }',
                           '  rsync -a "$src/" "$dest/"', "}",
                           'backup /data /backup || die "backup failed"'])
    yy = bullet_list(c, 72, yy - 36,
        ["Functions return an EXIT STATUS (0-255), not strings — print data to stdout, signal with return.",
         "local in every function; quote every parameter. Globals are a bug waiting for a second caller.",
         "die() { echo \"ERROR: $*\" >&2; exit 1; } — one error handler beats twenty inline exits."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "Debugging Toolkit",
                       "See what bash sees.")
    yy = _code(c, 72, y, ["bash -x script.sh            # trace every expansion (noisy, honest)",
                           "set -x / set +x              # trace one section only",
                           "trap 'echo \"failed at line $LINENO\"' ERR",
                           "shellcheck script.sh         # static analysis — catches 90% of bugs",
                           "bash -n script.sh            # syntax check without running"])
    yy = bullet_list(c, 72, yy - 36,
        ["Reproduce with -x first: most 'impossible' bugs are an unexpected expansion.",
         "trap ERR + $LINENO pinpoints the failing line in long scripts.",
         "Put shellcheck in CI — it flags unquoted vars, bad test syntax, and pipefail gaps."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Bash Scripting",
        ["Plumbing: pipes chain stdout→stdin; 2>&1 order matters — redirect the file first.",
         "Seven expansions rewrite each line before execution; quote to control them.",
         "Default to double quotes on every expansion; single quotes for literals.",
         "Start every script with set -euo pipefail — fail loud, fail early.",
         "Functions: local vars, echo for data, return for status; debug with -x and shellcheck."],
        pg)
    c.save()


# =====================================================================
# 7. SSH
# =====================================================================
def pdf_ssh(path):
    c = new_canvas(path); pg = 1
    title_page(c, "SSH\nVisual Guide",
               "Key auth, ssh-agent, tunnels,\nand hardening the daemon.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "Key-Based Auth: The Handshake",
                       "Prove identity with math, never send the secret.")
    box(c, 72, 470, 200, 64, BOX_BLUE, "client", "holds PRIVATE key", font_size=10)
    box(c, 340, 470, 200, 64, BOX_GREEN, "server", "holds PUBLIC key", font_size=10)
    steps = [("1. client offers key id", 420), ("2. server sends challenge", 390),
             ("3. client signs with private key", 360), ("4. server verifies → login", 330)]
    for lbl, yy2 in steps:
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
        c.drawCentredString(306, yy2, lbl)
    arrow(c, 272, 502, 340, 502, color=ACCENT, width=2)
    arrow(c, 340, 488, 272, 488, color=GREEN, width=2)
    yy = _code(c, 72, 290, ["$ ssh-keygen -t ed25519 -C 'laptop'   # modern key type",
                             "$ ssh-copy-id user@host              # install public key",
                             "$ ssh -i ~/.ssh/id_ed25519 user@host"])
    note(c, 72, 120, 468, "The private key NEVER leaves your machine. The server only ever sees signatures. Password auth is the fallback attackers brute-force — disable it (step 5).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "ssh-agent: Unlock Once, Use All Day",
                       "The agent holds decrypted keys in memory; clients ask it to sign.")
    box(c, 72, 470, 150, 60, BOX_TEAL, "ssh-agent", "holds keys\nin RAM", font_size=10)
    box(c, 246, 470, 140, 60, BOX_BLUE, "ssh", "asks agent\nto sign", font_size=10)
    box(c, 410, 470, 130, 60, BOX_GREEN, "scp / git", "same agent", font_size=10)
    arrow(c, 222, 500, 246, 500, color=ACCENT, width=2)
    arrow(c, 386, 500, 410, 500, color=ACCENT, width=2)
    yy = _code(c, 72, 430, ["$ eval $(ssh-agent) && ssh-add ~/.ssh/id_ed25519",
                             "$ ssh-add -l            # keys currently loaded",
                             "$ ssh -A user@jump      # agent FORWARDING — convenient, risky"])
    note(c, 72, 180, 468, "Agent forwarding (-A) lets the jump host use your keys — a compromised jump host can abuse them silently. Prefer ProxyJump instead: ssh -J jump@host target.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Tunnels: -L, -R, -D",
                       "SSH carries arbitrary TCP through the encrypted channel.")
    box(c, 72, 500, 468, 52, BOX_BLUE, "-L 8080:db:5432  (local forward)", "localhost:8080 → server → db:5432", font_size=10)
    box(c, 72, 420, 468, 52, BOX_GREEN, "-R 9090:localhost:3000  (remote forward)", "server:9090 → back through tunnel → your laptop:3000", font_size=10)
    box(c, 72, 340, 468, 52, BOX_ORANGE, "-D 1080  (dynamic / SOCKS)", "a local proxy; traffic exits at the server", font_size=10)
    yy = _code(c, 72, 300, ["$ ssh -L 8080:db.internal:5432 user@bastion    # reach private DB",
                             "$ ssh -R 2222:localhost:22 user@public       # expose laptop SSH outward",
                             "$ ssh -D 1080 user@host                     # SOCKS proxy on :1080"])
    note(c, 72, 120, 468, "Remote forwards punch INBOUND holes — disable on servers you don't control (AllowTcpForwarding no) or attackers will pivot through you.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "~/.ssh/config: Stop Typing Flags",
                       "Name your hosts once; every tool (ssh, scp, git, rsync) inherits it.")
    yy = _code(c, 72, y, ["Host prod", "  HostName 203.0.113.10", "  User deploy",
                           "  IdentityFile ~/.ssh/prod_ed25519", "  Port 2222", "",
                           "Host db", "  HostName db.internal", "  ProxyJump prod",
                           "  LocalForward 5433 localhost:5432"])
    yy = bullet_list(c, 72, yy - 36,
        ["ProxyJump chains bastions cleanly — no manual two-hop ssh, no agent forwarding needed.",
         "Match blocks apply settings per user/host: Match host db User readonly ...",
         "Keep secrets OUT of the config — IdentityFile points at keys, passphrases stay in the agent."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "Hardening sshd",
                       "Defaults are convenient; production wants the strict set.")
    yy = _table(c, 72, y, ["Setting", "Secure value", "Why"],
        [["PermitRootLogin", "no", "root should never log in directly"],
         ["PasswordAuthentication", "no", "keys only — kills brute force"],
         ["PubkeyAuthentication", "yes", "the one allowed method"],
         ["AllowUsers", "deploy", "everyone else rejected early"],
         ["MaxAuthTries", "3", "slow down guessing"],
         ["Port", "2222*", "obscurity only — do it WITH fail2ban"]],
        [150, 120, 198], fs=10)
    yy = _code(c, 72, yy - 30, ["$ sudo apt install fail2ban        # bans IPs after N failures",
                                 "$ sudo systemctl enable --now fail2ban",
                                 "$ sudo sshd -T | grep -i permit   # verify EFFECTIVE config"])
    note(c, 72, 120, 468, "Changing the port stops log noise, not attackers. Real defense = keys-only + fail2ban + updates. Test a NEW session before closing the old one — lockouts are forever.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "Files Over SSH: scp, sftp, rsync",
                       "Same encryption, different ergonomics.")
    yy = _table(c, 72, y, ["Tool", "Best for", "Example"],
        [["scp", "one-off copies", "scp app.tar.gz prod:/opt/"],
         ["sftp", "interactive browsing", "sftp user@host  (like ftp, secure)"],
         ["rsync -az", "syncs, deploys", "rsync -az --delete ./build/ prod:/srv/www/"]],
        [90, 150, 228], fs=10.5)
    yy = bullet_list(c, 72, yy - 36,
        ["rsync -az: a=archive (perms+times), z=compress. --delete mirrors deletions — double-check the trailing slashes.",
         "Trailing slash matters: src/ copies CONTENTS; src copies the DIRECTORY. Get it wrong, get nested dirs.",
         "All three honor ~/.ssh/config — Host nicknames work everywhere."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "SSH",
        ["Key auth proves identity with signatures — the private key never crosses the wire.",
         "ssh-agent unlocks keys once; prefer ProxyJump over agent forwarding through bastions.",
         "-L forwards local→remote, -R remote→local, -D gives a SOCKS proxy; tunnels are TCP only.",
         "~/.ssh/config names hosts once for ssh, scp, rsync, and git alike.",
         "Harden sshd: no root, keys only, AllowUsers, fail2ban — and test a new session before logging out."],
        pg)
    c.save()


# =====================================================================
# 8. Cron & Scheduling
# =====================================================================
def pdf_cron(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Cron & Scheduling\nVisual Guide",
               "Crontab syntax, systemd timers compared,\npitfalls, and logging.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "Crontab Anatomy: Five Fields",
                       "Minute, hour, day-of-month, month, day-of-week — then the command.")
    fields = [("MIN", "0-59", BOX_BLUE), ("HOUR", "0-23", BOX_GREEN),
              ("DOM", "1-31", BOX_ORANGE), ("MON", "1-12", BOX_TEAL), ("DOW", "0-7", BOX_PURP)]
    xx = 72
    for f, r, fill in fields:
        box(c, xx, 470, 88, 64, fill, f, r, font_size=11)
        xx += 96
    box(c, 72, 380, 468, 56, BOX_RED, "command", "/opt/backup/run.sh  >> /var/log/backup.log 2>&1", font_size=10)
    yy = _code(c, 72, 340, ["# m h dom mon dow  command",
                             "30 2 * * *   /opt/backup/run.sh      # 02:30 daily",
                             "*/15 * * * * /opt/metrics/push.sh    # every 15 min",
                             "0 9 * * 1     /opt/reports/weekly.sh # Mondays 09:00"])
    note(c, 72, 130, 468, "DOM and DOW are OR'd, not AND'd: '0 0 1 * 1' runs on the 1st AND every Monday. This surprises everyone once.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Special Strings & Step Values",
                       "Shorthand for the common rhythms.")
    yy = _table(c, 72, y, ["Shorthand", "Equals", "Use"],
        [["@reboot", "run once at boot", "start user agents"],
         ["@daily", "0 0 * * *", "midnight jobs"],
         ["@hourly", "0 * * * *", "hourly sweeps"],
         ["*/10 * * * *", "every 10 min", "pollers"],
         ["0 2-4 * * *", "02:00–04:00 hourly", "nightly window"],
         ["RANDOM*", "systemd only", "see step 5"]],
        [120, 150, 198], fs=10.5)
    yy = _code(c, 72, yy - 30, ["$ crontab -e      # edit YOUR crontab",
                                 "$ crontab -l      # list it",
                                 "$ sudo crontab -e -u appuser   # edit another user's"])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "The Environment Trap",
                       "Cron's environment is nearly empty — your shell's is not.")
    box(c, 72, 470, 220, 64, BOX_GREEN, "your shell", "full PATH, aliases, env", font_size=10)
    box(c, 320, 470, 220, 64, BOX_RED, "cron's shell", "PATH=/usr/bin:/bin, SHELL=/bin/sh", font_size=10)
    arrow(c, 292, 502, 320, 502, color=RED, width=2, label="NOT the same")
    yy = bullet_list(c, 72, 420,
        ["'Works in my shell, fails in cron' is ALWAYS the environment. Use absolute paths everywhere.",
         "Set what you need at the top of the crontab: PATH=..., SHELL=/bin/bash, MAILTO=you@x.",
         "A literal % in the command becomes a NEWLINE (stdin to the command) — escape it: \\%.",
         "Source a profile or env file inside the script itself — don't rely on interactive dotfiles."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "Logging: Cron Is Silent by Default",
                       "No output handling = mailed to you (or lost). Capture it yourself.")
    yy = _code(c, 72, y, ["# GOOD: explicit logs, dated, rotated by logrotate",
                           "30 2 * * * /opt/backup/run.sh >>/var/log/backup.log 2>&1",
                           "# BETTER: also timestamp each run",
                           '30 2 * * * /opt/backup/run.sh 2>&1 | ts >>/var/log/backup.log',
                           "# BEST for systemd users: a timer unit — output lands in the journal"])
    yy = bullet_list(c, 72, yy - 36,
        ["Always redirect BOTH streams (2>&1) — stderr-only failures are invisible otherwise.",
         "MAILTO=alerts@example sets where cron mails output; empty MAILTO disables mail.",
         "Check the cron daemon's own log when jobs never fire: /var/log/cron or journalctl -u cron."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "Cron vs systemd Timers",
                       "Pick by feature need, not fashion.")
    box(c, 72, 440, 220, 72, BOX_ORANGE, "cron", "one-liners · any unix · no deps", font_size=11)
    box(c, 320, 440, 220, 72, BOX_TEAL, "systemd timer", "deps · journal · catch-up · jitter", font_size=11)
    yy = _table(c, 72, 400, ["Need", "Winner"],
        [["run after network/db is up", "timer (After=)"],
         ["catch up missed runs (laptop asleep)", "timer (Persistent=true)"],
         ["randomized start (thundering herd)", "timer (RandomizedDelaySec=)"],
         ["accuracy to the second", "timer (AccuracySec=)"],
         ["five-minute one-liner", "cron"],
         ["works on macOS/BSD", "cron"]],
        [300, 168], fs=10.5)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "When the Job Never Runs: Checklist",
                       "Debug in this order.")
    yy = _checklist(c, 72, y,
        ["Is cron running?  systemctl status cron  (or crond)",
         "Syntax valid?  paste the line into crontab.guru",
         "Absolute paths in the script?  (environment trap)",
         "Executable bit set?  chmod +x the script",
         "% escaped?  MAILTO set?  logs redirected?",
         "Systemd timer instead?  systemctl list-timers --all"])
    note(c, 72, 180, 468, "Add a heartbeat line first: '* * * * * date >> /tmp/cron-alive.log' — if that never appears, the problem is cron itself, not your script.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Cron & Scheduling",
        ["Five fields: minute hour day-of-month month day-of-week — DOM/DOW are OR'd.",
         "Cron's environment is minimal: absolute paths, set PATH/SHELL/MAILTO, escape %.",
         "Redirect both streams to a log; silent cron jobs are undebuggable cron jobs.",
         "Timers win on dependencies, catch-up, jitter, and journal logging; cron wins on simplicity.",
         "Debug checklist: daemon running → syntax → env → perms → escaping → logs."],
        pg)
    c.save()


# =====================================================================
# 9. Package Management
# =====================================================================
def pdf_packages(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Package Management\nVisual Guide",
               "apt/dnf flows, repositories, pinning,\nand source builds vs packages.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "The Install Pipeline",
                       "Update metadata → resolve → fetch → verify → configure.")
    stages = [("update", BOX_BLUE, "refresh\npackage lists"), ("resolve", BOX_TEAL, "solve\ndependencies"),
              ("fetch", BOX_GREEN, "download\n.deb/.rpm"), ("verify", BOX_ORANGE, "GPG\nsignatures"),
              ("install", BOX_PURP, "unpack +\nconfigure")]
    xx = 72
    for s, fill, sub in stages:
        box(c, xx, 480, 84, 72, fill, s, sub.split("\n")[0], font_size=10)
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 8)
        c.drawCentredString(xx + 42, 492, sub.split("\n")[1])
        if xx < 470:
            arrow(c, xx + 84, 516, xx + 96, 516, color=ACCENT, width=2)
        xx += 96
    yy = _code(c, 72, 440, ["$ sudo apt update && sudo apt install nginx     # Debian/Ubuntu",
                             "$ sudo dnf install nginx                      # Fedora/RHEL",
                             "$ apt show nginx / dnf info nginx             # metadata first"])
    note(c, 72, 150, 468, "update ≠ upgrade: update refreshes the CATALOG; upgrade installs newer versions. Running install on a stale catalog is how you get ancient packages.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Repositories & Trust",
                       "Packages come from signed repos — the signature is the security.")
    box(c, 72, 480, 150, 60, BOX_BLUE, "distro repo", "main · vetted", font_size=10)
    box(c, 231, 480, 150, 60, BOX_GREEN, "updates repo", "security fixes", font_size=10)
    box(c, 390, 480, 150, 60, BOX_ORANGE, "third-party", "PPA / COPR", font_size=10)
    box(c, 186, 380, 240, 56, BOX_TEAL, "GPG keyring", "every package verified", font_size=10)
    arrow(c, 147, 480, 260, 436, color=ACCENT, width=1.5)
    arrow(c, 306, 480, 306, 436, color=ACCENT, width=1.5)
    arrow(c, 465, 480, 352, 436, color=ACCENT, width=1.5)
    yy = bullet_list(c, 72, 330,
        ["Each repo ships a GPG key; the package manager refuses unsigned or mis-signed packages.",
         "Third-party repos (PPA/COPR) run as root on install — adding one is a trust decision, not a typing exercise.",
         "Prefer the distro package over a random .deb from a website; prefer the website over curl|bash."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Pinning & Holds: Controlling Versions",
                       "Stop a critical package from upgrading under you.")
    yy = _code(c, 72, y, ["$ sudo apt-mark hold postgresql-15     # apt: freeze it",
                           "$ sudo dnf versionlock add nginx      # dnf: same idea",
                           "$ apt-cache policy nginx              # see candidate versions + pins",
                           "# /etc/apt/preferences.d/pin-nginx",
                           "Package: nginx", "Pin: version 1.24.*", "Pin-Priority: 1001"])
    yy = bullet_list(c, 72, yy - 36,
        ["Hold databases, kernels, and anything with on-disk format changes before major upgrades.",
         "Holds are technical debt with an expiry date — calendar a review, or you run an ancient Postgres forever.",
         "apt-cache policy / dnf list --showduplicates reveal what versions are actually available."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "Building From Source",
                       "The classic dance — and why packages usually win.")
    yy = _code(c, 72, y, ["$ ./configure --prefix=/opt/myapp   # detect system, set options",
                           "$ make -j$(nproc)                  # compile",
                           "$ sudo make install                 # copy into place",
                           "$ sudo checkinstall                # BETTER: builds a .deb/.rpm first!"])
    yy = _table(c, 72, yy - 30, ["", "Package install", "Source build"],
        [["speed", "seconds", "minutes–hours"],
         ["updates", "automatic", "manual rebuild"],
         ["uninstall", "clean", "hope there's uninstall"],
         ["custom flags", "no", "yes"],
         ["audit trail", "manager knows", "invisible"]],
        [110, 179, 179], fs=10.5)
    note(c, 72, 120, 468, "checkinstall is the bridge: it wraps 'make install' into a real package, so the package manager can track and remove it later.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "Dependency Hell, Visualized",
                       "Two apps want two versions of one library.")
    box(c, 72, 470, 150, 56, BOX_BLUE, "app A", "needs lib v1", font_size=10)
    box(c, 390, 470, 150, 56, BOX_GREEN, "app B", "needs lib v2", font_size=10)
    box(c, 231, 370, 150, 56, BOX_RED, "libfoo", "v1 XOR v2 — conflict!", font_size=10)
    arrow(c, 147, 470, 280, 426, color=RED, width=2)
    arrow(c, 465, 470, 332, 426, color=RED, width=2)
    yy = bullet_list(c, 72, 330,
        ["The resolver's job: find ONE set of versions satisfying everyone — or refuse loudly.",
         "Escapes: containers (each app ships its own lib), versioned paths (/opt), static linking.",
         "Never force with --nodeps / --force: you trade a loud error today for a segfault at 3 AM."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "Hygiene: Keep the System Clean",
                       "Small habits that prevent rot.")
    yy = _code(c, 72, y, ["$ sudo apt autoremove && sudo apt autoclean   # drop orphaned deps",
                           "$ dnf autoremove",
                           "$ apt list --upgradable        # what's pending",
                           "$ sudo unattended-upgrades    # auto security patches (servers: yes)"])
    yy = _checklist(c, 72, yy - 36,
        ["Separate security updates (auto) from feature upgrades (planned)",
         "Snapshot or back up before dist-upgrade / major version jumps",
         "Review third-party repos yearly — dead PPAs break updates silently",
         "One package manager per system — don't mix apt, snap, pip, and source"])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Package Management",
        ["update refreshes the catalog; upgrade installs — never confuse the two.",
         "GPG signatures make repos trustworthy; adding a third-party repo is a trust decision.",
         "Pin/hold version-sensitive packages (DBs, kernels) — with a calendar reminder to revisit.",
         "Source builds trade control for maintenance; checkinstall keeps them trackable.",
         "Dependency conflicts are solved by isolation (containers), not --force."],
        pg)
    c.save()


# =====================================================================
# 10. Kernel Basics
# =====================================================================
def pdf_kernel(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Kernel Basics\nVisual Guide",
               "Syscalls, kernel vs userspace,\nmodules, dmesg, and sysctl tuning.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "Two Worlds: Userspace vs Kernel",
                       "Hardware is behind a wall; syscalls are the gate.")
    box(c, 72, 480, 468, 90, BOX_BLUE, "USERSPACE", "your apps · bash · nginx — unprivileged (ring 3)", font_size=11)
    box(c, 72, 340, 468, 90, BOX_RED, "KERNEL", "scheduler · memory · drivers · filesystems — privileged (ring 0)", font_size=11)
    box(c, 72, 250, 468, 60, BOX_PURP, "HARDWARE", "CPU · RAM · disk · NIC", font_size=11)
    arrow(c, 306, 480, 306, 430, color=ACCENT, width=2.5, label="syscall gate")
    arrow(c, 306, 340, 306, 310, color=RED, width=2.5, label="drivers")
    note(c, 72, 150, 468, "A syscall is a controlled trap into the kernel: validated arguments, privileged work, safe return. ~450 syscalls on x86_64 Linux — everything an app does with the outside world goes through them.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Syscalls in Action: strace",
                       "Watch a program talk to the kernel live.")
    yy = _code(c, 72, y, ["$ strace -c ls /tmp          # count syscalls, not just list",
                           "$ strace -e openat,read,write cat /etc/hosts",
                           'openat(AT_FDCWD, "/etc/hosts", O_RDONLY) = 3',
                           "read(3, \"127.0.0.1 localhost\\n\", 131072) = 20",
                           "write(1, \"127.0.0.1 localhost\\n\", 20) = 20"])
    yy = _table(c, 72, yy - 30, ["Syscall", "Does"],
        [["open/openat", "open a file → file descriptor"],
         ["read / write", "move bytes via fd"],
         ["fork / clone", "create process/thread"],
         ["execve", "replace image with a program"],
         ["mmap", "map memory or files"],
         ["socket/connect", "networking"]],
        [130, 338], fs=10.5)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Kernel Modules: Drivers on Demand",
                       "The kernel is modular — drivers load and unload at runtime.")
    box(c, 72, 480, 468, 60, BOX_RED, "kernel core", "always resident: scheduler, mm, VFS", font_size=10)
    box(c, 72, 390, 145, 56, BOX_BLUE, "e1000.ko", "NIC driver", font_size=9)
    box(c, 231, 390, 145, 56, BOX_GREEN, "ext4.ko", "filesystem", font_size=9)
    box(c, 390, 390, 150, 56, BOX_ORANGE, "nvidia.ko", "GPU (DKMS)", font_size=9)
    arrow(c, 150, 390, 150, 420, color=MUTED, width=1.5)
    yy = _code(c, 72, 350, ["$ lsmod | head                 # loaded modules",
                             "$ sudo modprobe e1000        # load one",
                             "$ sudo modprobe -r e1000     # unload",
                             "$ modinfo e1000 | grep -i parm   # its tunables"])
    note(c, 72, 120, 468, "DKMS rebuilds out-of-tree modules (nvidia, zfs) automatically on kernel updates — without it, a kernel upgrade can leave you driverless at boot.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "dmesg: The Kernel's Diary",
                       "Boot messages, driver probes, hardware errors — ring buffer.")
    yy = _code(c, 72, y, ["$ dmesg | head -20            # boot, from the start",
                           "$ dmesg -T | tail -30         # human timestamps, recent",
                           "$ dmesg -l err,warn          # only errors and warnings",
                           "$ dmesg -w                   # follow live (like tail -f)"])
    yy = bullet_list(c, 72, yy - 36,
        ["First suspect for 'new hardware not working': the driver probe lines are here.",
         "OOM killer, segfaults, thermal throttling, disk errors — all announced in dmesg.",
         "Ring buffer is finite: persistent logs live in the journal (journalctl -k)."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "sysctl: Tune the Kernel Live",
                       "/proc/sys is the control panel — sysctl is the safe handle.")
    box(c, 72, 480, 220, 56, BOX_TEAL, "/proc/sys/vm/swappiness", "kernel variable", font_size=9)
    box(c, 320, 480, 220, 56, BOX_BLUE, "sysctl vm.swappiness", "read/write tool", font_size=9)
    arrow(c, 292, 508, 320, 508, color=MUTED, width=1.5, label="same thing")
    yy = _code(c, 72, 430, ["$ sysctl vm.swappiness                       # read",
                             "$ sudo sysctl -w vm.swappiness=10            # write (until reboot)",
                             "$ sudo sysctl -w net.core.somaxconn=4096     # bigger listen backlog",
                             "# persist: /etc/sysctl.d/99-tuning.conf",
                             "vm.swappiness = 10", "net.core.somaxconn = 4096"])
    note(c, 72, 130, 468, "sysctl -w is instant but ephemeral; files in /etc/sysctl.d/ survive reboot. Change ONE knob, measure, then keep or revert — tuning by folklore breaks systems.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "Kernel Versions & Upgrades",
                       "Know what you're running before you tune or debug.")
    yy = _code(c, 72, y, ["$ uname -r              # 6.8.0-52-generic",
                           "$ hostnamectl | grep Kernel",
                           "$ ls /boot/vmlinuz-*   # installed kernels"])
    yy = bullet_list(c, 72, yy - 36,
        ["Versioning: major.minor-patch — distro kernels add their own suffixes and backports.",
         "Keep at least one older kernel installed: if the new one won't boot, GRUB → Advanced → old kernel.",
         "LTS kernels for servers (stability); mainline for new hardware support.",
         "Reboot into the new kernel to actually RUN it — installing without rebooting changes nothing."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Kernel Basics",
        ["Userspace is unprivileged; every hardware/OS action crosses the syscall gate.",
         "strace reveals the syscall conversation — the ultimate 'what is it actually doing'.",
         "Modules load drivers on demand; DKMS keeps out-of-tree drivers alive across upgrades.",
         "dmesg is the kernel's diary: boot, drivers, OOM, hardware errors.",
         "sysctl tunes /proc/sys live; persist in /etc/sysctl.d and change one knob at a time."],
        pg)
    c.save()


# =====================================================================
# 11. cgroups & Namespaces
# =====================================================================
def pdf_cgroups(path):
    c = new_canvas(path); pg = 1
    title_page(c, "cgroups & Namespaces\nVisual Guide",
               "The 7 namespaces, cgroup v2 controllers,\nand how containers use both.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "The 7 Namespaces: What a Process Sees",
                       "Namespaces = isolation of VIEW. Each hides a global resource.")
    ns = [("pid", BOX_BLUE, "own PID 1"), ("net", BOX_GREEN, "own interfaces\n+ iptables"),
          ("mnt", BOX_ORANGE, "own mount\ntable"), ("uts", BOX_TEAL, "own hostname"),
          ("ipc", BOX_PURP, "own shared\nmemory"), ("user", BOX_RED, "own UID\nmapping"),
          ("cgroup", BOX_BLUE, "own cgroup\nview")]
    for i, (n, fill, s) in enumerate(ns):
        xx = 72 + (i % 4) * 120; yy2 = 480 - (i // 4) * 92
        box(c, xx, yy2, 108, 76, fill, n, s.split("\n")[0], font_size=10)
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 8)
        for j, ln in enumerate(s.split("\n")[1:]):
            c.drawCentredString(xx + 54, 508 - j * 11, ln)
    note(c, 72, 230, 468, "A container is just a process with (mostly) all seven namespaces switched on — same kernel, different view of the world.")
    yy = _code(c, 72, 190, ["$ lsns                        # every namespace on the system",
                             "$ sudo unshare --pid --fork --mount-proc bash   # DIY container-ish shell"])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Namespace Demo: unshare",
                       "Create the isolation yourself in one command.")
    yy = _code(c, 72, y, ["$ sudo unshare --pid --fork --mount-proc --net bash",
                           "# inside:", "# ps aux        # you're PID 1, alone in here",
                           "# ip addr       # no interfaces but lo — own net namespace",
                           "# hostname c1; hostname   # own UTS, host unaffected",
                           "# exit          # namespaces die with the last process"])
    yy = bullet_list(c, 72, yy - 36,
        ["unshare is the teaching tool: it proves namespaces are just kernel flags, not magic.",
         "Each flag (--pid, --net, --mnt, --uts, --ipc, --user) flips one namespace.",
         "Container runtimes do exactly this, then add filesystem + cgroup setup around it."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "cgroup v2: The Resource Hierarchy",
                       "cgroups = isolation of RESOURCES. One unified tree at /sys/fs/cgroup.")
    box(c, 216, 500, 180, 48, BOX_PURP, "/", "root cgroup", font_size=10)
    box(c, 72, 410, 150, 48, BOX_BLUE, "system.slice", "services", font_size=9)
    box(c, 231, 410, 150, 48, BOX_GREEN, "user.slice", "sessions", font_size=9)
    box(c, 390, 410, 150, 48, BOX_ORANGE, "app.slice", "your app", font_size=9)
    for xx in [147, 306, 465]:
        arrow(c, 306, 500, xx, 458, color=ACCENT, width=1.5)
    box(c, 390, 320, 150, 48, BOX_RED, "app.slice/web", "leaf: limits live here", font_size=9)
    arrow(c, 465, 410, 465, 368, color=ACCENT, width=1.5)
    yy = _code(c, 72, 280, ["$ systemd-cgls                  # the tree, readable",
                             "$ cat /sys/fs/cgroup/app.slice/web/memory.max",
                             "$ cat /sys/fs/cgroup/app.slice/web/cpu.weight"])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "Controllers: The Knobs",
                       "Each controller caps one resource dimension.")
    yy = _table(c, 72, y, ["Controller", "File", "Does"],
        [["cpu", "cpu.max / cpu.weight", "cap or share CPU time"],
         ["memory", "memory.max", "hard RAM cap → OOM kill inside group"],
         ["io", "io.max", "throttle block device throughput"],
         ["pids", "pids.max", "fork-bomb insurance"],
         ["cpuset", "cpuset.cpus", "pin to specific cores"]],
        [80, 190, 198], fs=10.5)
    yy = _code(c, 72, yy - 30, ["$ sudo mkdir /sys/fs/cgroup/demo",
                                 "$ echo 100M | sudo tee /sys/fs/cgroup/demo/memory.max",
                                 "$ echo $$ | sudo tee /sys/fs/cgroup/demo/cgroup.procs   # join it"])
    note(c, 72, 130, 468, "memory.max is a HARD wall: exceed it and the kernel OOM-kills inside your group. That's the mechanism behind every container memory limit.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "Containers = Namespaces + cgroups",
                       "Two kernel features, one product.")
    box(c, 72, 430, 220, 100, BOX_BLUE, "NAMESPACES", "isolate the VIEW\npid · net · mnt · uts · ipc", font_size=10)
    box(c, 320, 430, 220, 100, BOX_GREEN, "CGROUPS", "isolate RESOURCES\ncpu · memory · io · pids", font_size=10)
    box(c, 186, 300, 240, 72, BOX_ORANGE, "CONTAINER", "namespaces + cgroups\n+ image filesystem", font_size=11)
    arrow(c, 182, 470, 280, 372, color=ACCENT, width=2)
    arrow(c, 430, 470, 340, 372, color=ACCENT, width=2)
    yy = bullet_list(c, 72, 260,
        ["docker run --memory=512m --cpus=2 = cgroup limits; --network/--pid = namespaces.",
         "No virtual hardware, no guest kernel — that's why containers start in milliseconds.",
         "The price: weaker isolation than VMs (shared kernel). Choose per threat model."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "systemd Already Uses cgroups",
                       "Every service you run is already in the hierarchy.")
    yy = _code(c, 72, y, ["# /etc/systemd/system/api.service", "[Service]",
                           "MemoryMax=1G", "CPUQuota=50%", "TasksMax=100", "",
                           "$ systemctl show api.service -p MemoryMax,CPUQuota",
                           "$ systemd-cgtop     # top, but per cgroup"])
    yy = bullet_list(c, 72, yy - 36,
        ["You don't need Docker to get resource limits — systemd unit directives ARE cgroup settings.",
         "MemoryMax/CPUQuota/TasksMax in a unit file: the simplest production guardrail there is.",
         "systemd-cgtop shows which service is eating the machine, grouped properly."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "cgroups & Namespaces",
        ["Namespaces isolate what a process SEES (7 kinds); cgroups limit what it can USE.",
         "One unified cgroup v2 tree at /sys/fs/cgroup; controllers cap cpu, memory, io, pids.",
         "A container = all namespaces on + cgroup limits + an image filesystem. No magic.",
         "systemd puts every service in cgroups already — MemoryMax/CPUQuota are free guardrails.",
         "Weaker isolation than VMs (shared kernel) — match the tool to the threat model."],
        pg)
    c.save()


# =====================================================================
# 12. SELinux
# =====================================================================
def pdf_selinux(path):
    c = new_canvas(path); pg = 1
    title_page(c, "SELinux\nVisual Guide",
               "Security contexts, enforcing vs permissive,\npolicies, and denial troubleshooting.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "Contexts: user:role:type:level",
                       "Every process AND every file carries a label. Policy matches labels.")
    ctx = [("user", BOX_BLUE, "unconfined_u"), ("role", BOX_GREEN, "object_r"),
           ("type", BOX_ORANGE, "httpd_sys_content_t"), ("level", BOX_PURP, "s0")]
    xx = 72
    for lbl, fill, ex in ctx:
        box(c, xx, 470, 108, 64, fill, lbl, ex, font_size=9)
        if xx < 480:
            c.setFillColor(MUTED); c.setFont(TITLE_FONT, 14)
            c.drawString(xx + 108, 500, ":")
        xx += 120
    yy = _code(c, 72, 430, ["$ ls -Z /var/www/html/index.html",
                             "unconfined_u:object_r:httpd_sys_content_t:s0 index.html",
                             "$ ps -Z | grep httpd",
                             "system_u:system_r:httpd_t:s0  1234 ?  httpd"])
    note(c, 72, 150, 468, "The TYPE is what matters 95% of the time (type enforcement). Process type httpd_t may read file type httpd_sys_content_t — only if policy allows that pair.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Modes: Enforcing / Permissive / Disabled",
                       "Same policy, different courage.")
    box(c, 72, 470, 140, 64, BOX_RED, "enforcing", "denies +\nlogs", font_size=10)
    box(c, 231, 470, 140, 64, BOX_ORANGE, "permissive", "allows +\nlogs", font_size=10)
    box(c, 390, 470, 150, 64, BOX_TEAL, "disabled", "no SELinux\nat all", font_size=10)
    yy = _code(c, 72, 430, ["$ getenforce          # Enforcing?",
                             "$ sudo setenforce 0   # → permissive UNTIL REBOOT (debug!)",
                             "$ sudo setenforce 1   # → enforcing",
                             "# permanent: /etc/selinux/config → SELINUX=enforcing"])
    note(c, 72, 180, 468, "The golden debug move: setenforce 0 — if the problem vanishes, it's SELinux. Fix the LABELS or policy, then setenforce 1. Never 'fix' it by leaving it permissive forever.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Policy: Allow Rules Between Types",
                       "Policy = which subject types may do what to which object types.")
    box(c, 72, 460, 180, 60, BOX_BLUE, "httpd_t", "process type", font_size=10)
    box(c, 360, 460, 180, 60, BOX_GREEN, "httpd_sys_content_t", "file type", font_size=10)
    arrow(c, 252, 490, 360, 490, color=GREEN, width=2.5, label="allow … : file { read open }")
    box(c, 72, 350, 180, 60, BOX_BLUE, "httpd_t", "process type", font_size=10)
    box(c, 360, 350, 180, 60, BOX_RED, "shadow_t", "/etc/shadow", font_size=10)
    arrow(c, 252, 380, 360, 380, color=RED, width=2.5, label="no rule → DENIED")
    yy = _code(c, 72, 310, ["$ sesearch --allow -s httpd_t -t httpd_sys_content_t   # show the rule",
                             "$ sesearch --allow -s httpd_t -t shadow_t   # nothing → denied"])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "Fixing Labels & Booleans",
                       "Most 'SELinux broke my app' is a wrong label, not a wrong policy.")
    yy = _code(c, 72, y, ["$ sudo restorecon -Rv /var/www/html     # relabel to policy defaults",
                           "$ sudo semanage fcontext -a -t httpd_sys_content_t '/srv/www(/.*)?'",
                           "$ sudo restorecon -Rv /srv/www         # custom path, permanent rule",
                           "$ getsebool -a | grep httpd",
                           "$ sudo setsebool -P httpd_can_network_connect on   # -P = persistent"])
    yy = bullet_list(c, 72, yy - 36,
        ["Files created in the wrong place inherit the wrong type — mv preserves, cp relabels. Classic trap.",
         "semanage fcontext makes custom paths survive a filesystem relabel; chcon alone does not.",
         "Booleans are policy feature-switches (httpd_can_network_connect, etc.) — check them before writing policy."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "Troubleshooting Denials: The Drill",
                       "audit.log → why → fix. In that order.")
    steps = [("1", BOX_RED, "ausearch -m avc -ts recent", "find the denial"),
             ("2", BOX_ORANGE, "audit2why < audit.log", "explain it"),
             ("3", BOX_BLUE, "audit2allow", "draft a fix"),
             ("4", BOX_GREEN, "semanage / boolean", "apply properly")]
    xx = 72
    for n, fill, lbl, sub in steps:
        box(c, xx, 470, 108, 72, fill, n + " " + lbl.split()[0], sub, font_size=8)
        if xx < 400:
            arrow(c, xx + 108, 506, xx + 120, 506, color=ACCENT, width=2)
        xx += 120
    yy = _code(c, 72, 430, ["$ sudo ausearch -m avc -ts recent | audit2why",
                             "type=AVC ... denied { read } ... httpd_t ... var_log_t",
                             "  Was caused by: missing type enforcement rule —",
                             "  try: restorecon, or setsebool httpd_read_logs"])
    note(c, 72, 150, 468, "audit2allow generates policy — REVIEW it before loading. A generated 'allow everything' module is a hole you wrote yourself. Prefer relabels and booleans first.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "SELinux Survival Rules",
                       "The mindset that keeps it enforcing.")
    yy = _checklist(c, 72, y,
        ["Leave it ENFORCING — permissive is a debug state, not a configuration",
         "setenforce 0 to test, then fix labels/policy, then setenforce 1",
         "restorecon before writing custom policy — 80% of denials are mislabeled files",
         "semanage fcontext for custom paths so relabels stick",
         "Check booleans (getsebool) before inventing new policy",
         "Read audit2allow output like a contract — never load it blind"])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "SELinux",
        ["Everything has a context user:role:type:level — type enforcement decides access.",
         "Enforcing denies+logs; permissive allows+logs — use permissive only to diagnose.",
         "Policy = allow rules between subject types and object types; no rule means denied.",
         "Most breakage is mislabeled files: restorecon, semanage fcontext, booleans — in that order.",
         "Drill: ausearch → audit2why → fix properly; never load audit2allow output blind."],
        pg)
    c.save()


# =====================================================================
# 13. firewalld & nftables
# =====================================================================
def pdf_firewalld(path):
    c = new_canvas(path); pg = 1
    title_page(c, "firewalld & nftables\nVisual Guide",
               "Zones, services vs ports,\nrich rules, and nftables chains.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "Zones: Trust Levels for Interfaces",
                       "Each interface lives in ONE zone; the zone defines the default posture.")
    zones = [("trusted", BOX_GREEN, "allow all"), ("internal", BOX_TEAL, "mostly open"),
             ("dmz", BOX_ORANGE, "public services"), ("public", BOX_RED, "ssh only"),
             ("drop", BOX_PURP, "drop all")]
    for i, (z, fill, s) in enumerate(zones):
        box(c, 72 + i * 96, 470, 88, 64, fill, z, s, font_size=9)
    arrow(c, 72, 445, 540, 445, color=MUTED, width=1.5, label="less trust →")
    yy = _code(c, 72, 410, ["$ sudo firewall-cmd --get-active-zones",
                             "$ sudo firewall-cmd --zone=public --add-interface=eth0 --permanent",
                             "$ sudo firewall-cmd --get-default-zone"])
    note(c, 72, 150, 468, "A laptop on café Wi-Fi belongs in 'public'; the same laptop on the office LAN in 'work'. Zones make the firewall follow the network, not the machine.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Services vs Ports",
                       "Services are named port-sets — self-documenting and safer.")
    box(c, 72, 470, 220, 64, BOX_BLUE, "service: http", "ports 80/tcp · maintained", font_size=10)
    box(c, 320, 470, 220, 64, BOX_ORANGE, "port: 8080/tcp", "raw number · your problem", font_size=10)
    yy = _code(c, 72, 430, ["$ sudo firewall-cmd --zone=public --add-service=http --permanent",
                             "$ sudo firewall-cmd --zone=public --add-port=8080/tcp --permanent",
                             "$ firewall-cmd --get-services | tr ' ' '\\n' | grep -i sql",
                             "$ sudo firewall-cmd --reload"])
    yy = bullet_list(c, 72, yy - 36,
        ["--add-service=http opens whatever the service definition says — if it changes upstream, you inherit it correctly.",
         "--add-port is for YOUR custom apps. Name them in comments or a custom service XML.",
         "List services before inventing ports: most standard things already have a name."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Rich Rules: Surgical Exceptions",
                       "When a service/port is too blunt: match source, log, rate-limit.")
    yy = _code(c, 72, y, ["$ sudo firewall-cmd --zone=public --permanent \\",
                           "  --add-rich-rule='rule family=ipv4 source address=10.0.0.0/8 \\",
                           "  port port=22 protocol=tcp accept'",
                           "$ sudo firewall-cmd --permanent \\",
                           "  --add-rich-rule='rule service name=ssh log prefix=\"ssh: \" \\",
                           "  limit value=\"5/m\" accept'"])
    yy = bullet_list(c, 72, yy - 36,
        ["Anatomy: rule [family] [source] [destination] [service|port|protocol] [log] [limit] [accept|reject|drop].",
         "accept vs reject vs drop: reject sends ICMP 'refused' (fast fail); drop is silent (stealth, slow timeouts).",
         "Rich rules beat opening SSH to the world — scope management ports to your IP ranges."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "Runtime vs Permanent: Two Layers",
                       "Runtime is live-but-forgotten; permanent survives reboot.")
    box(c, 72, 470, 220, 64, BOX_ORANGE, "runtime", "active NOW\nlost on reload", font_size=10)
    box(c, 320, 470, 220, 64, BOX_BLUE, "permanent", "stored config\nneeds --reload", font_size=10)
    arrow(c, 292, 502, 320, 502, color=ACCENT, width=2, label="--reload applies →")
    yy = _code(c, 72, 430, ["$ sudo firewall-cmd --add-service=http            # runtime only (test!)",
                             "$ sudo firewall-cmd --runtime-to-permanent       # keep what worked",
                             "$ sudo firewall-cmd --reload                    # apply permanent set"])
    note(c, 72, 150, 468, "Workflow: test in runtime, verify the app works, THEN --runtime-to-permanent. A bad --permanent --reload over SSH can lock you out with no undo.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "Under the Hood: nftables",
                       "firewalld is the friendly face; nftables is the engine.")
    box(c, 216, 500, 180, 48, BOX_PURP, "table inet filter", "one table", font_size=10)
    box(c, 72, 410, 140, 48, BOX_BLUE, "chain INPUT", "to this host", font_size=9)
    box(c, 236, 410, 140, 48, BOX_GREEN, "chain FORWARD", "through host", font_size=9)
    box(c, 400, 410, 140, 48, BOX_ORANGE, "chain OUTPUT", "from host", font_size=9)
    for xx in [142, 306, 470]:
        arrow(c, 306, 500, xx, 458, color=ACCENT, width=1.5)
    box(c, 72, 320, 468, 48, BOX_RED, "rules: match → verdict", "ip saddr 10.0.0.0/8 tcp dport 22 accept", font_size=9)
    arrow(c, 306, 410, 306, 368, color=MUTED, width=1.5)
    yy = _code(c, 72, 280, ["$ sudo nft list ruleset          # see what firewalld actually built",
                             "$ sudo nft list chain inet filter INPUT"])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "Firewall Triage Drill",
                       "Is it the firewall? Prove it in 60 seconds.")
    yy = _code(c, 72, y, ["$ sudo firewall-cmd --state                    # running?",
                           "$ sudo firewall-cmd --list-all --zone=public   # what's open?",
                           "# test from the CLIENT:",
                           "$ nc -vz db.internal 5432     # refused = nothing listening OR reject",
                           "$ sudo tcpdump -i eth0 port 5432   # packets arrive but no reply = DROP"])
    yy = bullet_list(c, 72, yy - 36,
        ["Temporarily --set-target=ACCEPT on a test zone beats disabling firewalld (never do that).",
         "Remember BOTH firewalls: host firewalld AND cloud security groups / NACLs.",
         "Log dropped packets while debugging: rich rule with log prefix, then journalctl -k."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "firewalld & nftables",
        ["Zones assign trust per interface — the firewall follows the network.",
         "Prefer --add-service over raw ports; use rich rules for source-scoped exceptions.",
         "Runtime is for testing, permanent is for keeping — promote with --runtime-to-permanent.",
         "nftables tables → chains → rules is the engine; nft list ruleset shows the truth.",
         "Triage: state → list-all → client test → tcpdump; check cloud security groups too."],
        pg)
    c.save()


# =====================================================================
# 14. LVM & RAID
# =====================================================================
def pdf_lvm_raid(path):
    c = new_canvas(path); pg = 1
    title_page(c, "LVM & RAID\nVisual Guide",
               "PV/VG/LV layering, snapshots,\nand RAID 0/1/5/6/10 trade-offs.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "LVM Layering: PV → VG → LV",
                       "Disks become pools; pools become flexible volumes.")
    box(c, 72, 500, 140, 52, BOX_TEAL, "/dev/sda", "PV", font_size=10)
    box(c, 231, 500, 140, 52, BOX_TEAL, "/dev/sdb", "PV", font_size=10)
    arrow(c, 142, 500, 200, 440, color=ACCENT, width=1.5)
    arrow(c, 301, 500, 280, 440, color=ACCENT, width=1.5)
    box(c, 186, 400, 240, 56, BOX_BLUE, "vg_data", "volume group = pool", font_size=10)
    box(c, 72, 300, 140, 52, BOX_GREEN, "lv_web (50G)", "logical volume", font_size=9)
    box(c, 231, 300, 140, 52, BOX_GREEN, "lv_db (200G)", "logical volume", font_size=9)
    box(c, 390, 300, 150, 52, BOX_ORANGE, "free space", "grow into", font_size=9)
    arrow(c, 266, 400, 142, 352, color=ACCENT, width=1.5)
    arrow(c, 306, 400, 301, 352, color=ACCENT, width=1.5)
    yy = _code(c, 72, 260, ["$ sudo pvcreate /dev/sdb && sudo vgcreate vg_data /dev/sdb",
                             "$ sudo lvcreate -L 50G -n lv_web vg_data",
                             "$ sudo mkfs.ext4 /dev/vg_data/lv_web"])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Growing Volumes Online",
                       "The superpower: resize storage without downtime.")
    box(c, 72, 470, 150, 56, BOX_GREEN, "lv_web 50G", "today", font_size=10)
    box(c, 390, 470, 150, 56, BOX_GREEN, "lv_web 120G", "after", font_size=10)
    arrow(c, 222, 498, 390, 498, color=ACCENT, width=2.5, label="lvextend + resize2fs")
    yy = _code(c, 72, 430, ["$ sudo lvextend -L +70G /dev/vg_data/lv_web   # grow the LV",
                             "$ sudo resize2fs /dev/vg_data/lv_web         # grow ext4 (online!)",
                             "# xfs: sudo xfs_growfs /mountpoint           # (xfs only grows)",
                             "$ sudo vgextend vg_data /dev/sdc             # pool out of space? add disk"])
    note(c, 72, 150, 468, "Order matters: extend the LV first, then the filesystem. Shrinking is the dangerous direction — backup, unmount, e2fsck, resize2fs, lvreduce. ext4 shrinks; XFS never does.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Snapshots: Instant, Copy-on-Write",
                       "Freeze a moment for backups — cheap until it changes.")
    box(c, 72, 470, 200, 60, BOX_BLUE, "lv_db (origin)", "live, changing", font_size=10)
    box(c, 340, 470, 200, 60, BOX_ORANGE, "lv_db_snap", "frozen view", font_size=10)
    arrow(c, 272, 500, 340, 500, color=ORANGE, width=2, label="lvcreate -s")
    yy = _code(c, 72, 430, ["$ sudo lvcreate -s -L 10G -n snap /dev/vg_data/lv_db",
                             "$ sudo mount -o ro /dev/vg_data/snap /mnt/backup  # backup from here",
                             "$ sudo lvremove /dev/vg_data/snap                # delete when done"])
    yy = bullet_list(c, 72, yy - 36,
        ["Snapshots start nearly free; they grow as the origin diverges — size them for the change rate × backup window.",
         "A full snapshot INVALIDATES itself — monitor snapshot usage during long backups.",
         "Snapshot + rsync/tar = consistent backup of a live database volume."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "RAID 0 & RAID 1: Speed vs Mirror",
                       "Striping doubles speed and risk; mirroring doubles safety and cost.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11)
    c.drawString(72, 560, "RAID 0 — striping (no redundancy)")
    for i in range(4):
        box(c, 72 + i * 120, 480, 108, 52, BOX_BLUE if i % 2 == 0 else BOX_TEAL,
            f"disk {i+1}", f"blocks {i%2+1},{i%2+3}…", font_size=9)
    c.setFillColor(RED); c.setFont(BODY_FONT, 10)
    c.drawString(72, 460, "1 disk dies → ALL data lost. Capacity: sum of disks.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11)
    c.drawString(72, 420, "RAID 1 — mirroring")
    for i in range(2):
        box(c, 72 + i * 120, 340, 108, 52, BOX_GREEN, f"disk {i+1}", "identical copy", font_size=9)
    arrow(c, 180, 366, 192, 366, color=GREEN, width=2, label="mirror")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 320, "1 disk dies → zero data loss. Capacity: ONE disk. Reads can be parallel.")
    note(c, 72, 180, 468, "RAID is not backup: it survives DISK failure, not deletion, corruption, or ransomware. You still need snapshots and off-site copies.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "RAID 5 / 6 / 10: The Trade-off Table",
                       "Parity buys capacity; mirrors buy simplicity.")
    yy = _table(c, 72, y, ["Level", "Min disks", "Survives", "Capacity", "Use"],
        [["RAID 5", "3", "1 disk", "(n-1)/n", "bulk storage"],
         ["RAID 6", "4", "2 disks", "(n-2)/n", "large arrays"],
         ["RAID 10", "4", "1+*", "n/2", "databases"]],
        [70, 80, 80, 80, 158], fs=10.5)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(72, yy - 22, "* RAID 10 survives many 2-disk failures — unless both disks of one mirror pair die.")
    yy = bullet_list(c, 72, yy - 52,
        ["RAID 5 write penalty: each write = read old data + read parity + write both (the 'write hole' without battery/cache).",
         "Rebuild times on multi-TB disks stretch into DAYS — during which a second failure kills RAID 5. That's why RAID 6 exists.",
         "Databases want RAID 10: no parity math on the write path, fastest rebuilds (plain copy)."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "LVM on RAID: The Standard Stack",
                       "Hardware/RAID below, LVM above — each layer does one job.")
    box(c, 72, 500, 468, 48, BOX_RED, "physical disks", "RAID 10 via mdadm or hardware", font_size=10)
    box(c, 72, 430, 468, 48, BOX_TEAL, "PV on /dev/md0", "LVM sees one big disk", font_size=10)
    box(c, 72, 360, 468, 48, BOX_BLUE, "VG → LVs", "flexible volumes + snapshots", font_size=10)
    arrow(c, 306, 500, 306, 478, color=MUTED, width=1.5)
    arrow(c, 306, 430, 306, 408, color=MUTED, width=1.5)
    yy = _code(c, 72, 320, ["$ sudo mdadm --create /dev/md0 --level=10 --raid-devices=4 /dev/sd[b-e]",
                             "$ sudo pvcreate /dev/md0 && sudo vgcreate vg0 /dev/md0",
                             "$ cat /proc/mdstat        # watch the sync progress"])
    note(c, 72, 120, 468, "mdadm --detail --scan >> /etc/mdadm/mdadm.conf + update-initramfs -u — or the array won't assemble at boot and nothing above it exists.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "LVM & RAID",
        ["LVM: PVs (disks) → VG (pool) → LVs (volumes) — grow filesystems online.",
         "Snapshots are copy-on-write frozen views: perfect for consistent live backups.",
         "RAID 0 = speed, no safety. RAID 1 = mirror. RAID 5/6 = parity capacity. RAID 10 = DB favorite.",
         "RAID ≠ backup: it survives disk death, not deletion or ransomware.",
         "Standard stack: RAID below, LVM above — persist mdadm config or it won't assemble at boot."],
        pg)
    c.save()


# =====================================================================
# 15. Performance Tuning
# =====================================================================
def pdf_perf(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Performance Tuning\nVisual Guide",
               "The USE method, CPU/memory/IO profiling,\nperf, and flame graphs.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "The USE Method: Check Every Resource",
                       "For each resource ask: Utilization, Saturation, Errors.")
    box(c, 216, 480, 180, 56, BOX_PURP, "CPU · memory · disk · net", "each resource…", font_size=10)
    for i, (u, fill, s) in enumerate([("Utilization", BOX_BLUE, "how busy?"),
                                      ("Saturation", BOX_ORANGE, "how queued?"),
                                      ("Errors", BOX_RED, "how failing?")]):
        box(c, 72 + i * 160, 380, 148, 64, fill, u, s, font_size=10)
        arrow(c, 306, 480, 72 + i * 160 + 74, 444, color=MUTED, width=1.2)
    yy = _table(c, 72, 320, ["Resource", "Utilization", "Saturation", "Errors"],
        [["CPU", "%user+sys", "run queue", "—"],
         ["memory", "used/total", "swap/paging", "OOM kills"],
         ["disk", "%util", "await queue", "io errors"],
         ["network", "throughput", "drops", "retransmits"]],
        [90, 120, 120, 138], fs=10)
    note(c, 72, 120, 468, "USE kills the #1 tuning mistake: optimizing the wrong resource. A saturated disk looks like a slow CPU until you check await.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "CPU: Where Do Cycles Go?",
                       "user vs system vs steal vs idle — then per-process.")
    yy = _code(c, 72, y, ["$ mpstat -P ALL 1        # per-core: %usr %sys %iowait %steal %idle",
                           "$ pidstat -u 1           # per-process CPU",
                           "$ top → press 1          # per-core view",
                           "$ perf top               # live: which FUNCTIONS burn cycles"])
    yy = bullet_list(c, 72, yy - 36,
        ["High %iowait is NOT a CPU problem — the CPU is idle waiting on disk. Tune storage.",
         "%steal on a VM means the hypervisor took your cycles — noisy neighbor or overcommit.",
         "High %sys with lots of context switches → too many tiny syscalls or lock contention."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Memory: Used Isn't Used",
                       "Linux eats free RAM for cache — that's a feature.")
    yy = _code(c, 72, y, ["$ free -h", "              total   used   free  shared  buff/cache available",
                           "Mem:           31Gi   4.2Gi   2.1Gi   1.0Gi       24Gi       25Gi",
                           "$ vmstat 1   # si/so = swap in/out — ANY sustained so = pain",
                           "$ dmesg | grep -i oom   # did the OOM killer visit?"])
    yy = bullet_list(c, 72, yy - 36,
        ["Watch 'available', not 'free' — buff/cache is instantly reclaimable.",
         "Swap OUT (so) under load = thrashing. Swap used at idle = harmless old pages.",
         "OOM killer picks by oom_score — tune with /proc/<pid>/oom_score_adj for sacrificial vs sacred."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "Disk & Network I/O",
                       "Latency first, throughput second.")
    yy = _code(c, 72, y, ["$ iostat -x 1      # await (latency), %util, avgqu-sz per device",
                           "$ iotop -o         # which PROCESS is doing the I/O",
                           "$ ss -i            # per-socket retransmits, rtt",
                           "$ nstat | grep -i drop   # packet drops = saturation signal"])
    yy = bullet_list(c, 72, yy - 36,
        ["%util at 100% with low await = busy but fine. High await = the queue is the problem.",
         "iotop -o shows only processes actually doing I/O — skip the idle noise.",
         "Network retransmits + drops together = congestion; retransmits alone can mean a flaky peer."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "perf & Flame Graphs",
                       "Sample the stack, draw the truth.")
    yy = _code(c, 72, y, ["$ sudo perf record -F 99 -a -g -- sleep 30   # sample stacks, 30s",
                           "$ sudo perf report                         # who burned cycles",
                           "# flame graph (brendangregg/FlameGraph):",
                           "$ sudo perf script | stackcollapse-perf.pl | flamegraph.pl > out.svg"])
    # flame graph sketch
    c.setFillColor(INK); c.setFont(BODY_FONT, 9)
    c.drawString(72, 330, "flame graph anatomy:")
    bars = [(72, 300, 468, BOX_RED, "main"), (72, 278, 380, BOX_ORANGE, "handle_request"),
            (72, 256, 300, BOX_BLUE, "parse_json"), (72, 234, 180, BOX_TEAL, "malloc"),
            (372, 256, 80, BOX_GREEN, "db_query"), (452, 256, 88, BOX_PURP, "render")]
    for xx, yy2, w, fill, lbl in bars:
        c.setFillColor(fill); c.rect(xx, yy2, w, 20, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont(BODY_FONT, 8)
        c.drawString(xx + 5, yy2 + 7, lbl)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9)
    c.drawString(72, 200, "x-axis = time (width = cost)    y-axis = stack depth — the WIDEST plateau is your bottleneck")
    note(c, 72, 120, 468, "Read flame graphs by width, not height: the widest box at any level is where time goes. Ignore narrow towers — they're cheap.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "The Tuning Loop",
                       "Measure → hypothesize → change ONE thing → re-measure.")
    steps = [("measure", BOX_BLUE), ("hypothesize", BOX_TEAL), ("change ONE", BOX_ORANGE),
             ("re-measure", BOX_GREEN)]
    xx = 72
    for s, fill in steps:
        box(c, xx, 470, 108, 56, fill, s, "", font_size=10)
        if xx < 400:
            arrow(c, xx + 108, 498, xx + 120, 498, color=ACCENT, width=2)
        xx += 120
    arrow(c, 504, 470, 504, 420, color=MUTED, width=1.5)
    arrow(c, 504, 420, 72, 420, color=MUTED, width=1.5)
    arrow(c, 72, 420, 72, 470, color=MUTED, width=1.5)
    yy = bullet_list(c, 72, 380,
        ["Baseline FIRST: no 'before' numbers means no proof the change helped.",
         "One variable at a time — two changes and a win teaches you nothing reproducible.",
         "Tune the BOTTLENECK only (flame graph / USE). Optimizing idle resources is theater.",
         "Document the knob, the before/after, and the rollback — future-you is on call."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Performance Tuning",
        ["USE method per resource: Utilization, Saturation, Errors — before touching any knob.",
         "CPU: %iowait is a disk problem; %steal is a hypervisor problem; %sys spikes mean syscall storms.",
         "Memory: watch 'available' not 'free'; sustained swap-out is the red alert.",
         "perf + flame graphs turn 'it's slow' into 'this function costs 40%'. Read by width.",
         "Tuning loop: baseline → one change → re-measure. No baseline, no proof."],
        pg)
    c.save()


# =====================================================================
# 16. Troubleshooting Methodology
# =====================================================================
def pdf_troubleshooting(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Troubleshooting Methodology\nVisual Guide",
               "Reproduce, isolate layers, test hypotheses\n— a systematic flow for any outage.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "The Flowchart",
                       "The same loop works for a dead server or a flaky script.")
    flow = [("REPRODUCE", BOX_RED, "make it happen on demand"),
            ("GATHER", BOX_ORANGE, "logs · metrics · timeline"),
            ("ISOLATE", BOX_BLUE, "which layer is broken?"),
            ("HYPOTHESIZE", BOX_TEAL, "one cause, one test"),
            ("TEST", BOX_GREEN, "smallest experiment"),
            ("FIX + VERIFY", BOX_PURP, "prove it, monitor it")]
    yy2 = 560
    for lbl, fill, sub in flow:
        box(c, 186, yy2 - 52, 240, 48, fill, lbl, sub, font_size=10)
        if yy2 > 200:
            arrow(c, 306, yy2 - 52, 306, yy2 - 56, color=MUTED, width=1.5)
        yy2 -= 60
    note(c, 72, 110, 468, "The loop matters more than the tools: skipping REPRODUCE means you 'fix' things you can't prove were broken.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Reproduce: Define Broken Precisely",
                       "Vague symptoms get vague fixes.")
    yy = _table(c, 72, y, ["Vague", "Precise (reproducible)"],
        [["'the site is down'", "'curl https://x/ returns 502 in 300ms, every time'"],
         ["'it's slow sometimes'", "'p99 latency 4s on /search, 14:00–15:00 daily'"],
         ["'deploy broke it'", "'v2.4.1: /health 500s; v2.4.0 fine; rollback fixes it'"]],
        [150, 318], fs=10)
    yy = bullet_list(c, 72, yy - 36,
        ["Write the repro as a COMMAND someone else can run — that's your before/after proof.",
         "Note what CHANGED recently: deploys, config, certs, traffic, cron. Most outages have a birthday.",
         "If you can't reproduce it, you can't verify the fix — say so out loud before 'fixing'."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Isolate: Bisect the Stack",
                       "Split the system in half; test which half is guilty.")
    box(c, 72, 500, 468, 44, BOX_BLUE, "client / browser", "curl from laptop vs from server?", font_size=9)
    box(c, 72, 430, 468, 44, BOX_TEAL, "network / LB / TLS", "bypass LB? http vs https?", font_size=9)
    box(c, 72, 360, 468, 44, BOX_GREEN, "app server", "localhost curl vs remote?", font_size=9)
    box(c, 72, 290, 468, 44, BOX_ORANGE, "database / disk", "slow query log? iostat?", font_size=9)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(72, 250, "Each question eliminates HALF the stack. Three questions → one suspect layer.")
    yy = _code(c, 72, 210, ["$ curl localhost:8080/health     # app itself OK? (cuts network+LB)",
                             "$ curl https://app/health        # now add TLS+LB back",
                             "# works locally, fails remotely → the fault is BETWEEN, not IN"])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "Hypothesize & Test: One Variable",
                       "A hypothesis you can't test is a horoscope.")
    yy = _table(c, 72, y, ["Weak", "Strong (testable)"],
        [["'maybe DNS'", "'dig fails for this name on this host, works on another'"],
         ["'probably the firewall'", "'tcpdump shows SYN, no SYN-ACK on port 5432'"],
         ["'the deploy'", "'rollback to v2.4.0 clears the 500s in 60 seconds'"]],
        [150, 318], fs=10)
    yy = bullet_list(c, 72, yy - 36,
        ["State the expected result BEFORE running the test — otherwise every result 'confirms' your bias.",
         "Cheapest test first: a 10-second curl beats a 30-minute config rewrite.",
         "One change per test. Two changes + success = you learned nothing durable."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "Evidence Tools by Layer",
                       "Reach for the right lens per layer.")
    yy = _table(c, 72, y, ["Layer", "Tools", "Shows"],
        [["app", "logs, journalctl", "errors, stack traces"],
         ["process", "ps, strace, lsof", "what it's doing / holding"],
         ["system", "dmesg, vmstat, iostat", "kernel, memory, disk truth"],
         ["network", "ss, tcpdump, dig", "sockets, packets, DNS"],
         ["time", "timedatectl, ntp", "clock skew breaks TLS/auth"]],
        [90, 170, 208], fs=10.5)
    note(c, 72, 150, 468, "Clock skew is the silent killer: expired-looking certs, Kerberos failures, and 'random' auth errors. Check the clock early — it costs five seconds.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "After the Fix: Close the Loop",
                       "An unverified fix is a rumor.")
    yy = _checklist(c, 72, y,
        ["Re-run the repro command — confirm the precise symptom is gone",
         "Watch for 15+ minutes (or one full cycle) — flaky fixes resurface",
         "Check you didn't break the neighbors — run the adjacent repros too",
         "Write it down: symptom, cause, fix, time — your future on-call self says thanks",
         "Add the monitor/alert that would have caught it sooner",
         "Blameless note: what in the SYSTEM allowed this, not who"])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Troubleshooting Methodology",
        ["Loop: reproduce → gather → isolate → hypothesize → test → fix → verify. Don't skip steps.",
         "Define 'broken' as a runnable command — vague symptoms get vague fixes.",
         "Bisect the stack: each test should eliminate half the suspects.",
         "Hypotheses must be testable with a stated expected result; cheapest test first.",
         "Close the loop: verify, monitor, document, and add the alert that would have caught it."],
        pg)
    c.save()


# =====================================================================
# 17. Containers vs VMs
# =====================================================================
def pdf_containers_vms(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Containers vs VMs\nVisual Guide",
               "Isolation levels, overhead,\nwhen each wins — and the middle ground.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "VM Architecture: Hardware in Software",
                       "A hypervisor virtualizes hardware; each VM runs a full OS.")
    box(c, 72, 540, 468, 36, BOX_PURP, "physical hardware", "", font_size=9)
    box(c, 72, 492, 468, 40, BOX_BLUE, "hypervisor (KVM / ESXi)", "virtualizes CPU · RAM · disk · NIC", font_size=9)
    for i, lbl in enumerate(["VM 1: Ubuntu\nkernel + libs + app", "VM 2: RHEL\nkernel + libs + app"]):
        xx = 72 + i * 240
        box(c, xx, 380, 228, 96, BOX_GREEN, "guest OS", lbl.split("\n")[0], font_size=9)
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 8)
        for j, ln in enumerate(lbl.split("\n")[1:]):
            c.drawCentredString(xx + 114, 452 - j * 11, ln)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(72, 350, "Every VM carries its own kernel — strong isolation, real overhead per guest.")
    note(c, 72, 180, 468, "Type 1 hypervisors (KVM, ESXi) run on bare metal; Type 2 (VirtualBox) run inside a host OS. Production servers use Type 1.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "Container Architecture: One Kernel, Many Views",
                       "Namespaces + cgroups partition a single OS.")
    box(c, 72, 540, 468, 36, BOX_PURP, "physical hardware", "", font_size=9)
    box(c, 72, 470, 468, 62, BOX_RED, "ONE shared kernel", "namespaces + cgroups enforced here", font_size=10)
    for i, lbl in enumerate(["container 1\nlibs + app", "container 2\nlibs + app", "container 3\nlibs + app"]):
        xx = 72 + i * 160
        box(c, xx, 380, 148, 76, BOX_ORANGE, "container", lbl.split("\n")[0], font_size=9)
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 8)
        c.drawCentredString(xx + 74, 448, lbl.split("\n")[1])
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(72, 350, "No guest kernels — containers are processes with isolation flags. Milliseconds to start.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "Overhead Comparison",
                       "What the extra kernel(s) cost you.")
    metrics = [("boot time", "30–120 s", "50–500 ms", 400, 60),
               ("memory per unit", "~1 GB+", "~10–50 MB", 380, 40),
               ("density per host", "10s", "100s–1000s", 300, 50)]
    yy2 = 540
    for lbl, vm, ct, wvm, wct in metrics:
        c.setFillColor(INK); c.setFont(BODY_FONT, 10)
        c.drawString(72, yy2, lbl)
        c.setFillColor(BOX_BLUE); c.rect(200, yy2 - 6, wvm, 18, fill=1, stroke=0)
        c.setFillColor(BOX_GREEN); c.rect(200, yy2 - 28, wct, 18, fill=1, stroke=0)
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 8.5)
        c.drawString(200 + wvm + 6, yy2 - 2, "VM " + vm)
        c.drawString(200 + wct + 6, yy2 - 24, "container " + ct)
        yy2 -= 70
    note(c, 72, 180, 468, "Bars are illustrative, not benchmarks — measure your own workload. The DIRECTION is always the same: containers are 10–100x lighter per unit.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "Isolation & Security Compared",
                       "Stronger walls cost more concrete.")
    yy = _table(c, 72, y, ["", "VM", "Container"],
        [["isolation boundary", "hypervisor + own kernel", "kernel namespaces"],
         ["kernel exploit escapes", "to hypervisor only", "to HOST kernel"],
         ["tenants per host", "untrusted OK", "trust the kernel together"],
         ["live migration", "mature", "hard (CRIU)"],
         ["custom kernel/modules", "yes", "no — host kernel"],
         ["startup", "slow", "instant"]],
        [150, 159, 159], fs=10)
    yy = bullet_list(c, 72, yy - 36,
        ["Rule of thumb: hostile or mutually-untrusted tenants → VMs. One team, one org → containers.",
         "Containers share the kernel — a kernel CVE is a container-escape CVE. Patch hosts fast.",
         "Defense in depth for containers: read-only rootfs, drop capabilities, seccomp, user namespaces."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "The Middle Ground: Kata, gVisor, Firecracker",
                       "VM-grade isolation at container speed.")
    box(c, 72, 470, 140, 64, BOX_BLUE, "Kata Containers", "each pod in a\nlight VM", font_size=9)
    box(c, 231, 470, 140, 64, BOX_GREEN, "gVisor", "user-space kernel\n(Sentry) shim", font_size=9)
    box(c, 390, 470, 150, 64, BOX_ORANGE, "Firecracker", "microVMs:\n125ms boot", font_size=9)
    yy = _table(c, 72, 420, ["Tech", "Isolation trick", "Used by"],
        [["Kata", "lightweight QEMU VM per pod", "regulated multi-tenant K8s"],
         ["gVisor", "intercepts syscalls in userspace", "GCP serverless"],
         ["Firecracker", "KVM microVM, minimal device model", "AWS Lambda/Fargate"]],
        [90, 220, 158], fs=10)
    note(c, 72, 150, 468, "Pick the middle when containers are right operationally but the threat model needs VM walls — e.g. running customer code in your SaaS.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "Decision Guide",
                       "Match the tool to the job.")
    yy = _checklist(c, 72, y,
        ["Need different OS kernels (Windows + Linux)? → VMs, no contest",
         "Running untrusted third-party code? → VMs (or Kata/Firecracker)",
         "Microservices, CI jobs, dev envs, dense packing? → containers",
         "Need bare-metal speed with isolation? → containers + strict seccomp/caps",
         "Compliance demands kernel separation? → VMs, document it",
         "When unsure: containers by default, VMs where the threat model says so"])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Containers vs VMs",
        ["VMs virtualize hardware — each guest carries a full kernel: strong isolation, heavy overhead.",
         "Containers partition one kernel with namespaces + cgroups: millisecond starts, shared-kernel risk.",
         "Overhead gap is 10–100x per unit — density is containers' superpower.",
         "Untrusted tenants → VMs; one org's services → containers; harden both.",
         "Middle ground (Kata, gVisor, Firecracker) buys VM-grade walls at container speed."],
        pg)
    c.save()


# =====================================================================
# 18. Linux Boot Process
# =====================================================================
def pdf_boot(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Linux Boot Process\nVisual Guide",
               "UEFI/BIOS, GRUB, initramfs,\nsystemd stages, and boot failure triage.",
               CAT, None); pg += 1
    N = 6

    y = section_header(c, 1, N, "The Boot Timeline",
                       "Five acts from power button to login prompt.")
    acts = [("1", BOX_BLUE, "firmware", "UEFI/BIOS\nPOST + boot dev"), ("2", BOX_TEAL, "GRUB", "bootloader\nmenu + kernel"),
            ("3", BOX_GREEN, "kernel", "decompress\n+ initramfs"), ("4", BOX_ORANGE, "initramfs", "early userspace\nmount real root"),
            ("5", BOX_PURP, "systemd", "PID 1\ntargets + services")]
    xx = 72
    for n, fill, lbl, sub in acts:
        box(c, xx, 470, 88, 72, fill, n + " " + lbl, sub.split("\n")[0], font_size=9)
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 8)
        c.drawCentredString(xx + 44, 492, sub.split("\n")[1])
        if xx < 460:
            arrow(c, xx + 88, 506, xx + 100, 506, color=ACCENT, width=2)
        xx += 100
    yy = bullet_list(c, 72, 420,
        ["Firmware finds the bootloader (EFI System Partition, or MBR for legacy BIOS).",
         "GRUB loads the kernel + initramfs into memory and jumps to the kernel entry point.",
         "initramfs mounts the REAL root filesystem, then hands off to /sbin/init (systemd).",
         "systemd becomes PID 1 and walks sysinit → basic → multi-user → graphical."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, N, "UEFI vs BIOS & GRUB",
                       "Modern firmware, classic bootloader menu.")
    box(c, 72, 480, 220, 64, BOX_BLUE, "UEFI", "GPT · ESP partition\nSecure Boot capable", font_size=10)
    box(c, 320, 480, 220, 64, BOX_TEAL, "BIOS (legacy)", "MBR · 2TB limit\nno Secure Boot", font_size=10)
    yy = _code(c, 72, 430, ["# GRUB menu → press 'e' to edit the boot entry:",
                             "linux /vmlinuz-6.8.0 root=/dev/sda2 ro quiet splash",
                             "# handy kernel parameters:",
                             "single        # boot to single-user (rescue)",
                             "init=/bin/bash  # skip systemd entirely (emergency shell)",
                             "nomodeset     # survive broken GPU drivers"])
    note(c, 72, 150, 468, "init=/bin/bash is the skeleton key: it drops you to root without systemd, passwords, or mounts. Guard physical/console access accordingly — then remount -o remount,rw / to fix things.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, N, "initramfs: The Kernel's Starter Kit",
                       "A tiny filesystem with just enough to find the real one.")
    box(c, 72, 470, 468, 60, BOX_GREEN, "initramfs (in RAM)", "drivers · decryption · LVM/RAID assembly · fsck", font_size=10)
    box(c, 72, 370, 468, 60, BOX_BLUE, "real root filesystem", "mounted at / — pivot_root, initramfs discarded", font_size=10)
    arrow(c, 306, 470, 306, 430, color=ACCENT, width=2.5, label="pivot")
    yy = bullet_list(c, 72, 330,
        ["Why it exists: the drivers for YOUR disk (NVMe, RAID, LUKS) can't live in the kernel image itself.",
         "Encrypted root? The passphrase prompt you see runs INSIDE initramfs, before / is mounted.",
         "Regenerate after driver/config changes: update-initramfs -u (Debian) / dracut (RHEL).",
         "A stale initramfs after adding a disk driver = 'can't find root device' at boot."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, N, "systemd Takes Over: Targets in Order",
                       "PID 1 climbs the milestone ladder.")
    tgts = [("sysinit", BOX_TEAL, "mounts, udev"), ("basic", BOX_BLUE, "sockets, timers"),
            ("multi-user", BOX_GREEN, "servers, SSH"), ("graphical", BOX_ORANGE, "display manager")]
    xx = 72
    for t, fill, sub in tgts:
        box(c, xx, 480, 108, 60, fill, t, sub, font_size=9)
        if xx < 460:
            arrow(c, xx + 108, 510, xx + 120, 510, color=ACCENT, width=2)
        xx += 120
    yy = _code(c, 72, 430, ["$ systemd-analyze                    # total boot time",
                             "$ systemd-analyze blame | head       # slowest units",
                             "$ systemd-analyze critical-chain     # what the boot waited on",
                             "$ systemd-analyze plot > boot.svg   # visual timeline"])
    note(c, 72, 150, 468, "critical-chain is the truth serum: it shows the dependency path that actually delayed boot, not just the slowest units in isolation.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, N, "Boot Failure Triage",
                       "Where it died tells you what broke.")
    yy = _table(c, 72, y, ["Dies at", "Likely cause", "Recovery"],
        [["no POST / firmware", "hardware, boot order", "BIOS setup, reseat, check ESP"],
         ["GRUB rescue>", "can't find config/disk", "ls, set prefix+root, insmod normal"],
         ["kernel panic", "bad root=, driver, initramfs", "boot older kernel; rebuild initramfs"],
         ["can't mount root", "LUKS/LVM/RAID/fstab", "initramfs shell; check crypttab, mdadm"],
         ["systemd emergency", "failed fstab mount", "fix /etc/fstab (nofail!), reboot"]],
        [130, 160, 178], fs=10)
    yy = _code(c, 72, yy - 30, ["grub rescue> ls", "grub rescue> set prefix=(hd0,gpt2)/boot/grub",
                                 "grub rescue> insmod normal", "grub rescue> normal"])
    note(c, 72, 120, 468, "Add nofail to non-critical fstab entries (data disks, NFS): one missing disk then degrades the boot instead of dropping you to emergency mode.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, N, "Boot Hygiene Checklist",
                       "Boring habits that save 3 AM pages.")
    yy = _checklist(c, 72, y,
        ["Keep one older kernel installed — GRUB Advanced options is your rollback",
         "nofail on every non-root fstab entry (data, NFS, USB)",
         "Rebuild initramfs after storage/crypto driver changes — then TEST reboot",
         "Document LUKS passphrases and mdadm config somewhere off the machine",
         "systemd-analyze blame after major changes — catch slow boots early",
         "Test the rescue path BEFORE you need it: boot the old kernel once"])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Linux Boot Process",
        ["Five acts: firmware → GRUB → kernel → initramfs → systemd (PID 1).",
         "initramfs carries the drivers needed to find the real root — encrypted, RAID, LVM.",
         "GRUB's edit mode (init=/bin/bash, single) is the emergency toolkit — guard console access.",
         "systemd climbs sysinit → basic → multi-user → graphical; analyze with critical-chain.",
         "Triage by death point; nofail in fstab and a spare kernel turn disasters into reboots."],
        pg)
    c.save()


# =====================================================================
# main
# =====================================================================
BUILDERS = [
    ("bbg-filesystem", pdf_filesystem),
    ("bbg-permissions", pdf_permissions),
    ("bbg-processes", pdf_processes),
    ("bbg-systemd", pdf_systemd),
    ("bbg-net-commands", pdf_net_commands),
    ("bbg-bash", pdf_bash),
    ("bbg-ssh", pdf_ssh),
    ("bbg-cron", pdf_cron),
    ("bbg-packages", pdf_packages),
    ("bbg-kernel", pdf_kernel),
    ("bbg-cgroups", pdf_cgroups),
    ("bbg-selinux", pdf_selinux),
    ("bbg-firewalld", pdf_firewalld),
    ("bbg-lvm-raid", pdf_lvm_raid),
    ("bbg-perf", pdf_perf),
    ("bbg-troubleshooting", pdf_troubleshooting),
    ("bbg-containers-vms", pdf_containers_vms),
    ("bbg-boot", pdf_boot),
]


if __name__ == "__main__":
    outdir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(outdir, exist_ok=True)
    for slug, fn in BUILDERS:
        dest = os.path.join(outdir, slug + ".pdf")
        fn(dest)
        print("wrote", dest)
    print(f"done: {len(BUILDERS)} PDFs")
