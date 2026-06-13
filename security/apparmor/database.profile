#include <tunables/global>

profile evergreen-database flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # Deny all capabilities by default
  deny capability,

  # Databases need privilege dropping and resource management
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
  capability ipc_lock,

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

  # Database binary and library paths (read-only)
  / r,
  /lib/** r,
  /lib64/** r,
  /usr/** r,
  /usr/lib/postgresql/** r,
  /usr/lib/mysql/** r,
  /usr/share/postgresql/** r,
  /usr/share/mysql/** r,
  /etc/** r,
  /opt/** r,

  # Database executable paths
  /usr/bin/postgres x,
  /usr/bin/pg_* x,
  /usr/bin/mysql* x,
  /usr/bin/mysqld x,
  /usr/bin/redis-server x,
  /usr/bin/mongod x,
  /usr/bin/cockroach x,
  /usr/sbin/postgres x,
  /usr/lib/postgresql/**/bin/** x,
  /usr/libexec/** x,

  # Database data directories (read-write)
  /data/** rw,
  /var/lib/postgresql/** rw,
  /var/lib/mysql/** rw,
  /var/lib/redis/** rw,
  /var/lib/mongodb/** rw,
  /var/lib/cockroach/** rw,
  /var/run/** rw,
  /run/** rw,
  /run/postgresql/** rw,
  /run/mysqld/** rw,
  /run/redis/** rw,
  /run/mongodb/** rw,

  # WAL and log directories
  /var/log/** rw,
  /logs/** rw,
  /tmp/** rw,

  # Configuration files (read-only)
  /config/** r,
  /etc/postgresql/** r,
  /etc/mysql/** r,
  /etc/redis/** r,
  /etc/mongod.conf r,

  # Database socket files
  /run/**/*.sock rw,
  /tmp/**/*.sock rw,

  # Deny writes to sensitive host paths
  deny /proc/** w,
  deny /sys/** w,
  deny /boot/** rw,
  deny /media/** rw,
  deny /mnt/** rw,
  deny /dev/** w,

  # Allow specific /proc reads needed by database engines
  /proc/self/** r,
  /proc/thread-self/** r,
  /proc/sys/kernel/osrelease r,
  /proc/sys/kernel/hostname r,
  /proc/sys/kernel/uuid r,
  /proc/sys/vm/** r,
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

  # Network access for client connections and replication
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

  # Deny ptrace
  deny ptrace,

  # Signal handling within own process group
  signal (send) peer=evergreen-database,
  signal (receive) peer=evergreen-database,
  signal (read, write) peer=evergreen-database,
  signal (receive) peer=unconfined,

  # Deny DBUS
  deny dbus,

  # Deny exec of shells and interpreters (databases should not shell out)
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
  deny /usr/bin/curl x,
  deny /usr/bin/wget x,
  deny /usr/bin/nc x,
  deny /usr/bin/ncat x,
  deny /usr/bin/ssh x,
  deny /usr/bin/scp x,
  deny /usr/bin/rsync x,
  deny /usr/bin/tar x,
  deny /usr/bin/apt x,
  deny /usr/bin/apk x,
  deny /usr/bin/yum x,
}
