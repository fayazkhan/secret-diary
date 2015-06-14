from diary import show


def test_show():
    show()
    print.assert_called_once_with(humanized_time, content)
