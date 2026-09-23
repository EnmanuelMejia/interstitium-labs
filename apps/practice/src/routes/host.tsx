import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/host")({
  component: HostPage,
});

const steps = [
  {
    name: "Boot Windows, not the RHEL disk",
    text: "The secondary M.2 keeps RHEL only until you choose to erase it. If that system is the one running, reboot and start Windows 11 Pro. This session cannot see your disks and cannot press the keys.",
  },
  {
    name: "Name the disk before you touch it",
    text: "In an administrator PowerShell, list number, name, serial, and size. The Windows disk is the one that owns C:. The M.2 is the other disk. If you are not certain, stop. Clear-Disk on the wrong number erases Windows.",
  },
  {
    name: "Turn on Hyper-V",
    text: "Windows 11 Pro is the hypervisor. Proxmox is a different operating system: it would replace a boot disk, so it is not the host while Windows is. Enable Hyper-V, then reboot.",
  },
  {
    name: "Erase only the M.2 you named",
    text: "After the reboot, clear that disk number, initialize it GPT, and format one NTFS volume for virtual disks. Copy off anything you still need first. The RHEL install on that SSD does not survive this.",
  },
  {
    name: "Put the guest on that volume",
    text: "Hyper-V Manager, Generation 2, the VHDX stored on the new volume. A Default Switch is enough for a lab. An external switch is for a guest that should be a machine on the LAN. Do not bind that to Wi-Fi and expect it to behave.",
  },
  {
    name: "Install the guest from an ISO you downloaded",
    text: "A current RHEL ISO from Red Hat, or Fedora if you do not want a subscription. Modern RHEL kernels already speak Hyper-V disk and network. Leave the host enough RAM that the console stays alive.",
  },
];

export function HostPage() {
  return (
    <main>
      <p className="text-xs tracking-[0.18em] text-muted uppercase">Host · ThinkStation P920</p>
      <h1 className="mt-3 max-w-[16ch] text-hero leading-[0.95]">Windows is the hypervisor</h1>
      <p className="mt-5 max-w-[68ch] text-lg text-fg/85">
        Windows 11 Pro stays on the metal. Hyper-V runs the guests. The secondary M.2 becomes the virtual-disk volume
        only after you have named it. Nothing here can format that drive for you.
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
        {`# Administrator PowerShell, after Windows is the running system.
# Read this. Do not clear a disk in the same sitting as the first look.
Get-Disk | Format-Table Number, FriendlyName, SerialNumber, Size, PartitionStyle
Get-Partition | Format-Table DiskNumber, DriveLetter, Size, Type

Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
# Reboot. Then set $n to the M.2 that does not own C:.

$n = -1
if ($n -lt 0) { throw "Set the disk number first." }
Clear-Disk -Number $n -RemoveData -Confirm:$false
Initialize-Disk -Number $n -PartitionStyle GPT
New-Partition -DiskNumber $n -UseMaximumSize -DriveLetter V
Format-Volume -DriveLetter V -FileSystem NTFS -NewFileSystemLabel VMStore`}
      </pre>
    </main>
  );
}
