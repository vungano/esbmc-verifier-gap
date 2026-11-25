"""Pilot tasks P01–P20: spec, frozen ESBMC harness, hidden tests, golden C.

Hidden tests are never shown. The frozen harness is shown only at L5.
"""

TASKS = [
    {
        "id": "P01",
        "difficulty": "Basic",
        "function_name": "increment",
        "signature": "int increment(int x)",
        "specification": "Implement int increment(int x). Return x + 1 for every integer x from -10 through 10 inclusive.",
        "unwind": 8,
        "golden": "int increment(int x) { return x + 1; }",
        "harness": """int main() {
  int x = nondet_int();
  __ESBMC_assume(x >= -10 && x <= 10);
  assert(increment(x) == x + 1);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int x = -10; x <= 10; ++x) assert(increment(x) == x + 1);
  return 0;
}""",
    },
    {
        "id": "P02",
        "difficulty": "Basic",
        "function_name": "absolute_value",
        "signature": "int absolute_value(int x)",
        "specification": "Implement int absolute_value(int x). Return the non-negative magnitude of x for x from -10 through 10 inclusive.",
        "unwind": 8,
        "golden": "int absolute_value(int x) { return x < 0 ? -x : x; }",
        "harness": """int main() {
  int x = nondet_int();
  __ESBMC_assume(x >= -10 && x <= 10);
  assert(absolute_value(x) == (x < 0 ? -x : x));
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int x = -10; x <= 10; ++x) assert(absolute_value(x) == (x < 0 ? -x : x));
  return 0;
}""",
    },
    {
        "id": "P03",
        "difficulty": "Basic",
        "function_name": "maximum",
        "signature": "int maximum(int a, int b)",
        "specification": "Implement int maximum(int a, int b). Return the larger input, including when they are equal. Inputs are from -10 through 10.",
        "unwind": 8,
        "golden": "int maximum(int a, int b) { return a > b ? a : b; }",
        "harness": """int main() {
  int a = nondet_int();
  int b = nondet_int();
  __ESBMC_assume(a >= -10 && a <= 10);
  __ESBMC_assume(b >= -10 && b <= 10);
  assert(maximum(a, b) == (a > b ? a : b));
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int a = -10; a <= 10; ++a)
    for (int b = -10; b <= 10; ++b)
      assert(maximum(a, b) == (a > b ? a : b));
  return 0;
}""",
    },
    {
        "id": "P04",
        "difficulty": "Basic",
        "function_name": "is_even",
        "signature": "bool is_even(int x)",
        "specification": "Implement bool is_even(int x). Return true exactly when x is divisible by 2, including negative integers and zero. x is from -10 through 10.",
        "unwind": 8,
        "golden": "bool is_even(int x) { return x % 2 == 0; }",
        "harness": """int main() {
  int x = nondet_int();
  __ESBMC_assume(x >= -10 && x <= 10);
  assert(is_even(x) == (x % 2 == 0));
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int x = -10; x <= 10; ++x) assert(is_even(x) == (x % 2 == 0));
  return 0;
}""",
    },
    {
        "id": "P05",
        "difficulty": "Basic",
        "function_name": "clamp",
        "signature": "int clamp(int x, int low, int high)",
        "specification": "Implement int clamp(int x, int low, int high). Return low if x is below low, high if above high, and x otherwise. Assume low <= high; all values are from -5 through 5.",
        "unwind": 8,
        "golden": "int clamp(int x, int low, int high) { if (x < low) return low; if (x > high) return high; return x; }",
        "harness": """int main() {
  int x = nondet_int();
  int low = nondet_int();
  int high = nondet_int();
  __ESBMC_assume(x >= -5 && x <= 5);
  __ESBMC_assume(low >= -5 && low <= 5);
  __ESBMC_assume(high >= -5 && high <= 5);
  __ESBMC_assume(low <= high);
  int e = x < low ? low : (x > high ? high : x);
  assert(clamp(x, low, high) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int x = -5; x <= 5; ++x)
    for (int lo = -5; lo <= 5; ++lo)
      for (int hi = lo; hi <= 5; ++hi)
        assert(clamp(x, lo, hi) == (x < lo ? lo : (x > hi ? hi : x)));
  return 0;
}""",
    },
    {
        "id": "P06",
        "difficulty": "Branching",
        "function_name": "sign",
        "signature": "int sign(int x)",
        "specification": "Implement int sign(int x). Return -1 for negative values, 0 for zero and 1 for positive values. x is from -10 through 10.",
        "unwind": 8,
        "golden": "int sign(int x) { if (x < 0) return -1; if (x > 0) return 1; return 0; }",
        "harness": """int main() {
  int x = nondet_int();
  __ESBMC_assume(x >= -10 && x <= 10);
  assert(sign(x) == (x < 0 ? -1 : (x > 0 ? 1 : 0)));
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int x = -10; x <= 10; ++x)
    assert(sign(x) == (x < 0 ? -1 : (x > 0 ? 1 : 0)));
  return 0;
}""",
    },
    {
        "id": "P07",
        "difficulty": "Branching",
        "function_name": "maximum3",
        "signature": "int maximum3(int a, int b, int c)",
        "specification": "Implement int maximum3(int a, int b, int c). Return the largest input, handling ties correctly. Inputs are from -5 through 5.",
        "unwind": 8,
        "golden": "int maximum3(int a, int b, int c) { int m = a > b ? a : b; return m > c ? m : c; }",
        "harness": """int main() {
  int a = nondet_int();
  int b = nondet_int();
  int c = nondet_int();
  __ESBMC_assume(a >= -5 && a <= 5);
  __ESBMC_assume(b >= -5 && b <= 5);
  __ESBMC_assume(c >= -5 && c <= 5);
  int e = a > b ? a : b;
  e = e > c ? e : c;
  assert(maximum3(a, b, c) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int a = -5; a <= 5; ++a)
    for (int b = -5; b <= 5; ++b)
      for (int c = -5; c <= 5; ++c) {
        int e = a > b ? a : b;
        e = e > c ? e : c;
        assert(maximum3(a, b, c) == e);
      }
  return 0;
}""",
    },
    {
        "id": "P08",
        "difficulty": "Branching",
        "function_name": "sum_to_n",
        "signature": "int sum_to_n(int n)",
        "specification": "Implement int sum_to_n(int n). Return 0+1+...+n for n from 0 through 20.",
        "unwind": 24,
        "golden": "int sum_to_n(int n) { int s = 0; for (int i = 0; i <= n; ++i) s += i; return s; }",
        "harness": """int main() {
  int n = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 20);
  int e = 0;
  for (int i = 0; i <= n; ++i) e += i;
  assert(sum_to_n(n) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int n = 0; n <= 20; ++n) {
    int e = 0;
    for (int i = 0; i <= n; ++i) e += i;
    assert(sum_to_n(n) == e);
  }
  return 0;
}""",
    },
    {
        "id": "P09",
        "difficulty": "Branching",
        "function_name": "reverse_digits",
        "signature": "int reverse_digits(int n)",
        "specification": "Implement int reverse_digits(int n). Reverse the decimal digits of a non-negative integer n from 0 through 999. Do not preserve leading zeros in the reversed result.",
        "unwind": 12,
        "golden": "int reverse_digits(int n) { int r = 0; do { r = r * 10 + n % 10; n /= 10; } while (n > 0); return r; }",
        "harness": """int main() {
  int n = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 999);
  int v = n, e = 0;
  do { e = e * 10 + v % 10; v /= 10; } while (v > 0);
  assert(reverse_digits(n) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int n = 0; n <= 999; ++n) {
    int v = n, e = 0;
    do { e = e * 10 + v % 10; v /= 10; } while (v > 0);
    assert(reverse_digits(n) == e);
  }
  return 0;
}""",
    },
    {
        "id": "P10",
        "difficulty": "Branching",
        "function_name": "gcd",
        "signature": "int gcd(int a, int b)",
        "specification": "Implement int gcd(int a, int b). Return the non-negative greatest common divisor for a,b from 0 through 20, including gcd(0,0)==0.",
        "unwind": 24,
        "golden": """int gcd(int a, int b) {
  if (a == 0) return b;
  if (b == 0) return a;
  while (b != 0) { int t = a % b; a = b; b = t; }
  return a;
}""",
        "harness": """int main() {
  int a = nondet_int();
  int b = nondet_int();
  __ESBMC_assume(a >= 0 && a <= 20);
  __ESBMC_assume(b >= 0 && b <= 20);
  int e = 0;
  if (!(a == 0 && b == 0)) {
    for (int d = 1; d <= 20; ++d)
      if (a % d == 0 && b % d == 0) e = d;
  }
  assert(gcd(a, b) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int a = 0; a <= 20; ++a)
    for (int b = 0; b <= 20; ++b) {
      int e = 0;
      if (!(a == 0 && b == 0)) {
        for (int d = 1; d <= 20; ++d)
          if (a % d == 0 && b % d == 0) e = d;
      }
      assert(gcd(a, b) == e);
    }
  return 0;
}""",
    },
    {
        "id": "P11",
        "difficulty": "Loops",
        "function_name": "is_prime",
        "signature": "bool is_prime(int n)",
        "specification": "Implement bool is_prime(int n). Return true exactly when n from 0 through 100 is prime.",
        "unwind": 20,
        "golden": """bool is_prime(int n) {
  if (n < 2) return false;
  for (int d = 2; d * d <= n; ++d) if (n % d == 0) return false;
  return true;
}""",
        "harness": """int main() {
  int n = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 100);
  bool e = n >= 2;
  for (int d = 2; d * d <= n; ++d) if (n % d == 0) e = false;
  assert(is_prime(n) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int n = 0; n <= 100; ++n) {
    bool e = n >= 2;
    for (int d = 2; d * d <= n; ++d) if (n % d == 0) e = false;
    assert(is_prime(n) == e);
  }
  return 0;
}""",
    },
    {
        "id": "P12",
        "difficulty": "Loops",
        "function_name": "fibonacci",
        "signature": "int fibonacci(int n)",
        "specification": "Implement int fibonacci(int n). Return F_n where F_0=0, F_1=1 and F_n=F_(n-1)+F_(n-2), for n from 0 through 15.",
        "unwind": 20,
        "golden": """int fibonacci(int n) {
  if (n == 0) return 0;
  if (n == 1) return 1;
  int a = 0, b = 1, e = 0;
  for (int i = 2; i <= n; ++i) { e = a + b; a = b; b = e; }
  return e;
}""",
        "harness": """int main() {
  int n = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 15);
  int a = 0, b = 1, e = 0;
  if (n == 0) e = 0;
  else if (n == 1) e = 1;
  else {
    for (int i = 2; i <= n; ++i) { e = a + b; a = b; b = e; }
  }
  assert(fibonacci(n) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  int a = 0, b = 1;
  for (int n = 0; n <= 15; ++n) {
    int e;
    if (n == 0) e = 0;
    else if (n == 1) e = 1;
    else { e = a + b; a = b; b = e; }
    assert(fibonacci(n) == e);
  }
  return 0;
}""",
    },
    {
        "id": "P13",
        "difficulty": "Loops",
        "function_name": "digit_sum",
        "signature": "int digit_sum(int n)",
        "specification": "Implement int digit_sum(int n). Return the sum of decimal digits of n from 0 through 9999.",
        "unwind": 12,
        "golden": "int digit_sum(int n) { int s = 0; do { s += n % 10; n /= 10; } while (n > 0); return s; }",
        "harness": """int main() {
  int n = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 9999);
  int v = n, e = 0;
  do { e += v % 10; v /= 10; } while (v > 0);
  assert(digit_sum(n) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int n = 0; n <= 9999; ++n) {
    int v = n, e = 0;
    do { e += v % 10; v /= 10; } while (v > 0);
    assert(digit_sum(n) == e);
  }
  return 0;
}""",
    },
    {
        "id": "P14",
        "difficulty": "Loops",
        "function_name": "is_palindrome",
        "signature": "bool is_palindrome(int n)",
        "specification": "Implement bool is_palindrome(int n). Return true exactly when the decimal representation of n from 0 through 9999 reads the same forwards and backwards.",
        "unwind": 12,
        "golden": """bool is_palindrome(int n) {
  int v = n, r = 0;
  do { r = r * 10 + v % 10; v /= 10; } while (v > 0);
  return n == r;
}""",
        "harness": """int main() {
  int n = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 9999);
  int v = n, r = 0;
  do { r = r * 10 + v % 10; v /= 10; } while (v > 0);
  assert(is_palindrome(n) == (n == r));
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int n = 0; n <= 9999; ++n) {
    int v = n, r = 0;
    do { r = r * 10 + v % 10; v /= 10; } while (v > 0);
    assert(is_palindrome(n) == (n == r));
  }
  return 0;
}""",
    },
    {
        "id": "P15",
        "difficulty": "Loops",
        "function_name": "count_set_bits",
        "signature": "int count_set_bits(unsigned int n)",
        "specification": "Implement int count_set_bits(unsigned int n). Count the number of 1 bits in the binary representation of n from 0 through 255.",
        "unwind": 12,
        "golden": "int count_set_bits(unsigned int n) { int c = 0; while (n) { c += n & 1u; n >>= 1; } return c; }",
        "harness": """int main() {
  unsigned int n = nondet_uint();
  __ESBMC_assume(n <= 255);
  unsigned int v = n;
  int e = 0;
  while (v) { e += v & 1u; v >>= 1; }
  assert(count_set_bits(n) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (unsigned int n = 0; n <= 255; ++n) {
    unsigned int v = n;
    int e = 0;
    while (v) { e += v & 1u; v >>= 1; }
    assert(count_set_bits(n) == e);
  }
  return 0;
}""",
    },
    {
        "id": "P16",
        "difficulty": "Arrays",
        "function_name": "array_sum",
        "signature": "int array_sum(const int a[], int n)",
        "specification": "Implement int array_sum(const int a[], int n). Return the sum of the first n elements, where 0<=n<=5 and each element is from -5 through 5.",
        "unwind": 8,
        "golden": "int array_sum(const int a[], int n) { int s = 0; for (int i = 0; i < n; ++i) s += a[i]; return s; }",
        "harness": """int main() {
  int a[5];
  int n = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 5);
  for (int i = 0; i < 5; ++i) {
    a[i] = nondet_int();
    __ESBMC_assume(a[i] >= -5 && a[i] <= 5);
  }
  int e = 0;
  for (int i = 0; i < n; ++i) e += a[i];
  assert(array_sum(a, n) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  int a[5];
  for (int i = 0; i < 5; ++i) a[i] = i - 2;
  for (int n = 0; n <= 5; ++n) {
    int e = 0;
    for (int i = 0; i < n; ++i) e += a[i];
    assert(array_sum(a, n) == e);
  }
  int b[5] = {-5, -5, -5, -5, -5};
  assert(array_sum(b, 5) == -25);
  return 0;
}""",
    },
    {
        "id": "P17",
        "difficulty": "Arrays",
        "function_name": "is_sorted",
        "signature": "bool is_sorted(const int a[], int n)",
        "specification": "Implement bool is_sorted(const int a[], int n). Return true exactly when the first n elements are non-decreasing. Allow duplicates and an empty array. 0<=n<=5.",
        "unwind": 8,
        "golden": """bool is_sorted(const int a[], int n) {
  for (int i = 1; i < n; ++i) if (a[i] < a[i - 1]) return false;
  return true;
}""",
        "harness": """int main() {
  int a[5];
  int n = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 5);
  for (int i = 0; i < 5; ++i) {
    a[i] = nondet_int();
    __ESBMC_assume(a[i] >= -5 && a[i] <= 5);
  }
  bool e = true;
  for (int i = 1; i < n; ++i) if (a[i] < a[i - 1]) e = false;
  assert(is_sorted(a, n) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  int a[5] = {-2, -2, 0, 3, 3};
  for (int n = 0; n <= 5; ++n) assert(is_sorted(a, n));
  int b[5] = {-2, 2, 0, 3, 3};
  assert(!is_sorted(b, 5));
  return 0;
}""",
    },
    {
        "id": "P18",
        "difficulty": "Arrays",
        "function_name": "count_occurrences",
        "signature": "int count_occurrences(const int a[], int n, int target)",
        "specification": "Implement int count_occurrences(const int a[], int n, int target). Count elements equal to target among the first n elements. 0<=n<=5 and values are from -3 through 3.",
        "unwind": 8,
        "golden": """int count_occurrences(const int a[], int n, int target) {
  int c = 0;
  for (int i = 0; i < n; ++i) if (a[i] == target) ++c;
  return c;
}""",
        "harness": """int main() {
  int a[5];
  int n = nondet_int();
  int target = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 5);
  __ESBMC_assume(target >= -3 && target <= 3);
  for (int i = 0; i < 5; ++i) {
    a[i] = nondet_int();
    __ESBMC_assume(a[i] >= -3 && a[i] <= 3);
  }
  int e = 0;
  for (int i = 0; i < n; ++i) if (a[i] == target) ++e;
  assert(count_occurrences(a, n, target) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  int a[5] = {-3, 0, 0, 2, 0};
  for (int t = -3; t <= 3; ++t) {
    int e = 0;
    for (int i = 0; i < 5; ++i) if (a[i] == t) ++e;
    assert(count_occurrences(a, 5, t) == e);
  }
  assert(count_occurrences(a, 0, 0) == 0);
  return 0;
}""",
    },
    {
        "id": "P19",
        "difficulty": "Arrays",
        "function_name": "linear_search",
        "signature": "int linear_search(const int a[], int n, int target)",
        "specification": "Implement int linear_search(const int a[], int n, int target). Return the index of the first target occurrence, or -1 if absent. Array length is at most 5.",
        "unwind": 8,
        "golden": """int linear_search(const int a[], int n, int target) {
  for (int i = 0; i < n; ++i) if (a[i] == target) return i;
  return -1;
}""",
        "harness": """int main() {
  int a[5];
  int n = nondet_int();
  int target = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 5);
  __ESBMC_assume(target >= -5 && target <= 5);
  for (int i = 0; i < 5; ++i) {
    a[i] = nondet_int();
    __ESBMC_assume(a[i] >= -5 && a[i] <= 5);
  }
  int e = -1;
  for (int i = 0; i < n; ++i) if (a[i] == target && e == -1) e = i;
  assert(linear_search(a, n, target) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  int a[5] = {2, -1, 2, 3, 2};
  for (int t = -3; t <= 3; ++t) {
    int e = -1;
    for (int i = 0; i < 5; ++i) if (a[i] == t && e == -1) e = i;
    assert(linear_search(a, 5, t) == e);
  }
  assert(linear_search(a, 0, 2) == -1);
  return 0;
}""",
    },
    {
        "id": "P20",
        "difficulty": "Arrays",
        "function_name": "second_largest",
        "signature": "int second_largest(const int a[], int n)",
        "specification": "Implement int second_largest(const int a[], int n). Return the second-largest distinct value in an array of length 1 through 5 with values from -5 through 5. If fewer than two distinct values exist, return -1.",
        "unwind": 8,
        "golden": """int second_largest(const int a[], int n) {
  int max1 = a[0];
  int max2 = -100;
  int has2 = 0;
  for (int i = 1; i < n; ++i) if (a[i] > max1) max1 = a[i];
  for (int i = 0; i < n; ++i) {
    if (a[i] != max1 && (!has2 || a[i] > max2)) { max2 = a[i]; has2 = 1; }
  }
  return has2 ? max2 : -1;
}""",
        "harness": """int main() {
  int a[5];
  int n = nondet_int();
  __ESBMC_assume(n >= 1 && n <= 5);
  for (int i = 0; i < 5; ++i) {
    a[i] = nondet_int();
    __ESBMC_assume(a[i] >= -5 && a[i] <= 5);
  }
  int max1 = a[0];
  for (int i = 1; i < n; ++i) if (a[i] > max1) max1 = a[i];
  int max2 = -100;
  int has2 = 0;
  for (int i = 0; i < n; ++i) {
    if (a[i] != max1 && (!has2 || a[i] > max2)) { max2 = a[i]; has2 = 1; }
  }
  int e = has2 ? max2 : -1;
  assert(second_largest(a, n) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  int a[5] = {-5, 0, 5, 5, 2};
  assert(second_largest(a, 5) == 2);
  int b[5] = {1, 1, 1, 1, 1};
  assert(second_largest(b, 5) == -1);
  int c[2] = {-4, -2};
  assert(second_largest(c, 2) == -4);
  int d[4] = {1, 5, 3, 5};
  assert(second_largest(d, 4) == 3);
  return 0;
}""",
    },
    {
        "id": "T01",
        "difficulty": "Timeout",
        "expected_verdict": "esbmc_fail",
        "function_name": "is_prime",
        "signature": "bool is_prime(int n)",
        "specification": "Implement bool is_prime(int n). Return true exactly when n from 0 through 30 is prime.",
        "unwind": 8,
        "golden": """bool is_prime(int n) {
  if (n < 2) return false;
  for (int d = 2; d < n; ++d) if (n % d == 0) return false;
  return true;
}""",
        "harness": """int main() {
  int n = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 30);
  bool e = n==2||n==3||n==5||n==7||n==11||n==13||n==17||n==19||n==23||n==29;
  assert(is_prime(n) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int n = 0; n <= 30; ++n) {
    bool e = n >= 2;
    for (int d = 2; d * d <= n; ++d) if (n % d == 0) e = false;
    assert(is_prime(n) == e);
  }
  return 0;
}""",
    },
    {
        "id": "T02",
        "difficulty": "Timeout",
        "expected_verdict": "esbmc_fail",
        "function_name": "fibonacci",
        "signature": "int fibonacci(int n)",
        "specification": "Implement int fibonacci(int n). Return F_n where F_0=0, F_1=1 and F_n=F_(n-1)+F_(n-2), for n from 0 through 30.",
        "unwind": 8,
        "golden": """int fibonacci(int n) {
  if (n == 0) return 0;
  if (n == 1) return 1;
  int a = 0, b = 1, e = 0;
  for (int i = 2; i <= n; ++i) { e = a + b; a = b; b = e; }
  return e;
}""",
        "harness": """int main() {
  int n = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 30);
  const int F[31] = {0,1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597,2584,4181,6765,10946,17711,28657,46368,75025,121393,196418,317811,514229,832040};
  assert(fibonacci(n) == F[n]);
  return 0;
}""",
        "hidden_tests": """int main() {
  int a = 0, b = 1;
  for (int n = 0; n <= 30; ++n) {
    int e;
    if (n == 0) e = 0;
    else if (n == 1) e = 1;
    else { e = a + b; a = b; b = e; }
    assert(fibonacci(n) == e);
  }
  return 0;
}""",
    },
    {
        "id": "T03",
        "difficulty": "Timeout",
        "expected_verdict": "esbmc_fail",
        "function_name": "factorial",
        "signature": "int factorial(int n)",
        "specification": "Implement int factorial(int n). Return n! for n from 0 through 12. 0! is 1.",
        "unwind": 8,
        "golden": """int factorial(int n) {
  int p = 1;
  for (int i = 1; i <= n; ++i) p *= i;
  return p;
}""",
        "harness": """int main() {
  int n = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 12);
  const int F[13] = {1,1,2,6,24,120,720,5040,40320,362880,3628800,39916800,479001600};
  assert(factorial(n) == F[n]);
  return 0;
}""",
        "hidden_tests": """int main() {
  int e = 1;
  for (int n = 0; n <= 12; ++n) {
    if (n > 0) e *= n;
    assert(factorial(n) == e);
  }
  return 0;
}""",
    },
    {
        "id": "T04",
        "difficulty": "Timeout",
        "expected_verdict": "esbmc_fail",
        "function_name": "sum_to_n",
        "signature": "int sum_to_n(int n)",
        "specification": "Implement int sum_to_n(int n). Return 0+1+...+n for n from 0 through 80.",
        "unwind": 8,
        "golden": """int sum_to_n(int n) {
  int s = 0;
  for (int i = 0; i <= n; ++i) s += i;
  return s;
}""",
        "harness": """int main() {
  int n = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 80);
  assert(sum_to_n(n) == n * (n + 1) / 2);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int n = 0; n <= 80; ++n) {
    int e = 0;
    for (int i = 0; i <= n; ++i) e += i;
    assert(sum_to_n(n) == e);
  }
  return 0;
}""",
    },
    {
        "id": "T05",
        "difficulty": "Timeout",
        "expected_verdict": "esbmc_fail",
        "function_name": "gcd",
        "signature": "int gcd(int a, int b)",
        "specification": "Implement int gcd(int a, int b). Return the non-negative greatest common divisor for a,b from 0 through 50, including gcd(0,0)==0.",
        "unwind": 8,
        "golden": """int gcd(int a, int b) {
  if (a == 0 && b == 0) return 0;
  int m = a > b ? a : b;
  int g = 0;
  for (int d = 1; d <= m; ++d)
    if (a % d == 0 && b % d == 0) g = d;
  return g;
}""",
        "harness": """int main() {
  int a = nondet_int();
  int b = nondet_int();
  __ESBMC_assume(a >= 0 && a <= 50);
  __ESBMC_assume(b >= 0 && b <= 50);
  int x = a, y = b;
  while (y != 0) { int t = x % y; x = y; y = t; }
  assert(gcd(a, b) == x);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int a = 0; a <= 50; ++a)
    for (int b = 0; b <= 50; ++b) {
      int e = 0;
      if (!(a == 0 && b == 0)) {
        int m = a > b ? a : b;
        for (int d = 1; d <= m; ++d)
          if (a % d == 0 && b % d == 0) e = d;
      }
      assert(gcd(a, b) == e);
    }
  return 0;
}""",
    },
    {
        "id": "T06",
        "difficulty": "Timeout",
        "expected_verdict": "esbmc_fail",
        "function_name": "count_primes",
        "signature": "int count_primes(int n)",
        "specification": "Implement int count_primes(int n). Return how many primes lie in 2 through n inclusive. For n from 0 through 40; count_primes(n) is 0 when n < 2.",
        "unwind": 8,
        "golden": """int count_primes(int n) {
  int c = 0;
  for (int i = 2; i <= n; ++i) {
    int prime = 1;
    for (int d = 2; d < i; ++d) if (i % d == 0) prime = 0;
    if (prime) ++c;
  }
  return c;
}""",
        "harness": """int main() {
  int n = nondet_int();
  __ESBMC_assume(n >= 0 && n <= 40);
  const int pi[41] = {0,0,1,2,2,3,3,4,4,4,4,5,5,6,6,6,6,7,7,8,8,8,8,9,9,9,9,9,9,10,10,11,11,11,11,11,11,12,12,12,12};
  assert(count_primes(n) == pi[n]);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int n = 0; n <= 40; ++n) {
    int e = 0;
    for (int i = 2; i <= n; ++i) {
      int prime = i >= 2;
      for (int d = 2; d * d <= i; ++d) if (i % d == 0) prime = 0;
      if (prime) ++e;
    }
    assert(count_primes(n) == e);
  }
  return 0;
}""",
    },
    {
        "id": "T07",
        "difficulty": "Timeout",
        "expected_verdict": "esbmc_fail",
        "function_name": "mul",
        "signature": "int mul(int a, int b)",
        "specification": "Implement int mul(int a, int b). Return a*b for a,b from 0 through 30, without requiring a particular algorithm.",
        "unwind": 8,
        "golden": """int mul(int a, int b) {
  int s = 0;
  for (int i = 0; i < b; ++i) s += a;
  return s;
}""",
        "harness": """int main() {
  int a = nondet_int();
  int b = nondet_int();
  __ESBMC_assume(a >= 0 && a <= 30);
  __ESBMC_assume(b >= 0 && b <= 30);
  assert(mul(a, b) == a * b);
  return 0;
}""",
        "hidden_tests": """int main() {
  for (int a = 0; a <= 30; ++a)
    for (int b = 0; b <= 30; ++b)
      assert(mul(a, b) == a * b);
  return 0;
}""",
    },
    {
        "id": "T08",
        "difficulty": "Timeout",
        "expected_verdict": "esbmc_fail",
        "function_name": "count_set_bits",
        "signature": "int count_set_bits(unsigned int n)",
        "specification": "Implement int count_set_bits(unsigned int n). Count the number of 1 bits in n for n from 0 through 65535.",
        "unwind": 8,
        "golden": """int count_set_bits(unsigned int n) {
  int c = 0;
  while (n) { c += n & 1u; n >>= 1; }
  return c;
}""",
        "harness": """int main() {
  unsigned int n = nondet_uint();
  __ESBMC_assume(n <= 65535);
  int e = (int)((n>>0)&1u)+((n>>1)&1u)+((n>>2)&1u)+((n>>3)&1u)
        +((n>>4)&1u)+((n>>5)&1u)+((n>>6)&1u)+((n>>7)&1u)
        +((n>>8)&1u)+((n>>9)&1u)+((n>>10)&1u)+((n>>11)&1u)
        +((n>>12)&1u)+((n>>13)&1u)+((n>>14)&1u)+((n>>15)&1u);
  assert(count_set_bits(n) == e);
  return 0;
}""",
        "hidden_tests": """int main() {
  unsigned int samples[] = {0, 1, 2, 3, 7, 8, 15, 16, 255, 256, 1023, 1024, 32768, 65535};
  int ns = 14;
  for (int i = 0; i < ns; ++i) {
    unsigned int v = samples[i];
    int e = 0;
    unsigned int x = v;
    while (x) { e += x & 1u; x >>= 1; }
    assert(count_set_bits(v) == e);
  }
  return 0;
}""",
    },
]


def get_task(task_id):
    for task in TASKS:
        if task["id"] == task_id:
            return task
    raise KeyError(task_id)


def task_ids():
    return [task["id"] for task in TASKS]
