load,
output-file test4.out,
compare-to test4.cmp,
output-list RAM[5000]%D1.6.1 RAM[5001]%D1.6.1 RAM[5010]%D1.6.1 RAM[5011]%D1.6.1;

repeat 1000000 {
  vmstep;
}

output;
