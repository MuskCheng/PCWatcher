def test_get_cpu_percent():
    from monitor import SystemMonitor
    m = SystemMonitor()
    cpu = m.get_cpu_percent()
    assert 0 <= cpu <= 100

def test_get_memory():
    from monitor import SystemMonitor
    m = SystemMonitor()
    mem = m.get_memory()
    assert "percent" in mem
    assert 0 <= mem["percent"] <= 100
