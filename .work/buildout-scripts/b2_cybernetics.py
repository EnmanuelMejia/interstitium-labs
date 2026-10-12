import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_common import merge

D = 'cybernetics'

SIMS = [
    {
        "id": "cybernetics-sim-runaway-scale",
        "title": "The autoscaler that fed on its own alerts",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 2,
        "brief": "At 03:00 the fleet scaled from 12 to 400 instances, then collapsed. The scaling signal came from the monitoring the scaler itself was saturating. Diagnose the loop.",
        "steps": [
            {
                "symptom": "03:00 scale-up triggered by p99 latency alert. Each new instance increased monitoring load, which raised reported latency, which triggered more scale-up.",
                "options": [
                    "Runaway positive feedback: the controller's actions amplified the sensor reading that drove the controller",
                    "A DDoS attack",
                    "Bad deploy at 03:00",
                    "The monitoring agent has a memory leak"
                ],
                "correct": 0,
                "evidence": [
                    ["metrics.txt", "03:00 p99=900ms (12 instances) -> 03:20 p99=2400ms (180 instances) -> 03:40 fleet 400, API down. Monitoring scrape load per instance: constant. Total scrape load grew 33x."],
                    ["scaler-config.txt", "Scale rule: IF p99 > 800ms THEN add 20%. Cooldown: 0s. No damping, no max cap."]
                ],
                "explain": "This is circular causality in production: the effector (new instances) fed the sensor (latency, inflated by scrape load), which re-triggered the controller. Wiener's warning made concrete — a control loop with no damping and a corrupted sensor diverges."
            },
            {
                "symptom": "Positive feedback confirmed. What breaks the loop?",
                "options": [
                    "Add more instances faster",
                    "Introduce negative feedback: cooldown periods, a max instance cap, damping on the scale signal, and a sensor that measures real user latency instead of scrape-loaded latency",
                    "Disable the autoscaler permanently",
                    "Increase the latency threshold to 5000ms"
                ],
                "correct": 1,
                "evidence": [
                    ["control-theory.txt", "Stability requires negative feedback: the correction must oppose the error, with delay and gain tuned so the loop converges instead of oscillating or diverging."],
                ],
                "explain": "You do not fix a control loop by pushing harder — you fix it by making the feedback negative and honest: cooldowns and caps bound the gain, and an uncorrupted sensor closes the loop on reality."
            }
        ],
        "debrief": "Every autoscaler, alert pipeline, and incident response is a control loop. Ask of each one: what is the sensor, what is the effector, is the feedback negative, and what happens at the extremes. Positive feedback always finds the extreme.",
        "points": 15
    },
    {
        "id": "cybernetics-sim-soc-loop",
        "title": "Design the detection-response feedback loop",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "You are designing the SOC's core loop: detection -> triage -> containment -> learning. The CISO asks where automation belongs and where humans belong. Decide the control architecture.",
        "steps": [
            {
                "symptom": "Proposal A: full automation — detect, isolate, remediate, close, no humans. Proposal B: your design.",
                "options": [
                    "Proposal A — speed wins, humans are the bottleneck",
                    "A layered loop: fast inner loop (automated containment on high-confidence, reversible actions) inside a slow outer loop (human review, rule tuning, lessons learned feeding back into detection)",
                    "No automation — analysts handle everything",
                    "Automate only the ticketing"
                ],
                "correct": 1,
                "evidence": [
                    ["incident-review.txt", "Last quarter: 2 false-positive auto-isolations took down payroll. 1 slow human triage let ransomware dwell 6 hours. Both failure modes are loop-design failures."],
                    ["wiener-note.txt", "Control without communication fails; communication without control is noise. The loop needs both machine speed and human judgment, each where it belongs."],
                ],
                "explain": "Cybernetics gives the answer structure: nested loops at different timescales. The fast loop handles what is reversible and high-confidence; the slow loop — humans — handles judgment, novelty, and tuning the fast loop itself. Either extreme fails exactly as the incident review shows."
            },
            {
                "symptom": "The layered loop is approved. Where does the learning feedback go — what does the outer loop actually change?",
                "options": [
                    "It writes the incident report",
                    "It tunes the inner loop: detection thresholds, containment playbooks, confidence scores — every incident updates the controller's parameters",
                    "It hires more analysts",
                    "It buys more tools"
                ],
                "correct": 1,
                "evidence": [
                    ["soc-metrics.txt", "MTTR fell 40% after the outer loop started feeding false-positive analysis back into rule tuning. Same tools, better controller."],
                ],
                "explain": "The outer loop's product is a better inner loop. An incident that does not change a threshold, a playbook, or a score is information that never became control — entropy the organization paid for and threw away."
            }
        ],
        "debrief": "A SOC is a control system regulating the organization's risk state. Design it as nested feedback loops: fast automated inner loops for the reversible and certain, slow human outer loops for judgment — and every incident must tune the machine.",
        "points": 15
    },
    {
        "id": "cybernetics-sim-oscillation",
        "title": "The deploy pipeline that could not decide",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 3,
        "brief": "The canary deployer has rolled forward and back six times in an hour. Each rollback triggers a redeploy, each redeploy triggers a rollback. Find the oscillation source.",
        "steps": [
            {
                "symptom": "18:00 deploy v2.4 -> 18:07 rollback (error budget) -> 18:12 redeploy (metrics recovered) -> 18:19 rollback... six cycles. Error rate hovers exactly at the threshold.",
                "options": [
                    "Hunting oscillation from delayed feedback: the health sensor lags reality, so the controller corrects for a state that no longer exists",
                    "The new version is simply broken",
                    "The old version is simply broken",
                    "Two engineers fighting over the deploy button"
                ],
                "correct": 0,
                "evidence": [
                    ["deployer.log", "18:07 rollback decision used metrics from 17:52 (15-min aggregation lag). 18:12 redeploy used metrics from 18:00 (pre-rollback window). Each decision corrected the previous window's state."],
                    ["metrics-raw.txt", "Actual error rate: stable 0.8%, under the 1% threshold, the entire hour. The controller never saw the present."],
                ],
                "explain": "Delayed feedback turns negative feedback into oscillation: by the time the sensor reports, the system has moved on, so every correction overshoots. The error rate was fine — the controller was steering by a stale map."
            },
            {
                "symptom": "Stale sensor confirmed. What stabilizes the loop?",
                "options": [
                    "Deploy faster to outrun the lag",
                    "Faster sensing plus hysteresis: shorten the aggregation window, and require the signal to clear the threshold by a margin for a sustained period before reversing a decision",
                    "Remove the error-budget gate",
                    "Increase the rollback threshold"
                ],
                "correct": 1,
                "evidence": [
                    ["control-theory.txt", "Two cures for delay-induced oscillation: reduce the delay (faster sensor), and add hysteresis/deadband so the controller does not reverse on noise."],
                ],
                "explain": "Hysteresis is the thermostat principle: the heater does not flip at exactly 20.0 degrees or it chatters forever. A margin plus a dwell time lets the loop settle instead of hunting."
            }
        ],
        "debrief": "Oscillation is the signature of feedback delay. When a system hunts — flapping between states — check the sensor's freshness before blaming the thing being controlled. Faster truth plus hysteresis calms the loop.",
        "points": 20
    },
    {
        "id": "cybernetics-sim-info-overload",
        "title": "The SOC drowned in its own signals",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Alert volume tripled after a new log source came online: 12,000 alerts/day, 3 analysts. True positives are being missed in the flood. The channel is over capacity. Respond.",
        "steps": [
            {
                "symptom": "12,000 alerts/day. Analyst capacity: ~150 investigations/day. Missed: a real credential-stuffing campaign buried at position 9,400.",
                "options": [
                    "Hire 80 analysts",
                    "Treat it as a channel-capacity problem: the signal rate exceeds the receiver's bandwidth, so compress before transmitting — aggregate, deduplicate, prioritize, suppress the known-benign",
                    "Turn off the new log source",
                    "Tell analysts to work faster"
                ],
                "correct": 1,
                "evidence": [
                    ["alert-stats.txt", "Of 12,000 daily alerts: 61% duplicates, 22% known-benign (tuned but not suppressed), 9% informational, 8% actionable. Effective signal: ~960/day."],
                    ["shannon-note.txt", "Information theory: a channel has finite capacity. When the source exceeds it, you encode smarter (compression, prioritization) — you cannot will the channel wider."],
                ],
                "explain": "Shannon's answer applies to SOCs: the analysts are a finite-capacity channel. 92% of the volume is redundancy and noise — compress it out before it reaches the human, and the real signal fits the channel."
            },
            {
                "symptom": "Compression plan approved. What is the correct order of operations?",
                "options": [
                    "Suppress everything and tune later",
                    "Deduplicate first (safe, mechanical), then suppress the known-benign with documented rules, then risk-prioritize the remainder — measuring miss rate at each step",
                    "Prioritize first, dedupe later",
                    "Buy a bigger SIEM"
                ],
                "correct": 1,
                "evidence": [
                    ["rollout.txt", "Dedup: -61% volume, zero miss risk. Known-benign suppression: -22%, each rule peer-reviewed. Prioritization: ranked queue, miss rate monitored weekly."],
                ],
                "explain": "Order by reversibility and risk: mechanical dedup cannot hide signal, documented suppression is auditable, and prioritization keeps the residual risk visible and measured instead of silent."
            }
        ],
        "debrief": "Alert fatigue is an information-theoretic failure, not a morale failure. The fix is encoding: compress redundancy, filter the known-benign, prioritize the rest — and measure what the channel carries, not just its volume.",
        "points": 15
    },
    {
        "id": "cybernetics-sim-homeostasis",
        "title": "Hold the line: homeostasis under attack",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A traffic flood is pushing the API toward its breaking point. You must hold service levels steady — homeostasis — while the attack continues. Choose the control strategy.",
        "steps": [
            {
                "symptom": "Traffic 8x normal, 70% from 200 source IPs with bot signatures. p99 latency climbing, error rate 2% and rising. SLO: 99.9% success.",
                "options": [
                    "Overprovision: spin up 10x capacity and absorb it",
                    "Negative-feedback control: rate-limit the abusive sources, shed low-priority load, serve degraded-but-correct responses — regulate the internal state against the disturbance",
                    "Shut down the API until the attack ends",
                    "Block the entire internet except allowlisted customers"
                ],
                "correct": 1,
                "evidence": [
                    ["capacity.txt", "10x overprovisioning: 40 min to provision, cost 12x, and the botnet can scale faster than we can buy."],
                    ["physio-note.txt", "Homeostasis: the organism does not grow ten hearts under stress — it constricts vessels, prioritizes the brain, sheds heat. Regulate, don't just absorb."],
                ],
                "explain": "Absorption loses to any attacker who can scale; shutdown surrenders. Homeostatic control — sense the disturbance, oppose it proportionally, protect the essential functions — holds the SLO while the storm passes."
            },
            {
                "symptom": "Rate limiting is holding the SLO. The attack shifts: now low-and-slow from 50,000 residential IPs. Your controller's move?",
                "options": [
                    "Give up — it cannot be rate-limited by IP anymore",
                    "Adapt the controller: shift from IP-based to behavior-based signals (request patterns, TLS fingerprints, challenge-response), keeping the same homeostatic goal",
                    "Block all residential IPs",
                    "Raise the rate limits so legitimate users are unaffected"
                ],
                "correct": 1,
                "evidence": [
                    ["adaptation.txt", "Second-order control: when the disturbance changes form, the controller must change its sensor, not its goal. Goal (SLO) is invariant; the means adapt."],
                ],
                "explain": "This is the cybernetic lesson in one move: the goal stays fixed while the control strategy adapts to the disturbance. Rigid controllers break; adaptive controllers hold."
            }
        ],
        "debrief": "Homeostasis is the original control problem: hold the essential variable steady while the environment rages. Sense honestly, oppose proportionally, and when the attack changes shape, change the sensor — never the goal.",
        "points": 15
    }
]

CONSOLES = [
    {
        "id": "cybernetics-console-setpoint",
        "title": "Tune the controller setpoint",
        "console": "generic-web",
        "domain_id": D,
        "difficulty": 1,
        "brief": "In the autoscaler control panel, set the scale-up cooldown to 300 seconds to add damping to the loop, then submit.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Set the 'scale-cooldown-sec' field to 300.",
                "validate": {"action": "set-field", "params": {"id": "scale-cooldown-sec", "value": "300"}},
                "hint": "Set field scale-cooldown-sec to 300."
            },
            {
                "id": "t2",
                "instruction": "Submit the controller configuration form.",
                "validate": {"action": "submit-form", "params": {}},
                "hint": "Click submit on the configuration form."
            }
        ],
        "debrief": "Cooldown is damping made concrete: a pause between corrections so the loop can observe the effect of the last one before issuing the next."
    },
    {
        "id": "cybernetics-console-incident",
        "title": "Open the oscillation incident",
        "console": "ticketing",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Open a P2 ticket for the deploy-pipeline oscillation, assign it to the platform on-call, and move it to in-progress.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a P2 ticket titled 'Deploy pipeline oscillation — 6 flap cycles'.",
                "validate": {"action": "create-ticket", "params": {"title": "Deploy pipeline oscillation — 6 flap cycles", "priority": "P2"}},
                "hint": "Create a P2 ticket titled 'Deploy pipeline oscillation — 6 flap cycles'."
            },
            {
                "id": "t2",
                "instruction": "Assign the ticket to 'platform-oncall'.",
                "validate": {"action": "assign-ticket", "params": {"id": "1", "assignee": "platform-oncall"}},
                "hint": "Assign ticket 1 to platform-oncall."
            },
            {
                "id": "t3",
                "instruction": "Move the ticket to in-progress.",
                "validate": {"action": "update-status", "params": {"id": "1", "status": "in-progress"}},
                "hint": "Update ticket 1 status to in-progress."
            }
        ],
        "debrief": "Oscillation is an incident like any other: ticketed, owned, and worked until the loop is stable."
    },
    {
        "id": "cybernetics-console-firewall",
        "title": "Damp the flood at the edge",
        "console": "firewall",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The botnet's primary source 198.51.100.23 is hammering the API. Drop its traffic on INPUT, then set the INPUT default policy to DROP.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Add a rule dropping all TCP traffic from 198.51.100.23 on INPUT (port 443).",
                "validate": {"action": "add-rule", "params": {"chain": "INPUT", "protocol": "tcp", "port": 443, "source": "198.51.100.23", "action": "DROP"}},
                "hint": "Add an INPUT rule: protocol tcp, port 443, source 198.51.100.23, action DROP."
            },
            {
                "id": "t2",
                "instruction": "Set the INPUT chain default policy to DROP.",
                "validate": {"action": "set-default-policy", "params": {"chain": "INPUT", "policy": "DROP"}},
                "hint": "Set the default policy of the INPUT chain to DROP."
            }
        ],
        "debrief": "Edge filtering is the outermost control loop: oppose the disturbance as far from the core as possible, default-deny the rest."
    },
    {
        "id": "cybernetics-console-siem-rule",
        "title": "Build the oscillation detector",
        "console": "siem-dashboard",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Create a SIEM rule that fires when any host flaps state more than 5 times in 10 minutes, then acknowledge the existing alert ALT-4100.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a detection rule named 'oscillation-flap' with query 'flap_count > 5'.",
                "validate": {"action": "create-rule", "params": {"name": "oscillation-flap", "query": "flap_count > 5"}},
                "hint": "Create a rule named oscillation-flap with query 'flap_count > 5'."
            },
            {
                "id": "t2",
                "instruction": "Acknowledge alert ALT-4100.",
                "validate": {"action": "acknowledge-alert", "params": {"id": "ALT-4100"}},
                "hint": "Click acknowledge on alert ALT-4100."
            }
        ],
        "debrief": "Detecting oscillation is itself a feedback loop: the sensor watches the controllers, and its output tunes them. Control all the way up."
    }
]

MISSIONS = [
    {
        "id": "cybernetics-mission-head-telemetry",
        "title": "Inspect the newest telemetry",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Check the head of the sensor telemetry log to confirm the feed format.",
        "objectives": ["Head sensor-telemetry.log"],
        "checks": [
            {
                "command_pattern": "^head\\s+sensor-telemetry\\.log",
                "expect_contains": "timestamp",
                "hint": "Type: head sensor-telemetry.log"
            }
        ],
        "success_message": "Telemetry format confirmed — the sensor feed is live."
    },
    {
        "id": "cybernetics-mission-tail-telemetry",
        "title": "Read the latest sensor readings",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Tail the telemetry log to see the most recent controller inputs.",
        "objectives": ["Tail sensor-telemetry.log"],
        "checks": [
            {
                "command_pattern": "^tail\\s+sensor-telemetry\\.log",
                "expect_contains": "setpoint",
                "hint": "Type: tail sensor-telemetry.log"
            }
        ],
        "success_message": "Latest readings captured — the controller is seeing fresh data."
    },
    {
        "id": "cybernetics-mission-sort-readings",
        "title": "Sort the latency readings",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Sort the latency readings to find the extremes the controller reacted to.",
        "objectives": ["Sort latency-readings.txt"],
        "checks": [
            {
                "command_pattern": "^sort\\s+latency-readings\\.txt",
                "expect_contains": "900",
                "hint": "Type: sort latency-readings.txt"
            }
        ],
        "success_message": "Readings sorted — the spike that triggered scale-up is visible."
    },
    {
        "id": "cybernetics-mission-grep-errors",
        "title": "Find controller errors",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Search the controller log for ERROR lines around the incident window.",
        "objectives": ["Grep controller.log for 'ERROR'"],
        "checks": [
            {
                "command_pattern": "^grep\\s+ERROR\\s+controller\\.log",
                "expect_contains": "ERROR",
                "hint": "Type: grep ERROR controller.log"
            }
        ],
        "success_message": "Controller errors isolated — the decision points are mapped."
    },
    {
        "id": "cybernetics-mission-diff-config",
        "title": "Diff the controller configs",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Compare the stable controller config against the one deployed before the incident.",
        "objectives": ["Diff controller-v1.conf against controller-v2.conf"],
        "checks": [
            {
                "command_pattern": "^diff\\s+controller-v1\\.conf\\s+controller-v2\\.conf",
                "expect_contains": "cooldown",
                "hint": "Type: diff controller-v1.conf controller-v2.conf"
            }
        ],
        "success_message": "Config drift found — the removed cooldown explains the runaway."
    },
    {
        "id": "cybernetics-mission-count-samples",
        "title": "Count the telemetry samples",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Count how many telemetry samples the sensor recorded during the incident.",
        "objectives": ["Count lines in sensor-telemetry.log with wc"],
        "checks": [
            {
                "command_pattern": "^wc\\s+-l\\s+sensor-telemetry\\.log",
                "expect_contains": "sensor-telemetry.log",
                "hint": "Type: wc -l sensor-telemetry.log"
            }
        ],
        "success_message": "Sample count captured — the observation window is quantified."
    },
    {
        "id": "cybernetics-mission-echo-setpoint",
        "title": "Echo the current setpoint",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Print the controller's current setpoint value to confirm what the loop is regulating toward.",
        "objectives": ["Echo the setpoint value 800"],
        "checks": [
            {
                "command_pattern": "^echo\\s+800",
                "expect_contains": "800",
                "hint": "Type: echo 800"
            }
        ],
        "success_message": "Setpoint confirmed — the loop's target is explicit."
    }
]

if __name__ == '__main__':
    merge('cybernetics', sims=SIMS, consoles=CONSOLES, missions=MISSIONS)
