"""
NovaMind Sound Engine
=====================
Dedicated non-blocking sound system for NovaMind.
Handles audio playback using a separate thread to prevent UI blocking.
Supports Windows (winsound) and fallback mechanisms for other OS.
"""

import sys
import time
import threading
import queue
import platform
from typing import Optional, Dict

class SoundEngine:
    """
    Non-blocking sound engine with thread-safe queue.
    Singleton pattern recommended.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundEngine, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.enabled = False
        self.volume = 100  # 0-100 (simulated for system beeps)
        self.style = "mechanical"
        self.running = False
        
        # Audio worker config
        self.sound_queue = queue.Queue(maxsize=10) # Small buffer to prevent lag/stacking
        self.worker_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        
        # Throttling
        self.last_sound_time = 0
        self.min_interval = 0.05  # Min seconds between sounds
        
        # OS Detection
        self.system = platform.system().lower()
        self.has_sound_lib = False
        
        # Initialize backend
        self._init_backend()
        
        # Start worker
        self.start()
        
        self._initialized = True
        print("  [Sound] Engine initialized.")

    def _init_backend(self):
        """Initialize platform-specific sound libraries"""
        try:
            if self.system == "windows":
                import winsound
                self.backend = winsound
                self.has_sound_lib = True
                self.play_func = self._play_windows
            elif self.system == "darwin": # macOS
                # Fallback to system bell or limited functionality
                self.has_sound_lib = False 
                self.play_func = self._play_macos
            else: # Linux
                self.has_sound_lib = False
                self.play_func = self._play_linux
        except ImportError:
            self.has_sound_lib = False
            self.play_func = self._play_dummy

    def start(self):
        """Start the sound worker thread"""
        if self.worker_thread and self.worker_thread.is_alive():
            return
            
        self.running = True
        self.stop_event.clear()
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True, name="SoundWorker")
        self.worker_thread.start()

    def stop(self):
        """Stop the sound worker"""
        self.running = False
        self.stop_event.set()
        
        # Clear queue
        with self.sound_queue.mutex:
            self.sound_queue.queue.clear()
            
        if self.worker_thread:
            self.worker_thread.join(timeout=1.0)

    def set_enabled(self, enabled: bool):
        """Toggle sound on/off"""
        self.enabled = enabled
        if not enabled:
            # Clear pending sounds when disabling
            with self.sound_queue.mutex:
                self.sound_queue.queue.clear()

    def queue_keystroke_sound(self):
        """Queue a typing sound (non-blocking, throttled)"""
        if not self.enabled:
            return
            
        now = time.time()
        if now - self.last_sound_time < self.min_interval:
            return
            
        try:
            # Non-blocking put, skip if full (safety valve)
            self.sound_queue.put_nowait(("type", self.style))
            self.last_sound_time = now
        except queue.Full:
            pass 

    def queue_notification(self, type="default"):
        """Queue a notification sound"""
        if not self.enabled:
            return
        try:
            self.sound_queue.put_nowait(("notify", type))
        except queue.Full:
            pass

    def _worker_loop(self):
        """Main audio processing loop running in separate thread"""
        while self.running and not self.stop_event.is_set():
            try:
                # Wait for sound task (short timeout to check stop_event)
                try:
                    task = self.sound_queue.get(timeout=0.1)
                except queue.Empty:
                    continue
                
                sound_type, data = task
                
                if sound_type == "type":
                    self._play_keystroke(data)
                elif sound_type == "notify":
                    self._play_notification(data)
                    
                self.sound_queue.task_done()
                
            except Exception as e:
                # Failsafe: Log error but don't crash thread
                # print(f"Sound Error: {e}") 
                pass

    def _play_keystroke(self, style):
        """Execute the actual sound play (blocking is ok here)"""
        # Frequencies for different styles
        if style == "mechanical":
            freq = 800
            dur = 15
        elif style == "soft":
            freq = 400
            dur = 10
        elif style == "retro":
            freq = 1200
            dur = 20
        else:
            freq = 600
            dur = 15
            
        self.play_func(freq, dur)

    def _play_notification(self, type):
        """Execute notification sound"""
        if self.system == "windows" and self.has_sound_lib:
            try:
                # Use MessageBeep for system sounds
                import winsound
                winsound.MessageBeep(winsound.MB_OK)
            except:
                pass
        else:
            self.play_func(800, 100) # Fallback beep

    # --- Platform Specific Implementations ---

    def _play_windows(self, freq, duration):
        """Windows implementation using winsound.Beep"""
        try:
            self.backend.Beep(int(freq), int(duration))
        except Exception:
            pass

    def _play_macos(self, freq, duration):
        """macOS fallback (visual or system bell)"""
        # macOS doesn't have a simple freq/dur beep without external libs
        # We'll just use the system bell occasionally or do nothing
        # print("\a", end="", flush=True) 
        pass

    def _play_linux(self, freq, duration):
        """Linux fallback"""
        # print("\a", end="", flush=True)
        pass

    def _play_dummy(self, freq, duration):
        """No-op for when no sound is available"""
        pass

# Global instance
_sound_engine = SoundEngine()

def get_sound_engine():
    return _sound_engine
