# sim_database

the input netlist:

.subckt sub1 1 2 
.param r=100
r1 1 2 r=r 
.ends

.subckt sub2 1 2 
r2 1 2 100 
.ends

x1 n1 n2 sub1 r=1 
x2 n2 n3 sub1 r=2 
x3 n3 n4 sub2
r3 n1 n4 r=3 
