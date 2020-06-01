def tick2MBT(tick: int, tpb: int = 384) -> str:
    measure = int(tick / (tpb * 4))
    tick -= measure * tpb * 4
    beat = int(tick / tpb)
    tick -= beat * tpb

    return f'{measure+1:02}:{beat+1:02}:{tick:03}'


def sec2HMSF(seconds: float) -> str:
    hour = int(seconds / 3600)
    seconds -= hour * 3600
    minute = int(seconds / 60)
    seconds -= minute * 60
    ms = seconds - int(seconds)
    seconds -= ms

    return f'{hour:02}:{minute:02}:{int(seconds):02}:{int(ms*1000):03}'

