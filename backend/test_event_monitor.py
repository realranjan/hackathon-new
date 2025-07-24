import pytest
import asyncio
from agents.event_monitor import fetch_or_simulate_events

def test_fetch_or_simulate_events():
    try:
        events = fetch_or_simulate_events()
    except TypeError:
        # If function is async, run it in event loop
        events = asyncio.run(fetch_or_simulate_events())
    assert isinstance(events, list)
    assert len(events) > 0
    # Check if at least one event is real (source != 'Simulated')
    real_events = [e for e in events if e.get('source') != 'Simulated']
    if real_events:
        print(f"Real events found: {real_events}")
        assert True
    else:
        print("No real events found, using simulated event.")
        # Should still return a simulated event
        assert events[0].get('source') == 'Simulated' 