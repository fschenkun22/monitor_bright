"""
Monitor brightness controller supporting Windows, Linux, and macOS
"""
import platform
import subprocess
import sys


class BrightnessController:
    """Cross-platform monitor brightness controller"""
    
    def __init__(self):
        self.system = platform.system()
        
    def get_brightness(self):
        """Get current brightness level (0-100)"""
        if self.system == "Windows":
            return self._get_brightness_windows()
        elif self.system == "Linux":
            return self._get_brightness_linux()
        elif self.system == "Darwin":  # macOS
            return self._get_brightness_macos()
        else:
            raise NotImplementedError(f"Platform {self.system} is not supported")
    
    def set_brightness(self, level):
        """Set brightness level (0-100)"""
        if not isinstance(level, (int, float)):
            raise ValueError("Brightness level must be a number")
        
        if level < 0 or level > 100:
            raise ValueError("Brightness level must be between 0 and 100")
        
        if self.system == "Windows":
            return self._set_brightness_windows(level)
        elif self.system == "Linux":
            return self._set_brightness_linux(level)
        elif self.system == "Darwin":  # macOS
            return self._set_brightness_macos(level)
        else:
            raise NotImplementedError(f"Platform {self.system} is not supported")
    
    def list_monitors(self):
        """List available monitors"""
        if self.system == "Windows":
            return self._list_monitors_windows()
        elif self.system == "Linux":
            return self._list_monitors_linux()
        elif self.system == "Darwin":  # macOS
            return self._list_monitors_macos()
        else:
            raise NotImplementedError(f"Platform {self.system} is not supported")
    
    # Windows implementation
    def _get_brightness_windows(self):
        """Get brightness on Windows using WMI"""
        try:
            import wmi
            c = wmi.WMI(namespace='wmi')
            monitors = c.WmiMonitorBrightness()
            if monitors:
                return monitors[0].CurrentBrightness
            return None
        except ImportError:
            # Fallback: try using powershell
            try:
                result = subprocess.run(
                    ['powershell', '-Command', 
                     '(Get-Ciminstance -Namespace root/WMI -ClassName WmiMonitorBrightness)[0].CurrentBrightness'],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    return int(result.stdout.strip())
            except Exception:
                pass
            return None
    
    def _set_brightness_windows(self, level):
        """Set brightness on Windows using WMI"""
        try:
            import wmi
            c = wmi.WMI(namespace='wmi')
            methods = c.WmiMonitorBrightnessMethods()[0]
            methods.WmiSetBrightness(level, 0)
            return True
        except ImportError:
            # Fallback: try using powershell
            try:
                result = subprocess.run(
                    ['powershell', '-Command',
                     f'(Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightnessMethods)[0].WmiSetBrightness(1,{int(level)})'],
                    capture_output=True, text=True, timeout=5
                )
                return result.returncode == 0
            except Exception:
                return False
    
    def _list_monitors_windows(self):
        """List monitors on Windows"""
        monitors = []
        try:
            import wmi
            c = wmi.WMI(namespace='wmi')
            for i, monitor in enumerate(c.WmiMonitorBrightness()):
                monitors.append({
                    'id': i,
                    'name': f'Monitor {i}',
                    'current_brightness': monitor.CurrentBrightness
                })
        except Exception:
            monitors.append({'id': 0, 'name': 'Primary Monitor', 'current_brightness': None})
        return monitors
    
    # Linux implementation
    def _get_brightness_linux(self):
        """Get brightness on Linux using xrandr"""
        try:
            # Try to get the primary display
            result = subprocess.run(
                ['xrandr', '--verbose'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'Brightness:' in line:
                        brightness = float(line.split(':')[1].strip())
                        return round(brightness * 100)
            return None
        except Exception:
            # Try backlight sysfs interface
            try:
                with open('/sys/class/backlight/intel_backlight/brightness', 'r') as f:
                    current = int(f.read().strip())
                with open('/sys/class/backlight/intel_backlight/max_brightness', 'r') as f:
                    max_bright = int(f.read().strip())
                return round((current / max_bright) * 100)
            except Exception:
                return None
    
    def _set_brightness_linux(self, level):
        """Set brightness on Linux using xrandr"""
        try:
            # Get the primary display name
            result = subprocess.run(
                ['xrandr', '--current'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if ' connected' in line:
                        display_name = line.split()[0]
                        # Set brightness using xrandr
                        brightness_value = level / 100.0
                        subprocess.run(
                            ['xrandr', '--output', display_name, '--brightness', str(brightness_value)],
                            timeout=5
                        )
                        return True
            return False
        except Exception:
            # Try backlight sysfs interface
            try:
                with open('/sys/class/backlight/intel_backlight/max_brightness', 'r') as f:
                    max_bright = int(f.read().strip())
                new_brightness = int((level / 100.0) * max_bright)
                with open('/sys/class/backlight/intel_backlight/brightness', 'w') as f:
                    f.write(str(new_brightness))
                return True
            except Exception:
                return False
    
    def _list_monitors_linux(self):
        """List monitors on Linux"""
        monitors = []
        try:
            result = subprocess.run(
                ['xrandr', '--current'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                i = 0
                for line in result.stdout.split('\n'):
                    if ' connected' in line:
                        display_name = line.split()[0]
                        monitors.append({
                            'id': i,
                            'name': display_name,
                            'current_brightness': None
                        })
                        i += 1
        except Exception:
            monitors.append({'id': 0, 'name': 'Primary Monitor', 'current_brightness': None})
        return monitors
    
    # macOS implementation
    def _get_brightness_macos(self):
        """Get brightness on macOS"""
        try:
            result = subprocess.run(
                ['brightness', '-l'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                # Parse output to get brightness value
                for line in result.stdout.split('\n'):
                    if 'brightness' in line.lower():
                        value = float(line.split()[-1])
                        return round(value * 100)
            return None
        except Exception:
            return None
    
    def _set_brightness_macos(self, level):
        """Set brightness on macOS"""
        try:
            brightness_value = level / 100.0
            result = subprocess.run(
                ['brightness', str(brightness_value)],
                capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def _list_monitors_macos(self):
        """List monitors on macOS"""
        monitors = []
        try:
            result = subprocess.run(
                ['brightness', '-l'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for i, line in enumerate(lines):
                    if line.strip():
                        monitors.append({
                            'id': i,
                            'name': f'Display {i}',
                            'current_brightness': None
                        })
        except Exception:
            monitors.append({'id': 0, 'name': 'Primary Display', 'current_brightness': None})
        return monitors
