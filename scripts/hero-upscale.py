#!/usr/bin/env python3
"""4x neural upscale of the hero mezzanine to 5120x2880.

FSRCNN x4 via OpenCV DNN. This is a CNN super-resolution pass in the same
family as NVIDIA Video Super Resolution. RTX VSR itself only runs on an
NVIDIA GPU, which this pipeline does not have, so the weights used here
are the public FSRCNN x4 model.

Stdout is raw BGR24, 5120x2880, one frame per input frame. Feed it to ffmpeg:

  python3 -u scripts/hero-upscale.py in.mp4 FSRCNN_x4.pb | \\
    ffmpeg -f rawvideo -pix_fmt bgr24 -s 5120x2880 -r 30 -i - ...
"""
import sys

import cv2


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("usage: hero-upscale.py INPUT MODEL.pb\n")
        return 2
    cap = cv2.VideoCapture(sys.argv[1])
    if not cap.isOpened():
        sys.stderr.write("cannot open %s\n" % sys.argv[1])
        return 1
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(sys.argv[2])
    sr.setModel("fsrcnn", 4)
    cv2.setNumThreads(2)
    n = 0
    out = sys.stdout.buffer
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        up = sr.upsample(frame)
        if up.shape[1] != 5120 or up.shape[0] != 2880:
            sys.stderr.write("unexpected shape %s\n" % (up.shape,))
            return 1
        out.write(up.tobytes())
        n += 1
        if n % 15 == 0:
            sys.stderr.write("upscaled %d\n" % n)
            sys.stderr.flush()
    sys.stderr.write("frames %d\n" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
