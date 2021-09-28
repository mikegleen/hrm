# -*- coding: utf-8 -*-  needed because of embedded "£"
"""

DEPRECATED. Replaced by thumb.py

Create two thumbnail images:
    portrait: width 342, height 484
    landscape: width 1280, height 826

See get_args for details.

"""
import argparse
from collections import namedtuple
import math
import os.path
from PIL import Image
import sys

BACKGROUND = 'F2F4F6'
PORTRAIT_WIDTH = 342
PORTRAIT_HEIGHT = 484
LANDSCAPE_WIDTH = 1280
LANDSCAPE_HEIGHT = 826

PORTRAIT_RATIO = float(PORTRAIT_WIDTH) / float(PORTRAIT_HEIGHT)
LANDSCAPE_RATIO = float(LANDSCAPE_WIDTH) / float(LANDSCAPE_HEIGHT)

ImgSize = namedtuple('ImgSize', ['w', 'h'])
EVENT_PORTRAIT = ImgSize(342, 484)
EVENT_LANDSCAPE = ImgSize(1280, 826)
MEDIACENTRE_THUMBNAIL = ImgSize(1280, 826)
NEWS_THUMBNAIL = ImgSize(1280, 826)
NEWS_WIDE = ImgSize(1280, 410)
EXHIBITION_THUMBNAIL = ImgSize(700, 454)

IMGS = {'ev-p': EVENT_PORTRAIT,
        'ev-l': EVENT_LANDSCAPE,
        'm-t': MEDIACENTRE_THUMBNAIL,
        'minor-t': NEWS_THUMBNAIL,
        'minor-w': NEWS_WIDE,
        'ex-t': EXHIBITION_THUMBNAIL}


def trace(level, template, *args):
    if _args.verbose >= level:
        print(template.format(*args))


def make_background(hexstr):  # hexstr can be like F1F2F3 or 0xF1F2F3
    hexint = int(hexstr, 16)
    red = (hexint >> 16) & 0xFF
    green = (hexint >> 8) & 0xFF
    blue = hexint & 0xFF
    return red, green, blue


def pad_height(inimage, target_width, target_height):
    """
    The input image is too wide. Resize it so that the width is target_width
    and then pad the top and bottom so that the height is target_height.

    :param inimage:
    :param target_width:
    :param target_height:
    :return the resized and padded image
    """
    trace(2, 'Begin pad_height. Target width, height = ({}, {})', target_width,
          target_height)
    width, height = inimage.size
    wh_ratio = float(width) / float(height)
    unpadded_height = int(target_width / wh_ratio)
    trace(2, 'Resizing image to ({}, {})', target_width, unpadded_height)
    resized_image = inimage.resize((target_width, unpadded_height))
    y_origin = int(math.ceil((target_height - unpadded_height) / 2.))
    target_image = Image.new('RGBA', (target_width, target_height),
                             _args.background_tuple)
    target_image.paste(resized_image, (0, y_origin))
    return target_image


def pad_width(inimage, target_width, target_height):
    """
    The input image is too tall. Resize it so that the height is target_height
    and then pad the left and right so that the width is target_width.

    :param inimage:
    :param target_width:
    :param target_height:
    :return the resized and padded image
    """
    trace(2, 'Begin pad_width. Target width, height = ({}, {})', target_width,
          target_height)
    if _args.width:
        target_width = _args.width
        trace(2, 'Overriding target width: ', target_width)
    width, height = inimage.size
    wh_ratio = float(width) / float(height)
    unpadded_width = int(target_height * wh_ratio)
    trace(2, "Resizing image to ({}, {})", unpadded_width, target_height)
    resized_image = inimage.resize((unpadded_width, target_height))
    x_origin = int(math.ceil((target_width - unpadded_width) / 2.))
    target_image = Image.new('RGBA', (target_width, target_height),
                             _args.background_tuple)
    target_image.paste(resized_image, (x_origin, 0))
    return target_image


def oneimage(img, sizeref):
    pass


def onefile(infile, outdir):
    basename = os.path.basename(infile)  # 'a/b/xyz.jpg' -> 'xyz.jpg'
    front, extension = os.path.splitext(basename)  # 'xyz.jpg' -> 'xyz', '.jpg'
    portrait_thumb_name = front + '_portrait_thumb' + '.jpeg'
    landscape_thumb_name = front + '_landscape_thumb' + '.jpeg'
    portrait_target = os.path.join(outdir, portrait_thumb_name)
    landscape_target = os.path.join(outdir, landscape_thumb_name)
    input_image = Image.open(infile)
    width, height = input_image.size
    wh_ratio = width / height
    trace(2, "Input: {}\nSize (width, height) in pixels: {}, {}, "
          "width/height = {:.3f}", infile, width, height, wh_ratio)
    if _args.portrait:
        trace(2, "Begin building portrait image. Target w/h ratio: {:.3f}",
              PORTRAIT_RATIO)
        if wh_ratio > PORTRAIT_RATIO:
            portrait = pad_height(input_image, PORTRAIT_WIDTH, PORTRAIT_HEIGHT)
        else:
            portrait = pad_width(input_image, PORTRAIT_WIDTH, PORTRAIT_HEIGHT)
        trace(1, 'Saving portrait thumbnail: {}', portrait_target)
        portrait.save(portrait_target)
    if _args.landscape:
        trace(2, "Begin building landscape image.  Target w/h ratio: {:.3f}",
              LANDSCAPE_RATIO)
        if wh_ratio > LANDSCAPE_RATIO:
            landscape = pad_height(input_image, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT)
        else:
            landscape = pad_width(input_image, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT)
        trace(1, 'Saving landscape thumbnail: {}', landscape_target)
        landscape.save(landscape_target)


def main(args):
    if os.path.isdir(args.infile):
        for filename in os.listdir(args.infile):
            onefile(filename, args.infile)
    else:
        onefile(args.infile, args.outdir)


def get_args():
    parser = argparse.ArgumentParser(description='''
    Create two thumbnail images:
    portrait: (width 342, height 484)
    landscape: (width 1280, height 826).

    The thumbnail files are created with the same name as the original file
    but with _thumb_portrait and _thumb_landscape appended before the
    extension.
    ''')
    parser.add_argument('infile', help='''Original sized input file.''')
    parser.add_argument('-b', '--background', default=BACKGROUND, help='''
        Hex number describing the background color. Default = {}.
        The number should be coded as six hex digits. The leading "0x" is
        optional.'''.format(BACKGROUND))
    parser.add_argument('--height', type=int, default=0, help='''
        Set an explicit height to pad to (sorry, -h is taken).
        ''')
    parser.add_argument('-l', '--landscape', action='store_true', help='''
        If set, only produce a landscape thumbnail.
        ''')
    parser.add_argument('-o', '--outdir',
                        default=os.path.join('results', 'thumb'),
                        help='''Directory to contain the
        output landscape file. If omitted, the default is "results/thumb".
        ''')
    parser.add_argument('-p', '--portrait', action='store_true', help='''
        If set, only produce a portrait thumbnail.
        ''')
    parser.add_argument('-v', '--verbose', type=int, default=1, help='''
        Set the verbosity. The default is 1 which prints summary information.
        ''')
    parser.add_argument('-w', '--width', type=int, default=0, help='''
        Set an explicit width to pad to (portrait only).
        ''')

    args = parser.parse_args()
    args.background_tuple = make_background(args.background)
    if args.landscape is False and args.portrait is False:
        args.landscape = args.portrait = True
    return args

if __name__ == '__main__':

    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    _args = get_args()
    trace(2, 'Background color: (0x{:02X}, 0x{:02X}, 0x{:02X})',
          *_args.background_tuple)
    main(_args)
