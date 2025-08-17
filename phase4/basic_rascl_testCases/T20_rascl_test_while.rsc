int a[5], b;
float c, d[4];

main ()
{
  a[2] = 5;
  b = a[2] + a[3] * 2;
  while (b > 0)
  {
    print b;
    b = b - 1
  };
  print a[2]
}
