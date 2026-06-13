#include <tunables/global>

profile evergreen-docker-socket-proxy flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>
  #include <abstractions/docker>

  # Allow only specific capabilities needed for Docker API proxying
  capability chown,
  capability dac_override,
  capability fowner,
  capability fsetid,
  capability kill,
  capability net_bind_service,
  capability setgid,
  capability setpcap,
  capability setuid,

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

  # Docker socket access - allow only specific operations
  /var/run/docker.sock rw,
  /run/docker.sock rw,

  # Deny writing to Docker socket beyond proxy functionality
  deny /var/run/docker.sock create,
  deny /var/run/docker.sock lock,
  deny /var/run/docker.sock unlink,

  # File system access
  / r,
  /lib/** r,
  /lib64/** r,
  /usr/** r,
  /etc/** r,
  /opt/** r,

  # Application paths
  /app/** r,
  /config/** r,

  # Temp files for request/response buffering
  /tmp/** rw,

  # Deny writes to sensitive host paths
  deny /proc/** w,
  deny /sys/** w,
  deny /dev/** w,
  deny /boot/** w,
  deny /media/** w,
  deny /mnt/** w,

  # Network access - proxy needs to accept connections and forward to Docker
  network inet stream,
  network inet dgram,
  network inet6 stream,
  network inet6 dgram,
  network unix stream,
  network unix dgram,

  # Deny raw sockets and netlink - not needed for HTTP proxy
  deny network raw,
  deny network packet,
  deny network netlink,

  # Deny mount operations
  deny mount,
  deny umount,
  deny pivot_root,

  # Allow signals within own process group
  signal (send) peer=evergreen-docker-socket-proxy,
  signal (receive) peer=evergreen-docker-socket-proxy,
  signal (read, write) peer=evergreen-docker-socket-proxy,

  # Deny ptrace
  deny ptrace,

  # Deny DBUS
  deny dbus,

  # Logging path
  /var/log/** rw,
  /logs/** rw,

  # Health check endpoint
  /proc/self/status r,
  /proc/self/fd/** r,
  /proc/self/root/** r,
  /proc/sys/kernel/osrelease r,
  /proc/thread-self/** r,
}
