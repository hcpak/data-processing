#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FlowLog batch analysis using pandas.

Performs the following analyses:
  1. Hourly traffic aggregation (bytes, packets, record count)
  2. Top 10 source IPs with REJECT action
  3. Bytes sum by protocol
Results are saved as Parquet files.
"""
from __future__ import print_function

import os

import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "data", "raw", "flowlog.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "processed")

# Protocol number to name mapping
PROTOCOL_MAP = {
    6: "TCP",
    17: "UDP",
}


def load_data(path):
    """Load FlowLog CSV and parse timestamp column."""
    print("Loading data from %s ..." % path)
    df = pd.read_csv(path, parse_dates=["timestamp"])
    print("  Loaded %d records" % len(df))
    print("  Date range: %s ~ %s" % (df["timestamp"].min(), df["timestamp"].max()))
    print("  Columns: %s" % list(df.columns))
    print()
    return df


def analyze_hourly_traffic(df):
    """Aggregate traffic by hour."""
    print("=== 1. Hourly Traffic Aggregation ===")

    df["hour"] = df["timestamp"].dt.floor("h")

    hourly = df.groupby("hour").agg(
        total_bytes=("bytes", "sum"),
        total_packets=("packets", "sum"),
        record_count=("bytes", "count"),
        accept_count=("action", lambda x: (x == "ACCEPT").sum()),
        reject_count=("action", lambda x: (x == "REJECT").sum()),
    ).reset_index()

    hourly = hourly.sort_values("hour")

    print("  Total hours: %d" % len(hourly))
    print()

    # Show peak traffic hours (top 5)
    peak = hourly.nlargest(5, "total_bytes")
    print("  Peak traffic hours (Top 5 by bytes):")
    for _, row in peak.iterrows():
        print("    %s | %12s bytes | %6d packets | %5d records" % (
            row["hour"].strftime("%Y-%m-%d %H:00"),
            "{:,}".format(row["total_bytes"]),
            row["total_packets"],
            row["record_count"],
        ))
    print()

    return hourly


def analyze_reject_top_ips(df):
    """Find Top 10 source IPs with REJECT action."""
    print("=== 2. REJECT Top 10 Source IPs ===")

    rejected = df[df["action"] == "REJECT"]
    print("  Total REJECT records: %d / %d (%.1f%%)" % (
        len(rejected), len(df), 100.0 * len(rejected) / len(df),
    ))

    top_ips = rejected.groupby("src_ip").agg(
        reject_count=("action", "count"),
        total_bytes=("bytes", "sum"),
        unique_dst_ports=("dst_port", "nunique"),
    ).reset_index()

    top_ips = top_ips.nlargest(10, "reject_count")
    top_ips = top_ips.reset_index(drop=True)
    top_ips.index = top_ips.index + 1

    print()
    print("  Rank | Source IP         | REJECT Count | Bytes        | Unique Dst Ports")
    print("  -----|-------------------|-------------|------------- |----------------")
    for rank, row in top_ips.iterrows():
        print("  %4d | %-17s | %11d | %12s | %d" % (
            rank,
            row["src_ip"],
            row["reject_count"],
            "{:,}".format(row["total_bytes"]),
            row["unique_dst_ports"],
        ))
    print()

    return top_ips


def analyze_protocol_bytes(df):
    """Sum bytes by protocol."""
    print("=== 3. Bytes by Protocol ===")

    proto_stats = df.groupby("protocol").agg(
        total_bytes=("bytes", "sum"),
        total_packets=("packets", "sum"),
        record_count=("bytes", "count"),
    ).reset_index()

    proto_stats["protocol_name"] = proto_stats["protocol"].map(PROTOCOL_MAP).fillna("OTHER")
    proto_stats["bytes_pct"] = 100.0 * proto_stats["total_bytes"] / proto_stats["total_bytes"].sum()
    proto_stats = proto_stats.sort_values("total_bytes", ascending=False)

    print()
    for _, row in proto_stats.iterrows():
        print("  %s (proto=%d): %s bytes (%.1f%%) | %s packets | %d records" % (
            row["protocol_name"],
            row["protocol"],
            "{:,}".format(row["total_bytes"]),
            row["bytes_pct"],
            "{:,}".format(row["total_packets"]),
            row["record_count"],
        ))
    print()

    return proto_stats


def save_parquet(df, filename, description):
    """Save a DataFrame as Parquet file."""
    path = os.path.join(OUTPUT_DIR, filename)
    df.to_parquet(path, index=False)
    size_kb = os.path.getsize(path) / 1024.0
    print("  Saved: %s (%.1f KB) - %s" % (path, size_kb, description))


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    df = load_data(INPUT_FILE)

    # Run analyses
    hourly = analyze_hourly_traffic(df)
    reject_top = analyze_reject_top_ips(df)
    proto_bytes = analyze_protocol_bytes(df)

    # Save results as Parquet
    print("=== Saving Results as Parquet ===")
    save_parquet(hourly, "hourly_traffic.parquet", "Hourly traffic aggregation")
    save_parquet(reject_top, "reject_top10_ips.parquet", "REJECT Top 10 source IPs")
    save_parquet(proto_bytes, "protocol_bytes.parquet", "Bytes by protocol")
    print()
    print("All done!")


if __name__ == "__main__":
    main()
