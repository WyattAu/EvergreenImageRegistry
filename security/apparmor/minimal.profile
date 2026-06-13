#include <tunables/global>

profile evergreen-minimal flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # Deny ALL capabilities - this profile is for static binaries
  deny capability,

  # No file writes allowed - scratch images are read-only
  deny /** w,
  deny /tmp/** rw,
  deny /run/** rw,
  deny /var/** rw,

  # Allow read access to application and libraries
  / r,
  /lib/** r,
  /lib64/** r,
  /usr/** r,
  /etc/** r,
  /binary r,
  /app/** r,

  # Deny all networking - static binaries should not need network
  deny network,

  # Deny all process operations
  deny ptrace,
  deny signal (send) peer=unconfined,

  # Deny all mount/umount
  deny mount,
  deny umount,
  deny pivot_root,

  # Deny DBUS
  deny dbus,

  # Deny raw file access
  deny /proc/**,
  deny /sys/**,
  deny /dev/**,

  # Allow reading /dev/null, /dev/zero, /dev/urandom for standard I/O
  /dev/null r,
  /dev/zero r,
  /dev/urandom r,
  /dev/random r,

  # Allow /proc/self for own process info
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
}
