import argparse
import os
import sys

import cv2

from video_converter import VideoOverlayConverter, VideoPoseConverter, VideoSegmentationConverter

def parse_args():
    parser = argparse.ArgumentParser(prog='video_pose_tracker')

    parser.add_argument('-i', '--input', type=str, help='Path to input file.')
    parser.add_argument('-o', '--output', type=str, help='Path to output file.')
    parser.add_argument('--gui', action='store_true', help='The flag to launch with GUI.')
    parser.add_argument('--mode', type=str, choices=['pose', 'overlay', 'chromakey'], default='pose', help='The output video mode.')
    parser.add_argument('--audio', action='store_true', help='The flag to write audio in input file.')
    parser.add_argument('--background', type=str, help='Path to background image file. Enabled for only chromakey mode.')
    parser.add_argument('--chromakey_clip_mode', type=str, choices=['foreground', 'background'], help='Whether to cut out the background or the foreground.')
    
    return parser.parse_args(sys.argv[1:])

def main(in_args):
    if in_args.gui:
        print('GUI mode is not support now.')
    else:
        if not os.path.isfile(in_args.input):
            raise FileNotFoundError(f'Input file "{in_args.input}" is not found.')

        if in_args.mode == 'pose':
            converter = VideoPoseConverter(in_args.input)
        elif in_args.mode == 'overlay':
            converter = VideoOverlayConverter(in_args.input)
        elif in_args.mode == 'chromakey':
            background = cv2.imread(in_args.background)
            converter = VideoSegmentationConverter(in_args.input, background)
        converter.save_audio = in_args.audio
        converter.execute(in_args.output)

    return 0

if __name__ == '__main__':
    exit(main(parse_args()))
