#!/usr/bin/env python3
"""
Memory Bus Adapter - Connects Weaver's memory system to A-C-Gee's ADR-004 message bus.

This adapter enables:
- Asynchronous memory writes (non-blocking)
- Cross-agent knowledge notifications
- Message bus integration for memory events
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from memory_core import MemoryStore, MemoryEntry

class MemoryBusAdapter:
    """Connects memory system to ADR-004 message bus."""

    def __init__(self, memory_root: str = ".claude/memory", bus_root: str = "memories/communication/message_bus"):
        self.store = MemoryStore(memory_root)
        self.bus_root = Path(bus_root)
        self.bus_root.mkdir(parents=True, exist_ok=True)

    def publish(self, topic: str, payload: Dict[str, Any]):
        """Publish message to ADR-004 bus (append to topic file)."""
        topic_file = self.bus_root / f"{topic}.jsonl"

        message = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "topic": topic,
            "payload": payload
        }

        with open(topic_file, "a") as f:
            f.write(json.dumps(message) + "\n")

    def consume(self, topic: str, since: Optional[str] = None) -> List[Dict[str, Any]]:
        """Consume messages from topic (read from JSONL file)."""
        topic_file = self.bus_root / f"{topic}.jsonl"

        if not topic_file.exists():
            return []

        messages = []
        with open(topic_file, "r") as f:
            for line in f:
                msg = json.loads(line.strip())
                if since is None or msg["timestamp"] > since:
                    messages.append(msg)

        return messages

    def handle_write_request(self, message: Dict[str, Any]):
        """Handle async memory write request."""
        agent_id = message["agent"]
        entry_dict = message["entry"]

        # Convert dict to MemoryEntry
        entry = MemoryEntry(
            date=entry_dict.get("date", datetime.utcnow().strftime("%Y-%m-%d")),
            agent=agent_id,
            type=entry_dict["type"],
            topic=entry_dict["topic"],
            tags=entry_dict.get("tags", []),
            confidence=entry_dict.get("confidence", "medium"),
            visibility=entry_dict.get("visibility", "collective-only"),
            content=entry_dict["content"],
            quality_score=entry_dict.get("quality_score", 0),
            connections=entry_dict.get("connections", []),
            evidence=entry_dict.get("evidence", []),
            reuse_count=entry_dict.get("reuse_count", 0)
        )

        # Write memory
        filepath = self.store.write_entry(agent_id, entry)

        # Publish completion event
        self.publish("memory.write_complete", {
            "agent": agent_id,
            "filepath": str(filepath),
            "topic": entry.topic,
            "tags": entry.tags,
            "quality_score": entry.quality_score,
            "visibility": entry.visibility
        })

        # Notify subscribed agents (publish to tag-specific topics)
        if entry.visibility in ["public", "collective-only"]:
            for tag in entry.tags:
                self.publish(f"knowledge.{tag}", {
                    "event": "memory.created",
                    "agent": agent_id,
                    "topic": entry.topic,
                    "filepath": str(filepath),
                    "quality_score": entry.quality_score
                })

        return filepath

    def handle_search_request(self, message: Dict[str, Any]):
        """Handle async memory search request."""
        request_id = message["request_id"]
        query = message["query"]
        agent = message.get("agent")

        # Search memories
        results = self.store.search(
            query=query,
            agent=agent,
            tags=message.get("tags"),
            type=message.get("type"),
            confidence=message.get("confidence")
        )

        # Convert results to dict
        results_dict = [
            {
                "filepath": r.filepath,
                "agent": r.agent,
                "topic": r.topic,
                "tags": r.tags,
                "confidence": r.confidence,
                "quality_score": r.quality_score,
                "created": r.created
            }
            for r in results
        ]

        # Publish results
        self.publish("memory.search_complete", {
            "request_id": request_id,
            "results": results_dict,
            "count": len(results_dict)
        })

        return results_dict

    def process_queue(self):
        """Process all pending memory requests."""
        # Process write requests
        write_requests = self.consume("memory.write_request")
        for msg in write_requests:
            try:
                self.handle_write_request(msg["payload"])
            except Exception as e:
                self.publish("memory.write_error", {
                    "agent": msg["payload"].get("agent"),
                    "error": str(e)
                })

        # Process search requests
        search_requests = self.consume("memory.search_request")
        for msg in search_requests:
            try:
                self.handle_search_request(msg["payload"])
            except Exception as e:
                self.publish("memory.search_error", {
                    "request_id": msg["payload"].get("request_id"),
                    "error": str(e)
                })


def main():
    """CLI for memory bus adapter."""
    import argparse

    parser = argparse.ArgumentParser(description="Memory Bus Adapter CLI")
    parser.add_argument("--process", action="store_true", help="Process pending requests")
    parser.add_argument("--write", help="Write memory (JSON payload)")
    parser.add_argument("--search", help="Search memories")
    parser.add_argument("--agent", help="Agent ID")

    args = parser.parse_args()

    adapter = MemoryBusAdapter()

    if args.process:
        adapter.process_queue()
        print("✅ Processed all pending requests")

    elif args.write:
        payload = json.loads(args.write)
        filepath = adapter.handle_write_request(payload)
        print(f"✅ Memory written: {filepath}")

    elif args.search:
        results = adapter.handle_search_request({
            "request_id": "cli-search",
            "query": args.search,
            "agent": args.agent
        })
        print(f"✅ Found {len(results)} memories")
        for r in results:
            print(f"  - {r['topic']} (by {r['agent']}, score: {r['quality_score']})")


if __name__ == "__main__":
    main()
