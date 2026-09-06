---
title: Virtualization and Deployment
date: 2026-08-24 
tags: cs
slug: virtualization_and_deployment
---

A desirable thing in computer science is to decouple the program from its execution environment. Yet, a full abstraction of the low-level execution is likely impossible, so in practice the goal is more modest: to build deployment systems that provide consistent and predictable execution environments across different and potentially failing hardware machines. In concrete terms, the program needs CPU time, memory while it is executing, files and network connections, compatible libraries and configuration, and somewhere durable for the data that must outlive it. None of these is unlimited or inherently private. So how do we achieve reliable provisioning of these resources? Let's "re-derive" the current solution from the ground-up.

To start, consider that programs have to share and compete for finite hardware resources, but they must not interfere with one another. The operating system handles much of this problem through [virtualization](https://en.wikipedia.org/wiki/Virtualization): it replaces direct access to hardware with managed abstractions. Each program can then behave as if the resources were its own. 

**Execution**. For the CPU, the main abstraction is the [process](https://en.wikipedia.org/wiki/Process_(computing)). A logical CPU executes one instruction stream at a time, so the kernel shares it among runnable processes. It periodically saves the state of one process and restores another in a [context switch](https://en.wikipedia.org/wiki/Context_switch). The scheduler decides which process runs next. Together, these mechanisms virtualize CPU time and form the basis of multitasking and [time-sharing](https://en.wikipedia.org/wiki/Time-sharing). Processes run in user mode and cannot execute privileged instructions; they must use system calls to ask the kernel to act on their behalf.

**Memory**. Memory is virtualized in a similar way. Each process sees its own [virtual address space](https://en.wikipedia.org/wiki/Virtual_address_space) and uses virtual rather than physical addresses. The processor's [memory-management unit](https://en.wikipedia.org/wiki/Memory_management_unit) consults [page tables](https://en.wikipedia.org/wiki/Page_table) to map virtual pages to physical page frames. Protection bits control whether a page may be read, written, or executed. Two processes can therefore use the same virtual address without referring to the same location in RAM. The kernel can also map a physical page into several processes when sharing is useful. A [virtual memory](https://en.wikipedia.org/wiki/Virtual_memory) system may move inactive pages to persistent storage, but its central purpose is address translation and isolation, not simply providing more memory than the available RAM.

**Persistence**. Persistent storage is virtualized through higher-level abstractions, mainly [files and directories](https://en.wikipedia.org/wiki/File_system). Applications read and write named byte sequences instead of addressing raw disk blocks. The file system maps names and file offsets to blocks on a local or remote storage device. It also maintains metadata and permissions, and provides mechanisms for recovering a consistent structure after a crash. On Unix-like systems, an open file is represented by a [file descriptor](https://en.wikipedia.org/wiki/File_descriptor). These abstractions let many applications share storage without depending on a disk's physical layout or device interface. Unlike the volatile state of a process, files can survive after the process exits or the machine restarts.

**Environment**. These abstractions are enough to execute a program, but the program may still require a particular interpreter and particular versions of its libraries. Installing every dependency system-wide creates conflicts: two programs may need incompatible versions of the same package. A virtual environment gives each program a separate location for its dependencies, so one program can be upgraded without changing the environment of another.

As a Python example, [`python -m venv .venv`](https://docs.python.org/3/library/venv.html) creates a directory with a Python executable and a private `site-packages` directory. "Activating" it simply prepends its executable directory to `PATH`, so commands such as `python` and `pip` use that environment by default. Other package managers like [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/concepts.html) apply this idea more broadly - create a directory, called an *environment prefix*, that can contain a custom Python interpreter, native libraries, command-line tools, packages for other languages, etc. Then activate it by adding the executables to `PATH` and setting some relevant environment variables.

This is dependency isolation, not process or security isolation. A virtual environment does not provide a private kernel, network, process tree, memory allocation, or file system. It is also only partly portable: compiled dependencies still target a particular operating system and CPU architecture, and Python environments often contain absolute paths. Dependency specifications or lock files make an environment easier to recreate, but they do not turn it into a virtual machine.

**Security**. A virtual environment separates dependencies, but it does not make them trustworthy. A malicious package may read credentials, modify files, or send data over the network. Keeping code in a `venv` changes where Python finds it, not what it is allowed to do. Ideally what we need is a fully isolated execution environment. Luckily, on Linux [Bubblewrap](https://github.com/containers/bubblewrap) (`bwrap`) can run code in a restricted process sandbox. It uses a few key technologies.

**Namespaces.** A [namespace](https://en.wikipedia.org/wiki/Linux_namespaces) is a kernel object that represents one view of one kind of resource. For example, a mount namespace contains a tree of mounted filesystems; a PID namespace contains mappings between process IDs and processes; and a network namespace contains network interfaces, routes, ports, and sockets. Every process belongs to one instance of each namespace type. In the following example, the host shell uses the original namespace instances, while a sandbox with mount, PID, and network isolation uses a different set. All the instances still live inside the same kernel.

```text
process              mount namespace    PID namespace    network namespace
─────────────────    ───────────────    ─────────────    ─────────────────
host shell                  M0                 P0                 N0
sandboxed program           M1                 P1                 N1

M0: host mount tree         P0: all host PIDs       N0: host network
M1: selected mounts         P1: sandbox PIDs only   N1: loopback only
```

When a process makes a system call, the kernel uses the namespace instance assigned to that process. For the sandboxed program above, `open("/etc/config")` resolves the path through the mount tree in M1. `kill(42)` interprets 42 using P1, and `socket(...)` creates the socket in N1. Bubblewrap does not intercept these calls, it only modifies namespaces.

Each namespace type can be changed independently: a process might receive a private network namespace while continuing to share its parent's mount namespace. A user namespace deserves special attention because it allows unprivileged sandboxing. Bubblewrap can map UID 0 inside the namespace to UID 1000 on the host. It can then perform root-like setup operations on resources owned by the new namespace. Access to host files is still checked as UID 1000, however, so root inside the namespace is not root on the host.

**Filesystem root.** The classic [`chroot`](https://en.wikipedia.org/wiki/Chroot) operation changes how a process resolves `/`, but it does not isolate the mount table, processes, users, or network. It is therefore not a strong security boundary by itself. Bubblewrap uses the same basic idea of giving a process a different root, but combines it with a mount namespace. It creates an empty root on a temporary filesystem, adds selected paths with bind mounts, and then uses [`pivot_root`](https://man7.org/linux/man-pages/man2/pivot_root.2.html) to make that tree the root of the namespace. The old root is detached, so paths that were not explicitly mounted are unreachable.

```text
host path          Bubblewrap operation        visible in sandbox
────────────────   ───────────────────────    ──────────────────
/usr               read-only bind mount   ──> /usr
/project           writable bind mount    ──> /work
temporary memory   new tmpfs              ──> /tmp
/home/alice        not mounted            ──> absent
```

The bind-mounted files are not copies. They are the same underlying files viewed through a different mount table; read-only mount flags decide whether the sandbox may modify them. Bubblewrap can also mount a new `/proc` for an isolated PID namespace and a restricted `/dev`. With PID isolation, the sandbox cannot see host processes and Bubblewrap supplies a minimal PID 1 to reap children. A network namespace can remove external networking entirely, leaving only a loopback interface.



**Control groups.** A namespace controls what a process can see, while a cgroup controls how much CPU, memory, I/O, or how many processes a group may use. A [cgroup](https://en.wikipedia.org/wiki/Cgroups) is an account to which the kernel charges the resource use of a set of processes. Limits apply to the account as a whole: if ten processes belong to a cgroup with a 1 GB memory limit, then they share that 1 GB.

```text
host cgroup hierarchy
└── sandbox.scope
    ├── memory.current              (current memory use)
    ├── memory.max = 1073741824     (1 GB)
    ├── cpu.max    = 50000 100000   (50% of one CPU)
    ├── pids.max   = 128
    └── cgroup.procs                (member process IDs)
```

With cgroups, a memory controller charges pages to the group; when a new allocation would cross `memory.max`, the kernel attempts to reclaim memory and, if that fails, invokes the out-of-memory mechanism within the cgroup. The CPU controller treats `cpu.max = 50000 100000` as a shared budget of 50 milliseconds of CPU time in every 100-millisecond period; after the group spends it, its runnable processes are throttled until the next period. The PID controller rejects the creation of another process once `pids.max` is reached, which prevents a fork bomb from filling the host's process table.

A cgroup need not have a limit: it can be useful merely for measuring a workload or managing all of its processes as a unit. A cgroup namespace is different again: it only changes how this hierarchy appears to a process and does not create limits of its own.

The operating system's abstractions, virtual environments, and process sandboxes let many applications coexist, but one boundary remains: every process depends on the same [kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)). A process cannot choose a different kernel or execute privileged operations as an operating system would. It also cannot remain independent of a kernel failure. To let several users run, administer, or even crash operating systems of their own on one physical computer, the machine itself must be virtualized. This leads to the [virtual machine](https://en.wikipedia.org/wiki/Virtual_machine).

**Virtual machines.** A virtual machine monitor, now called a *hypervisor*, sits between the hardware and several guest operating systems. It presents each guest with virtual CPUs, memory, disks, and devices, making the guest appear to own a computer. Privileged operations transfer control to the hypervisor, which can perform, emulate, or deny them. So we have something like this:

```text
application      application          application
guest OS A       guest OS B            guest OS C
────────────────────────────────────────────────────
             hypervisor / VMM
────────────────────────────────────────────────────
          physical CPU, RAM, disk, NIC
```

The hypervisor preserves the interface expected by the guest while changing what lies behind it. The guest maps program addresses to *guest-physical* addresses, which the hypervisor maps to host RAM. Processor features such as [nested page tables](https://en.wikipedia.org/wiki/Second_Level_Address_Translation) make this efficient. Virtual disks and network cards similarly retain a familiar device interface backed by a host implementation.

VMs let different kernels coexist; each can have its own configuration and administrators, and one guest's crash need not affect another. The cost is that each guest carries its own kernel, boot process, system services, and distribution. This is worthwhile when the kernel boundary matters, but excessive when an application merely needs a process and its libraries (often the case).

**Containers.** Suppose several applications can use the same Linux kernel and don't need simulated processors or guest kernels. They need separate views of processes, filesystems, networks, and identities, plus fair access to shared CPU and memory. A Linux *container* is an ordinary host process launched with kernel mechanisms that provide those properties. It shares the host kernel and makes the same system calls as any other process.

We already discussed the mechanisms that provide the abstraction:

- Namespaces control what a process can see. A PID namespace allows a process to be PID 1 inside the container while having an unrelated PID on the host. Mount namespaces give it a different mount table. Network namespaces give it separate interfaces, routes, ports.
- Cgroups control what a group of processes can use. Without cgroups, a process with a private view of the world could still consume all host memory.

Containers combine these mechanisms with filesystem restrictions, capabilities, and device controls. A Bubblewrapped process can therefore be container-like, but a complete container runtime also manages its image, resource limits, networking, and lifecycle. Containers are lighter than VMs because they share a kernel, but that kernel is also their common security boundary.

```text
container A: app + libraries       container B: app + libraries
  PID/mount/net namespaces           PID/mount/net namespaces
  cgroup limits                      cgroup limits
──────────────────────────────────────────────────────────────
                    one host kernel
──────────────────────────────────────────────────────────────
                   physical hardware
```

**From a container to a portable application.** Isolation alone does not provide the files an application expects. The host would still need the correct interpreter, libraries, certificates, and directory layout. Copying and installing these by hand on every machine would recreate the dependency problem that containers are meant to avoid.

An *image* packages this user-space environment as a read-only filesystem, together with metadata such as the command to start. To create a container, the runtime uses the image as its initial filesystem and adds settings such as mounts, networking, and resource limits. It also adds a small writable layer in which the running application can create and modify files. The image itself remains unchanged, so it can provide the same starting environment to many containers.

```text
build recipe
    │
    ▼
image: application + selected dependencies + metadata
    │
    ▼
runtime settings: ports, secrets, volumes, limits
    │
    ▼
running container: process or process group
```

Images are built in layers: one might contain a base system, the next a language runtime, and the next the application. A layer records only the changes made on top of the previous one, so unchanged layers can be cached and shared. This makes images faster to rebuild and distribute; it does not change the filesystem ultimately seen by the application.

The writable layer belongs to one particular container and normally disappears with it. Durable data must therefore live in a mounted volume or an external service, while configuration and secrets are supplied when the container starts. Updating an application then means building a new image and replacing the old container, not modifying it in place.

Images can be uploaded to a *registry* and downloaded onto another machine. Registries give images convenient names and tags such as `api:v42`, but these labels can be reassigned. A *digest* is a fingerprint calculated from all the image's contents: changing the contents produces a different digest. It therefore identifies the exact image to run.

Docker uses a client-server design. The `docker` command sends requests to `dockerd`, a background server on the host that manages images, networks, and volumes. It delegates container execution to `containerd` and an OCI runtime such as `runc`, which creates the isolated process that the host kernel then runs.

**The cluster problem.** Docker manages containers on one machine. Across many machines, someone must place containers, replace failed ones, and deploy new versions without stopping the service. This is the job of an *orchestrator*.

An orchestrator uses a declarative interface: instead of saying *“run this container on node 7,”* we say *“keep five healthy instances of version v42 running.”* A controller compares this desired state with the actual cluster and acts to close the gap. This loop is called *reconciliation*:

```text
desired state ──> controller ──> actions on machines
      ▲                              │
      └──── observed actual state ───┘
```

If a replica dies, the controller starts another. If it loses the response to an operation, it may repeat it; operations should therefore be idempotent where possible. *“Ensure five replicas”* is safer than *“create one replica.”*

**Kubernetes.** Kubernetes is an orchestrator built around this model. A cluster has a *control plane* and a set of worker machines called *nodes*. The control plane is the coordinating software: it stores the desired state, runs controllers, and uses a scheduler to choose a node for each new workload. Each node runs a *kubelet*, an agent that receives work from the control plane and asks the container runtime to start it. Another aspect, called [consensus](https://en.wikipedia.org/wiki/Consensus_(computer_science)), deals with keeping replicated copies of the control-plane state in agreement when machines fail.

The unit of work is a *Pod*: one or more containers placed on the same node, sharing an IP address and optionally storage. Most Pods contain one application container. A helper container in the same Pod is called a *sidecar*; a proxy, which forwards network traffic, is one common example.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels: { app: api }
  template:
    metadata:
      labels: { app: api }
    spec:
      containers:
        - name: api
          image: registry.example/api@sha256:example
          resources:
            requests: { cpu: "250m", memory: "256Mi" }
            limits:   { cpu: "1", memory: "512Mi" }
```

As an example, the deployment above declares three Pod replicas. The digest pins an exact image; the requests guide scheduling; and the limits cap resource use. Placing Pods resembles a multidimensional [bin packing problem](https://en.wikipedia.org/wiki/Bin_packing_problem): Pods consume several finite node resources, so the scheduler uses heuristics to find a good arrangement. The scheduler chooses nodes, their kubelets start the Pods, and a controller replaces any that disappear. A production deployment also needs health checks, access control, networking, observability, and persistent storage.

Kubernetes is not simply “Docker at scale.” Docker builds and runs containers; Kubernetes coordinates them across machines and can talk directly to runtimes such as containerd or CRI-O. The nodes may themselves be VMs: VMs isolate kernels and tenants, containers divide each node, and Kubernetes coordinates the containers.

**Choosing the boundary.** Kubernetes is useful when cluster scheduling and automatic repair justify its complexity. Simpler or more managed options place the boundary elsewhere:

- **System service:** runs and restarts a process on one machine, often using `systemd`.
- **Docker Compose:** declares several related containers, networks, and volumes on one machine; it is not a cluster scheduler.
- **Platform as a service:** accepts source code or an image while the provider chooses hosts, routing, deployment, and monitoring conventions.
- **Serverless:** accepts a function or service and lets the provider start and scale instances, in exchange for a more constrained runtime.
- **MicroVM:** boots a guest kernel with minimal virtual hardware, giving stronger isolation than a container with more overhead. [Firecracker](https://firecracker-microvm.github.io/) is one implementation.
- **WebAssembly:** runs portable bytecode in a sandbox, but does not transparently run every existing Linux application.

**Conclusion.** Hypervisors let operating systems share hardware. Containers let isolated environments share a kernel. Images make those environments reproducible, and orchestrators keep them running across a cluster. The right stack is likely the smallest one that provides the isolation, portability, and recovery an application needs. The future of computing will likely continue this pattern: raising the abstraction boundary while making the layers beneath it safer, cheaper, and less visible.
