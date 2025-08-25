from typing import Dict, List, Callable, Any
from collections import defaultdict
import weakref
from event_type import EventType
from event_context import EventContext

class EventEmitter:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventEmitter, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._listeners: Dict[EventType, List[Callable]] = defaultdict(list)
        self._debug_mode = False
    
    def emit(self, event_type: EventType, context: EventContext) -> None:
        if self._debug_mode:
            print(f"[EVENT] Emitting {event_type.value} with context: {context}")
        
        if event_type not in self._listeners:
            return
        
        # Create a copy to avoid modification during iteration
        listeners = self._listeners[event_type].copy()
        for listener in listeners:
            try:
                listener(event_type, context)
            except Exception as e:
                if self._debug_mode:
                    print(f"[EVENT] Error in listener for {event_type.value}: {e}")
    
    def subscribe(self, event_type: EventType, callback: Callable) -> None:
        self._listeners[event_type].append(callback)
        
        if self._debug_mode:
            print(f"[EVENT] Subscribed to {event_type.value}")
    
    def unsubscribe(self, event_type: EventType, callback: Callable) -> None:
        if event_type not in self._listeners:
            return
        
        if callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)
        
        if self._debug_mode:
            print(f"[EVENT] Unsubscribed from {event_type.value}")
    
    def clear_all_listeners(self) -> None:
        self._listeners.clear()
        if self._debug_mode:
            print("[EVENT] Cleared all listeners")
    
    def set_debug_mode(self, enabled: bool) -> None:
        self._debug_mode = enabled
    
    def get_listener_count(self, event_type: EventType = None) -> int:
        if event_type is None:
            return sum(len(listeners) for listeners in self._listeners.values())
        return len(self._listeners.get(event_type, []))