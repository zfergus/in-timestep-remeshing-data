$fn= $preview ? 32 : 32 ;

h = 1;
r = 0.2;

pole_h = 1.5;
pole_r = 0.07;

spike_r1 = 0.1;
spike_r2 = 0.02;
spike_h = 0.4;

n_spikes = 5;
n_spike_rows = 4;


h_start = h/2 - spike_r1;
h_end = -h/2 + spike_r1;

 union() {
cylinder(h = h, r1 = r, r2 = r, center = true);

for(j = [0: n_spike_rows]){
    tt= j/n_spike_rows * (h_end - h_start) + h_start;
    offset = (j % 2 ==0) ? 0 : 0.5/n_spikes*360; 
for (i = [0:n_spikes-1]) {
    
    translate([0, 0, tt]){
        rotate(a = offset + i/n_spikes*360, v = [0, 0, 1]) {
            translate([r, 0, 0]){
                rotate(a = 90, v = [0, 1, 0]) {
                    cylinder(h = spike_h, r1 = spike_r1, r2 = spike_r2, center = true);
                }
            }
        }
}
}
}


cylinder(h = pole_h, r1 = pole_r, r2 = pole_r, center = true);
}