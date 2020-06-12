
from pyprone.core.enums.midifile import DEFAULT_TICKS_PER_BEAT

def tick2MBT(tick: int, tpb: int = DEFAULT_TICKS_PER_BEAT) -> str:
    measure = int(tick / (tpb * 4))
    tick -= measure * tpb * 4
    beat = int(tick / tpb)
    tick -= beat * tpb

    return f'{measure+1:02}:{beat+1:02}:{tick:03}'

def MBT2tick(m:int, b:int, t:int, tpb: int = DEFAULT_TICKS_PER_BEAT) -> int:
    return ((m - 1) * 4 + (b - 1)) * tpb + t

def sec2HMSF(seconds: float) -> str:
    hour = int(seconds / 3600)
    seconds -= hour * 3600
    minute = int(seconds / 60)
    seconds -= minute * 60
    ms = seconds - int(seconds)
    seconds -= ms

    return f'{hour:02}:{minute:02}:{int(seconds):02}:{int(ms*1000):03}'

def tempo2bpm(tempo: int) -> float:
    return 60000000 / tempo