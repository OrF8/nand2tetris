load,
output-file test5.out,
compare-to test5.cmp,
output-list RAM[5000]%D1.6.1 RAM[5001]%D1.6.1 RAM[5002]%D1.6.1;

repeat 1000000 {
  vmstep;
}

output;
