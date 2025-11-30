"""
WebSocket API for live trade streaming to frontend.

Provides real-time trade data for building live footprints and candles.
"""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Optional, Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse

from app.ingestion.trade_stream import (
    TradeStreamer,
    TradeStreamConfig,
    Trade,
    LiveCandle,
    get_trade_streamer,
    start_trade_streaming,
    stop_trade_streaming
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/trades", tags=["trades"])

# Track connected clients
connected_clients: Set[WebSocket] = set()

# Background task for periodic current candle updates
_current_candle_task: Optional[asyncio.Task] = None


async def broadcast_current_candle_periodically():
    """Background task to broadcast current candle every 500ms"""
    while True:
        try:
            await asyncio.sleep(0.5)  # Update twice per second
            
            if not connected_clients:
                continue
                
            streamer = get_trade_streamer()
            if not streamer.running:
                continue
                
            current = streamer.get_current_candle()
            if current:
                data = {"type": "current_candle", "data": current}
                disconnected = set()
                for client in connected_clients:
                    try:
                        await client.send_json(data)
                    except Exception:
                        disconnected.add(client)
                
                for client in disconnected:
                    connected_clients.discard(client)
                    
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error broadcasting current candle: {e}")


@router.get("/status")
async def get_streaming_status():
    """Get the current status of trade streaming"""
    streamer = get_trade_streamer()
    return {
        "running": streamer.running,
        "symbol": streamer.config.symbol,
        "trade_count": len(streamer.trades),
        "candle_count": len(streamer.candles),
        "connected_clients": len(connected_clients)
    }


@router.post("/start")
async def start_streaming(
    symbol: str = Query("BTC/USDT:USDT", description="CCXT unified symbol"),
    exchange: str = Query("binanceusdm", description="Exchange: binanceusdm or bybit"),
    candle_interval_ms: int = Query(60000, description="Candle interval (ms) - 60000=1m"),
    price_bucket_size: float = Query(1.0, description="Price bucket size for profiles")
):
    """Start trade streaming"""
    global _current_candle_task
    
    config = TradeStreamConfig(
        symbol=symbol,
        exchange=exchange,
        candle_interval_ms=candle_interval_ms,
        price_bucket_size=price_bucket_size
    )
    
    try:
        streamer = await start_trade_streaming(config)
        
        # Add callbacks to broadcast to clients
        def trade_callback(trade: Trade):
            asyncio.create_task(broadcast_trade(trade))
        
        def candle_callback(candle: LiveCandle):
            asyncio.create_task(broadcast_candle(candle))
        
        streamer.add_trade_callback(trade_callback)
        streamer.add_candle_callback(candle_callback)
        
        # Start background task for current candle updates
        if _current_candle_task is None or _current_candle_task.done():
            _current_candle_task = asyncio.create_task(broadcast_current_candle_periodically())
            logger.info("Started current candle broadcast task")
        
        return {
            "status": "started",
            "symbol": symbol,
            "exchange": exchange,
            "candle_interval_ms": candle_interval_ms,
            "price_bucket_size": price_bucket_size
        }
    except ImportError as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.exception("Failed to start trade streaming")
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.post("/stop")
async def stop_streaming():
    """Stop trade streaming"""
    global _current_candle_task
    
    # Cancel the background task
    if _current_candle_task and not _current_candle_task.done():
        _current_candle_task.cancel()
        try:
            await _current_candle_task
        except asyncio.CancelledError:
            pass
        _current_candle_task = None
        logger.info("Stopped current candle broadcast task")
    
    await stop_trade_streaming()
    return {"status": "stopped"}


@router.get("/current-candle")
async def get_current_candle():
    """Get the current (incomplete) live candle"""
    streamer = get_trade_streamer()
    candle = streamer.get_current_candle()
    if candle:
        return candle
    return {"error": "No candle available"}


@router.get("/candles")
async def get_recent_candles(limit: int = Query(50, description="Number of candles")):
    """Get recent live candles with profiles"""
    streamer = get_trade_streamer()
    return {
        "candles": streamer.get_recent_candles(limit),
        "current": streamer.get_current_candle()
    }


@router.get("/recent")
async def get_recent_trades(limit: int = Query(100, description="Number of trades")):
    """Get recent trade executions"""
    streamer = get_trade_streamer()
    return {
        "trades": streamer.get_recent_trades(limit),
        "count": len(streamer.trades)
    }


@router.websocket("/stream")
async def websocket_trades(websocket: WebSocket):
    """WebSocket endpoint for streaming trades and candles"""
    await websocket.accept()
    connected_clients.add(websocket)
    logger.info(f"Trade WebSocket client connected. Total: {len(connected_clients)}")
    
    try:
        streamer = get_trade_streamer()
        
        # Send initial status
        await websocket.send_json({
            "type": "status",
            "running": streamer.running,
            "symbol": streamer.config.symbol,
            "trade_count": len(streamer.trades)
        })
        
        # Send current candle if exists
        current = streamer.get_current_candle()
        if current:
            await websocket.send_json({
                "type": "current_candle",
                "data": current
            })
        
        # Send recent candles
        candles = streamer.get_recent_candles(20)
        if candles:
            await websocket.send_json({
                "type": "candles",
                "data": candles
            })
        
        # Keep connection alive
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0
                )
                
                try:
                    msg = json.loads(data)
                    if msg.get("command") == "get_current":
                        current = streamer.get_current_candle()
                        if current:
                            await websocket.send_json({
                                "type": "current_candle",
                                "data": current
                            })
                except json.JSONDecodeError:
                    pass
                    
            except asyncio.TimeoutError:
                await websocket.send_json({"type": "ping"})
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"Trade WebSocket error: {e}")
    finally:
        connected_clients.discard(websocket)
        logger.info(f"Trade WebSocket disconnected. Total: {len(connected_clients)}")


async def broadcast_trade(trade: Trade):
    """Broadcast a trade to all connected clients"""
    if not connected_clients:
        return
    
    data = {"type": "trade", "data": trade.to_dict()}
    
    disconnected = set()
    for client in connected_clients:
        try:
            await client.send_json(data)
        except Exception:
            disconnected.add(client)
    
    for client in disconnected:
        connected_clients.discard(client)


async def broadcast_candle(candle: LiveCandle):
    """Broadcast a completed candle to all connected clients"""
    if not connected_clients:
        return
    
    data = {"type": "candle", "data": candle.to_dict()}
    
    disconnected = set()
    for client in connected_clients:
        try:
            await client.send_json(data)
        except Exception:
            disconnected.add(client)
    
    for client in disconnected:
        connected_clients.discard(client)
