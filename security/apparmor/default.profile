#include <tunables/global>

profile evergreen-default flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # Deny all capabilities by default
  deny capability,

  # Allow only necessary capabilities for general container workloads
  capability chown,
  capability dac_override,
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

  # File system access - deny writes to sensitive paths
  deny /proc/** w,
  deny /sys/** w,
  deny /dev/** w,

  # Allow reads for application operation
  / r,
  /lib/** r,
  /lib64/** r,
  /usr/** r,
  /etc/** r,
  /opt/** r,
  /tmp/** rw,
  /var/** rw,
  /run/** rw,

  # Application-specific paths
  /app/** r,
  /config/** r,
  /data/** rw,
  /logs/** rw,

  # Deny access to sensitive host paths
  deny /proc/sysrq-trigger rw,
  deny /proc/sys/** w,
  deny /sys/firmware/** rw,
  deny /proc/acpi/** rw,
  deny /proc/kcore rw,
  deny /proc/keys rw,
  deny /proc/latency_stats rw,
  deny /proc/timer_list rw,
  deny /proc/timer_stats rw,
  deny /proc/sched_debug rw,
  deny /sys/kernel/debug/** rw,

  # Network access - allow TCP/UDP, deny raw sockets
  network inet stream,
  network inet dgram,
  network inet6 stream,
  network inet6 dgram,
  network unix stream,
  network unix dgram,
  deny network raw,
  deny network packet,
  deny network netlink,

  # Deny ptrace except for own processes
  deny ptrace (trace) peer=*,

  # Deny mount/umount
  deny mount,
  deny umount,

  # Deny signal injection to other containers
  signal (send) peer=unconfined,
  signal (receive) peer=unconfined,
  signal (read, write) peer=unconfined,

  # Allow signals within own process group
  signal (send) peer=evergreen-default,
  signal (receive) peer=evergreen-default,

  # Deny database operations via DBUS
  deny dbus,
}
