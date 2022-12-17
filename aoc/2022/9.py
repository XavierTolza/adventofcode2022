import numpy as np

demo_data="""R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
demo_data="""R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

demo_result=13,1

directions = np.round(np.exp(1j*np.linspace(0,3*2*np.pi/4,4)).astype(np.complex128).view(np.float64).reshape((4,2))).astype(np.int8)
directions = dict(zip("RULD",directions))

def move_one(head,tail,direction):
    head += direction
    vect = head-tail
    d = np.linalg.norm(vect,axis=-1)
    if d>=2:
        argmax = np.argmax(np.abs(vect))
        newpos = head.copy()
        newpos[argmax] -= 1*np.sign(vect[argmax])
        tail_vect = newpos-tail
    else:
        tail_vect = np.zeros_like(tail)
    return tail_vect
    

def move(positions,cmd,nb):
    for _ in range(nb):
        direction = directions[cmd]
        for head,tail in zip(positions,positions[1:]):
            direction = move_one(head,tail,direction)
        positions[-1,:]+= direction
        yield positions.copy()
        
def simulate_movements(data,n_parts:int=2):
    pos = np.zeros((n_parts,2),dtype=np.int32)
    log = []
    for line in data.split("\n"):
        cmd, nb = line.split(" ")
        nb = int(nb)
        
        for i,_log in enumerate(move(pos,cmd,nb)):
            log.append(_log)

    log = np.array(log)
    print(np.reshape(log,(-1,4)))
    return log

def get_result(data,*args,**kwargs):
    return np.unique(simulate_movements(data,*args,**kwargs)[:,-1],axis=0).shape[0]

def main(data):
    # res1 = get_result(data,2)
    res2 = get_result(data,10)
    return res1, res2
