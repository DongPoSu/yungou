g_a = 1  # LGB
g_b = 2


def test_scope(p_a, p_b=3):
    l_a = 4
    print(g_a, g_b, p_a, p_b, l_a)
    print(max([g_a, g_b, p_a, p_b, l_a]))


test_scope(g_b)
