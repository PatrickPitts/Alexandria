def test(**kwargs):
    for key, value in kwargs.items():
        if value:
            print("The value of {} is {}".format(key, value))
    if int("abc"):
        print("success!")

test(Genre = "Science Fiction", ISBN = 1234567890123, Author = None)
