from csharp_prober import CSharpProber

def test_inject_if_probe():
    code = "if (x > 0) { doWork(); }"
    prober = CSharpProber()
    result = prober.inject(code)
    assert 'Console.WriteLine("DEBUG: if (x > 0) entered");' in result
