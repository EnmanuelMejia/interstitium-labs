# Batch A — write to batch-A.json — 8 modules (IL28-M01 through IL28-M08)

M1 | Binary, Hexadecimal & Two's Complement | bits/bytes, base conversion, two's complement, bitwise ops; drills: IP-octet conversions, bitmasking for subnets. prerequisiteFor: [IL28-M03]
M2 | Boolean Algebra & Digital Logic | AND/OR/NOT/XOR, De Morgan, truth tables, Karnaugh-lite; apply to firewall rules, RBAC conditions, pipeline conditionals. prerequisiteFor: [IL28-M04]
M3 | IP Addressing, Subnetting & CIDR/VLSM | IPv4 octets, CIDR notation, subnet math, VLSM, supernetting; heavy worked examples (given 10.0.0.0/16, carve /24s; given host count, find mask). prerequisiteFor: [IL28-M13, IL28-M14]
M4 | Set Theory & Access Logic | sets, Venn, union/intersection/difference applied to RBAC role membership, security-group rules, policy evaluation (Azure Policy allow/deny sets). prerequisiteFor: [IL28-M48]
M5 | Modular Arithmetic & Cryptography Foundations | mod arithmetic, primes, Diffie-Hellman intuition (small numbers), hashing vs encryption, why TLS handshakes work at a conceptual level; NO claims about specific vendor crypto. prerequisiteFor: [IL28-M47]
M6 | Reliability Math: MTBF, MTTR, SLA & Percentiles | availability = MTBF/(MTBF+MTTR), SLA percentages to downtime minutes, percentiles vs averages for latency SLOs, basic queuing (Little's Law) for capacity planning. prerequisiteFor: [IL28-M45, IL28-M49]
M7 | Linux Essentials: Filesystem, Permissions & Shell | FHS, file types, chmod/chown/umask (octal!), redirection, pipes, grep/sed/awk basics, man pages. prerequisiteFor: [IL28-M08]
M8 | RHEL Deep-Dive: Inodes, File Descriptors & Disk Troubleshooting | THE inode module: df vs du, "no space on disk" with free space (inodes: df -i), deleted-but-open files (lsof +L1), file descriptors (/proc/PID/fd, ulimit), quotas, /tmp; full worked troubleshooting transcripts. Include the exact panel questions as drill items. prerequisiteFor: [IL28-M09, IL28-M10]
