module = {
  "id": "IL28-M24",
  "code": "IL-28",
  "title": "Docker Networking, Volumes & Compose",
  "summary": "Connect containers with bridge networks and DNS-based service discovery, persist data with volumes versus bind mounts, and define multi-service stacks in an original docker-compose file you bring up yourself.",
  "objectives": [
    "Explain bridge networking and how containers resolve each other by name.",
    "Publish container ports to the host with -p and describe what EXPOSE does not do.",
    "Compare host, bridge, and none network modes and choose appropriately.",
    "Contrast named volumes with bind mounts for data persistence.",
    "Write and operate a multi-service docker-compose stack from scratch."
  ],
  "notes": [
    {
      "title": "Bridge networks: isolation plus automatic DNS",
      "body": """The default docker0 bridge — and any user-defined bridge network — gives each container its own IP on a private subnet while Docker runs an embedded DNS server at 127.0.0.11 inside every container. The practical magic: on a user-defined bridge network, containers resolve each other by name (or by Compose service name) with zero configuration. Worked example:

$ docker network create appnet
$ docker run -d --name cache --network appnet redis:alpine
$ docker run -d --name web --network appnet nginx:alpine
$ docker exec web wget -qO- --timeout=2 http://cache:6379 | head -c 40

The wget reaches the Redis container via the hostname \"cache\" — Docker's DNS resolved it to the container's bridge IP, and the TCP connection succeeded (Redis replies with a protocol error to HTTP, which is exactly the proof of connectivity we want). On the default bridge this name resolution does NOT work — only user-defined networks get automatic DNS, which is why docker compose creates one per project automatically. Inspect the plumbing with docker network inspect appnet: it lists each attached container, its IPv4 address, and aliases. The mental model: a bridge network is a virtual switch; DNS is the phone book; together they let services find each other by stable names even as container IPs churn across restarts — the same service-discovery idea Kubernetes builds on."""
    },
    {
      "title": "Publishing ports: -p and what EXPOSE does not do",
      "body": """A container's ports are private to its network by default. docker run -p HOST:CONTAINER publishes a container port on a host interface, creating the NAT rule that lets outside traffic in. Worked example:

$ docker run -d -p 8080:80 --name web nginx:alpine
$ curl -s -o /dev/null -w \"%{http_code}\" http://localhost:8080
200

The container listens on 80 (per its EXPOSE 80 metadata); the host forwards localhost:8080 to it. Variants: -p 127.0.0.1:8080:80 binds only the loopback (safer for admin UIs you do not want LAN-exposed); -p 8080:80 with no host IP binds all interfaces; -P publishes every EXPOSEd port on random host ports. Three sharp edges. One: EXPOSE alone publishes nothing — it is documentation (M22); without -p the port stays unreachable from the host. Two: publishing the same host port twice fails — the second container errors on bind, a classic \"works alone, breaks together\" defect. Three: -p on the default bridge plus container-to-container traffic means your app should listen on 0.0.0.0 inside the container, not 127.0.0.1 — binding localhost inside the container accepts only the container's own loopback, and published-port traffic arrives on the container's eth0. When curl fails, check in order: is the app listening on 0.0.0.0, is the port published, is a host firewall blocking it."""
    },
    {
      "title": "Host and none: the other network modes",
      "body": """Bridge is the default, but two other modes matter. Host mode (--network host) removes network isolation entirely: the container shares the host's network namespace, so a process listening on port 80 binds the host's port 80 directly — no -p needed, no NAT overhead. Use it for network-monitoring agents or ultra-low-latency services; avoid it for ordinary apps because any port conflict hits the host and isolation is gone. Note it is a Linux-only feature — Docker Desktop's VM makes host mode behave differently, a favorite interview gotcha. None mode (--network none) gives the container a loopback interface and nothing else: no external connectivity at all. Use it for untrusted batch jobs or security-sensitive one-shot tasks where network exfiltration must be impossible. Worked comparison:

$ docker run --rm --network host nginx:alpine  # binds host's port 80 directly
$ docker run --rm --network none alpine ping -c1 8.8.8.8  # fails: no route

Decision guide: bridge for normal multi-container apps (isolation + DNS), host for agents that must see host traffic, none for compute-only sandboxes. Panels ask \"when would you use host networking?\" expecting the monitoring/low-latency answer plus the port-conflict and Linux-only caveats — not \"for speed\" alone."""
    },
    {
      "title": "Volumes vs bind mounts: where persistent data lives",
      "body": """Container filesystems are ephemeral (M22) — data that must survive needs storage outside the container's writable layer. Named volumes (-v cache-data:/data) are Docker-managed storage in Docker's own directory: portable, easy to back up, and the right default for databases and caches. Bind mounts (-v /host/path:/data) map a specific host directory into the container: transparent and editable from the host, ideal for mounting source code into dev containers or config files. Worked example — proving a named volume persists:

$ docker run -d --name cache -v cache-data:/data redis:alpine
$ docker exec cache redis-cli set greeting hello
OK
$ docker exec cache redis-cli save
OK
$ docker rm -f cache
$ docker run -d --name cache2 -v cache-data:/data redis:alpine
$ docker exec cache2 redis-cli get greeting
hello

Solution walkthrough: the data lived in the cache-data volume, not in either container's writable layer, so destroying the first container lost nothing; the SAVE forced Redis to flush to /data/dump.rdb before removal. Contrast with anonymous volumes (a bare -v /data with no name): they persist too, but with random hash names that accumulate as orphans — always name your volumes. Inspect with docker volume ls and docker volume inspect; reclaim with docker volume prune (destructive — confirm nothing needed first). Rule: volumes for data, bind mounts for code/config you edit on the host."""
    },
    {
      "title": "Compose: the whole stack in one file",
      "body": """docker compose turns a multi-container system into a single declarative YAML file: services, networks, and volumes defined together and managed as one unit (up, down, logs, ps). Here is an original two-service stack — a web frontend plus a Redis cache — of the kind you will run in the lab:

services:
  web:
    image: nginx:alpine
    ports:
      - \"8080:80\"
    networks:
      - appnet
    depends_on:
      - cache
  cache:
    image: redis:alpine
    volumes:
      - cache-data:/data
    networks:
      - appnet

networks:
  appnet:
    driver: bridge

volumes:
  cache-data:

Solution walkthrough, top to bottom: services defines the two containers; web publishes host 8080 to container 80; both join the user-defined bridge appnet, so web resolves the hostname \"cache\" via Docker DNS with no extra config; depends_on orders startup (web starts after cache — note: it orders startup, it does NOT wait for Redis to be ready; readiness needs a healthcheck or wait-for script); cache mounts the named volume at /data for persistence. Networks and volumes sections declare the shared resources once. docker compose up -d brings up the project (named after the directory); docker compose ps, logs, and exec operate per service; docker compose down stops and removes containers but KEEPS volumes, while down -v destroys them too — know the difference before typing."""
    },
    {
      "title": "Operating the stack: the daily compose commands",
      "body": """Writing the file is half the skill; operating it is the other half. The daily command set, each with its purpose. docker compose up -d builds (if needed) and starts everything detached; add --build to force a rebuild after Dockerfile changes — without it, Compose reuses the old image and your fix silently does not deploy, a classic \"but I changed the code\" incident. docker compose ps shows service state at a glance; docker compose logs -f web tails one service's logs; docker compose exec cache redis-cli ping runs a command in the running container (PONG proves Redis is up). Worked debugging session:

$ docker compose up -d
$ docker compose ps
NAME            STATUS
lab-web-1       Up
lab-cache-1     Up
$ docker compose exec cache redis-cli ping
PONG
$ curl -s -o /dev/null -w \"%{http_code}\" http://localhost:8080
200

Every layer verified: both services up, cache answering, web reachable through the published port. For teardown, docker compose down removes containers and the project network but preserves named volumes (data survives); docker compose down -v also deletes volumes (data destroyed — the nuclear option for a fresh start). Two production notes: pin image tags in compose files (redis:alpine is a floating tag — prefer redis:7-alpine after verifying), and keep secrets out of the YAML — use env_file pointing at an untracked .env, never commit credentials into the compose file."""
    }
  ],
  "cards": [
    {"front": "How do containers on a user-defined bridge resolve each other?", "back": "Docker's embedded DNS (127.0.0.11) resolves container/service names automatically — but only on user-defined networks, not the default bridge."},
    {"front": "What does 'docker run -p 8080:80' do, precisely?", "back": "Publishes the container's port 80 on host port 8080 via a NAT rule; without -p, EXPOSE alone leaves the port unreachable from the host."},
    {"front": "Your app binds 127.0.0.1 inside the container and curl to the published port fails. Why?", "back": "Published traffic arrives on the container's eth0, not its loopback — the app must listen on 0.0.0.0."},
    {"front": "When is --network host the right choice, and what are its caveats?", "back": "Network agents or ultra-low-latency services needing the host stack directly; caveats: no isolation, host port conflicts, Linux-only."},
    {"front": "What is --network none for?", "back": "Containers with only loopback and no external networking — untrusted batch jobs or tasks where exfiltration must be impossible."},
    {"front": "Named volume vs bind mount — which for a database, which for dev source code?", "back": "Named volume for the database (managed, portable, persists); bind mount for source code (editable live from the host)."},
    {"front": "You removed a container but kept its named volume. Is the data still there?", "back": "Yes — volumes live outside the container's writable layer; reattach the same volume name to a new container."},
    {"front": "What does depends_on guarantee — and what does it NOT guarantee?", "back": "Startup order only — it does not wait for the dependency to be ready; use healthchecks or wait-for scripts for readiness."},
    {"front": "docker compose down vs docker compose down -v?", "back": "down removes containers/network but keeps volumes (data survives); down -v also destroys volumes."},
    {"front": "You changed the Dockerfile but 'docker compose up -d' did not pick it up. Why?", "back": "Compose reuses the existing image without --build — the fix never built. Use up -d --build after Dockerfile changes."},
    {"front": "How do you run a one-off command in a running Compose service?", "back": "docker compose exec <service> <command>, e.g. docker compose exec cache redis-cli ping."},
    {"front": "Where do secrets belong in a Compose setup?", "back": "In an untracked .env referenced via env_file — never hardcoded in the compose YAML."}
  ],
  "quiz": [
    {"q": "Two containers on a user-defined bridge: web reaches the cache at hostname 'cache'. What provides this?", "choices": ["The default bridge's DNS", "Docker's embedded DNS on user-defined networks", "/etc/hosts edited by hand", "The host's DNS server"], "answer": 1, "explain": "User-defined bridge networks get automatic DNS resolution by container/service name; the default bridge does not."},
    {"q": "EXPOSE 80 is set but you ran without -p. Can the host reach the app?", "choices": ["Yes — EXPOSE publishes automatically", "No — EXPOSE is metadata; publishing needs -p", "Only on Linux", "Only with --network host"], "answer": 1, "explain": "EXPOSE documents intent; reachability requires an explicit publish flag."},
    {"q": "docker run -p 8080:80 fails with 'port is already allocated'. Cause and fix?", "choices": ["The image is corrupt — rebuild", "Another process/container holds host port 8080 — stop it or choose a free host port", "Use EXPOSE instead", "Add --network host"], "answer": 1, "explain": "Host ports are exclusive; find the holder (or pick another port)."},
    {"q": "When would you choose --network host?", "choices": ["For every web app, for speed", "For a network-monitoring agent needing the host's interfaces — accepting no isolation and Linux-only", "To isolate the container", "It is the default"], "answer": 1, "explain": "Host mode suits agents/sniffers; ordinary apps lose isolation and risk host port conflicts."},
    {"q": "A batch job must not reach the network at all. Which mode?", "choices": ["bridge", "host", "none", "overlay"], "answer": 2, "explain": "none gives only loopback — no external connectivity, so exfiltration is impossible."},
    {"q": "Redis data must survive container replacement. Which mount?", "choices": ["Anonymous volume", "Named volume at /data — survives container removal and reattaches by name", "Bind mount of /tmp", "No mount — the writable layer persists"], "answer": 1, "explain": "Named volumes persist outside the container lifecycle; the writable layer dies with the container."},
    {"q": "In the compose file, what does depends_on: [cache] guarantee for web?", "choices": ["cache is ready to serve before web starts", "cache's container starts before web's — not readiness", "web restarts if cache dies", "They share a filesystem"], "answer": 1, "explain": "depends_on orders startup only; readiness needs healthchecks or wait-for logic."},
    {"q": "After editing the Dockerfile, 'docker compose up -d' shows the old behavior. What was missed?", "choices": ["docker compose down first", "--build, so the image actually rebuilds", "A version bump in the YAML", "Nothing — it rebuilds automatically"], "answer": 1, "explain": "Compose reuses the cached image unless --build forces a rebuild."},
    {"q": "You need a completely fresh start including wiping cached data. Which command?", "choices": ["docker compose down", "docker compose down -v", "docker compose stop", "docker compose restart"], "answer": 1, "explain": "down -v also destroys named volumes; plain down preserves them."}
  ],
  "weight": 1,
  "prerequisiteFor": ["IL28-M25"],
  "drills": [
    {
      "id": "il28-m24-networking",
      "title": "Container networking drill",
      "items": [
        {"prompt": "Publish container port 80 on host port 8080, loopback only. Give the flag.", "answer": "-p 127.0.0.1:8080:80", "explain": "Binding the host IP to loopback keeps the service off the LAN."},
        {"prompt": "From container web, prove DNS resolves container cache on their shared network.", "answer": "docker exec web wget -qO- --timeout=2 http://cache:6379 (a Redis protocol-error reply proves name resolution + TCP).", "explain": "Any successful TCP to the hostname proves Docker DNS worked."},
        {"prompt": "List containers on network appnet with their IPs. Give the command.", "answer": "docker network inspect appnet", "explain": "Shows attached containers, IPv4 addresses, and aliases."},
        {"prompt": "curl to a published port fails but the app is up. Name three checks in order.", "answer": "App listening on 0.0.0.0 (not 127.0.0.1); port actually published (-p); host firewall allowing it.", "explain": "Inside-out debugging: bind address, publish rule, firewall."},
        {"prompt": "When is host networking justified, and what do you give up?", "answer": "Agents needing host interfaces or extreme low latency; you give up isolation, risk host port conflicts, and it is Linux-only.", "explain": "The complete trade-off, not just 'speed'."},
        {"prompt": "A security review demands a PDF renderer with no network. Which mode and flag?", "answer": "--network none — loopback only, exfiltration impossible.", "explain": "None mode is the sandbox answer."},
        {"prompt": "Why does name resolution fail on the default bridge?", "answer": "Automatic embedded DNS exists only on user-defined networks; the default bridge predates the feature.", "explain": "Always create a network (or let Compose) for multi-container apps."}
      ]
    },
    {
      "id": "il28-m24-volumes-compose",
      "title": "Volumes and Compose drill",
      "items": [
        {"prompt": "Run redis with a named volume at /data. Give the docker run.", "answer": "docker run -d --name cache -v cache-data:/data redis:alpine", "explain": "Named volume cache-data mounted at the data dir."},
        {"prompt": "Prove the volume (not the container) holds the data.", "answer": "Write a key, redis-cli save, remove the container, start a new one on the same volume, read the key back.", "explain": "Data surviving container replacement proves volume persistence."},
        {"prompt": "When do you choose a bind mount over a named volume?", "answer": "For host-editable content: dev source code, config files you iterate on — not for database data.", "explain": "Bind mounts are for the edit loop; volumes are for data."},
        {"prompt": "Write the compose services block for web (nginx:alpine, 8080:80) depending on cache.", "answer": "services:\n  web:\n    image: nginx:alpine\n    ports: ['8080:80']\n    depends_on: [cache]", "explain": "Service, image, published port, startup ordering."},
        {"prompt": "Declare the shared bridge network and named volume in compose.", "answer": "networks:\n  appnet:\n    driver: bridge\nvolumes:\n  cache-data:", "explain": "Top-level networks/volumes sections declare shared resources once."},
        {"prompt": "Tail web's logs and ping Redis through compose. Give both commands.", "answer": "docker compose logs -f web && docker compose exec cache redis-cli ping", "explain": "logs per service; exec runs one-off commands in a running service."},
        {"prompt": "A teammate committed AWS keys in the compose file. What now?", "answer": "Move to untracked .env + env_file, rotate the exposed keys immediately — committed secrets are compromised.", "explain": "Same rule as code: committed secrets are burned secrets."}
      ]
    }
  ],
  "handsOnLab": {
    "id": "il28-m24-lab",
    "title": "Multi-service stack: web + cache",
    "brief": "You will write an original docker-compose stack (nginx web + Redis cache on a custom bridge with a named volume), prove DNS service discovery, prove volume persistence across container replacement, and practice the full operate cycle.",
    "steps": [
      "Set up: mkdir compose-lab && cd compose-lab.",
      "Write compose.yaml exactly as the services/networks/volumes example in the notes (web: nginx:alpine on 8080:80, cache: redis:alpine with cache-data:/data, both on appnet, web depends_on cache).",
      "Bring it up: docker compose up -d, then docker compose ps — both services Up.",
      "Prove the cache: docker compose exec cache redis-cli ping — expect PONG.",
      "Prove DNS discovery: docker compose exec web wget -qO- --timeout=2 http://cache:6379 | head -c 60 — a Redis protocol-error reply proves the hostname 'cache' resolved and TCP connected.",
      "Prove publishing: curl -s -o /dev/null -w '%{http_code}\\n' http://localhost:8080 — expect 200 from nginx.",
      "Prove persistence: docker compose exec cache redis-cli set labkey persisted && docker compose exec cache redis-cli save; then docker compose rm -f -s cache; docker compose up -d; then docker compose exec cache redis-cli get labkey — expect 'persisted'.",
      "Observe ordering limits: docker compose logs cache | head -20 and note that depends_on ordered startup but did not wait for readiness.",
      "Teardown keeping data: docker compose down, then docker volume ls — cache-data still present; bring the stack up again and re-read labkey.",
      "Nuclear teardown: docker compose down -v, confirm the volume is gone, and write stack.md documenting each proof and the down vs down -v difference."
    ],
    "deliverable": "compose.yaml and stack.md with the DNS, publishing, persistence, and teardown proofs.",
    "checkpoint": "PONG from redis-cli; Redis error-reply via hostname 'cache'; 200 from localhost:8080; labkey survives container replacement and plain down, but not down -v."
  },
  "mockTask": {
    "id": "il28-m24-mock",
    "type": "choice",
    "q": "Panel: 'Two containers need to talk, data must survive restarts, and the web port must be reachable. Sketch it.'",
    "choices": ["Both on the default bridge, data in the writable layer, EXPOSE 80", "User-defined bridge network (DNS by service name), named volume for data, -p 8080:80 publishing, app listening on 0.0.0.0", "--network host for both, bind-mount /tmp, no published ports", "One container with both processes, --network none"],
    "answer": 1,
    "explain": "User-defined bridge gives DNS discovery; named volumes survive container replacement; -p publishes explicitly (EXPOSE alone does nothing); 0.0.0.0 binding is required for published traffic. The other options lose data, discovery, or isolation."
  },
  "crossLinks": [],
  "videos": [
    {"title": "Docker Crash Course", "url": "https://www.youtube.com/watch?v=Kyx2PsuwomE", "source": "Traversy Media (YouTube)", "durationMin": 35, "order": 1, "watchBefore": "notes", "blurb": "Fast practical Docker primer covering networking and Compose — a quick refresher before this module's stack lab."}
  ],
  "estimatedMinutes": 0
}
