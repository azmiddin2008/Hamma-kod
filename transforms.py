def transform(self, x, y):
    #return self.transform_2D(x, y)
    return self.transform_3D(x, y)
def transform_2D(self, x, y):
    return x, y
def transform_3D(self, x, y):
    tr_y = y * self.chiziq_y / self.height
    if tr_y > self.chiziq_y:
        tr_y = self.chiziq_y

    farq_x = x-self.chiziq_x
    farq_y = self.chiziq_y-tr_y

    foiz = farq_y/self.chiziq_y
    foiz = pow(foiz, 4)

    tr_x = self.chiziq_x + farq_x*foiz
    tr_y = self.chiziq_y - foiz*self.chiziq_y

    return int(tr_x), int(tr_y)