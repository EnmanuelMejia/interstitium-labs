import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/host")({
  component: HostPage,
});

const steps = [
  {
    name: "Confirm the machine",
    text: "The ThinkStation P920 is a dual Xeon Scalable workstation. RHEL 10 requires x86-64-v3, which means AVX2. Those Xeons have it. On any Linux already installed, grep -o avx2 /proc/cpuinfo must print something. A blank result will not boot RHEL 10.",
  },
  {
    name: "Install RHEL 10.2 on the metal",
    text: "Boot the 10.2 ISO in UEFI mode, not a guest. Register the system and update it before you add virtual machines. This box is the hypervisor. Do not install the labs site on the metal if you can avoid it.",
  },
  {
    name: "Turn on KVM",
    text: "Install qemu-kvm, libvirt, virt-install, and virt-viewer. Start the modular libvirt sockets. Then run virt-host-validate. A WARN about the IOMMU is acceptable until you actually assign a device.",
  },
  {
    name: "Give the guests a bridge",
    text: "A NAT network is enough for one labs VM. A bridge is what you want if the guest should be a machine on your LAN. Do not bind the bridge to a Wi-Fi interface and expect it to behave.",
  },
  {
    name: "Create the labs guest",
    text: "One RHEL or Fedora guest, virtio disk and virtio net, a few vCPUs, and RAM you can spare. Leave the host enough memory that the console stays alive. The guest runs Node 22, which RHEL 10 ships, and serves the site. The browser stage is the real-time piece. It does not need a second GPU.",
  },
  {
    name: "Serve the public site from the guest",
    text: "On the guest, install git and nginx, then clone EnmanuelMejia/interstitium-labs and point nginx at the docs directory. The catalog fix is already on main: a failed catalog load is plain text, not HTML. This preview is the folded practice app. It is not that static tree, so do not expect the 3D stage on the guest until that app is published into the repo.",
  },
  {
    name: "Blender, not Unreal",
    text: "Install Blender on the host if the P920 has a Quadro and you want to model the mark. Do not bind that GPU to vfio unless you have another way to see the console. Unreal Pixel Streaming is not running, and this page will not pretend the signaling URL is set.",
  },
];

export function HostPage() {
  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Host · ThinkStation P920</p>
      <h1 className="mt-3 max-w-[16ch] text-hero leading-[0.95]">RHEL 10.2 as the hypervisor</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        Bare metal on the P920. KVM for the guests. The labs stay a guest so a bad experiment does not take the
        console with it. Commands below match the RHEL 10 virtualization guide, not a custom kernel.
      </p>
      <ol className="mt-10 max-w-[72ch] space-y-8">
        {steps.map((step, i) => (
          <li key={step.name}>
            <p className="text-xs tracking-[0.14em] text-muted uppercase">
              0{i + 1} · {step.name}
            </p>
            <p className="mt-2 text-fg/90">{step.text}</p>
          </li>
        ))}
      </ol>
      <pre className="mt-10 max-w-[72ch] overflow-x-auto rounded-xl border border-line bg-surface p-4 text-sm leading-relaxed text-fg/90">
        {`# On the metal, after RHEL 10.2 is registered
sudo dnf install -y qemu-kvm libvirt virt-install virt-viewer
sudo dnf install -y libguestfs-tools virt-top
for drv in qemu network nodedev nwfilter secret storage interface; do
  sudo systemctl enable --now virt\${drv}d{,-ro,-admin}.socket
done
sudo virt-host-validate

# Pick the guest OS variant from the first column, then install.
osinfo-query os | grep -i rhel
sudo virt-install \\
  --name interstitium \\
  --memory 8192 --vcpus 4 \\
  --disk size=40,bus=virtio \\
  --os-variant REPLACE_WITH_OSINFO_ID \\
  --network network=default,model=virtio \\
  --cdrom /var/lib/libvirt/images/rhel-10.2-x86_64-dvd.iso

# On the guest, after it has a network
sudo dnf install -y git nginx
sudo git clone https://github.com/EnmanuelMejia/interstitium-labs.git /srv/interstitium
sudo sed -i 's|root /usr/share/nginx/html|root /srv/interstitium/docs|' /etc/nginx/nginx.conf
sudo systemctl enable --now nginx
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload`}
      </pre>
      <p className="mt-4 max-w-[68ch] text-sm text-muted">
        Official procedure:{" "}
        <a
          className="underline"
          href="https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/configuring_and_managing_linux_virtual_machines/preparing-rhel-to-host-virtual-machines"
          target="_blank"
          rel="noreferrer"
        >
          Preparing RHEL to host virtual machines
        </a>
        . RHEL 10.2 shipped 20 May 2026, kernel 6.12, and it will not boot a CPU without AVX2.
      </p>
    </main>
  );
}
