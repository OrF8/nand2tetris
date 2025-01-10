load,
output-file test2.out,
compare-to test2.cmp,
output-list RAM[5002]%D1.6.1 RAM[5004]%D1.6.1 RAM[5006]%D1.6.1 RAM[5008]%D1.6.1 RAM[5010]%D1.6.1;

repeat 1000000 {
  vmstep;
}

output;
