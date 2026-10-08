"""IL-27 Math Foundations track: IL27-MX01..MX08.
Full flesh-out: original readings with worked examples + solutions,
flashcards, original quiz, drills with answer keys, vizNotes for the
animations worker, hands-on lab, mock task."""

MODULES_MATH = [
{
"id": "IL27-MX01",
"code": "IL-27",
"title": "Binary, Hexadecimal & Octal Arithmetic",
"summary": "Learn to read and compute in base 2, 8, and 16 from zero: positional notation, fast conversions, bitwise ops, and two's complement. You need this for -> subnet masks, MAC addresses, Unix permissions, and reading memory dumps.",
"objectives": [
"Convert fluently between binary, octal, decimal, and hexadecimal, including 8-bit octets and multi-byte values.",
"Add and subtract binary numbers by hand and verify with place values.",
"Apply bitwise AND, OR, XOR, NOT, and shifts, and explain what each does to a bit pattern.",
"Explain why hexadecimal is the standard shorthand for binary (memory addresses, MACs, IPv6) and why octal survives in Unix permissions.",
"Describe two's complement and compute the 8-bit two's complement negation of a small integer."
],
"notes": [
{"title": "Positional notation: one idea, every base",
"body": "Every number system you will meet is the same idea: each digit position has a weight, and the value is the sum of digit x weight. Decimal is base 10 (weights 1, 10, 100...). Binary is base 2 (weights 1, 2, 4, 8, 16, 32, 64, 128...). Hexadecimal is base 16 (weights 1, 16, 256, 4096...). Octal is base 8 (weights 1, 8, 64...).\n\nMemorize the 8-bit binary weights left to right: 128 64 32 16 8 4 2 1. To convert binary to decimal, add the weights under the 1s. To convert decimal to binary, subtract the largest weight that fits, write 1, and continue with the remainder.\n\nWorked example (with solution):\nConvert 10110100 (binary) to decimal.\nWeights:  128  64  32  16  8  4  2  1\nBits:        1    0   1   1  0  1  0  0\nSum = 128 + 32 + 16 + 4 = 180. Answer: 180.\n\nConvert 200 (decimal) to binary.\n200 - 128 = 72 -> 1; 72 - 64 = 8 -> 1; 64 no -> 0; 32 no -> 0; 16 no -> 0; 8 - 8 = 0 -> 1; rest 0.\nBits: 1 1 0 0 1 0 0 0 = 11001000. Check: 128+64+8 = 200. Correct."},
{"title": "Hexadecimal: binary's readable costume (and octal's cameo)",
"body": "Binary strings get long fast. Hexadecimal (base 16, digits 0-9 then A=10, B=11, C=12, D=13, E=14, F=15) exists because 16 = 2^4: every hex digit maps to exactly 4 bits (a nibble), and one byte is exactly 2 hex digits. That makes hex a transparent window into binary - you can see the bit pattern in the hex.\n\nConversion rule: binary -> hex, group bits in fours from the RIGHT, convert each group. Hex -> binary, expand each digit to 4 bits.\n\nWorked example (with solution):\nConvert 1101011011110101 (binary) to hex.\nGroup: 1101 0110 1111 0101 -> D 6 F 5. Answer: 0xD6F5.\n\nConvert 0xC0A8 to binary.\nC=1100, 0=0000, A=1010, 8=1000 -> 1100000010101000. That is 192.168 in decimal - the start of every private 192.168.x.x address you will ever type.\n\nOctal (base 8) is the odd one out: 8 = 2^3, so each octal digit is 3 bits. It survives in exactly one place you must know: Unix file permissions. 0755 means owner=rwx(7=111), group=r-x(5=101), other=r-x(5=101). When you chmod 644 a file you are writing binary with octal shorthand."},
{"title": "Bitwise operations and two's complement",
"body": "Bitwise ops work column by column, no carries: AND (1 only if both 1), OR (1 if either 1), XOR (1 if different), NOT (flip). Shifts move bits left (x2 per position) or right (integer /2).\n\nThe single most important AND in infrastructure: IP address AND subnet mask = network address. 192.168.1.10 AND 255.255.255.0: the mask's 1-bits keep the address bits, the 0-bits zero the host bits, leaving 192.168.1.0. Subnetting is literally applied Boolean algebra.\n\nTwo's complement is how computers store negatives: flip all bits of the positive value, add 1. In 8 bits, -1 is 11111111, -128 is 10000000. The leftmost bit becomes the sign bit.\n\nWorked example (with solution):\nCompute 10110100 AND 11110000, then OR the result with 00001111.\nAND:  1 0 1 1 0 1 0 0\n      1 1 1 1 0 0 0 0\n    = 1 0 1 1 0 0 0 0  (both 1 only in first four columns)\nOR with 00001111:\n      1 0 1 1 0 0 0 0\n      0 0 0 0 1 1 1 1\n    = 1 0 1 1 1 1 1 1  = 0xBF = 191.\n\nTwo's complement of 5 in 8 bits: 5 = 00000101 -> flip = 11111010 -> +1 = 11111011 = -5. Check: 5 + (-5) = 00000101 + 11111011 = 1 00000000; the 9th bit falls off in 8-bit arithmetic, leaving 0. Correct."
}
],
"cards": [
{"front": "Binary weights of an 8-bit octet, left to right", "back": "128, 64, 32, 16, 8, 4, 2, 1. Sum of all = 255."},
{"front": "Binary 11000000 in decimal", "back": "192 (128 + 64)."},
{"front": "Why does one hex digit equal exactly 4 bits?", "back": "16 = 2^4, so each hex digit (0-F) maps to one nibble. One byte = exactly 2 hex digits."},
{"front": "Binary 1011 0110 as hex", "back": "0xB6 (1011=B, 0110=6)."},
{"front": "What does 0xC0A8 mean in dotted decimal?", "back": "192.168 (C0=192, A8=168)."},
{"front": "What Unix permissions does octal 755 encode?", "back": "rwxr-xr-x: owner 7=111 (rwx), group 5=101 (r-x), other 5=101 (r-x)."},
{"front": "10110100 AND 11110000", "back": "10110000 - AND keeps a 1 only where both bits are 1."},
{"front": "How is -5 stored in 8-bit two's complement?", "back": "Flip 00000101 -> 11111010, add 1 -> 11111011."}
],
"quiz": [
{"q": "What is 10110100 in decimal?", "choices": ["172", "180", "188", "196"], "answer": 1, "index": 1, "explain": "128 + 32 + 16 + 4 = 180."},
{"q": "What is 200 in 8-bit binary?", "choices": ["11001000", "11010000", "10101000", "11000100"], "answer": 0, "index": 0, "explain": "128 + 64 + 8 = 200 -> bits at 128, 64, 8 positions: 11001000."},
{"q": "What is 0xD6F5 in binary?", "choices": ["1101011011110101", "1101011001110101", "1101011011110100", "1101011011010101"], "answer": 0, "index": 0, "explain": "D=1101, 6=0110, F=1111, 5=0101."},
{"q": "The binary 1100000010101000 in dotted decimal is:", "choices": ["192.168.0.1", "192.168.1.0", "192.168.0.0", "192.167.0.0"], "answer": 2, "index": 2, "explain": "First octet 11000000=192, second 10101000=168, then 00000000=0, 00000000=0."},
{"q": "What does octal 644 mean as rwx triplets?", "back": None, "choices": ["rw-r--r--", "rwxr--r--", "rw-rw-r--", "r--r--r--"], "answer": 0, "index": 0, "explain": "6=110=rw-, 4=100=r--, 4=100=r--."},
{"q": "10110100 XOR 11110000 =", "choices": ["01000100", "11110100", "10110000", "01001100"], "answer": 0, "index": 0, "explain": "XOR is 1 where bits differ: columns give 0,1,0,0,0,1,0,0 = 01000100."},
{"q": "What is the 8-bit two's complement of 1 (i.e., -1)?", "choices": ["10000001", "11111111", "11111110", "10000000"], "answer": 1, "index": 1, "explain": "Flip 00000001 -> 11111110, add 1 -> 11111111."},
{"q": "A left shift of 00000101 by 2 positions gives:", "choices": ["00010100", "00001010", "00000101", "01010000"], "answer": 0, "index": 0, "explain": "Left shift multiplies by 4: 5 x 4 = 20 = 00010100."}
],
"weight": 2,
"prerequisiteFor": ["IL27-MX03", "IL27-M05", "IL27-MX02"],
"drills": [
{"id": "mx01-drill-conversions", "title": "Base Conversion Sprint",
"items": [
{"prompt": "10101010 binary to decimal", "answer": "170", "explain": "128+32+8+2 = 170."},
{"prompt": "255 decimal to binary", "answer": "11111111", "explain": "All 8 weights sum to 255."},
{"prompt": "0xFF in decimal", "answer": "255", "explain": "F=15: 15x16+15 = 255."},
{"prompt": "0x1A4 in binary", "answer": "110100100", "explain": "1=0001, A=1010, 4=0100 -> 000110100100 = 110100100."},
{"prompt": "Octal 755: write the three rwx triplets", "answer": "rwxr-xr-x", "explain": "7=111=rwx, 5=101=r-x, 5=101=r-x."},
{"prompt": "11001100 AND 10101010", "answer": "10001000", "explain": "Column AND: 1,0,0,0,1,0,0,0."}
]}
],
"handsOnLab": {
"id": "mx01-lab",
"title": "Bit Gym: conversions and masks by hand, verified in PowerShell",
"brief": "Do 20 conversions on paper, then verify every one with PowerShell one-liners and compute a network address with -band.",
"steps": [
"On paper, convert these to decimal: 11000000, 10101000, 00001010, 11110000, 00000001.",
"Convert these to 8-bit binary on paper: 192, 168, 10, 255, 0.",
"Convert to hex on paper: 11000000 10101000 -> ?, and expand 0x0A to binary.",
"Verify all three sets in PowerShell: [Convert]::ToInt32('10101000',2), [Convert]::ToString(192,2).PadLeft(8,'0'), '{0:X}' -f 168.",
"Compute a network address: $ip=192; $mask=255; $ip -band $mask for each octet of 192.168.10.77 / 255.255.255.0 and confirm 192.168.10.0.",
"Compute -5 in 8-bit two's complement on paper, then verify: [Convert]::ToString(251,2) (251 is the unsigned view of -5)."
],
"deliverable": "A photo/scan of your paper work plus a PowerShell transcript showing all verifications match.",
"checkpoint": "You can convert any octet both directions in under 10 seconds and explain why AND with 255.255.255.0 zeroes the host octet."
},
"mockTask": {"id": "mx01-mock", "type": "choice",
"q": "A junior asks why IPv6 addresses are written in hex instead of decimal. Best answer?",
"choices": ["Hex is shorter than binary and each digit maps cleanly to 4 bits, so the 128-bit address stays readable and bit-aligned", "Hex compresses better in ZIP files", "Decimal cannot represent values above 255", "IPv6 routers only understand base 16"],
"answer": 0, "explain": "16 = 2^4 makes hex a transparent nibble-by-nibble view of the 128-bit address; 32 hex digits vs 128 bits."},
"crossLinks": ["il04-networking"],
"videos": [],
"vizNotes": [
{"title": "Bit-weight abacus", "description": "Interactive row of 8 toggleable bits with weights 128..1 above each; toggling updates the decimal and hex readouts live. Learner task: make 192, then 168."},
{"title": "AND-mask light table", "description": "Two 8-bit rows (IP octet, mask octet) with a third result row; clicking a mask bit flips it and the result column lights only when both inputs are 1. Animate 192.168.1.10 AND 255.255.255.0."}
],
"estimatedMinutes": 240,
"fastTrackEligible": True
},
{
"id": "IL27-MX02",
"code": "IL-27",
"title": "Boolean Algebra & Logic Gates",
"summary": "Truth tables, De Morgan's laws, and simplification - the algebra behind subnet masks, firewall rules, GPO filtering, and every IF in your scripts. You need this for -> MX03/MX04, allowlisting logic, and reading any access-control rule.",
"objectives": [
"Write truth tables for AND, OR, NOT, XOR, NAND, NOR from memory.",
"Apply De Morgan's laws to simplify negated compound conditions.",
"Simplify Boolean expressions using identity, complement, and distributive laws.",
"Translate firewall/allowlist rules and PowerShell Where-Object filters into Boolean expressions and spot redundancies.",
"Explain how a subnet mask ANDs an address at the bit level."
],
"notes": [
{"title": "The six gates and their truth tables",
"body": "Boolean algebra has two values: 1 (true) and 0 (false). Three operations are fundamental: AND (x.y, 1 only if both 1), OR (x+y, 1 if either 1), NOT (x-bar, flips). Three more are derived: XOR (1 if different - the 'one or the other but not both'), NAND (NOT-AND), NOR (NOT-OR).\n\nTruth table for the big four (A, B):\nA B | AND OR XOR NOT A\n0 0 |  0   0   0    1\n0 1 |  0   1   1    1\n1 0 |  0   1   1    0\n1 1 |  1   1   0    0\n\nNAND is AND then flipped (1110 down the column); NOR is OR then flipped (1000). In scripts you meet these as -and, -or, -not, -xor in PowerShell and &&, ||, ! in most other languages.\n\nWorked example (with solution):\nEvaluate (A AND B) OR (NOT A AND C) for A=1, B=0, C=1.\nA AND B = 1 AND 0 = 0. NOT A = 0; 0 AND C = 0 AND 1 = 0. OR: 0 OR 0 = 0. Answer: 0.\nThis pattern (A.B + A'.C) is the skeleton of 'allow if (admin AND mfa) OR (not admin AND vpn)' rules."
},
{"title": "De Morgan's laws: the two rules that untangle every NOT",
"body": "De Morgan's laws: NOT (A AND B) = (NOT A) OR (NOT B). NOT (A OR B) = (NOT A) AND (NOT B). In words: to negate a compound condition, flip the operator and negate each part. This is the single most-used simplification in access control.\n\nWhy it matters: a firewall admin writes 'block everything that is NOT (from 10.0.0.0/8 AND port 443)'. De Morgan expands that to 'block if (NOT from 10.0.0.0/8) OR (NOT port 443)' - which is exactly how you would write two separate deny rules. If you cannot do this expansion in your head, you cannot audit an allowlist.\n\nWorked example (with solution):\nSimplify: NOT (isAdmin OR isOnVPN).\nBy De Morgan: (NOT isAdmin) AND (NOT isOnVPN).\nPowerShell form: -not ($isAdmin -or $isOnVPN) is identical to ((-not $isAdmin) -and (-not $isOnVPN)).\n\nSimplify: NOT (A AND NOT B).\nFlip AND->OR, negate parts: (NOT A) OR (NOT (NOT B)) = (NOT A) OR B. The double negation cancels. So 'not (A and not B)' is just 'B or not A' - check with A=1,B=0: original NOT(1 AND 1)=0; simplified 0 OR 0=0. Correct."
},
{"title": "Simplification laws and reading real rules",
"body": "Core laws: identity (A AND 1 = A; A OR 0 = A), complement (A AND NOT A = 0; A OR NOT A = 1), idempotent (A AND A = A), distributive (A AND (B OR C) = (A AND B) OR (A AND C)), absorption (A OR (A AND B) = A).\n\nAbsorption is the redundancy-killer: 'allow admins, and also allow admins who use VPN' collapses to 'allow admins'. When you inherit a 400-line firewall policy, absorption is how you find the 60 lines that do nothing.\n\nWorked example (with solution):\nSimplify (A AND B) OR (A AND NOT B).\nFactor A: A AND (B OR NOT B) [distributive]. B OR NOT B = 1 [complement]. A AND 1 = A [identity]. Answer: A.\nSanity check with A=1, B=0: original (0) OR (1) = 1; simplified A = 1. Correct.\n\nReal rule reading: GPO 'apply if (user in Finance AND device compliant) OR (user in Finance AND device hybrid-joined)' - factor 'user in Finance': Finance AND (compliant OR hybrid-joined). One group check, one device-state check. That is how you refactor before you automate."
}
],
"cards": [
{"front": "Truth table column for XOR (A,B over 00,01,10,11)", "back": "0, 1, 1, 0 - 1 only when inputs differ."},
{"front": "De Morgan's law for NOT (A AND B)", "back": "(NOT A) OR (NOT B) - flip the operator, negate each part."},
{"front": "De Morgan's law for NOT (A OR B)", "back": "(NOT A) AND (NOT B)."},
{"front": "Simplify: A OR (A AND B)", "back": "A (absorption - the second term adds nothing)."},
{"front": "Simplify: (A AND B) OR (A AND NOT B)", "back": "A (factor A, B OR NOT B = 1)."},
{"front": "In PowerShell, what is -not ($a -or $b) equivalent to?", "back": "(-not $a) -and (-not $b)."},
{"front": "What does NAND output for inputs 1,1?", "back": "0 (AND gives 1, NAND flips it)."},
{"front": "Why is AND the subnet mask operation?", "back": "Mask 1-bits preserve address bits; 0-bits force host bits to 0, isolating the network portion."}
],
"quiz": [
{"q": "NOT (A AND B) is equivalent to:", "choices": ["(NOT A) OR (NOT B)", "(NOT A) AND (NOT B)", "A OR B", "NOT A OR B"], "answer": 0, "index": 0, "explain": "De Morgan: negate each part and flip AND to OR."},
{"q": "A XOR B for A=1, B=1 equals:", "choices": ["1", "0", "2", "undefined"], "answer": 1, "index": 1, "explain": "XOR is 1 only when inputs differ."},
{"q": "Simplify (A OR B) AND (A OR NOT B):", "choices": ["A", "B", "1", "A AND B"], "answer": 0, "index": 0, "explain": "Distribute: A OR (B AND NOT B) = A OR 0 = A."},
{"q": "A firewall rule blocks traffic that is NOT (from 10.0.0.0/8 AND port 443). Per De Morgan it blocks traffic that is:", "choices": ["not from 10.0.0.0/8 OR not port 443", "not from 10.0.0.0/8 AND not port 443", "from 10.0.0.0/8 OR port 443", "from 10.0.0.0/8 AND port 443"], "answer": 0, "index": 0, "explain": "NOT (A AND B) = (NOT A) OR (NOT B)."},
{"q": "What is A AND (NOT A)?", "choices": ["0", "1", "A", "NOT A"], "answer": 0, "index": 0, "explain": "Complement law: a value AND its negation is always 0."},
{"q": "Evaluate (1 OR 0) AND (NOT 0):", "choices": ["1", "0", "2", "error"], "answer": 0, "index": 0, "explain": "(1) AND (1) = 1."},
{"q": "NOR outputs 1 only when:", "choices": ["both inputs are 0", "both inputs are 1", "inputs differ", "at least one input is 1"], "answer": 0, "index": 0, "explain": "NOR = NOT(OR); OR is 0 only for 0,0, so NOR is 1 only there."},
{"q": "PowerShell: -not ($x -and (-not $y)) simplifies to:", "choices": ["(-not $x) -or $y", "$x -or $y", "(-not $x) -and $y", "$x -and $y"], "answer": 0, "index": 0, "explain": "De Morgan: flip -and to -or, negate each: (-not $x) -or (-not (-not $y)) = (-not $x) -or $y."}
],
"weight": 2,
"prerequisiteFor": ["IL27-MX04", "IL27-M27"],
"drills": [
{"id": "mx02-drill-demorgan", "title": "De Morgan Reps",
"items": [
{"prompt": "Negate: (A AND B)", "answer": "(NOT A) OR (NOT B)", "explain": "Flip AND->OR, negate each."},
{"prompt": "Negate: (admin OR vpn)", "answer": "(NOT admin) AND (NOT vpn)", "explain": "Flip OR->AND, negate each."},
{"prompt": "Simplify: X OR (NOT X AND Y)", "answer": "X OR Y", "explain": "Distribute: (X OR NOT X) AND (X OR Y) = 1 AND (X OR Y)."},
{"prompt": "Evaluate: (1 AND 1) OR (0 AND 1)", "answer": "1", "explain": "1 OR 0 = 1."},
{"prompt": "NAND truth column for 00,01,10,11", "answer": "1,1,1,0", "explain": "NAND flips AND: only 1,1 gives 0."},
{"prompt": "Simplify: (A AND B) OR (NOT A AND B)", "answer": "B", "explain": "Factor B: (A OR NOT A) AND B = B."}
]}
],
"handsOnLab": {
"id": "mx02-lab",
"title": "Rule Refactor: simplify a mini firewall policy with Boolean algebra",
"brief": "Take a 6-rule allow/block list, express it in Boolean form, simplify with De Morgan/absorption, and prove equivalence with a PowerShell truth-table script.",
"steps": [
"Write the policy as one Boolean expression: ALLOW = (admin AND mfa) OR (admin AND vpn) OR (contractor AND vpn AND mfa).",
"Apply absorption/distributive laws on paper to simplify; show each step.",
"Write a PowerShell script that loops $admin,$mfa,$vpn,$contractor over 0..1 (16 rows) and prints original vs simplified result per row.",
"Run it and confirm all 16 rows agree.",
"Add a DENY rule: block NOT (ALLOW); expand with De Morgan and list the resulting deny conditions in plain English.",
"Document the before/after rule count and the English meaning of the simplified policy."
],
"deliverable": "Paper derivation + PowerShell script + 16-row equivalence table + plain-English policy summary.",
"checkpoint": "You can expand any negated compound condition with De Morgan on sight and prove two policies equivalent by exhaustive truth table."
},
"mockTask": {"id": "mx02-mock", "type": "choice",
"q": "An allowlist says: allow if NOT (untrusted device OR outside business hours). A user on an untrusted device during business hours is:",
"choices": ["Denied - the device condition fails regardless of time", "Allowed - business hours satisfy the rule", "Allowed - only one condition must pass", "Denied - but only after hours"],
"answer": 0, "explain": "De Morgan: allow = (trusted device) AND (business hours). Both must hold; untrusted device fails the first."},
"crossLinks": [],
"videos": [],
"vizNotes": [
{"title": "Gate playground", "description": "Clickable AND/OR/XOR/NOT gates: toggle the two input switches, watch the output lamp and the highlighted truth-table row. Include NAND/NOR toggle."},
{"title": "De Morgan morph", "description": "Expression NOT (A AND B) shown as a gate diagram; press 'apply De Morgan' and animate the gate morphing into (NOT A) OR (NOT B) with a side truth table proving equivalence row by row."}
],
"estimatedMinutes": 220,
"fastTrackEligible": False
},
{
"id": "IL27-MX03",
"code": "IL-27",
"title": "Subnetting Math: CIDR, VLSM & Supernetting",
"summary": "The math engine behind Module M05: prefix-to-mask conversion, block sizes, range carving, VLSM right-sizing, and supernetting - with fully worked examples. You need this for -> every networking module and the interview whiteboard.",
"objectives": [
"Convert between CIDR prefix length and dotted-decimal mask in both directions without a calculator.",
"Given an address and prefix, compute network address, broadcast address, first/last usable host, and usable count.",
"Carve a parent prefix into equal or custom subnets and list every subnet's range.",
"Right-size subnets with VLSM for a set of host requirements, minimizing waste.",
"Aggregate contiguous prefixes into a supernet (route summarization) and verify coverage."
],
"notes": [
{"title": "CIDR, masks, and the block-size shortcut",
"body": "A /N prefix means the first N of the 32 bits are network bits. The mask is N ones followed by (32-N) zeros. Host bits H = 32 - N. Total addresses = 2^H. Usable hosts = 2^H - 2 (network and broadcast reserved; /31 and /32 are special cases).\n\nThe block size (increment) in the interesting octet = 256 - mask octet value. /26: mask 255.255.255.192, interesting octet 192, block size 256-192 = 64. Subnets start at multiples of 64: .0, .64, .128, .192.\n\nMemorize the /24-to-/30 table: /24: 256/254, /25: 128/126, /26: 64/62, /27: 32/30, /28: 16/14, /29: 8/6, /30: 4/2.\n\nWorked example (with solution):\nGiven 172.16.5.77/22, find mask, network, broadcast, usable range.\n/22 -> mask: 22 ones = 11111111.11111111.11111100.00000000 = 255.255.252.0. Interesting octet is the 3rd (252), block size = 256-252 = 4. Subnets in 3rd octet: 0,4,8,... 5 falls in the 4-block: network = 172.16.4.0. Broadcast = next network minus 1 = 172.16.7.255. Usable: 172.16.4.1 through 172.16.7.254 (1022 hosts = 2^10 - 2)."
},
{"title": "Carving subnets and VLSM right-sizing",
"body": "To carve: decide how many host bits each subnet needs (smallest H with 2^H - 2 >= required hosts), the new prefix is 32 - H, and subnets step by the block size.\n\nVLSM (Variable Length Subnet Masking) = right-sizing each subnet instead of giving every department a /24. Rule: sort requirements largest first, allocate each the smallest fitting block, and never overlap.\n\nWorked example (with solution):\nCarve 192.168.10.0/24 into 4 equal subnets.\nNeed 4 subnets -> borrow 2 bits -> /26. Block size 64. Subnets: 192.168.10.0/26 (.1-.62, bcast .63), .64/26 (.65-.126, bcast .127), .128/26 (.129-.190, bcast .191), .192/26 (.193-.254, bcast .255).\n\nVLSM example: from 10.0.0.0/24, serve needs of 100, 50, 25, and 10 hosts.\n100 hosts -> H=7 (2^7-2=126) -> /25, block 128: 10.0.0.0/25 (.1-.126).\n50 hosts -> H=6 (62) -> /26, block 64: 10.0.0.128/26 (.129-.190).\n25 hosts -> H=5 (30) -> /27, block 32: 10.0.0.192/27 (.193-.222).\n10 hosts -> H=4 (14) -> /28, block 16: 10.0.0.224/28 (.225-.238).\nWaste: (126-100)+(62-50)+(30-25)+(14-10) = 26+12+5+4 = 47 addresses vs 4x/24 wasting hundreds. Largest-first ordering is what prevents overlap."
},
{"title": "Supernetting: summarizing routes",
"body": "Supernetting (route summarization) is subnetting in reverse: find the longest prefix that covers a set of contiguous networks. Routers then carry one route instead of many - smaller tables, faster lookups.\n\nMethod: write the networks in binary, find the longest common leading bit-string, that length is the summary prefix. The summary must cover exactly the intended range - a summary that swallows extra space can black-hole traffic.\n\nWorked example (with solution):\nSummarize 192.168.0.0/24, 192.168.1.0/24, 192.168.2.0/24, 192.168.3.0/24.\nThird octets: 0=00000000, 1=00000001, 2=00000010, 3=00000011. Common leading bits: 000000 (6 bits). Prefix = 16 + 6 = /22. Summary: 192.168.0.0/22, covering 192.168.0.0-192.168.3.255. Verify: /22 block size in 3rd octet = 4 -> .0-.3. Exact fit, no waste, no overreach.\n\nCounter-example: summarizing 192.168.0.0/24 and 192.168.2.0/24 skips .1 - common bits of 0 (00000000) and 2 (00000010) are 000000 (6 bits) -> /22 would wrongly include 192.168.1.0/24 and 192.168.3.0/24. Non-contiguous networks cannot share one clean summary; advertise them separately."
}
],
"cards": [
{"front": "/26 in dotted decimal, block size, usable hosts", "back": "255.255.255.192; block size 64; 62 usable hosts."},
{"front": "Network, broadcast, usable range of 10.20.30.45/28", "back": "Block 16: network 10.20.30.32, broadcast 10.20.30.47, usable .33-.46."},
{"front": "How many usable hosts in a /22?", "back": "2^10 - 2 = 1022."},
{"front": "VLSM rule of thumb for ordering requirements", "back": "Largest first - allocate the biggest block before carving smaller ones to avoid overlap."},
{"front": "Smallest prefix fitting 100 hosts", "back": "/25 (126 usable; /26 only gives 62)."},
{"front": "Summarize 192.168.0.0/24 through 192.168.3.0/24", "back": "192.168.0.0/22."},
{"front": "Why subtract 2 for usable hosts?", "back": "Network address (all-zero host bits) and broadcast address (all-one host bits) are reserved."},
{"front": "Block-size formula", "back": "256 minus the mask value in the interesting octet."}
],
"quiz": [
{"q": "What is the subnet mask for /27?", "choices": ["255.255.255.224", "255.255.255.240", "255.255.255.192", "255.255.255.248"], "answer": 0, "index": 0, "explain": "27 ones: 8+8+8+3 -> 255.255.255.224 (128+64+32)."},
{"q": "192.168.44.70/26: what is the network address?", "choices": ["192.168.44.64", "192.168.44.0", "192.168.44.128", "192.168.44.32"], "answer": 0, "index": 0, "explain": "Block size 64; 70 falls in the 64-block: .64."},
{"q": "Broadcast address of 10.5.5.200/27?", "choices": ["10.5.5.223", "10.5.5.191", "10.5.5.207", "10.5.5.255"], "answer": 0, "index": 0, "explain": "Block 32; 200 in 192-block (.192-.223); broadcast .223."},
{"q": "How many /28 subnets fit in a /24?", "choices": ["16", "8", "32", "4"], "answer": 0, "index": 0, "explain": "28-24 = 4 borrowed bits -> 2^4 = 16."},
{"q": "Smallest subnet for 14 hosts:", "choices": ["/28", "/27", "/29", "/26"], "answer": 0, "index": 0, "explain": "/29 gives 6 usable (too few); /28 gives 14 - exact fit."},
{"q": "Which summary covers 10.1.0.0/24 and 10.1.1.0/24 exactly?", "choices": ["10.1.0.0/23", "10.1.0.0/22", "10.0.0.0/16", "10.1.0.0/24"], "answer": 0, "index": 0, "explain": "Third octets 0,1 share 7 bits -> /23, block 2: .0-.1 exact."},
{"q": "Usable host range of 172.20.8.0/22:", "choices": ["172.20.8.1 - 172.20.11.254", "172.20.8.1 - 172.20.8.254", "172.20.8.0 - 172.20.11.255", "172.20.9.1 - 172.20.10.254"], "answer": 0, "index": 0, "explain": "Block 4 in 3rd octet: .8-.11; usable .8.1 through .11.254."},
{"q": "A /31 is special because:", "choices": ["it has no reserved network/broadcast - both addresses usable for point-to-point links", "it holds 31 hosts", "it is the same as /32", "it cannot be used on Ethernet"], "answer": 0, "index": 0, "explain": "RFC 3021: /31 point-to-point links use both addresses, no broadcast needed."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M05", "IL27-M06"],
"drills": [
{"id": "mx03-drill-carve", "title": "Subnet Carving Reps",
"items": [
{"prompt": "/25 mask in dotted decimal", "answer": "255.255.255.128", "explain": "128 = one borrowed bit in the last octet."},
{"prompt": "Network address of 192.168.99.150/26", "answer": "192.168.99.128", "explain": "Block 64; 150 in 128-block."},
{"prompt": "Broadcast of 192.168.99.150/26", "answer": "192.168.99.191", "explain": "Next network .192 minus 1."},
{"prompt": "Usable hosts in a /29", "answer": "6", "explain": "2^3 - 2."},
{"prompt": "Carve 10.0.0.0/24 into 8 equal subnets: new prefix?", "answer": "/27", "explain": "8 = 2^3 borrowed bits; 24+3=27."},
{"prompt": "Summarize 172.16.4.0/24 + 172.16.5.0/24 + 172.16.6.0/24 + 172.16.7.0/24", "answer": "172.16.4.0/22", "explain": "Octets 4-7 share 6 bits -> /22, block 4: .4-.7."}
]}
],
"handsOnLab": {
"id": "mx03-lab",
"title": "Address Plan: VLSM design for a 3-site company",
"brief": "Design a complete VLSM addressing plan from 172.20.0.0/16 for given requirements, document every subnet, and verify with a PowerShell checker.",
"steps": [
"Requirements: HQ LAN 800 hosts, Branch LAN 300, DMZ 60, WAN links x4 (2 hosts each), management 20.",
"Compute the smallest fitting prefix for each (show 2^H-2 math).",
"Allocate largest-first from 172.20.0.0/16; list network, broadcast, usable range per subnet.",
"Write a PowerShell function Test-SubnetOverlap that takes network/prefix pairs and reports any overlap; run it on your plan (expect none).",
"Write the supernet summary the HQ router would advertise for all HQ subnets.",
"Present the plan as a table: site, subnet, prefix, usable range, gateway (.1), broadcast."
],
"deliverable": "Address plan table + overlap-checker script output + supernet summary with verification math.",
"checkpoint": "You can carve and VLSM any requirement set on paper and prove no overlaps programmatically."
},
"mockTask": {"id": "mx03-mock", "type": "choice",
"q": "Interview whiteboard: 'We need 5 subnets with at least 28 hosts each from 192.168.50.0/24. What prefix and how many subnets result?'",
"choices": ["/27, giving 8 subnets of 30 usable hosts - use 5, reserve 3", "/28, giving 16 subnets of 14 hosts", "/26, giving 4 subnets of 62 hosts", "/25, giving 2 subnets"],
"answer": 0, "explain": "/28 too small (14 < 28); /27 gives 30 usable, 8 subnets - meets the need with growth room."},
"crossLinks": ["il04-networking"],
"videos": "CISCO_IPV4",
"vizNotes": [
{"title": "Prefix slider", "description": "Slider for /8../30 over a fixed address: mask bits light up, block size and host count update, and the network/broadcast/usable range redraw live."},
{"title": "VLSM carving board", "description": "Animated allocation of 10.0.0.0/24 into VLSM blocks: each requirement drops in largest-first, the bar subdivides, waste shown as hatched remainder per block."},
{"title": "Supernet merger", "description": "Four /24 bars merge into one /22: binary third-octet columns align, common prefix bits highlight, and an overreach warning flashes if a non-contiguous network is added."}
],
"estimatedMinutes": 300,
"fastTrackEligible": True
},
{
"id": "IL27-MX04",
"code": "IL-27",
"title": "Modular Arithmetic: Crypto Foundations",
"summary": "Clock arithmetic, Diffie-Hellman, and a toy RSA - the math under TLS, password hashing, and key exchange, built from zero with small numbers you can verify by hand. You need this for -> M28/M32 and any security conversation in the interview.",
"objectives": [
"Compute a mod n fluently and use modular reduction to keep numbers small.",
"Explain why (a + b) mod n = ((a mod n) + (b mod n)) mod n and use it to simplify.",
"Walk through a small Diffie-Hellman exchange and show both sides derive the same secret.",
"Walk through a toy RSA encrypt/decrypt with small primes and verify the round trip.",
"Explain at a high level how modular arithmetic enables hashing buckets and key exchange."
],
"notes": [
{"title": "Clock arithmetic: the mod operator",
"body": "a mod n is the remainder when a is divided by n. 17 mod 5 = 2. Clocks are mod 12: 10 + 5 = 3 (o'clock) because 15 mod 12 = 3. The key property: you can reduce mod n at ANY point in a computation - (a+b) mod n = ((a mod n)+(b mod n)) mod n, and the same for multiplication. This is what lets cryptography work with 2048-bit numbers: reduce early, reduce often.\n\nWorked example (with solution):\nCompute (47 x 53) mod 7 without a calculator doing 47x53.\n47 mod 7 = 5 (42 is divisible by 7). 53 mod 7 = 4 (49 divisible). (5 x 4) mod 7 = 20 mod 7 = 6. Answer: 6.\nVerify: 47x53 = 2491; 2491 / 7 = 355.857...; 355x7 = 2485; 2491-2485 = 6. Correct.\n\nNegative mods: -3 mod 7 = 4 (add 7 until positive). In PowerShell, -3 % 7 gives -3 (truncated), so crypto code normalizes: (($x % $n) + $n) % $n."
},
{"title": "Diffie-Hellman with pocket numbers",
"body": "Two strangers agree on public prime p and base g, each picks a secret, and they derive a SHARED secret over a public channel. The magic: (g^a)^b mod p = (g^b)^a mod p = g^(ab) mod p. An eavesdropper sees g, p, and the public values but cannot feasibly recover a or b (the discrete logarithm problem).\n\nWorked example (with solution):\nPublic: p = 23, g = 5. Alice secret a = 6, Bob secret b = 15.\nAlice public: 5^6 mod 23. 5^2=25->2; 5^4 = 2^2=4; 5^6 = 5^4 x 5^2 = 4x2 = 8 mod 23. Alice sends 8.\nBob public: 5^15 mod 23. 5^8 = 4^2 = 16; 5^15 = 5^8 x 5^4 x 5^2 x 5^1 = 16x4x2x5 = 640 mod 23. 23x27=621; 640-621=19. Bob sends 19.\nShared: Alice computes 19^6 mod 23; Bob computes 8^15 mod 23. Both equal 5^(6x15) mod 23 = 5^90 mod 23.\nCompute 5^90 mod 23: order of 5 mod 23 divides 22; 5^11 mod 23? 5^2=2,5^4=4,5^8=16, 5^11=5^8*5^2*5=16*2*5=160 mod 23 = 160-138=22 = -1. So 5^22 = 1, 5^90 = 5^(88+2) = 1 x 25 mod 23 = 2.\nShared secret = 2. Verify Alice: 19^6 mod 23: 19 = -4; (-4)^2=16; (-4)^4=16^2=256 mod 23 = 256-253=3; (-4)^6 = 3x16=48 mod 23 = 2. Correct - both sides get 2 without ever sending it."
},
{"title": "Toy RSA: encryption you can check by hand",
"body": "RSA: pick primes p, q; n = p*q; choose e coprime to (p-1)(q-1); find d with e*d mod (p-1)(q-1) = 1. Public key (e, n) encrypts: c = m^e mod n. Private key d decrypts: m = c^d mod n. Security rests on factoring n being hard when n is huge; with toy primes you can watch every step.\n\nWorked example (with solution):\n p = 3, q = 11 -> n = 33, phi = (3-1)(11-1) = 20. Choose e = 3 (coprime to 20). Find d: 3d mod 20 = 1 -> d = 7 (21 mod 20 = 1).\nEncrypt m = 5: c = 5^3 mod 33 = 125 mod 33. 33x3=99; 125-99=26. c = 26.\nDecrypt: m = 26^7 mod 33. 26 = -7. (-7)^2=49 mod 33=16. (-7)^4 = 16^2=256 mod 33: 33x7=231, 256-231=25. (-7)^7 = (-7)^4 x (-7)^2 x (-7) = 25x16x(-7) mod 33. 25x16=400 mod 33: 33x12=396, remainder 4. 4x(-7) = -28 mod 33 = 5. m = 5. Round trip verified.\n\nReal RSA uses 2048-bit n; the math is identical, only the numbers are astronomical. Password hashing (bcrypt/Argon2) and TLS key exchange both live on modular arithmetic."
}
],
"cards": [
{"front": "17 mod 5", "back": "2."},
{"front": "Why can you reduce mod n in the middle of a computation?", "back": "(a op b) mod n = ((a mod n) op (b mod n)) mod n for + and x - intermediate reduction never changes the result."},
{"front": "Diffie-Hellman shared secret formula", "back": "Both sides compute g^(ab) mod p: Alice (g^b)^a, Bob (g^a)^b."},
{"front": "What hard problem protects Diffie-Hellman?", "back": "The discrete logarithm problem: given g, p, g^a mod p, recovering a is infeasible for large p."},
{"front": "Toy RSA: p=3, q=11, e=3 - what is n and d?", "back": "n=33, phi=20, d=7 (3x7=21=1 mod 20)."},
{"front": "Encrypt m=5 with toy RSA (e=3, n=33)", "back": "c = 125 mod 33 = 26."},
{"front": "Normalize a possibly-negative PowerShell modulo", "back": "(($x % $n) + $n) % $n."},
{"front": "What does modular arithmetic have to do with hash tables?", "back": "hash mod table_size maps keys to buckets - same remainder idea as clock arithmetic."}
],
"quiz": [
{"q": "(47 x 53) mod 7 =", "choices": ["6", "5", "4", "3"], "answer": 0, "index": 0, "explain": "47 mod 7=5, 53 mod 7=4, 5x4=20 mod 7=6."},
{"q": "-3 mod 7 (mathematical, always non-negative) =", "choices": ["4", "-3", "3", "10"], "answer": 0, "index": 0, "explain": "Add 7: -3+7=4."},
{"q": "In Diffie-Hellman with p=23, g=5, Alice's secret 6, her public value is:", "choices": ["8", "19", "2", "10"], "answer": 0, "index": 0, "explain": "5^6 mod 23 = 8 (computed via 5^2=2, 5^4=4, 5^6=8)."},
{"q": "The shared secret in that exchange equals:", "choices": ["2", "8", "19", "5"], "answer": 0, "index": 0, "explain": "5^90 mod 23 = 2; both sides derive it."},
{"q": "Toy RSA decrypt: c=26, d=7, n=33 gives:", "choices": ["5", "26", "7", "3"], "answer": 0, "index": 0, "explain": "26^7 mod 33 = 5, verified in the notes."},
{"q": "Why must e be coprime to phi(n) in RSA?", "choices": ["So that a modular inverse d exists (e*d = 1 mod phi)", "To make n prime", "To speed up encryption", "To allow negative messages"], "answer": 0, "index": 0, "explain": "d exists iff gcd(e, phi)=1; without d there is no decryption key."},
{"q": "An attacker sees p, g, and both public DH values. What can they NOT feasibly compute?", "back": None, "choices": ["Either private secret (discrete log)", "The prime p", "The base g", "The public values"], "answer": 0, "index": 0, "explain": "Recovering a from g^a mod p is the discrete logarithm problem."},
{"q": "Compute (2^10) mod 7:", "choices": ["2", "4", "1", "0"], "answer": 0, "index": 0, "explain": "2^3=8=1 mod 7, so 2^10 = 2^9 x 2 = 1 x 2 = 2."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M28"],
"drills": [
{"id": "mx04-drill-mod", "title": "Mod Arithmetic Reps",
"items": [
{"prompt": "29 mod 6", "answer": "5", "explain": "24 divisible by 6, remainder 5."},
{"prompt": "(8 + 9) mod 5 via reduction", "answer": "2", "explain": "(3+4) mod 5 = 7 mod 5 = 2."},
{"prompt": "3^4 mod 5", "answer": "1", "explain": "81 mod 5 = 1 (80 divisible)."},
{"prompt": "DH: p=23,g=5, secrets 6 and 15 -> shared secret?", "answer": "2", "explain": "5^90 mod 23 = 2, worked in notes."},
{"prompt": "Toy RSA: n=33, e=3, encrypt m=2", "answer": "8", "explain": "2^3=8 mod 33."},
{"prompt": "-10 mod 7", "answer": "4", "explain": "-10+14=4."}
]}
],
"handsOnLab": {
"id": "mx04-lab",
"title": "Crypto by hand, verified in PowerShell",
"brief": "Implement modpow, Diffie-Hellman, and toy RSA in PowerShell from scratch; verify every hand computation from the notes.",
"steps": [
"Write function ModPow($b,$e,$m) using square-and-multiply with reduction each step (no [bigint] needed for toy sizes, but support it).",
"Reproduce the DH exchange: p=23, g=5, a=6, b=15; assert both sides derive 2.",
"Reproduce toy RSA: n=33, e=3, d=7; encrypt 5 -> 26, decrypt 26 -> 5; assert round trip for all m in 1..32 coprime to 33.",
"Demonstrate the reduction property: show (47*53)%7 equals ((47%7)*(53%7))%7.",
"Time ModPow with 2048-bit-scale numbers using [bigint] to feel why reduction matters (compare with naive b**e then mod).",
"Write a 3-sentence explanation of what DH protects against that you could say in the interview."
],
"deliverable": "PowerShell script with asserts + timing comparison + your 3-sentence DH explanation.",
"checkpoint": "You can run a DH exchange and RSA round trip from memory and explain the discrete-log and factoring assumptions."
},
"mockTask": {"id": "mx04-mock", "type": "choice",
"q": "Interviewer: 'Why can't an eavesdropper who sees the whole Diffie-Hellman exchange compute the shared secret?'",
"choices": ["They would need to solve the discrete logarithm - recover a from g^a mod p - which is infeasible for large primes", "The exchange is encrypted with RSA first", "The secret is never a number, only a hash", "Modular arithmetic is not reversible at all"],
"answer": 0, "explain": "All values are public except the secrets; security = hardness of discrete log, not secrecy of the algorithm."},
"crossLinks": ["il11-network-crypto-foundations--zt-hashing", "il11-network-crypto-foundations--zt-encryption"],
"videos": [],
"vizNotes": [
{"title": "Clock mod explorer", "description": "Interactive mod-12 clock: drag the hand by adding numbers, watch wraparound; toggle to mod-7/mod-23 to show the same idea generalizes."},
{"title": "DH paint-mixing animation", "description": "Classic paint analogy animated: public yellow paint (g,p), Alice adds secret red, Bob adds secret blue; exchanged mixtures combine to the same final color. Show the parallel mod-p numbers underneath each step."}
],
"estimatedMinutes": 260,
"fastTrackEligible": False
},
{
"id": "IL27-MX05",
"code": "IL-27",
"title": "Set Theory: AD Groups & GPO Logic",
"summary": "Unions, intersections, differences, and Venn diagrams applied to the two places infrastructure admins live: Active Directory group nesting and Group Policy scope/filtering. You need this for -> M12/M13 and auditing any access model.",
"objectives": [
"Define union, intersection, difference, complement, and subset, and draw each as a Venn diagram.",
"Model AD group nesting (including nested and circular nesting) as set relationships.",
"Translate GPO scope (links, security filtering, WMI filters) into set operations and predict application.",
"Use set difference to explain deny-vs-allow and 'exception group' patterns.",
"Apply inclusion-exclusion to count effective memberships without double-counting."
],
"notes": [
{"title": "Sets, Venn diagrams, and the five operations",
"body": "A set is a collection of distinct things. A = {users in Finance}, B = {laptop owners}. Union A u B: in either. Intersection A n B: in both. Difference A - B: in A but not B. Complement A': everything not in A. Subset A c B: every member of A is in B.\n\nVenn diagrams make these visual: two overlapping circles; the lens is the intersection, the crescent is the difference. Inclusion-exclusion counts the union without double-counting: |A u B| = |A| + |B| - |A n B|.\n\nWorked example (with solution):\n200 users: 120 in Finance (F), 90 own laptops (L), 60 are in both.\nOnly Finance (F - L) = 120 - 60 = 60. Only laptops (L - F) = 90 - 60 = 30. Both = 60. Neither = 200 - (60+30+60) = 50.\nCheck via inclusion-exclusion: |F u L| = 120 + 90 - 60 = 150; neither = 200 - 150 = 50. Consistent."
},
{"title": "AD groups are sets (nesting is subset)",
"body": "An AD security group IS a set of principals. Nesting group G2 inside G1 makes G2 a subset of G1's effective membership: every member of G2 is effectively in G1. Token bloat, the classic AD headache, is inclusion-exclusion failing you: a user's token lists every group in their transitive closure, and deeply nested groups multiply SIDs.\n\nCircular nesting (A in B, B in A) is legal in AD and means A and B have identical effective membership - the sets are equal. AGDLP (Accounts -> Global -> Domain Local -> Permissions) is a set pipeline: each stage is a subset relationship that keeps the permission sets manageable.\n\nWorked example (with solution):\nG_Helpdesk has 8 direct users. G_Support contains G_Helpdesk plus 4 direct users. G_Admins contains G_Support plus 2 direct users.\nEffective members: |G_Helpdesk| = 8. |G_Support| = 8 + 4 = 12 (subsets don't double count). |G_Admins| = 12 + 2 = 14.\nIf you grant 'log on as batch' to G_Admins, the affected set is exactly those 14 - audit by expanding the transitive closure, never by eyeballing direct members."
},
{"title": "GPO scope as set operations",
"body": "A GPO applies to: (objects under linked OUs/Site/Domain) INTERSECT (security filtering: Authenticated Users or listed groups with Apply permission) INTERSECT (WMI filter true) MINUS (deny Apply permission) MINUS (Block Inheritance, unless Enforced). That single sentence predicts every 'why didn't my policy apply' ticket.\n\nDeny beats allow in security filtering: the effective set is (Allow set) - (Deny set). An 'exception group' pattern is literally set difference: policy applies to All_Laptops minus Kiosk_Devices.\n\nWorked example (with solution):\nGPO linked to OU=Sales (300 computer objects). Security filtering: GG_Sales_Laptops (180 members, all in OU=Sales). WMI filter: SELECT * FROM Win32_OperatingSystem WHERE Version LIKE '10.%' (matches 150 of the 180). Deny group: GG_NoPolicy (10 members, all in the 150).\nApplied set = 300 n 180 n 150 - 10 = 150 - 10 = 140 computers.\nIf the helpdesk asks 'why didn't it hit PC-77', check each set in order: in OU? in GG_Sales_Laptops? OS match? in deny group? The first 'no' is the answer - set logic turns guessing into a checklist."
}
],
"cards": [
{"front": "|A u B| in terms of |A|, |B|, |A n B|", "back": "|A| + |B| - |A n B| (inclusion-exclusion)."},
{"front": "What does nesting G2 inside G1 mean as sets?", "back": "G2 becomes a subset of G1's effective membership."},
{"front": "GPO application as a set formula", "back": "(Linked scope) n (security filter) n (WMI true) - (deny Apply) - (blocked inheritance unless enforced)."},
{"front": "Why does deny beat allow in security filtering?", "back": "Effective set = Allow set minus Deny set; deny removes membership explicitly."},
{"front": "What is the 'exception group' pattern as sets?", "back": "Policy scope = base set - exception set (set difference)."},
{"front": "Circular group nesting means what about the two groups?", "back": "Identical effective membership - the sets are equal."},
{"front": "200 users, 120 in F, 90 in L, 60 in both: how many in neither?", "back": "50 (union = 150)."},
{"front": "What is a transitive closure in AD group terms?", "back": "All groups a principal belongs to directly or through any depth of nesting - the full effective set."}
],
"quiz": [
{"q": "A=Finance (120), B=laptop owners (90), both=60. How many are in A - B?", "choices": ["60", "30", "90", "150"], "answer": 0, "index": 0, "explain": "120 - 60 = 60."},
{"q": "G2 (8 users) nested in G1 (4 direct users). Effective members of G1?", "choices": ["12", "8", "4", "32"], "answer": 0, "index": 0, "explain": "8 + 4 = 12; nesting adds the subset once."},
{"q": "A GPO is linked to an OU but Block Inheritance is set and the GPO is NOT enforced. It applies to:", "choices": ["no objects under that OU", "all objects under that OU", "only the OU object itself", "only admins"], "answer": 0, "index": 0, "explain": "Block Inheritance removes it from the applied set unless Enforced overrides."},
{"q": "Security filtering allows GG_A (100 users); deny Apply on GG_B (10 users, all in GG_A). Effective target count?", "choices": ["90", "100", "10", "110"], "answer": 0, "index": 0, "explain": "Allow set minus deny set: 100 - 10 = 90."},
{"q": "Which set operation models 'users who are in Finance but do NOT own laptops'?", "choices": ["Difference (F - L)", "Union", "Intersection", "Complement of F"], "answer": 0, "index": 0, "explain": "Difference keeps members of F excluding L."},
{"q": "Two groups nested in each other (A in B, B in A) have:", "choices": ["identical effective membership", "no members", "only direct members", "an error in AD"], "answer": 0, "index": 0, "explain": "Mutual subsets are equal sets; AD permits this."},
{"q": "WMI filter matches 150 of 180 security-filtered computers; deny group has 10 of those 150. GPO hits:", "choices": ["140", "150", "170", "180"], "answer": 0, "index": 0, "explain": "180 n 150 - 10 = 140."},
{"q": "AGDLP nesting exists primarily to:", "back": None, "choices": ["keep permission sets manageable via subset pipelines", "speed up logons", "encrypt group traffic", "replace OUs"], "answer": 0, "index": 0, "explain": "Accounts->Global->Domain Local->Permissions stages subset relationships so ACLs stay small."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M12", "IL27-M13"],
"drills": [
{"id": "mx05-drill-sets", "title": "Set Operation Reps",
"items": [
{"prompt": "|A|=50, |B|=30, |A n B|=10: |A u B|?", "answer": "70", "explain": "50+30-10."},
{"prompt": "Complement of 'laptop owners' among 200 users where 90 own laptops", "answer": "110 users", "explain": "200-90."},
{"prompt": "GPO: scope 300, filter 180 (subset of scope), WMI 150 (subset), deny 10 (subset) -> applied?", "answer": "140", "explain": "150-10."},
{"prompt": "Name the operation: 'all Finance users except contractors'", "answer": "Set difference", "explain": "Finance - Contractors."},
{"prompt": "If every member of G_Junior is in G_Staff, G_Junior is a ___ of G_Staff", "answer": "subset", "explain": "Subset definition."},
{"prompt": "Union of two disjoint sets of 40 and 25", "answer": "65", "explain": "Disjoint: intersection 0, sum directly."}
]}
],
"handsOnLab": {
"id": "mx05-lab",
"title": "Access Audit: model a real OU/GPO/group design as sets",
"brief": "Build a PowerShell set toolkit (union/intersect/difference on object arrays) and use it to audit a simulated AD structure for GPO application and group overlap.",
"steps": [
"Create simulated data: 3 OUs with computer lists, 4 groups with overlapping membership, 2 GPOs with scope/filter/deny definitions (as hashtables).",
"Write functions Union-Set, Intersect-Set, Diff-Set operating on arrays of names.",
"Compute each GPO's applied computer set with the full formula; print counts.",
"Find the overlap (intersection) of the two GPOs' applied sets - these machines get both policies; flag any conflict risk.",
"Compute each group's transitive closure with a recursive expander; detect the planted circular nesting and report the equal sets.",
"Write the audit summary: for each GPO, one sentence stating its applied set in plain English."
],
"deliverable": "PowerShell set toolkit + audit script output + plain-English GPO scope sentences + circular-nesting finding.",
"checkpoint": "You can predict GPO application and group effective membership with set arithmetic before ever opening a console."
},
"mockTask": {"id": "mx05-mock", "type": "choice",
"q": "A policy must apply to all laptops EXCEPT kiosks, and kiosks are a subset of laptops. The correct construction is:",
"choices": ["Security filter on Laptops group minus deny Apply on Kiosks group (set difference)", "Two separate GPOs, one for each", "Link the GPO to the Kiosks OU only", "WMI filter on the word 'kiosk' in the hostname"],
"answer": 0, "explain": "Base set minus exception set = exactly the target; deny Apply implements the difference."},
"crossLinks": [],
"videos": [],
"vizNotes": [
{"title": "Venn builder", "description": "Drag-and-drop Venn: two/three circles labeled with AD groups; click regions to highlight union/intersection/difference with live member counts from a sample dataset."},
{"title": "GPO scope pipeline", "description": "Animated funnel: OU scope -> security filter -> WMI filter -> deny removal, objects dropping out at each stage with counts, ending in the applied set."}
],
"estimatedMinutes": 220,
"fastTrackEligible": False
},
{
"id": "IL27-MX06",
"code": "IL-27",
"title": "Probability & Statistics for Reliability: MTBF, MTTR & SLA Math",
"summary": "Availability arithmetic, SLA downtime budgets, serial vs parallel systems, and reading p95 like an operator - the statistics that justify every HA design and every SLA conversation. You need this for -> M31/M35 and talking reliability in the interview.",
"objectives": [
"Compute availability from MTBF and MTTR and convert between nines and downtime budgets.",
"Calculate serial-system and parallel (redundant) system availability from component values.",
"Translate SLA percentages (99%, 99.9%, 99.95%, 99.99%) into allowed downtime per month/year.",
"Explain expected value and use it to compare backup/HA options by cost of downtime.",
"Interpret mean vs median vs p95 latency and explain why p95 drives user experience."
],
"notes": [
{"title": "Availability: the one formula",
"body": "Availability A = MTBF / (MTBF + MTTR). MTBF (mean time between failures) measures reliability; MTTR (mean time to repair) measures recoverability. A system that fails yearly but recovers in an hour: A = 8760 / 8761 = 99.9886%. A system that fails monthly but recovers in 5 minutes: A = 730 / 730.083 = 99.9886%. Same nines, totally different operational feel - the second one pages you 12x more often.\n\nUnavailability U = 1 - A. Downtime per year = U x 8760 hours. Memorize the nines: 99% = 3.65 days/yr (87.6h); 99.9% = 8.76h/yr (43.8 min/month); 99.95% = 4.38h/yr (21.9 min/month); 99.99% = 52.6 min/yr (4.38 min/month); 99.999% = 5.26 min/yr.\n\nWorked example (with solution):\nA file server has MTBF = 2000 hours, MTTR = 4 hours. Availability?\nA = 2000 / 2004 = 0.998004 = 99.80%. Yearly downtime = 0.001996 x 8760 = 17.5 hours. That misses a 99.9% SLA (budget 8.76h) - you need either higher MTBF or lower MTTR. Halving MTTR to 2h: A = 2000/2002 = 99.9001%, downtime 8.75h - just inside. MTTR is usually the cheaper lever: monitoring, runbooks, and tested restores."
},
{"title": "Serial vs parallel: the architecture math",
"body": "Serial (every component must work): A_system = A1 x A2 x ... x An. Availability MULTIPLIES DOWN - three 99.9% components in series give 99.7%. Every dependency you add costs nines.\n\nParallel (redundant, any one suffices): U_system = U1 x U2 (unavailabilities multiply), so A = 1 - (1-A1)(1-A2). Two 99% components in parallel: U = 0.01 x 0.01 = 0.0001 -> A = 99.99%. Redundancy buys nines fast - IF failures are independent. Shared power, shared switch, or the same bad patch break independence, and the math silently lies.\n\nWorked example (with solution):\nWeb tier: 2 load-balanced servers, each 99.5% available, sharing one 99.9% switch. What is tier availability?\nParallel servers: U = 0.005 x 0.005 = 0.000025 -> A_servers = 99.9975%.\nSeries with switch: 0.999975 x 0.999 = 0.998975 = 99.8975%.\nThe single switch dominates - the 'HA' pair is really a 99.9% system wearing a 99.9975% costume. This is why network redundancy (stacked switches, dual NICs) comes before server redundancy in real designs."
},
{"title": "SLA budgets, expected value, and p95",
"body": "An SLA is a downtime BUDGET, not a promise of uptime. 99.9% monthly = 43.8 minutes of allowed outage. Error budgets (from SRE practice) say: spend the budget on risky changes while budget remains; freeze when exhausted. If you burned 40 minutes in week one, week two is change-freeze territory.\n\nExpected value: EV = sum(probability x outcome). A $500 redundant PSU that prevents a 2%-annual-chance 8-hour outage on a system costing $10k/hour in downtime: EV of loss without it = 0.02 x 8 x 10000 = $1,600/yr. The PSU pays for itself 3x over - that is the entire business case for HA in one line.\n\nPercentiles: p50 (median) is the typical experience; p95 is what your unhappiest 5% feel; p99 the worst 1%. Averages hide sins - a 50ms average with a 5s p99 means 1 in 100 users rage-quits. Operators watch p95/p99, not the mean.\n\nWorked example (with solution):\nMonthly latencies (ms): 40, 45, 42, 48, 44, 41, 46, 43, 47, 900. Mean = 129.6ms, median = 44.5ms, p95 ~ 900ms.\nReport the mean and you claim '130ms typical' - wrong; 9 of 10 users saw ~44ms and one saw 900ms. The p95 tells the true story: the system is fine except for a tail you must investigate (GC pause? noisy neighbor?). Always pair the median with p95."
}
],
"cards": [
{"front": "Availability formula", "back": "A = MTBF / (MTBF + MTTR)."},
{"front": "Yearly downtime budget for 99.9%", "back": "8.76 hours/year (43.8 min/month)."},
{"front": "Yearly downtime budget for 99.99%", "back": "52.6 minutes/year."},
{"front": "Two 99% components in parallel: system availability?", "back": "99.99% (U = 0.01 x 0.01 = 0.0001)."},
{"front": "Three 99.9% components in series:", "back": "99.7% (0.999^3 = 0.997)."},
{"front": "Why can redundancy math lie?", "back": "It assumes independent failures; shared power/network/patches correlate failures."},
{"front": "Mean 130ms, median 44ms, p95 900ms - what do you investigate?", "back": "The tail: something makes ~5-10% of requests 20x slower; the mean hid it."},
{"front": "Expected value of a 2%-annual 8h outage at $10k/h", "back": "$1,600/year expected loss (0.02 x 8 x 10000)."}
],
"quiz": [
{"q": "MTBF 2000h, MTTR 4h. Availability?", "choices": ["99.80%", "99.90%", "99.98%", "99.60%"], "answer": 0, "index": 0, "explain": "2000/2004 = 0.998004."},
{"q": "Yearly downtime at 99.95%?", "choices": ["4.38 hours", "8.76 hours", "52.6 minutes", "21.9 hours"], "answer": 0, "index": 0, "explain": "0.0005 x 8760 = 4.38h."},
{"q": "Two 99.5% servers in parallel give:", "choices": ["99.9975%", "99.0%", "99.75%", "100%"], "answer": 0, "index": 0, "explain": "U = 0.005^2 = 0.000025 -> A = 99.9975%."},
{"q": "Adding that parallel pair behind a single 99.9% switch yields about:", "choices": ["99.90%", "99.9975%", "99.80%", "99.99%"], "answer": 0, "index": 0, "explain": "0.999975 x 0.999 = 0.998975 - the switch dominates."},
{"q": "A 99.9% SLA was breached by 2 hours in a month. Over budget by:", "choices": ["~76 minutes", "exactly 2 hours", "0 - SLAs reset", "43.8 minutes"], "answer": 0, "index": 0, "explain": "Budget 43.8 min; 120 - 43.8 = 76.2 min over."},
{"q": "Halving MTTR from 4h to 2h on MTBF 2000h changes availability from 99.80% to:", "choices": ["99.90%", "99.95%", "99.85%", "99.99%"], "answer": 0, "index": 0, "explain": "2000/2002 = 99.9001%."},
{"q": "p99 latency of 5s with 50ms median means:", "choices": ["1% of requests take ~5s - investigate the tail", "average latency is 5s", "the system is down", "median is miscalculated"], "answer": 0, "index": 0, "explain": "p99 describes the worst 1%; the typical experience is still 50ms."},
{"q": "EV of buying a $500 PSU preventing a 2%/yr, 8h, $10k/h outage:", "back": None, "choices": ["Saves $1,100/yr net ($1,600 EV loss avoided - $500)", "Loses money", "Breaks even exactly", "Cannot be computed"], "answer": 0, "index": 0, "explain": "0.02x8x10000 = $1,600 expected loss; net $1,100."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M35", "IL27-M31"],
"drills": [
{"id": "mx06-drill-sla", "title": "Nines & Budgets Sprint",
"items": [
{"prompt": "MTBF 8760h, MTTR 8.76h: availability?", "answer": "99.9%", "explain": "8760/8768.76 = 0.999."},
{"prompt": "Monthly budget at 99.95%", "answer": "21.9 minutes", "explain": "0.0005 x 43800 min."},
{"prompt": "Two 99.9% components in series", "answer": "99.8%", "explain": "0.999^2 = 0.998001."},
{"prompt": "Three 99% components in parallel", "answer": "99.9999%", "explain": "U = 0.01^3 = 1e-6."},
{"prompt": "EV: 5%/yr chance of 4h outage at $25k/h", "answer": "$5,000/yr", "explain": "0.05x4x25000."},
{"prompt": "p95 = 900ms on 1000 requests: how many were slower?", "answer": "~50", "explain": "5% of 1000."}
]}
],
"handsOnLab": {
"id": "mx06-lab",
"title": "Reliability Calculator: model your homelab's nines",
"brief": "Build a PowerShell availability toolkit and use it to find the cheapest path from your homelab's current nines to 99.9%.",
"steps": [
"Write functions Get-Availability(MTBF,MTTR), Get-YearlyDowntime(A), Get-SerialAvailability(@A), Get-ParallelAvailability(@A).",
"Model your homelab: list 5 components with estimated MTBF/MTTR (be honest), compute series availability.",
"Identify the dominant unavailability contributor (the serial term closest to 1 in U).",
"Propose two fixes: (a) halve its MTTR, (b) add a parallel redundant unit; compute both new system availabilities and costs.",
"Compute EV of each fix vs a $5k/h downtime cost at your estimated failure rate; pick the winner with math.",
"Write the one-paragraph business case you would give a manager."
],
"deliverable": "PowerShell toolkit + before/after availability model + EV comparison + business-case paragraph.",
"checkpoint": "You can compute system nines, name the dominant failure term, and justify HA spend with expected value."
},
"mockTask": {"id": "mx06-mock", "type": "choice",
"q": "Interviewer: 'Our file server is 99.5% available and the business wants 99.9%. What's your first move?'",
"choices": ["Measure MTBF and MTTR separately - if MTTR dominates, invest in monitoring/runbooks/restores before buying hardware", "Buy a second server immediately", "Promise 99.99% to be safe", "Move everything to the cloud"],
"answer": 0, "explain": "A = MTBF/(MTBF+MTTR): you cannot fix what you haven't decomposed; MTTR is usually the cheaper lever."},
"crossLinks": [],
"videos": [],
"vizNotes": [
{"title": "Nines ladder", "description": "Interactive ladder 90%..99.999%: hover each rung to see yearly/monthly/daily downtime budget animate as a filling bar. Toggle MTTR slider to watch availability move."},
{"title": "Series vs parallel circuit", "description": "Circuit diagram: components as bulbs in series (one fails = dark) vs parallel (all must fail = dark); slider per-component availability, system nines update live; 'shared switch' toggle shows correlated-failure collapse."}
],
"estimatedMinutes": 240,
"fastTrackEligible": False
},
{
"id": "IL27-MX07",
"code": "IL-27",
"title": "Queuing Basics for Infrastructure",
"summary": "Little's Law, utilization, and why everything melts at 100% - the math of ticket queues, helpdesk staffing, server request queues, and backup windows. You need this for -> M34/M36 and sizing anything with a line.",
"objectives": [
"State Little's Law (L = lambda x W) and apply it to tickets, requests, and backup jobs.",
"Compute utilization rho = lambda / mu and explain why queues explode as rho approaches 1.",
"Distinguish arrival rate, service rate, and wait time, and measure each from real data.",
"Size a ticket queue / support rotation with basic queuing intuition.",
"Explain how queuing applies to backup windows, patching waves, and login storms."
],
"notes": [
{"title": "Little's Law: the one equation of every queue",
"body": "L = lambda x W. L = average number in the system (waiting + being served), lambda = arrival rate (jobs/hour), W = average time each job spends in the system (hours). It holds for ANY queue - helpdesk tickets, print spoolers, TCP connections, backup jobs - regardless of distributions.\n\nRearrange freely: W = L / lambda (how long will I wait given the line I see?), lambda = L / W (what arrival rate does this backlog imply?).\n\nWorked example (with solution):\nThe ticket queue holds steady at 40 open tickets; the team closes 10 per day. Average ticket age?\nlambda = 10/day, L = 40 -> W = 40/10 = 4 days. A user filing today waits ~4 days on average.\nManagement wants 1-day turnaround without hiring: need W=1 -> L = lambda x W = 10 x 1 = 10 open tickets max. Either cut arrivals (self-service) or raise service rate - the math allows no third option."
},
{"title": "Utilization and the hockey-stick curve",
"body": "Utilization rho = lambda / mu, where mu = service rate (max jobs/hour the server/team can complete). rho < 1 is stable; rho >= 1 means the queue grows forever. The cruelty: wait time doesn't grow linearly - for the simplest queue (M/M/1), average wait = 1/(mu - lambda), which EXPLODES as lambda approaches mu.\n\nAt rho = 0.5, waits are mild. At rho = 0.9, waits are ~9x the service time. At rho = 0.99, ~99x. This is why a server at 'only' 90% CPU during a login storm feels dead, and why running any shared resource above ~70-80% sustained utilization is asking for a queueing catastrophe at the first burst.\n\nWorked example (with solution):\nA backup server writes at mu = 12 jobs/hour. Arrivals: 10 jobs/hour at night.\nrho = 10/12 = 0.833. M/M/1 average time in system W = 1/(mu - lambda) = 1/(12-10) = 0.5 hour per job.\nAdd two more nightly jobs (lambda = 12): rho = 1.0 - the queue NEVER drains; backlog grows all night. Add just one (lambda=11): W = 1/(12-11) = 1 hour - doubling the wait from one extra job/hour. The knee of the curve is brutal: small arrival increases near saturation cause huge wait increases."
},
{"title": "Queues you will actually size",
"body": "Helpdesk staffing: if tickets arrive at 6/hour and each takes 20 min (mu = 3/hour per tech), one tech gives rho = 6/3 = 2 - impossible. Two techs: mu = 6, rho = 1.0 - still unstable (no headroom for bursts). Three techs: mu = 9, rho = 0.67 - healthy with burst headroom. Staffing math is queuing math.\n\nPatching waves: 500 machines, deployment tool does 50/hour (mu), maintenance window 4 hours needs lambda <= 125/hour - fine sequentially, but if all 500 check in at once (thundering herd), the queue is 500 deep and W = 500/50 = 10 hours. Stagger with randomized check-in offsets (splay) to flatten lambda.\n\nLogin storms (Monday 9 AM), backup windows, DHCP lease renewals after an outage - every 'everything is slow at the same time' incident is a queue with rho momentarily >= 1. The fix is always one of: raise mu (faster service), lower lambda (stagger/splay), or add parallel servers (more checkout lanes).\n\nWorked example (with solution):\nAfter a power outage, 2000 devices request DHCP simultaneously. Server handles mu = 100 leases/sec. How long until the last device gets an address, and what would cut it in half?\nW_last = L/mu = 2000/100 = 20 seconds of pure queue drain (plus service time). To halve: double mu (faster server/two servers = 200/sec -> 10s), or halve L by prestaging (shorter lease backlog). Note the first devices wait ~0s, the last waits ~20s - the queue is unfair by arrival order, which is why 'my laptop got an IP but the printer didn't' after outages."
}
],
"cards": [
{"front": "Little's Law", "back": "L = lambda x W (avg in system = arrival rate x avg time in system)."},
{"front": "40 open tickets, 10 closed/day: average ticket age?", "back": "4 days (W = L/lambda)."},
{"front": "Utilization rho =", "back": "lambda / mu (arrival rate over service rate). rho >= 1 = queue grows forever."},
{"front": "M/M/1 average time in system", "back": "W = 1 / (mu - lambda)."},
{"front": "mu=12/hr, lambda=11/hr: average time in system?", "back": "1 hour (1/(12-11)) - vs 30 min at lambda=10."},
{"front": "Why does 90% utilization feel so much worse than 70%?", "back": "Wait grows as 1/(mu-lambda) - the hockey-stick knee near rho=1."},
{"front": "Three ways to fix an overloaded queue", "back": "Raise mu (faster/more servers), lower lambda (stagger/splay), add parallel servers."},
{"front": "What is a thundering herd / login storm in queuing terms?", "back": "lambda momentarily >> mu: a huge L arrives at once and drains at mu."}
],
"quiz": [
{"q": "A queue holds 60 print jobs steady; printer finishes 30/hour. Average job time in system?", "choices": ["2 hours", "30 minutes", "1 hour", "4 hours"], "answer": 0, "index": 0, "explain": "W = 60/30 = 2h."},
{"q": "mu = 12/hr, lambda = 10/hr. Utilization?", "choices": ["0.83", "1.2", "0.5", "2.0"], "answer": 0, "index": 0, "explain": "10/12 = 0.833."},
{"q": "At lambda = 12, mu = 12, the queue is:", "choices": ["unstable - grows without bound", "empty", "at exactly 12 jobs", "draining"], "answer": 0, "index": 0, "explain": "rho = 1: arrivals match max service; any burst accumulates forever."},
{"q": "Tickets arrive 6/hr, each takes 20 min. Minimum techs for stability?", "choices": ["3 (2 gives rho=1.0, no headroom)", "2", "1", "4"], "answer": 0, "index": 0, "explain": "Per tech mu=3/hr; 2 techs -> rho=1.0 unstable; 3 -> rho=0.67."},
{"q": "2000 DHCP requests at once, mu=100/sec. Last device waits about:", "choices": ["20 seconds", "2 seconds", "200 seconds", "0 seconds"], "answer": 0, "index": 0, "explain": "2000/100 = 20s drain."},
{"q": "Best fix for a Monday 9 AM login storm queue?", "choices": ["Stagger logins / add parallel servers (cut lambda or raise mu)", "Buy faster disks only", "Reboot the DC", "Increase password length"], "answer": 0, "index": 0, "explain": "Queue fix = lower lambda (splay) or raise mu (capacity)."},
{"q": "Little's Law holds for:", "choices": ["any queue, regardless of arrival/service distributions", "only M/M/1 queues", "only ticket systems", "only networks"], "answer": 0, "index": 0, "explain": "L = lambda*W is distribution-independent in steady state."},
{"q": "Backup window 4h, tool does 50 machines/hour. Max fleet without staggering?", "back": None, "choices": ["200 machines", "500 machines", "50 machines", "400 machines"], "answer": 0, "index": 0, "explain": "50 x 4 = 200; beyond that lambda x W exceeds the window."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M34", "IL27-M36"],
"drills": [
{"id": "mx07-drill-little", "title": "Little's Law Reps",
"items": [
{"prompt": "L=25, lambda=5/hr: W?", "answer": "5 hours", "explain": "25/5."},
{"prompt": "Want W=2h with lambda=8/hr: max L?", "answer": "16", "explain": "8x2."},
{"prompt": "mu=20/hr, lambda=15/hr: rho?", "answer": "0.75", "explain": "15/20."},
{"prompt": "mu=20/hr, lambda=15/hr: M/M/1 W?", "answer": "12 minutes", "explain": "1/(20-15)=0.2h=12min."},
{"prompt": "Same server, lambda rises to 19/hr: W?", "answer": "60 minutes", "explain": "1/(20-19)=1h - 5x the wait from +4 arrivals."},
{"prompt": "Name the three queue fixes", "answer": "Raise mu, lower lambda, add parallel servers", "explain": "Capacity, demand-shaping, parallelism."}
]}
],
"handsOnLab": {
"id": "mx07-lab",
"title": "Queue Simulator: watch the hockey stick",
"brief": "Simulate an M/M/1 queue in PowerShell, plot wait vs utilization, and use it to size a patching wave.",
"steps": [
"Write a discrete-event M/M/1 simulator: exponential interarrivals (lambda), exponential service (mu), 10k jobs; record average W.",
"Validate against theory: run lambda=8, mu=10; compare simulated W to 1/(mu-lambda)=0.5h.",
"Sweep lambda from 1 to 9.9 (mu=10); print W per rho and observe the knee (describe where it bends).",
"Apply to patching: 500 machines, tool mu=50/hr. Simulate all-at-once arrival vs arrivals splayed over 2h; compare max W.",
"Size a helpdesk: arrivals 6/hr, 20-min handle time; simulate 2 vs 3 techs (M/M/c approx via mu scaling) and report W.",
"Write the one-paragraph 'why we stagger' justification with your numbers."
],
"deliverable": "Simulator script + validation output + sweep table + patching/helpdesk sizings + justification paragraph.",
"checkpoint": "You can simulate any queue, find its knee, and size capacity or staggering from the numbers."
},
"mockTask": {"id": "mx07-mock", "type": "choice",
"q": "Interviewer: 'Patching 500 machines takes 10 hours but our window is 4. What do you do?'",
"choices": ["Show the math: need mu >= 125/hr - add distribution points/parallel streams or stagger across windows; you cannot negotiate with arithmetic", "Patch faster by skipping testing", "Extend the window unilaterally", "Patch only half the fleet"],
"answer": 0, "explain": "L/mu <= W constrains you; the levers are raise mu, lower L per window, or parallelize."},
"crossLinks": [],
"videos": [],
"vizNotes": [
{"title": "Hockey-stick plotter", "description": "Live plot of M/M/1 wait vs rho 0..0.99: draggable lambda slider, wait curve bends upward dramatically; marker flags the 0.7-0.8 'design zone'."},
{"title": "Ticket queue tank", "description": "Animated tank: inflow pipe (lambda) vs drain (mu); sliders for both; water level = L, color shifts red as rho->1; burst button injects a login storm."}
],
"estimatedMinutes": 220,
"fastTrackEligible": False
},
{
"id": "IL27-MX08",
"code": "IL-27",
"title": "Big-O for Scripting: Why Your Loop Is Slow",
"summary": "Complexity intuition for admins: recognize O(n^2) before it eats your afternoon, prefer O(n log n), and measure with Measure-Command. You need this for -> M16 and writing fleet scripts that finish.",
"objectives": [
"Define Big-O informally and rank O(1), O(log n), O(n), O(n log n), O(n^2).",
"Identify the complexity of single loops, nested loops, and common cmdlets.",
"Explain why 'for each user, query AD again' is O(n^2)-ish and how to fix it with one bulk query.",
"Use Measure-Command to compare two approaches on real data.",
"Choose the right tool (hash table vs array search) using complexity reasoning."
],
"notes": [
{"title": "What Big-O means for an admin",
"body": "Big-O describes how work GROWS with input size n. O(1): constant - a hash table lookup takes the same time for 10 or 10 million entries. O(log n): halving each step - binary search; 1M entries take ~20 steps. O(n): one pass - reading every line once. O(n log n): sorting. O(n^2): nested loops - for each of n users, scan all n computers.\n\nThe admin translation: O(n^2) is fine at n=50 (2,500 ops) and a disaster at n=50,000 (2.5 BILLION ops). When a script 'worked in the lab but dies in production', 90% of the time n grew and the complexity was quadratic.\n\nWorked example (with solution):\nScript A: foreach ($u in $users) { Get-ADUser $u } with 5,000 users at 0.2s per query = 1,000s (~17 min). Script B: $all = Get-ADUser -Filter * -Properties * once (5s), then hash lookup per user (O(1) each): 5 + 5000x0.0001 = ~5.5s.\nSpeedup: ~180x. The fix wasn't faster hardware - it was replacing n server round-trips (O(n) with a huge constant) with one bulk fetch plus O(1) lookups. Constants matter too: an O(n) with a 0.2s network constant beats an O(n log n) in-memory sort at small n, but loses as n grows."
},
{"title": "Spotting n-squared in the wild",
"body": "The classic admin n-squared: nested iteration over two collections. 'For each computer, check if it's in the stale list' with -contains on an ARRAY is O(n x m): each -contains scans the array. With 10k computers and a 10k stale list, that's 100M comparisons.\n\nFixes: (1) hash set - put the stale list in a [hashtable] or HashSet, lookups become O(1): total O(n+m). (2) Sort both and merge in one pass: O(n log n). (3) Let the server do it: one LDAP filter instead of client-side loops.\n\nString building is the other trap: $s += $line in a loop copies the whole string each time -> O(n^2) characters copied. Use [System.Text.StringBuilder] or collect in an array and -join once: O(n).\n\nWorked example (with solution):\nCompare: array -contains vs hashtable lookup over 20,000 items, 5,000 lookups.\nArray: 5,000 lookups x avg 10,000 comparisons = 50M comparisons. Hashtable: 5,000 x ~1 = 5,000.\nMeasure-Command { 1..5000 | % { $array -contains $_ } } vs Measure-Command { 1..5000 | % { $hash.ContainsKey($_) } } typically shows 100-1000x difference. The lesson: data structure choice IS algorithm choice. An array is a list; a hashtable is an index - and you already know from databases that indexes beat scans."
},
{"title": "Measuring, sorting, and searching",
"body": "Never guess - measure: Measure-Command { ... } reports real elapsed time. Compare candidate approaches on production-scale data (or a faithful fraction) before committing. If doubling n quadruples time, you found your n-squared.\n\nSorting costs O(n log n): Sort-Object on 100k objects is fine; on 10M rows, do it in the database (indexed ORDER BY) not in PowerShell. Searching: linear scan O(n) vs binary search O(log n) - but binary search needs sorted data; if you search once, the sort cost dominates, so just scan. If you search 1,000 times, sort once (O(n log n)) then binary-search (O(log n) each).\n\nPipeline streaming is O(n) memory-friendly: Get-Content big.log | Where-Object {...} processes line by line. $(Get-Content big.log) first loads everything - same O(n) time but O(n) memory, and on a 10GB log that's the difference between running and crashing.\n\nWorked example (with solution):\nTask: find which of 50,000 AD users logged on in the last 30 days (have lastLogonTimestamp).\nBad: foreach user { Get-ADUser $u -Properties lastLogonTimestamp } - 50k queries, ~2.8 hours at 0.2s each.\nGood: Get-ADUser -Filter 'lastLogonTimestamp -ge $cutoff' -Properties lastLogonTimestamp - one server-side indexed query, seconds.\nBest lesson: the fastest code is the code the server runs for you. Push filters to AD/SQL (WHERE/LDAP filter), keep PowerShell for what servers can't express."
}
],
"cards": [
{"front": "Rank: O(1), O(log n), O(n), O(n log n), O(n^2)", "back": "Fastest to slowest growth: constant < logarithmic < linear < linearithmic < quadratic."},
{"front": "Why does 'foreach user { Get-ADUser $user }' scale badly?", "back": "n server round-trips with a large per-call constant; one bulk query + O(1) hash lookups is ~100x faster."},
{"front": "Array -contains in a loop over m items is:", "back": "O(n x m) - each -contains scans; use a hashtable for O(1) lookups."},
{"front": "Why is $s += $line in a loop quadratic?", "back": "Each += copies the whole string; use StringBuilder or collect-and-join for O(n)."},
{"front": "How do you prove which approach is faster?", "back": "Measure-Command on production-scale data; doubling n -> 4x time reveals n-squared."},
{"front": "When is binary search worth it?", "back": "Many searches on the same data: sort once O(n log n), then O(log n) per search."},
{"front": "Pipeline vs $( ) collection on a 10GB log:", "back": "Same O(n) time, but pipeline streams O(1) memory vs O(n) memory - streaming doesn't crash."},
{"front": "The fastest filter for 50k AD users by lastLogonTimestamp?", "back": "Server-side LDAP filter in one Get-ADUser call, not 50k client-side queries."}
],
"quiz": [
{"q": "A nested loop over 50,000 users x 50,000 computers performs about:", "choices": ["2.5 billion iterations", "100,000 iterations", "50,000 iterations", "2.5 million iterations"], "answer": 0, "index": 0, "explain": "n^2 = 2.5e9."},
{"q": "Replacing array -contains with hashtable lookups changes per-lookup cost from:", "choices": ["O(n) to O(1)", "O(1) to O(n)", "O(n^2) to O(n)", "O(log n) to O(1)"], "answer": 0, "index": 0, "explain": "Scan becomes hash probe."},
{"q": "Binary search on 1,048,576 sorted entries takes about:", "choices": ["20 comparisons", "1,048,576 comparisons", "524,288 comparisons", "1 comparison"], "answer": 0, "index": 0, "explain": "log2(2^20) = 20."},
{"q": "Doubling input quadruples runtime. The complexity is:", "choices": ["O(n^2)", "O(n)", "O(log n)", "O(2^n)"], "answer": 0, "index": 0, "explain": "(2n)^2 = 4n^2."},
{"q": "Best fix for 'foreach ($c in $computers) { if ($staleArray -contains $c) ... }'?", "choices": ["Put $staleArray in a hashtable/HashSet first", "Add more RAM", "Run it twice", "Sort the output"], "answer": 0, "index": 0, "explain": "O(1) lookups collapse O(n*m) to O(n+m)."},
{"q": "Sorting 100k objects with Sort-Object is roughly:", "choices": ["O(n log n) - fine at this size", "O(1)", "O(n^2) - avoid always", "free"], "answer": 0, "index": 0, "explain": "Comparison sorts are n log n; 100k is comfortable."},
{"q": "Why stream Get-Content through the pipeline instead of $( )?", "choices": ["O(1) memory vs O(n) - big files don't exhaust RAM", "It runs in O(log n) time", "It sorts automatically", "No difference"], "answer": 0, "index": 0, "explain": "Streaming processes line-by-line; collection loads all."},
{"q": "50k per-user AD queries at 0.2s each take ~2.8 hours. One bulk query takes ~5s. The lesson:", "back": None, "choices": ["Push work to the server; n round-trips lose to one indexed query", "AD is slow", "PowerShell cannot handle 50k users", "0.2s is too slow a constant"], "answer": 0, "index": 0, "explain": "Server-side filtering beats client-side loops by orders of magnitude."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M16"],
"drills": [
{"id": "mx08-drill-bigo", "title": "Complexity Spotting",
"items": [
{"prompt": "Single loop over n items", "answer": "O(n)", "explain": "One pass."},
{"prompt": "Nested loop, n x n", "answer": "O(n^2)", "explain": "Quadratic."},
{"prompt": "Hashtable lookup", "answer": "O(1)", "explain": "Constant average."},
{"prompt": "Binary search, sorted, n=1M", "answer": "O(log n) ~ 20 steps", "explain": "Halving."},
{"prompt": "Sort-Object on n items", "answer": "O(n log n)", "explain": "Comparison sort."},
{"prompt": "$s += $line x 10k lines", "answer": "O(n^2) char copies - use StringBuilder", "explain": "Repeated full-string copy."}
]}
],
"handsOnLab": {
"id": "mx08-lab",
"title": "The 180x Fix: bulk-fetch vs per-object queries",
"brief": "Prove the complexity lesson with measurements: build the slow version and the fast version of a user-audit script, measure both, and explain the gap.",
"steps": [
"Generate 5,000 fake user objects (PSCustomObject) as your dataset.",
"Slow version: simulate a 5ms 'server round trip' per user with Start-Sleep -Milliseconds 5 inside a foreach; Measure-Command it.",
"Fast version: one bulk 'fetch' (single 50ms sleep) into a hashtable keyed by name; then O(1) lookups; Measure-Command it.",
"Compute the speedup ratio and project both to 100,000 users (multiply: linear projection is fair here - explain why).",
"Repeat the experiment for array -contains vs hashtable ContainsKey with 20k items x 2k lookups.",
"Write the rule-of-thumb card: three 'smells' of slow scripts and their fixes."
],
"deliverable": "Both scripts + Measure-Command outputs + projection math + rule-of-thumb card.",
"checkpoint": "You can smell O(n^2) in a script on sight and prove the fix with measurements."
},
"mockTask": {"id": "mx08-mock", "type": "choice",
"q": "Your audit script takes 3 hours on 40k machines. It does 'foreach machine { query CMDB API }'. First optimization?",
"choices": ["Bulk-fetch the CMDB data once into a hashtable, then O(1) lookups - kills n API round-trips", "Buy a faster workstation", "Run it overnight", "Split into 4 scripts"],
"answer": 0, "explain": "The n round-trips dominate; one bulk fetch + hash lookups is the complexity fix, not hardware."},
"crossLinks": [],
"videos": [],
"vizNotes": [
{"title": "Growth race", "description": "Animated race: n dots processed by O(n) vs O(n^2) vs O(log n) runners as n slider grows 10..100k; quadratic runner visibly stalls, with live op-count readouts."},
{"title": "Hashtable vs scan", "description": "Side-by-side: 10k-item array scan (highlight sweeps per lookup) vs hashtable (single probe); run 100 lookups and watch the cumulative time bars diverge."}
],
"estimatedMinutes": 220,
"fastTrackEligible": False
}
]
