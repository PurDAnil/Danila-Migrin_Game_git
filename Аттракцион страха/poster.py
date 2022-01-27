class Poster:
    # 30, 25
    # 30, 970
    # 20, 900 y
    def __init__(self, app, x, y, z, image):
        app.posters[0].append(x)
        app.posters[1].append(y)
        app.posters[2].append(z)
        app.posters[3].append(image)
