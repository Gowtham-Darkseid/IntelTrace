"""Localhost Traffic Stress & Flood Simulation Module

STRICT SCOPE: 127.0.0.1 ONLY - Educational/Testing Purpose
This module simulates various traffic patterns on localhost for:
- Load testing local applications
- Network stack testing
- Educational demonstration of traffic patterns

LEGAL NOTICE: This tool is restricted to localhost (127.0.0.1) only.
Any attempt to target external hosts will be blocked.
"""
import socket
import threading
import time
import random
from datetime import datetime


class LocalhostStressSimulator:
    """Simulates various traffic patterns exclusively on localhost."""
    
    ALLOWED_TARGETS = ['127.0.0.1', 'localhost', '::1']
    
    def __init__(self):
        self.active_threads = []
        self.stats = {
            'packets_sent': 0,
            'connections_made': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
        self.stop_flag = False

    def validate_target(self, target):
        """Ensure target is localhost only."""
        # Resolve hostname to IP
        try:
            if target.lower() == 'localhost':
                return True
            resolved = socket.gethostbyname(target)
            if resolved in ['127.0.0.1', '::1'] or resolved.startswith('127.'):
                return True
        except Exception:
            pass
        return False

    def simulate_syn_flood(self, port=8080, duration=10, rate=100):
        """Simulate SYN flood pattern on localhost port.
        
        Args:
            port: Target port on localhost
            duration: Test duration in seconds
            rate: Connections per second
        """
        print(f"[stress] Starting SYN flood simulation on 127.0.0.1:{port}")
        print(f"[stress] Duration: {duration}s, Rate: {rate} conn/s")
        
        self.stats['start_time'] = datetime.now()
        self.stop_flag = False
        end_time = time.time() + duration
        
        def worker():
            while time.time() < end_time and not self.stop_flag:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    sock.connect(('127.0.0.1', port))
                    self.stats['connections_made'] += 1
                    sock.close()
                except Exception:
                    self.stats['errors'] += 1
                time.sleep(1.0 / rate)
        
        # Launch multiple threads
        num_threads = min(10, rate // 10 + 1)
        for _ in range(num_threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            self.active_threads.append(t)
        
        # Wait for completion
        for t in self.active_threads:
            t.join()
        
        self.stats['end_time'] = datetime.now()
        return self._generate_report('SYN Flood')

    def simulate_udp_flood(self, port=8080, duration=10, packet_size=1024, rate=100):
        """Simulate UDP flood pattern on localhost port.
        
        Args:
            port: Target UDP port on localhost
            duration: Test duration in seconds
            packet_size: Size of each UDP packet in bytes
            rate: Packets per second
        """
        print(f"[stress] Starting UDP flood simulation on 127.0.0.1:{port}")
        print(f"[stress] Duration: {duration}s, Rate: {rate} pkt/s, Size: {packet_size}B")
        
        self.stats['start_time'] = datetime.now()
        self.stop_flag = False
        end_time = time.time() + duration
        
        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b'X' * packet_size
            
            while time.time() < end_time and not self.stop_flag:
                try:
                    sock.sendto(payload, ('127.0.0.1', port))
                    self.stats['packets_sent'] += 1
                except Exception:
                    self.stats['errors'] += 1
                time.sleep(1.0 / rate)
            
            sock.close()
        
        # Launch multiple threads
        num_threads = min(5, rate // 20 + 1)
        for _ in range(num_threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            self.active_threads.append(t)
        
        # Wait for completion
        for t in self.active_threads:
            t.join()
        
        self.stats['end_time'] = datetime.now()
        return self._generate_report('UDP Flood')

    def simulate_http_flood(self, port=8080, duration=10, rate=50):
        """Simulate HTTP flood pattern on localhost web server.
        
        Args:
            port: Target HTTP port on localhost
            duration: Test duration in seconds
            rate: Requests per second
        """
        print(f"[stress] Starting HTTP flood simulation on 127.0.0.1:{port}")
        print(f"[stress] Duration: {duration}s, Rate: {rate} req/s")
        
        self.stats['start_time'] = datetime.now()
        self.stop_flag = False
        end_time = time.time() + duration
        
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Mozilla/5.0 (X11; Linux x86_64)',
        ]
        
        def worker():
            while time.time() < end_time and not self.stop_flag:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect(('127.0.0.1', port))
                    
                    # Send HTTP GET request
                    ua = random.choice(user_agents)
                    request = f"GET /?test={random.randint(1000,9999)} HTTP/1.1\r\n"
                    request += f"Host: 127.0.0.1:{port}\r\n"
                    request += f"User-Agent: {ua}\r\n"
                    request += "Connection: close\r\n\r\n"
                    
                    sock.send(request.encode())
                    self.stats['packets_sent'] += 1
                    sock.recv(4096)  # Read response
                    sock.close()
                    self.stats['connections_made'] += 1
                except Exception:
                    self.stats['errors'] += 1
                time.sleep(1.0 / rate)
        
        # Launch multiple threads
        num_threads = min(5, rate // 10 + 1)
        for _ in range(num_threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            self.active_threads.append(t)
        
        # Wait for completion
        for t in self.active_threads:
            t.join()
        
        self.stats['end_time'] = datetime.now()
        return self._generate_report('HTTP Flood')

    def simulate_slowloris(self, port=8080, duration=10, connections=50):
        """Simulate Slowloris attack pattern on localhost.
        
        Args:
            port: Target HTTP port on localhost
            duration: Test duration in seconds
            connections: Number of slow connections to maintain
        """
        print(f"[stress] Starting Slowloris simulation on 127.0.0.1:{port}")
        print(f"[stress] Duration: {duration}s, Connections: {connections}")
        
        self.stats['start_time'] = datetime.now()
        self.stop_flag = False
        end_time = time.time() + duration
        
        sockets = []
        
        # Open slow connections
        for _ in range(connections):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect(('127.0.0.1', port))
                
                # Send partial HTTP request
                sock.send(b"GET / HTTP/1.1\r\n")
                sock.send(f"Host: 127.0.0.1:{port}\r\n".encode())
                
                sockets.append(sock)
                self.stats['connections_made'] += 1
            except Exception:
                self.stats['errors'] += 1
        
        # Keep connections alive with periodic headers
        while time.time() < end_time and not self.stop_flag:
            for sock in sockets:
                try:
                    sock.send(f"X-a: {random.randint(1,9999)}\r\n".encode())
                    self.stats['packets_sent'] += 1
                except Exception:
                    self.stats['errors'] += 1
            time.sleep(5)
        
        # Clean up
        for sock in sockets:
            try:
                sock.close()
            except Exception:
                pass
        
        self.stats['end_time'] = datetime.now()
        return self._generate_report('Slowloris')

    def simulate_icmp_flood(self, duration=10, rate=100):
        """Simulate ICMP ping flood on localhost.
        
        Note: Requires raw socket permissions (sudo)
        
        Args:
            duration: Test duration in seconds
            rate: Pings per second
        """
        print(f"[stress] Starting ICMP flood simulation on 127.0.0.1")
        print(f"[stress] Duration: {duration}s, Rate: {rate} ping/s")
        print(f"[stress] Note: ICMP requires root/sudo - simulating at application layer")
        
        self.stats['start_time'] = datetime.now()
        self.stop_flag = False
        end_time = time.time() + duration
        
        # Use TCP echo as alternative (port 7)
        def worker():
            while time.time() < end_time and not self.stop_flag:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    sock.connect(('127.0.0.1', 7))  # Echo port
                    sock.send(b'PING')
                    sock.recv(4)
                    self.stats['packets_sent'] += 1
                    sock.close()
                except Exception:
                    self.stats['errors'] += 1
                time.sleep(1.0 / rate)
        
        # Launch threads
        num_threads = min(5, rate // 20 + 1)
        for _ in range(num_threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            self.active_threads.append(t)
        
        for t in self.active_threads:
            t.join()
        
        self.stats['end_time'] = datetime.now()
        return self._generate_report('ICMP Flood (simulated)')

    def stop(self):
        """Stop all active simulations."""
        print("[stress] Stopping all active simulations...")
        self.stop_flag = True
        time.sleep(1)
        self.active_threads.clear()

    def _generate_report(self, attack_type):
        """Generate detailed simulation report."""
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        report = {
            'type': 'stress_simulation_report',
            'attack_type': attack_type,
            'target': '127.0.0.1 (localhost)',
            'duration_seconds': round(duration, 2),
            'statistics': {
                'packets_sent': self.stats['packets_sent'],
                'connections_made': self.stats['connections_made'],
                'errors': self.stats['errors'],
                'success_rate': round(
                    (self.stats['connections_made'] / 
                     max(1, self.stats['connections_made'] + self.stats['errors'])) * 100, 2
                ),
                'avg_rate': round(self.stats['packets_sent'] / max(1, duration), 2)
            },
            'timestamps': {
                'start': self.stats['start_time'].isoformat(),
                'end': self.stats['end_time'].isoformat()
            }
        }
        
        return report
