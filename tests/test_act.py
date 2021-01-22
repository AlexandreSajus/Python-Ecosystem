import run


def test_bunny_act():
    # Test
    l_a = run.liveAgents.copy()
    l_a[1].act(0, run.state, l_a, run.age_fox)


if __name__ == "__main__":
    for i in range(1_000_000):
        test_bunny_act()
