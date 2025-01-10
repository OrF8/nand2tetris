load,
output-file test1.out,
compare-to test1.cmp,
output-list RAM[5000]%D1.6.1;

repeat 1000000 {
  vmstep;
}

output;
