import run


def test_bunny_find_partner():
    # Test
    l_a = run.liveAgents.copy()
    l_a[1].find_partner(run.state, l_a, run.age_fox)


if __name__ == "__main__":
    for i in range(100_000):
        test_bunny_find_partner()
