ref=3
signal=1

tEnd=100;ts=0.1
KP=2;KD=8;KI=1
t=0;e=0;eSum=0;eOld=0
while t < tEnd:
    t=t+ts
    e=signal-ref
    out=KP*e + KD*(e-eOld)/ts + KI*eSum*ts
    eOld=e     
    eSum+=e