from matlab_prober import MatlabProber

def test_inject_matlab_probe():
    code = "if x > 0\n    disp('hello')\nend"
    prober = MatlabProber()
    result = prober.inject(code)
    assert "fprintf('DEBUG: if x > 0 entered\\n');" in result
