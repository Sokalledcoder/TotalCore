"""
WebSocket API for live order book streaming to frontend.

Provides real-time order book data for heatmap visualization.
"""
from __future__ import annotations

import asyncio
import json
import logging
from typing import List, Optional, Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse

from app.ingestion.orderbook_stream import (
    OrderBookStreamer,
    OrderBookStreamConfig,
    OrderBookSnapshot,
    get_orderbook_streamer,
    start_orderbook_streaming,
    stop_orderbook_streaming
)
from app.ingestion.orderbook_storage import get_orderbook_storage

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/orderbook", tags=["orderbook"])

# Track connected WebSocket clients
connected_clients: Set[WebSocket] = set()

# Global streaming task
_streaming_task: Optional[asyncio.Task] = None


@router.get("/status")
async def get_streaming_status():
    """Get the current status of order book streaming"""
    streamer = get_orderbook_streamer()
    return {
        "running": streamer.running,
        "symbol": streamer.config.symbol,
        "snapshot_count": len(streamer.snapshots),
        "connected_clients": len(connected_clients)
    }


@router.post("/start")
async def start_streaming(
    symbol: str = Query("BTC/USDT:USDT", description="CCXT unified symbol"),
    exchange: str = Query("binanceusdm", description="Exchange: binanceusdm or bybit"),
    depth_limit: int = Query(500, description="Order book depth levels (~$2K each side)"),
    snapshot_interval_ms: int = Query(250, description="Snapshot interval in ms")
):
    """Start order book streaming"""
    global _streaming_task
    
    config = OrderBookStreamConfig(
        symbol=symbol,
        exchange=exchange,
        depth_limit=depth_limit,
        snapshot_interval_ms=snapshot_interval_ms
    )
    
    try:
        streamer = await start_orderbook_streaming(config)
        
        # Add callback to broadcast to connected clients
        def broadcast_callback(snapshot: OrderBookSnapshot):
            asyncio.create_task(broadcast_snapshot(snapshot))
        
        streamer.add_callback(broadcast_callback)
        
        return {
            "status": "started",
            "symbol": symbol,
            "exchange": exchange,
            "depth_limit": depth_limit,
            "snapshot_interval_ms": snapshot_interval_ms
        }
    except ImportError as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "hint": "Install ccxt with: pip install ccxt[async]"}
        )
    except Exception as e:
        logger.exception("Failed to start streaming")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@router.post("/stop")
async def stop_streaming():
    """Stop order book streaming"""
    await stop_orderbook_streaming()
    return {"status": "stopped"}


@router.get("/snapshots")
async def get_snapshots(limit: int = Query(100, description="Number of snapshots to return")):
    """Get recent order book snapshots"""
    streamer = get_orderbook_streamer()
    return {
        "snapshots": streamer.get_recent_snapshots(limit),
        "count": len(streamer.snapshots)
    }


@router.get("/latest")
async def get_latest():
    """Get the latest order book snapshot"""
    streamer = get_orderbook_streamer()
    snapshot = streamer.get_latest_snapshot()
    if snapshot:
        return snapshot
    return {"error": "No snapshots available", "hint": "Start streaming first"}


@router.get("/depth")
async def get_aggregated_depth(
    price_bucket: float = Query(1.0, description="Price bucket size for aggregation"),
    levels: int = Query(50, description="Number of price levels")
):
    """Get aggregated order book depth for visualization"""
    streamer = get_orderbook_streamer()
    return streamer.get_aggregated_depth(price_bucket, levels)


@router.get("/history")
async def get_historical_snapshots(
    symbol: str = Query("BTC/USDT:USDT", description="Symbol to query"),
    start_ts: int = Query(..., description="Start timestamp (ms)"),
    end_ts: int = Query(..., description="End timestamp (ms)"),
    max_snapshots: int = Query(500, description="Maximum snapshots to return")
):
    """Get historical order book snapshots from storage"""
    storage = get_orderbook_storage()
    snapshots = storage.get_snapshots(symbol, start_ts, end_ts, max_snapshots)
    return {
        "snapshots": snapshots,
        "count": len(snapshots)
    }


@router.get("/storage/stats")
async def get_storage_stats(
    symbol: str = Query(None, description="Optional symbol filter")
):
    """Get order book storage statistics"""
    storage = get_orderbook_storage()
    return storage.get_stats(symbol)


@router.post("/storage/cleanup")
async def cleanup_old_data(
    older_than_days: int = Query(7, description="Delete data older than N days")
):
    """Clean up old order book data from storage"""
    storage = get_orderbook_storage()
    deleted = storage.cleanup_old_data(older_than_days)
    return {"deleted_rows": deleted}


@router.websocket("/stream")
async def websocket_orderbook(websocket: WebSocket):
    """
    WebSocket endpoint for streaming order book data to frontend.
    
    Clients connect here and receive real-time order book snapshots.
    """
    await websocket.accept()
    connected_clients.add(websocket)
    logger.info(f"WebSocket client connected. Total clients: {len(connected_clients)}")
    
    try:
        # Send initial status
        streamer = get_orderbook_streamer()
        await websocket.send_json({
            "type": "status",
            "running": streamer.running,
            "symbol": streamer.config.symbol,
            "snapshot_count": len(streamer.snapshots)
        })
        
        # Send recent history if available
        recent = streamer.get_recent_snapshots(100)
        if recent:
            await websocket.send_json({
                "type": "history",
                "snapshots": recent
            })
        
        # Keep connection alive and handle client messages
        while True:
            try:
                # Wait for client message (ping/commands)
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0  # Timeout for keepalive
                )
                
                # Handle client commands
                try:
                    msg = json.loads(data)
                    if msg.get("command") == "get_latest":
                        snapshot = streamer.get_latest_snapshot()
                        if snapshot:
                            await websocket.send_json({
                                "type": "snapshot",
                                "data": snapshot
                            })
                    elif msg.get("command") == "get_depth":
                        depth = streamer.get_aggregated_depth()
                        await websocket.send_json({
                            "type": "depth",
                            "data": depth
                        })
                except json.JSONDecodeError:
                    pass  # Ignore invalid JSON (might be ping)
                    
            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                await websocket.send_json({"type": "ping"})
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        connected_clients.discard(websocket)
        logger.info(f"WebSocket client disconnected. Total clients: {len(connected_clients)}")


async def broadcast_snapshot(snapshot: OrderBookSnapshot):
    """Broadcast a snapshot to all connected WebSocket clients"""
    if not connected_clients:
        return
        
    data = {
        "type": "snapshot",
        "data": snapshot.to_dict()
    }
    
    # Broadcast to all clients
    disconnected = set()
    for client in connected_clients:
        try:
            await client.send_json(data)
        except Exception:
            disconnected.add(client)
    
    # Remove disconnected clients
    for client in disconnected:
        connected_clients.discard(client)
