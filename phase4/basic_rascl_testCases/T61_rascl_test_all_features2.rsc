float a;
float g[10];
int b, c;
int d[5];

function int test_t61() {
  a = 5.;
  b = 1;
  if (a == b) || (b < 0)
  {
    d[a] = 5;
    g[0] = a + -b
  }
  else
  {
    while (b < 5) {
        g[1] = -a * b;
	b = b + 1
    }
  };
  print c;
  return c
}

main () {
  int retval;
  retval = test_t61()
}

