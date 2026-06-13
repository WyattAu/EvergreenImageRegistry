#include <tunables/global>

profile evergreen-go-runtime flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # Deny all capabilities by default, then allow what Go services need
  deny capability,

  # Go services need setgid/setuid for privilege dropping at startup
  capability chown,
  capability dac_override,
  capability dac_read_search,
  capability fowner,
  capability fsetid,
  capability kill,
  capability net_bind_service,
  capability setgid,
  capability setpcap,
  capability setuid,
  capability sys_chroot,

  # Deny dangerous capabilities
  deny capability sys_admin,
  deny capability sys_boot,
  deny capability sys_module,
  deny capability sys_rawio,
  deny capability sys_time,
  deny capability sys_tty_config,
  deny capability mknod,
  deny capability audit_write,
  deny capability audit_control,
  deny capability setfcap,
  deny capability sys_ptrace,
  deny capability net_admin,
  deny capability net_raw,
  deny capability sys_resource,
  deny capability ipc_lock,
  deny capability ipc_owner,

  # File system access - Go services need read for config/libs, write for data
  / r,
  /lib/** r,
  /lib64/** r,
  /usr/** r,
  /etc/** r,
  /opt/** r,
  /app/** r,
  /config/** r,

  # Go services write data (Prometheus TSDB, Grafana dashboards, Consul data)
  /data/** rw,
  /tmp/** rw,
  /var/** rw,
  /run/** rw,
  /logs/** rw,

  # Deny writes to sensitive host paths
  deny /proc/** w,
  deny /sys/** w,
  deny /boot/** rw,
  deny /media/** rw,
  deny /mnt/** rw,
  deny /dev/** w,

  # Allow specific /proc reads needed by Go runtime
  /proc/self/** r,
  /proc/thread-self/** r,
  /proc/sys/kernel/osrelease r,
  /proc/sys/kernel/hostname r,
  /proc/sys/kernel/uuid r,
  /proc/meminfo r,
  /proc/cpuinfo r,
  /proc/filesystems r,
  /proc/version r,
  /proc/loadavg r,
  /proc/stat r,
  /proc/uptime r,
  /proc/self/fd/** r,
  /proc/self/root/** r,

  # Deny dangerous /proc paths
  deny /proc/sysrq-trigger rw,
  deny /proc/sys/** w,
  deny /proc/kcore rw,
  deny /proc/keys rw,
  deny /proc/latency_stats rw,
  deny /proc/timer_list rw,
  deny /proc/timer_stats rw,
  deny /proc/sched_debug rw,
  deny /proc/acpi/** rw,
  deny /proc/kallsyms rw,
  deny /proc/iomem rw,
  deny /proc/ioports rw,
  deny /proc/bus/** rw,

  # Deny dangerous /sys paths
  deny /sys/firmware/** rw,
  deny /sys/kernel/debug/** rw,
  deny /sys/kernel/mm/** rw,
  deny /sys/module/** rw,

  # Allow standard I/O devices
  /dev/null rw,
  /dev/zero r,
  /dev/urandom r,
  /dev/random r,

  # Network access - Go services are network-heavy (HTTP, gRPC, mesh sidecars)
  network inet stream,
  network inet dgram,
  network inet6 stream,
  network inet6 dgram,
  network unix stream,
  network unix dgram,

  # Deny raw sockets and packet access
  deny network raw,
  deny network packet,
  deny network netlink,

  # Deny mount operations
  deny mount,
  deny umount,
  deny pivot_root,

  # Deny ptrace except own processes (pprof needs self-profiling)
  deny ptrace (trace) peer=*,
  ptrace (read) peer=evergreen-go-runtime,

  # Signal handling
  signal (send) peer=evergreen-go-runtime,
  signal (receive) peer=evergreen-go-runtime,
  signal (read, write) peer=evergreen-go-runtime,
  signal (receive) peer=unconfined,

  # Deny DBUS
  deny dbus,

  # Deny exec of shells and interpreters (Go services should not shell out)
  deny /bin/sh x,
  deny /bin/bash x,
  deny /bin/ash x,
  deny /bin/dash x,
  deny /bin/zsh x,
  deny /usr/bin/sh x,
  deny /usr/bin/bash x,
  deny /usr/bin/env x,
  deny /usr/bin/perl x,
  deny /usr/bin/python* x,
  deny /usr/bin/ruby x,

  # Allow exec of the application binary only
  /app/** x,
  /binary x,
  /usr/local/bin/** x,
}
