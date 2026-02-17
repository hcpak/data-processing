#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VPC FlowLog data generator.

Generates realistic VPC FlowLog records with the following fields:
  timestamp, src_ip, dst_ip, src_port, dst_port, protocol, bytes, packets, action
"""
from __future__ import print_function

import csv
import os
import random
import time
from datetime import datetime, timedelta


# -- Configuration --
NUM_RECORDS = 150000
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "raw")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "flowlog.csv")

# Simulate a 7-day window
BASE_TIME = datetime(2025, 1, 1, 0, 0, 0)
TIME_RANGE_SECONDS = 7 * 24 * 3600

# Internal subnet CIDRs (10.0.x.x)
INTERNAL_SUBNETS = ["10.0.1", "10.0.2", "10.0.3", "10.0.4"]

# External IPs simulating scanners, CDNs, DNS servers, etc.
EXTERNAL_IPS = [
    "203.0.113.%d" % i for i in range(1, 51)
] + [
    "198.51.100.%d" % i for i in range(1, 31)
]

# Well-known ports and their typical protocols
PORT_PROFILES = [
    # (dst_port, protocol_num, label)
    (80, 6, "http"),
    (443, 6, "https"),
    (22, 6, "ssh"),
    (53, 17, "dns"),
    (53, 6, "dns-tcp"),
    (3306, 6, "mysql"),
    (5432, 6, "postgres"),
    (8080, 6, "http-alt"),
    (8443, 6, "https-alt"),
    (123, 17, "ntp"),
]

# Suspicious scanner ports (higher REJECT rate)
SCANNER_PORTS = [23, 445, 3389, 1433, 6379, 27017, 9200]


def generate_internal_ip():
    """Generate a random internal IP address."""
    subnet = random.choice(INTERNAL_SUBNETS)
    return "%s.%d" % (subnet, random.randint(2, 254))


def generate_timestamp(base, range_seconds):
    """Generate a random timestamp within the given range."""
    offset = random.randint(0, range_seconds)
    dt = base + timedelta(seconds=offset)
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def generate_record():
    """Generate a single FlowLog record."""
    timestamp = generate_timestamp(BASE_TIME, TIME_RANGE_SECONDS)

    # Decide traffic direction: inbound (60%) vs outbound (40%)
    if random.random() < 0.6:
        # Inbound: external -> internal
        src_ip = random.choice(EXTERNAL_IPS)
        dst_ip = generate_internal_ip()
    else:
        # Outbound: internal -> external
        src_ip = generate_internal_ip()
        dst_ip = random.choice(EXTERNAL_IPS)

    # 80% normal traffic, 20% scanner/suspicious traffic
    if random.random() < 0.8:
        profile = random.choice(PORT_PROFILES)
        dst_port = profile[0]
        protocol = profile[1]
        # Normal traffic: 95% ACCEPT
        action = "ACCEPT" if random.random() < 0.95 else "REJECT"
        bytes_sent = random.randint(64, 1500000)
        packets = max(1, bytes_sent // random.randint(64, 1500))
    else:
        dst_port = random.choice(SCANNER_PORTS)
        protocol = 6
        # Suspicious traffic: 80% REJECT
        action = "REJECT" if random.random() < 0.8 else "ACCEPT"
        bytes_sent = random.randint(40, 1500)
        packets = random.randint(1, 5)

    src_port = random.randint(1024, 65535)

    return {
        "timestamp": timestamp,
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port,
        "dst_port": dst_port,
        "protocol": protocol,
        "bytes": bytes_sent,
        "packets": packets,
        "action": action,
    }


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    fieldnames = [
        "timestamp", "src_ip", "dst_ip", "src_port",
        "dst_port", "protocol", "bytes", "packets", "action",
    ]

    print("Generating %d FlowLog records..." % NUM_RECORDS)
    start = time.time()

    with open(OUTPUT_FILE, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(NUM_RECORDS):
            writer.writerow(generate_record())

            if (i + 1) % 50000 == 0:
                print("  %d / %d records generated" % (i + 1, NUM_RECORDS))

    elapsed = time.time() - start
    file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024.0 * 1024.0)

    print("Done!")
    print("  Output: %s" % OUTPUT_FILE)
    print("  Records: %d" % NUM_RECORDS)
    print("  File size: %.2f MB" % file_size_mb)
    print("  Elapsed: %.2f seconds" % elapsed)


if __name__ == "__main__":
    main()
