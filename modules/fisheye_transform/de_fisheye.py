"""
https://github.com/duducosmos/defisheye/tree/master
"""


import cv2
from numpy import arange, sqrt, arctan, sin, tan, meshgrid, pi, hypot
from PIL import Image

class Defisheye:
    """
    Defisheye

    fov: fisheye field of view (aperture) in degrees
    pfov: perspective field of view (aperture) in degrees
    xcenter: x center of fisheye area
    ycenter: y center of fisheye area
    radius: radius of fisheye area
    angle: image rotation in degrees clockwise
    dtype: linear, equalarea, orthographic, stereographic
    format: circular, fullframe
    """

    def __init__(self, 
                 infile: str,
                 fov: int = 180,
                 pfov: int = 120,
                 xcenter: int = None,
                 ycenter: int = None,
                 radius: int = None,   
                 angle: int = 0, 
                 dtype: str = "linear", 
                 format: str = "fullframe"
                 ) -> None:    
        
        self._fov = fov
        self._pfov = pfov
        self._xcenter = xcenter
        self._ycenter = ycenter
        self._radius = radius
        self._angle = angle
        self._dtype = dtype
        self._format = format

        if type(infile) == str:
            _image = cv2.imread(infile)
        else:
            raise Exception("Image format not recognized")

        width = _image.shape[1]
        height = _image.shape[0]
        xcenter = width // 2
        ycenter = height // 2

        dim = min(width, height)
        x0 = xcenter - dim // 2
        xf = xcenter + dim // 2
        y0 = ycenter - dim // 2
        yf = ycenter + dim // 2

        self._image = _image[y0:yf, x0:xf, :]

        self._width = self._image.shape[1]
        self._height = self._image.shape[0]

        if self._xcenter is None:
            self._xcenter = (self._width - 1) // 2

        if self._ycenter is None:
            self._ycenter = (self._height - 1) // 2

    def _map(self, i, j, ofocinv, dim):

        xd = i - self._xcenter
        yd = j - self._ycenter

        rd = hypot(xd, yd)
        phiang = arctan(ofocinv * rd)

        if self._dtype == "linear":
            ifoc = dim * 180 / (self._fov * pi)
            rr = ifoc * phiang
            # rr = "rr={}*phiang;".format(ifoc)

        elif self._dtype == "equalarea":
            ifoc = dim / (2.0 * sin(self._fov * pi / 720))
            rr = ifoc * sin(phiang / 2)
            # rr = "rr={}*sin(phiang/2);".format(ifoc)

        elif self._dtype == "orthographic":
            ifoc = dim / (2.0 * sin(self._fov * pi / 360))
            rr = ifoc * sin(phiang)
            # rr="rr={}*sin(phiang);".format(ifoc)

        elif self._dtype == "stereographic":
            ifoc = dim / (2.0 * tan(self._fov * pi / 720))
            rr = ifoc * tan(phiang / 2)

        rdmask = rd != 0
        xs = xd.copy()
        ys = yd.copy()

        xs[rdmask] = (rr[rdmask] / rd[rdmask]) * xd[rdmask] + self._xcenter
        ys[rdmask] = (rr[rdmask] / rd[rdmask]) * yd[rdmask] + self._ycenter

        xs[~rdmask] = 0
        ys[~rdmask] = 0

        xs = xs.astype(int)
        ys = ys.astype(int)
        return xs, ys

    def convert(self, outfile=None):
        if self._format == "circular":
            dim = min(self._width, self._height)
        elif self._format == "fullframe":
            dim = sqrt(self._width ** 2.0 + self._height ** 2.0)

        if self._radius is not None:
            dim = 2 * self._radius

        # compute output (perspective) focal length and its inverse from ofov
        # phi=fov/2; r=N/2
        # r/f=tan(phi);
        # f=r/tan(phi);
        # f= (N/2)/tan((fov/2)*(pi/180)) = N/(2*tan(fov*pi/360))

        ofoc = dim / (2 * tan(self._pfov * pi / 360))
        ofocinv = 1.0 / ofoc

        i = arange(self._width)
        j = arange(self._height)
        i, j = meshgrid(i, j)

        xs, ys, = self._map(i, j, ofocinv, dim)
        img = self._image.copy()

        img[i, j, :] = self._image[xs, ys, :]
        if outfile is not None:
            cv2.imwrite(outfile, img)
        return img


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("--infile", type=str, default="./images/example2.jpg", help="Input image")
    parser.add_argument("--fov", type=int, default=180, help="fisheye field of view (aperture) in degrees")
    parser.add_argument("--pfov", type=int, default=120, help="perspective field of view (aperture) in degrees")
    parser.add_argument("--xcenter", type=int, default=None, help="x center of fisheye area")
    parser.add_argument("--ycenter", type=int, default=None, help="y center of fisheye area")
    parser.add_argument("--radius", type=int, default=None, help="radius of fisheye area")
    parser.add_argument("--angle", type=int, default=0, help="image rotation in degrees clockwise")
    parser.add_argument("--dtype", type=str, default="linear", 
                        choices=["linear", "equalarea", "orthographic", "stereographic"], 
                        help="choice in [linear, equalarea, orthographic, stereographic]")
    parser.add_argument("--format", type=str, default="fullframe", 
                        choices=["circular", "fullframe"], 
                        help="choice in [circular, fullframe]")

    opt = parser.parse_args()

    defisheye = Defisheye(**vars(opt))
    defisheye.convert(outfile="./images/defisheye.jpg")


