Stream A: Startup Optimization (T4.1.1 -> T4.1.2 -> T4.1.3); 12 hours
Stream B: CPU Pinning (T4.2.1 -> T4.2.2 -> T4.2.3); 16 hours
Stream C: Kernel Bypass (T4.3.1, T4.3.2); 8 hours
Stream D: Atomic Deploy (T4.4.1 -> T4.4.2 -> T4.4.3); 12 hours
Stream E: Real-Time Scheduling (T4.5.1 -> T4.5.2 -> T4.5.3); 10 hours
network stack) to ~2-5us (user-space processing). Not all images benefit from DPDK; only those performing packet-level
- before SKB allocation. XDP is less invasive than DPDK (no hugepages, no dedicated NICs) but provides significant